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
    render_history_grid
)

# Update the page config for better layout
st.set_page_config(
    page_title="Kasuku Transcriber",
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
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True  # Show welcome initially
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'home'  # 'home' or 'history'
    # Add state for current transcription result
    if 'current_transcription' not in st.session_state:
        st.session_state.current_transcription = None
    if 'current_transcription_language' not in st.session_state:
        st.session_state.current_transcription_language = None
    # Add state to track if user just logged in
    if 'first_login' not in st.session_state:
        st.session_state.first_login = True  # 'home' or 'history' 

# Update this section in your main_app() function in app.py

def main_app():
    """Main application after login"""
    load_css()
    
    # Render sidebar and get language selection
    selected_language, language_code = render_sidebar()
    
    # Route to appropriate view based on current_view
    if st.session_state.current_view == 'history':
        render_history_grid()
        return
    
    # Home view - main transcription interface
    # Load appropriate model based on language
    if language_code == "sw":
        processor, model, device = load_swahili_model()
    else:
        processor, model, device = load_english_model()
    
    if processor is None or model is None:
        st.error("Failed to load model. Please try again.")
        return
    
    # Check if we should show welcome message
    show_welcome = st.session_state.get('show_welcome', True)
    
    # Render main interface
    col1, col2, col3 = render_main_interface(show_welcome=show_welcome)
    
    # Main recording interface
    with col2:
        recorded_audio = st.audio_input(f"Record yourself in {selected_language}")
        
        audio_data = None
        sample_rate = None
        
        if recorded_audio is not None:
            # Hide welcome message when recording starts
            st.session_state.show_welcome = False
            
            # Only clear current transcription if it's a new recording
            # (This prevents clearing when just interacting with buttons)
            if 'current_audio_bytes' not in st.session_state:
                st.session_state.current_audio_bytes = None
            
            current_audio_bytes = recorded_audio.getvalue()
            if current_audio_bytes != st.session_state.current_audio_bytes:
                # New recording - clear previous transcription
                st.session_state.current_transcription = None
                st.session_state.current_transcription_language = None
                st.session_state.current_audio_bytes = current_audio_bytes
            
            audio_data, sample_rate = process_recorded_audio(recorded_audio)
        else:
            # No audio recorded - clear the stored audio bytes
            st.session_state.current_audio_bytes = None
        
        # Transcribe button
        if audio_data is not None:
            if st.button("Transcribe Audio", 
                        type="secondary",
                        icon=":material/speech_to_text:", 
                        key="transcribe_button"):
                with st.spinner(f"Transcribing {selected_language} audio... Please wait."):
                    processed_audio, processed_sr = preprocess_audio(audio_data, sample_rate)
                    
                    if processed_audio is not None:
                        transcription = transcribe_audio(
                            processor, model, device, processed_audio, language_code
                        )
                        
                        if transcription:
                            # Store current transcription in session state
                            st.session_state.current_transcription = transcription
                            st.session_state.current_transcription_language = selected_language
                            # Clear the show_welcome flag after successful transcription
                            st.session_state.show_welcome = False
    
    # Show current transcription result if it exists
    if st.session_state.get('current_transcription'):
        render_transcription_result(
            st.session_state.current_transcription, 
            st.session_state.current_transcription_language
        )
    
    # Show welcome message again if no current transcription and no audio
    if not st.session_state.get('current_transcription') and recorded_audio is None:
        st.session_state.show_welcome = True
    
    
def main():
    """Main function to handle authentication flow"""
    # Initialize session state variables
    initialize_session_state()
    
    # Show login page or main app based on authentication status
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
