import streamlit as st
import librosa
import io

# Import from our modules
from backend import (
    load_swahili_model, 
    load_english_model, 
    preprocess_audio, 
    transcribe_audio,
    process_recorded_audio,
    create_transcription_item
)
from frontend import (
    load_css,
    login_page,
    render_sidebar,
    render_main_interface,
    render_transcription_result,
    add_accessibility_features
)

# Update the page config for better layout
st.set_page_config(
    page_title="Kasuku ASR",
    page_icon="🦜",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'transcription_history' not in st.session_state:
        st.session_state.transcription_history = []
    if 'show_success_message' not in st.session_state:
        st.session_state.show_success_message = False
    if 'success_message' not in st.session_state:
        st.session_state.success_message = ""

def main_app():
    """Main application after login"""
    load_css()
    
    # Render sidebar and get language selection
    selected_language, language_code = render_sidebar()
    
    # Load appropriate model based on language
    if language_code == "sw":
        processor, model, device = load_swahili_model()
    else:
        processor, model, device = load_english_model()
    
    if processor is None or model is None:
        st.error("Failed to load model. Please try again.")
        return
    
    # Render main interface
    col1, col2, col3 = render_main_interface()
    
    # Main recording interface
    with col2:
        recorded_audio = st.audio_input(f"Record yourself in {selected_language}")
        
        audio_data = None
        sample_rate = None
        
        if recorded_audio is not None:
            audio_data, sample_rate = process_recorded_audio(recorded_audio)
        
        # Transcribe button
        if audio_data is not None:
            st.markdown("---")
            if st.button("Transcribe Audio", type="primary", key="transcribe_button"):
                with st.spinner(f"Transcribing {selected_language} audio... Please wait."):
                    processed_audio, processed_sr = preprocess_audio(audio_data, sample_rate)
                    
                    if processed_audio is not None:
                        transcription = transcribe_audio(
                            processor, model, device, processed_audio, language_code
                        )
                        
                        if transcription:
                            # Create transcription item
                            transcription_item = create_transcription_item(
                                transcription, 
                                selected_language, 
                                st.session_state.user_name
                            )
                            
                            # Add to history
                            st.session_state.transcription_history.append(transcription_item)
                            
                            # Render result
                            render_transcription_result(transcription, selected_language)

def main():
    """Main function to handle authentication flow"""
    # Initialize session state variables
    initialize_session_state()
    
    # Show login page or main app based on authentication status
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()
        # Add accessibility features at the end
        add_accessibility_features()

if __name__ == "__main__":
    main()
