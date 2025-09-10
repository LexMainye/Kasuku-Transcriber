import streamlit as st
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import numpy as np
import io

# Configure Streamlit page
st.set_page_config(
    page_title="Parrot ASR",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c5f88;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff8dc;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f4e79;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-size: 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2c5f88;
    }
    .model-info {
        background-color: #e8f4fd;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #d1ecf1;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource  
def load_swahili_model():
    """Load the Swahili fine-tuned Whisper model with caching"""
    try:
        model_name = "smainye/sw_cv_tune_whisper_tiny_best_model"
        
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

def main():
    # Header
    st.markdown('<div class="main-header"> Parrot ASR 🦜</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.markdown("## Language Selection")
    
    # Language selection
    language_options = {
        "Swahili": "sw",
        "English": "en"
    }
    selected_language = st.sidebar.selectbox(
        "Select Language to record yourself in:",
        options=list(language_options.keys()),
        index=0
    )
    language_code = language_options[selected_language]
    
    # Load appropriate model based on language selection
    if selected_language == "Swahili":
        processor, model, device = load_swahili_model()
        model_name = "smainye/sw_cv_tune_whisper_tiny_best_model"
    else:
        processor, model, device = load_english_model()
        model_name = "openai/whisper-small"
    
    if processor is None or model is None:
        st.error(f"Failed to load the {selected_language} model. Please try again.")
        return
    

    
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
    
        
        # Audio recording widget
        recorded_audio = st.audio_input(f"Record in yourself in {selected_language}")
        
        audio_data = None
        sample_rate = None
        
        if recorded_audio is not None:
            try:
                # Convert recorded audio
                audio_bytes = recorded_audio.getvalue()
                audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes), sr=None)
                
            except Exception as e:
                st.error(f"Error processing recorded audio: {str(e)}")
        
        # Transcribe button
        if audio_data is not None:
            st.markdown("---")
            if st.button("Transcribe Audio", type="primary"):
                with st.spinner(f"Transcribing {selected_language} audio... Please wait."):
                    # Preprocess audio
                    processed_audio, processed_sr = preprocess_audio(audio_data, sample_rate)
                    
                    if processed_audio is not None:
                        # Transcribe
                        transcription = transcribe_audio(
                            processor, model, device, processed_audio, language_code
                        )
                        
                        if transcription:
                            st.markdown("### Transcription Result")
                            
                            st.markdown(f"""
                            <div class="success-box">
                            <strong>Transcribed Text ({selected_language}):</strong><br>
                            <p style="font-size: 1.2rem; margin-top: 0.5rem; font-weight: 500; color: #2d5016;">{transcription}</p>
                            </div>
                            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
    <p> Powered by Fine-tunned Whisper Models | Specialized for Non Standard Kenyan speech </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()