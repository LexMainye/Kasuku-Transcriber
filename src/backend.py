import streamlit as st
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import numpy as np
import io
import hashlib
import datetime
import uuid
import base64
from pathlib import Path
import tempfile
import os
import json
import atexit

def load_environment_variables():
    """
    Load Google Cloud environment variables from shell configuration.
    Tries multiple methods to ensure variables are loaded.
    """
    print("\n" + "="*50)
    print("LOADING ENVIRONMENT VARIABLES")
    print("="*50)
    
    # Method 1: Check if already in environment
    google_vars = {
        'GOOGLE_PROJECT_ID': os.getenv('GOOGLE_PROJECT_ID'),
        'GOOGLE_PRIVATE_KEY_ID': os.getenv('GOOGLE_PRIVATE_KEY_ID'),
        'GOOGLE_PRIVATE_KEY': os.getenv('GOOGLE_PRIVATE_KEY'),
        'GOOGLE_CLIENT_EMAIL': os.getenv('GOOGLE_CLIENT_EMAIL'),
        'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
        'GOOGLE_CLIENT_X509_CERT_URL': os.getenv('GOOGLE_CLIENT_X509_CERT_URL')
    }
    
    # Check if all variables are already set
    all_set = all(v is not None for v in google_vars.values())
    
    if all_set:
        print("✓ All environment variables already loaded!")
        return True
    
    print("Environment variables not found. Attempting to load from shell...")
    
    # Method 2: Load from shell with various techniques
    shells_to_try = [
        ('/bin/zsh', '~/.zshrc'),
        ('/bin/bash', '~/.bashrc'),
        ('/bin/bash', '~/.bash_profile'),
    ]
    
    for shell_path, rc_file in shells_to_try:
        if not os.path.exists(shell_path):
            continue
            
        print(f"\nTrying {shell_path} with {rc_file}...")
        
        try:
            # Expand home directory
            expanded_rc = os.path.expanduser(rc_file)
            
            if not os.path.exists(expanded_rc):
                print(f"  {rc_file} not found, skipping...")
                continue
            
            # Create a command that sources the RC file and exports all GOOGLE_ vars
            command = f"""
            source {expanded_rc}
            export | grep GOOGLE || env | grep GOOGLE
            """
            
            result = subprocess.run(
                command,
                shell=True,
                executable=shell_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"  ✓ Successfully read from {rc_file}")
                
                # Parse the output
                loaded_count = 0
                for line in result.stdout.strip().split('\n'):
                    # Handle both 'export VAR=value' and 'VAR=value' formats
                    line = line.strip()
                    
                    # Remove 'export ' prefix if present
                    if line.startswith('export '):
                        line = line[7:]
                    
                    # Remove 'declare -x ' prefix if present
                    if line.startswith('declare -x '):
                        line = line[11:]
                    
                    if '=' in line and 'GOOGLE' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove surrounding quotes
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        os.environ[key] = value
                        loaded_count += 1
                        print(f"    ✓ Loaded: {key}")
                
                if loaded_count > 0:
                    print(f"  Successfully loaded {loaded_count} variables")
                    break
            else:
                print(f"  No GOOGLE variables found in {rc_file}")
                
        except subprocess.TimeoutExpired:
            print(f"  Timeout reading {rc_file}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Final verification
    print("\n" + "-"*50)
    print("FINAL STATUS:")
    print("-"*50)
    
    google_vars_final = {
        'GOOGLE_PROJECT_ID': os.getenv('GOOGLE_PROJECT_ID'),
        'GOOGLE_PRIVATE_KEY_ID': os.getenv('GOOGLE_PRIVATE_KEY_ID'),
        'GOOGLE_PRIVATE_KEY': os.getenv('GOOGLE_PRIVATE_KEY'),
        'GOOGLE_CLIENT_EMAIL': os.getenv('GOOGLE_CLIENT_EMAIL'),
        'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
        'GOOGLE_CLIENT_X509_CERT_URL': os.getenv('GOOGLE_CLIENT_X509_CERT_URL')
    }
    
    all_loaded = True
    for key, value in google_vars_final.items():
        if value:
            # Show first/last few chars for security
            if len(value) > 20:
                display_value = f"{value[:10]}...{value[-10:]}"
            else:
                display_value = "***"
            print(f"✓ {key}: {display_value}")
        else:
            print(f"✗ {key}: NOT SET")
            all_loaded = False
    
    print("="*50 + "\n")
    
    if not all_loaded:
        print("\n⚠️  WARNING: Some environment variables are missing!")
        print("\nPlease check your ~/.zshrc file contains:")
        print('export GOOGLE_PROJECT_ID="your-value"')
        print('export GOOGLE_PRIVATE_KEY_ID="your-value"')
        print('export GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"')
        print('export GOOGLE_CLIENT_EMAIL="your-value"')
        print('export GOOGLE_CLIENT_ID="your-value"')
        print('export GOOGLE_CLIENT_X509_CERT_URL="your-value"')
        print("\nThen run: source ~/.zshrc")
        print("Or start your app with: zsh -c 'source ~/.zshrc && streamlit run app.py'\n")
    
    return all_loaded


# Demo credentials with phone number included
DEMO_USERS = {
    "alex@kasuku.com": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # 'password'
        "name": "Alex",
        "phone": "0712345678"
    }
}

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(identifier: str, password: str):
    """
    Authenticate user with email OR phone number + password.

    identifier: Email address OR phone number (string)
    password:   Password (string)
    """
    password_hash = hash_password(password)

    # Check direct email match
    if identifier in DEMO_USERS:
        if password_hash == DEMO_USERS[identifier]["password_hash"]:
            return True, DEMO_USERS[identifier]["name"]

    # Check phone number match
    for email, user in DEMO_USERS.items():
        if user.get("phone") and identifier.strip() == user["phone"]:
            if password_hash == user["password_hash"]:
                return True, user["name"]

    return False, None

