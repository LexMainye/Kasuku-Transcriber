import streamlit as st
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import numpy as np
import io
import hashlib
import datetime
import uuid

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
        model_name = "smainye/sw_finetunned_tune_whisper_small_model"
        
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
        model_name = "openai/whisper-small"
        
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
    """Transcribe audio using the Whisper model"""
    try:
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
                    max_length=448,
                    num_beams=5,
                    do_sample=True,
                    temperature=0.6,
                    top_p=0.9
                )
            else:  # English
                predicted_ids = model.generate(
                    input_features,
                    language=language,
                    task="transcribe",
                    max_length=448,
                    num_beams=4,
                    do_sample=False
                )
        
        # Decode transcription
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        return transcription.strip()
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
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
