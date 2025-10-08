import streamlit as st
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import numpy as np
import io
import hashlib
import datetime
import uuid
import io
import base64
from pathlib import Path
import tempfile
import os


# Demo credentials with phone number included
DEMO_USERS = {
    "alex@kasuku.com": {
        "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # 'password'
        "name": "Alex",
        "phone": "+254712345678"
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
        model_name = "cdli/whisper-small-Swahili_finetuned_small_CV20"
        
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
        model_name = "cdli/whisper-small_finetuned_kenyan_english_nonstandard_speech_v0.9"
        
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


# Optional: Add alternative transcription function with timestamp support
def transcribe_audio_with_timestamps(processor, model, device, audio_data, language="sw"):
    """
    Transcribe audio with word-level timestamps.
    Useful for longer transcriptions where timing is important.
    """
    try:
        inputs = processor(audio_data, sampling_rate=16000, return_tensors="pt")
        input_features = inputs.input_features.to(device)
        
        with torch.no_grad():
            # Generate with return_timestamps enabled
            predicted_ids = model.generate(
                input_features,
                language=language,
                task="transcribe",
                max_length=448,
                num_beams=5 if language == "sw" else 4,
                do_sample=(language == "sw"),
                temperature=0.6 if language == "sw" else 1.0,
                top_p=0.9 if language == "sw" else 1.0,
                return_timestamps=True  # Enable timestamp generation
            )
        
        # Decode with timestamps
        transcription = processor.batch_decode(
            predicted_ids, 
            skip_special_tokens=False,  # Keep timestamp tokens
            output_offsets=True
        )
        
        return transcription
        
    except Exception as e:
        st.error(f"Error during transcription with timestamps: {str(e)}")
        return None

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

try:
    from chatterbox import Chatterbox
    CHATTERBOX_AVAILABLE = True
except ImportError:
    CHATTERBOX_AVAILABLE = False
    print("Chatterbox not installed. Install with: pip install chatterbox-tts")

# Initialize Chatterbox (add this near other initialization code)
@st.cache_resource
def initialize_chatterbox():
    """Initialize Chatterbox TTS engine with caching"""
    if not CHATTERBOX_AVAILABLE:
        return None
    
    try:
        tts_engine = Chatterbox()
        return tts_engine
    except Exception as e:
        print(f"Failed to initialize Chatterbox: {str(e)}")
        return None


def text_to_speech_chatterbox(text, language="en", gender="female", rate=1.0, pitch=1.0):
    """
    Convert text to speech using Chatterbox TTS (offline, high quality)
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code ('en' for English, 'sw' for Swahili)
        gender (str): Voice gender ('female' or 'male')
        rate (float): Speech rate (0.5 to 2.0, default 1.0)
        pitch (float): Voice pitch (0.5 to 2.0, default 1.0)
    
    Returns:
        str: Path to the generated audio file, or None if failed
    """
    if not CHATTERBOX_AVAILABLE:
        print("Chatterbox not available, falling back to gTTS")
        return text_to_speech_gtts(text, language)
    
    try:
        tts_engine = initialize_chatterbox()
        
        if tts_engine is None:
            print("Failed to initialize Chatterbox")
            return text_to_speech_gtts(text, language)
        
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_path = temp_file.name
        
        # Configure voice settings
        voice_config = {
            'language': language,
            'gender': gender.lower(),
            'rate': rate,
            'pitch': pitch
        }
        
        # Generate speech
        tts_engine.speak(
            text=text,
            output_path=temp_path,
            **voice_config
        )
        
        return temp_path
        
    except Exception as e:
        print(f"Chatterbox TTS Error: {str(e)}")
        # Fallback to gTTS
        return text_to_speech_gtts(text, language)


def text_to_speech_enhanced(text, language="en", gender="female", rate=1.0, pitch=1.0, use_chatterbox=True):
    """
    Enhanced TTS with automatic fallback between Chatterbox and gTTS
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code ('en' for English, 'sw' for Swahili)
        gender (str): Voice gender ('female' or 'male')
        rate (float): Speech rate (0.5 to 2.0)
        pitch (float): Voice pitch (0.5 to 2.0)
        use_chatterbox (bool): Try Chatterbox first if available
    
    Returns:
        tuple: (audio_file_path, tts_engine_used) or (None, None) if failed
    """
    if use_chatterbox and CHATTERBOX_AVAILABLE:
        audio_path = text_to_speech_chatterbox(text, language, gender, rate, pitch)
        if audio_path:
            return audio_path, "chatterbox"
    
    # Fallback to gTTS
    audio_path = text_to_speech_gtts(text, language)
    if audio_path:
        return audio_path, "gtts"
    
    return None, None


def get_available_voices():
    """
    Get list of available voices for the TTS system
    
    Returns:
        dict: Available voices organized by language and gender
    """
    if CHATTERBOX_AVAILABLE:
        try:
            tts_engine = initialize_chatterbox()
            if tts_engine:
                return {
                    "English": {
                        "female": ["Emma", "Olivia", "Ava"],
                        "male": ["James", "Noah", "Liam"]
                    },
                    "Swahili": {
                        "female": ["Amani", "Zuri", "Nia"],
                        "male": ["Jabari", "Kazi", "Rafiki"]
                    }
                }
        except:
            pass
    
    # Fallback voice list for gTTS
    return {
        "English": {
            "female": ["Default Female"],
            "male": ["Default Male"]
        },
        "Swahili": {
            "female": ["Default Female"],
            "male": ["Default Male"]
        }
    }


def convert_audio_format(input_path, output_format='mp3'):
    """
    Convert audio file to different format (useful for web playback)
    
    Args:
        input_path (str): Path to input audio file
        output_format (str): Desired output format ('mp3', 'wav', 'ogg')
    
    Returns:
        str: Path to converted audio file or None if failed
    """
    try:
        from pydub import AudioSegment
        
        # Load audio
        audio = AudioSegment.from_file(input_path)
        
        # Create output path
        output_path = input_path.rsplit('.', 1)[0] + f'.{output_format}'
        
        # Export in desired format
        audio.export(output_path, format=output_format)
        
        return output_path
        
    except ImportError:
        print("pydub not installed. Install with: pip install pydub")
        return input_path
    except Exception as e:
        print(f"Audio conversion error: {str(e)}")
        return input_path


def preload_tts_cache(common_phrases, language="en"):
    """
    Preload commonly used phrases into TTS cache for faster response
    
    Args:
        common_phrases (list): List of common phrases to preload
        language (str): Language code
    """
    if not CHATTERBOX_AVAILABLE:
        return
    
    try:
        tts_engine = initialize_chatterbox()
        if tts_engine:
            for phrase in common_phrases:
                # Generate and cache
                temp_path = text_to_speech_chatterbox(phrase, language)
                if temp_path:
                    cleanup_temp_audio(temp_path)
    except Exception as e:
        print(f"TTS preload error: {str(e)}")


# Keep existing gTTS function as fallback
def text_to_speech_gtts(text, language="en"):
    """
    Convert text to speech using Google TTS (requires internet connection)
    Fallback option when Chatterbox is not available
    """
    try:
        from gtts import gTTS
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(temp_path)
        
        return temp_path
        
    except ImportError:
        print("gTTS not installed. Install with: pip install gtts")
        return None
    except Exception as e:
        print(f"gTTS Error: {str(e)}")
        return None
def text_to_speech_gtts(text, language="en"):
    """
    Convert text to speech using Google TTS (requires internet connection)
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code ('en' for English, 'sw' for Swahili)
    
    Returns:
        str: Path to the generated audio file, or None if failed
    """
    try:
        from gtts import gTTS
        import tempfile
        
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        
        # Generate TTS
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(temp_path)
        
        return temp_path
        
    except ImportError:
        print("gTTS not installed. Install with: pip install gtts")
        return None
    except Exception as e:
        print(f"gTTS Error: {str(e)}")
        return None

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
<<<<<<< HEAD
        print(f"Cleanup error: {str(e)}")
=======
        print(f"Cleanup error: {str(e)}")
>>>>>>> ba0838bbbb968a3965fcf04cc3513c49ad0b0e3a