@st.cache_resource  
def load_swahili_model():
    """Load the Swahili fine-tuned Whisper model with caching"""
    try:
        model_name = "smainye/whisper-small-kenyan-swahili-nonstandard"
        
        with st.spinner("Loading Swahili Whisper model..."):
            processor = WhisperProcessor.from_pretrained(model_name)
            model = WhisperForConditionalGeneration.from_pretrained(model_name)
            
            # Move to GPU if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = model.to(device)
            
        return processor, model, device
    except Exception as e:
        st.error(f"Error loading Swahili model: {str(e)}")
        return None, None, None

@st.cache_resource  
def load_english_model():
    """Load the English Whisper model with caching"""
    try:
        model_name = "smainye/whisper-small-kenyan-english-nonstandard"
        
        with st.spinner("Loading English Whisper model..."):
            processor = WhisperProcessor.from_pretrained(model_name)
            model = WhisperForConditionalGeneration.from_pretrained(model_name)
            
            # Move to GPU if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = model.to(device)
            
        return processor, model, device
    except Exception as e:
        st.error(f"Error loading English model: {str(e)}")
        return None, None, None

def preprocess_audio(audio_data, sample_rate, target_sr=16000):
    """Preprocess audio for Whisper model"""
    try:
        # Resample to 16kHz if needed
        if sample_rate != target_sr:
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=target_sr)
        
        # Normalize audio
        audio_data = audio_data.astype(np.float32)
        if np.max(np.abs(audio_data)) > 0:
            audio_data = audio_data / np.max(np.abs(audio_data))
        
        return audio_data, target_sr
    except Exception as e:
        st.error(f"Error preprocessing audio: {str(e)}")
        return None, None

def transcribe_audio(processor, model, device, audio_data, language="sw"):
    """
    Transcribe audio using the Whisper model with support for longer audio.
    Implements chunking strategy for audio longer than 30 seconds.
    """
    try:
        # Whisper models work best with 30-second chunks
        CHUNK_LENGTH = 30  # seconds
        SAMPLE_RATE = 16000
        chunk_samples = CHUNK_LENGTH * SAMPLE_RATE
        
        # Check if audio needs chunking
        audio_length = len(audio_data) / SAMPLE_RATE
        
        if audio_length <= CHUNK_LENGTH:
            # Short audio - process directly
            return _transcribe_single_chunk(
                processor, model, device, audio_data, language
            )
        else:
            # Long audio - use chunking with overlap
            return _transcribe_long_audio(
                processor, model, device, audio_data, language, 
                chunk_samples, SAMPLE_RATE
            )
            
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None

def _transcribe_single_chunk(processor, model, device, audio_data, language):
    """Transcribe a single chunk of audio (≤30 seconds)"""
    # Process audio
    inputs = processor(audio_data, sampling_rate=16000, return_tensors="pt")
    input_features = inputs.input_features.to(device)
    
    # Generate transcription with appropriate parameters
    with torch.no_grad():
        if language == "sw":
            predicted_ids = model.generate(
                input_features,
                language=language,
                task="transcribe",
                max_length=1024,
                num_beams=5,
                do_sample=True,
                temperature=0.9,
                top_p=0.9
            )
        else:  # English
            predicted_ids = model.generate(
                input_features,
                language=language,
                task="transcribe",
                max_length=1024,
                num_beams=5,
                do_sample=False
            )
    
    # Decode transcription
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription.strip()

def _transcribe_long_audio(processor, model, device, audio_data, language, 
                           chunk_samples, sample_rate):
    """
    Transcribe long audio by splitting into overlapping chunks.
    Uses 5-second overlap to maintain context between chunks.
    """
    OVERLAP = 5  # seconds overlap between chunks
    overlap_samples = OVERLAP * sample_rate
    
    transcriptions = []
    total_samples = len(audio_data)
    
    # Calculate number of chunks
    num_chunks = max(1, int(np.ceil((total_samples - overlap_samples) / 
                                    (chunk_samples - overlap_samples))))
    
    # Progress bar for long audio
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(num_chunks):
        # Calculate chunk boundaries
        start_idx = i * (chunk_samples - overlap_samples)
        end_idx = min(start_idx + chunk_samples, total_samples)
        
        # Extract chunk
        chunk = audio_data[start_idx:end_idx]
        
        # Update progress
        progress = (i + 1) / num_chunks
        progress_bar.progress(progress)
        
        # Transcribe chunk
        chunk_transcription = _transcribe_single_chunk(
            processor, model, device, chunk, language
        )
        
        if chunk_transcription:
            transcriptions.append(chunk_transcription)
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Combine transcriptions with smart merging
    final_transcription = _merge_transcriptions(transcriptions)
    
    return final_transcription

def _merge_transcriptions(transcriptions):
    """
    Intelligently merge chunk transcriptions, removing duplicate phrases
    at overlap boundaries.
    """
    if not transcriptions:
        return ""
    
    if len(transcriptions) == 1:
        return transcriptions[0]
    
    merged = transcriptions[0]
    
    for i in range(1, len(transcriptions)):
        current = transcriptions[i]
        
        # Try to find overlap by checking last words of merged with first words of current
        merged_words = merged.split()
        current_words = current.split()
        
        # Check for overlapping sequences (up to 10 words)
        overlap_found = False
        for overlap_length in range(min(10, len(merged_words), len(current_words)), 0, -1):
            if merged_words[-overlap_length:] == current_words[:overlap_length]:
                # Found overlap - merge without duplication
                merged = merged + " " + " ".join(current_words[overlap_length:])
                overlap_found = True
                break
        
        if not overlap_found:
            # No overlap found - simple concatenation with space
            merged = merged + " " + current
    
    # Clean up extra spaces
    return " ".join(merged.split())

def process_recorded_audio(recorded_audio):
    """Process recorded audio from Streamlit audio input"""
    try:
        audio_bytes = recorded_audio.getvalue()
        audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None)
        return audio_data, sample_rate
    except Exception as e:
        st.error(f"Error processing recorded audio: {str(e)}")
        return None, None

def create_transcription_item(transcription, selected_language, user_name):
    """Create a new transcription item with metadata"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    transcription_item = {
        "id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "language": selected_language,
        "transcription": transcription,
        "user": user_name
    }
    
    return transcription_item

def copy_transcription(index, transcription_history):
    """Get a specific transcription text for copying"""
    if 0 <= index < len(transcription_history):
        return transcription_history[index]["transcription"]
    return None

def delete_transcription(index, transcription_history):
    """Delete a transcription by index"""
    if 0 <= index < len(transcription_history):
        deleted_item = transcription_history.pop(index)
        return True, deleted_item
    return False, None

def filter_transcriptions(transcription_history, search_query=None, language_filter="All"):
    """Filter transcriptions based on search query and language filter"""
    filtered_history = [(i, item) for i, item in enumerate(transcription_history)]
    
    if search_query:
        filtered_history = [
            (i, item) for i, item in filtered_history 
            if search_query.lower() in item["transcription"].lower()
        ]
    
    if language_filter != "All":
        filtered_history = [
            (i, item) for i, item in filtered_history 
            if item["language"] == language_filter
        ]
    
    return filtered_history

def save_transcription_to_history(transcription, selected_language, user_name, transcription_history):
    """Save a transcription to history with proper item creation"""
    transcription_item = create_transcription_item(
        transcription, 
        selected_language, 
        user_name
    )
    transcription_history.append(transcription_item)
    return transcription_history

# Google Cloud TTS Functions with Environment Variable Support

# Global variable to track temporary credential file
_temp_cred_file = None


def debug_private_key():
    """Debug helper to check private key format"""
    private_key = os.getenv('GOOGLE_PRIVATE_KEY')
    if not private_key:
        print("ERROR: GOOGLE_PRIVATE_KEY not set")
        return
    
    has_literal_backslash_n = '\\n' in private_key
    has_actual_newlines = '\n' in private_key
    has_begin = 'BEGIN PRIVATE KEY' in private_key
    has_end = 'END PRIVATE KEY' in private_key
    
    print(f"Private key length: {len(private_key)}")
    print(f"Has literal \\n: {has_literal_backslash_n}")
    print(f"Has actual newlines: {has_actual_newlines}")
    print(f"First 50 chars: {private_key[:50]}")
    print(f"Last 50 chars: {private_key[-50:]}")
    print(f"Has BEGIN marker: {has_begin}")
    print(f"Has END marker: {has_end}")



def create_credentials_from_env():
    """
    Create Google Cloud credentials dictionary from environment variables
    """
    required_env_vars = [
        'GOOGLE_PROJECT_ID',
        'GOOGLE_PRIVATE_KEY_ID', 
        'GOOGLE_PRIVATE_KEY',
        'GOOGLE_CLIENT_EMAIL',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_X509_CERT_URL'
    ]
    
    # Check if all required environment variables are set
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Warning: Missing environment variables: {missing_vars}")
        return None
    
    # Get the private key
    private_key = os.getenv('GOOGLE_PRIVATE_KEY')
    
    print(f"DEBUG: Original key length: {len(private_key)}")
    
    # Step 1: Replace any literal \n strings with actual newlines
    if '\\n' in private_key:
        private_key = private_key.replace('\\n', '\n')
        print("DEBUG: Replaced literal \\n sequences")
    
    # Step 2: Fix the broken markers by rejoining split lines
    # The key comes with these broken across lines:
    # "-----BEGIN PRIVATE \nKEY-----" and "-----END \nPRIVATE KEY-----"
    
    lines = private_key.split('\n')
    print(f"DEBUG: Split into {len(lines)} lines")
    
    fixed_lines = []
    skip_next = False
    
    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue
            
        line = lines[i].strip()
        
        # Check if this line is incomplete and needs the next line
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            
            # Fix: "-----BEGIN PRIVATE" + "KEY-----"
            if line == '-----BEGIN PRIVATE' and next_line == 'KEY-----':
                fixed_lines.append('-----BEGIN PRIVATE KEY-----')
                skip_next = True
                continue
            
            # Fix: "-----END" + "PRIVATE KEY-----"
            if line == '-----END' and next_line == 'PRIVATE KEY-----':
                fixed_lines.append('-----END PRIVATE KEY-----')
                skip_next = True
                continue
        
        # Keep all non-empty lines
        if line:
            fixed_lines.append(line)
    
    print(f"DEBUG: After fixing, {len(fixed_lines)} lines")
    if fixed_lines:
        print(f"DEBUG: First line: '{fixed_lines[0]}'")
        print(f"DEBUG: Last line: '{fixed_lines[-1]}'")
    
    # Step 3: Reconstruct with proper newlines
    private_key = '\n'.join(fixed_lines) + '\n'
    
    print(f"DEBUG: Final key starts with: {private_key[:50]}")
    print(f"DEBUG: Final key ends with: {private_key[-50:]}")
    
    # Verify proper markers
    if '-----BEGIN PRIVATE KEY-----' not in private_key:
        print("ERROR: Missing proper BEGIN PRIVATE KEY marker")
        return None
        
    if '-----END PRIVATE KEY-----' not in private_key:
        print("ERROR: Missing proper END PRIVATE KEY marker")
        return None
    
    # Should have at least 3 lines (BEGIN, key data, END)
    if len(fixed_lines) < 3:
        print(f"ERROR: Only {len(fixed_lines)} lines, need at least 3")
        return None
    
    print("✓ Private key formatted correctly!")
    
    # Create credentials dictionary
    credentials_dict = {
        "type": "service_account",
        "project_id": os.getenv('GOOGLE_PROJECT_ID'),
        "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID'),
        "private_key": private_key,
        "client_email": os.getenv('GOOGLE_CLIENT_EMAIL'),
        "client_id": 113898445227721331105,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_X509_CERT_URL'),
        "universe_domain": "googleapis.com"
    }
    
    return credentials_dict

def setup_google_credentials():
    """
    Setup Google Cloud credentials from environment variables or file
    Returns the path to the credentials file used
    """
    global _temp_cred_file
    
    # First try environment variables
    credentials_dict = create_credentials_from_env()
    
    if credentials_dict:
        # Create temporary credentials file from environment variables
        temp_cred_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(credentials_dict, temp_cred_file)
        temp_cred_file.close()
        
        # Store the path for cleanup
        _temp_cred_file = temp_cred_file.name
        
        # Set the environment variable for Google Cloud
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_cred_file.name
        print("Using Google Cloud credentials from environment variables")
        return temp_cred_file.name
    
    # Fall back to file-based credentials
    CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"
    if CREDENTIALS_PATH.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS_PATH)
        print("Using Google Cloud credentials from credentials.json file")
        return str(CREDENTIALS_PATH)
    
    print("Warning: No Google Cloud credentials found in environment variables or credentials.json")
    return None

def cleanup_temp_credentials():
    """Clean up temporary credential files on exit"""
    global _temp_cred_file
    if _temp_cred_file and os.path.exists(_temp_cred_file):
        try:
            os.unlink(_temp_cred_file)
            print(f"Cleaned up temporary credential file: {_temp_cred_file}")
        except Exception as e:
            print(f"Error cleaning up temporary credential file: {e}")

# Register cleanup function to run when the program exits
atexit.register(cleanup_temp_credentials)

# Setup Google Cloud credentials
CREDENTIALS_FILE = setup_google_credentials()

if not CREDENTIALS_FILE:
    print("Warning: Google Cloud credentials not configured")
    GOOGLE_TTS_AVAILABLE = False
else:
    try:
        from google.cloud import texttospeech
        GOOGLE_TTS_AVAILABLE = True
        print("Google Cloud TTS initialized successfully")
    except ImportError:
        GOOGLE_TTS_AVAILABLE = False
        print("Google Cloud TTS not installed. Install with: pip install google-cloud-texttospeech")

@st.cache_data(max_entries=50)
def text_to_speech(text, language="en", gender="Female"):
    """
    Convert text to speech using Google Cloud TTS (high-quality, online).
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code ('en' or 'sw')
        gender (str): Voice gender ('Female' or 'Male')
    
    Returns:
        tuple: (audio_base64, tts_engine_used) or (None, None) if failed
    """
    if not GOOGLE_TTS_AVAILABLE:
        st.error("Google Cloud TTS library not installed.")
        return None, None
    
    if not CREDENTIALS_FILE:
        st.error("Google Cloud credentials not configured.")
        return None, None
    
    try:
        # Initialize client
        client = texttospeech.TextToSpeechClient()

        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Select the voice based on language and gender
        lang_code = "en-US" if language == "en" else "sw-KE"
        
        if language == "en":
            # English Wavenet voices are stable
            if gender == "Male":
                voice_name = "en-US-Chirp3-HD-Iapetus"
            else:
                voice_name = "en-US-Chirp3-HD-Leda"
        else:  # Swahili
            if gender == "Male":
                voice_name = "sw-KE-Chirp3-HD-Iapetus"  # Male (Standard)
            else:
                voice_name = "sw-KE-Chirp3-HD-Leda"  # Female (Standard)

        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code, name=voice_name
        )

        # Select the audio file type
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # Convert audio content (bytes) directly to base64
        # No more temporary files!
        audio_base64 = base64.b64encode(response.audio_content).decode()
            
        return audio_base64, "google-cloud"
        # ------------------------------

    except Exception as e:
        print(f"Google Cloud TTS Error: {str(e)}")
        st.error(f"Failed to generate speech: {e}")
        return None, None

def get_audio_base64(file_path):
    """Convert audio file to base64 for HTML audio player"""
    try:
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        return audio_base64
    except Exception as e:
        print(f"Audio encoding error: {str(e)}")
        return None

def cleanup_temp_audio(file_path):
    """Clean up temporary audio file"""
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Cleanup error: {str(e)}")