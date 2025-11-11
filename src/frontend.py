import streamlit as st
import random
from st_copy import copy_button

from backend import (
    authenticate_user, 
    filter_transcriptions, 
    delete_transcription,
    get_audio_base64, 
    cleanup_temp_audio, 
    text_to_speech  # <-- Google Cloud function
)
# ---------------------------------------------------

def load_css():
    """Load custom CSS styling for the application"""
    st.markdown("""
    <style>
        /* Import Google Material Symbols */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        
        /* Import Space Grotesk font with proper weights */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');
        
        /* Apply Space Grotesk font to entire application */
        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Base font settings */
        body {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 400;
            line-height: 1.4;
        }
        
        /* Title styling with Space Grotesk */
        h1.kasuku-title {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            text-align: center;
            color: #333;
            letter-spacing: -0.02em;
            margin-bottom: 1rem !important;
        }
        
        /* Headings with Space Grotesk */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
        }
        
        /* Streamlit specific elements */
        .stMarkdown, .stText, .stAlert, .stExpander, .stContainer {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Input labels and text */
        .stTextInput label, .stSelectbox label, .stTextArea label,
        .stNumberInput label, .stDateInput label, .stTimeInput label {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }
        
        /* Input fields */
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
        }
        
        /* Button styling with Space Grotesk */
        .stButton > button {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em;
        }
        
        /* Secondary button styling */
        .stButton > button[data-testid="baseButton-secondary"] {
            width: 100%;
            background-color: #ff4b4b !important;
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background-color: #ff6b6b !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }
        
        /* Primary button style */
        .stButton > button[data-testid="baseButton-primary"] {
            width: 100%;
            background-color: #81C784 !important;
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button[data-testid="baseButton-primary"]:hover {
            background-color: #A5D6A7 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        
        .streamlit-expanderContent {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Chat messages and history */
        .chat-bubble, .scrollable-history, .transcription-card {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .chat-bubble .timestamp {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 300 !important;
        }
        
        .chat-bubble .language-tag {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
        }
        
        .chat-bubble .message {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
        }
        
        /* Transcription cards */
        .transcription-card {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .card-lang-text {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
        }
        
        .card-timestamp {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 300 !important;
        }
        
        .card-text {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
        }
        
        /* Success messages and alerts */
        .success-message, .success-box, .stAlert {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Custom buttons */
        .copy-button, .delete-button, .clear-transcription-button {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
        }
        
        /* Material icons integration */
        .material-button {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Footer and additional text */
        .footer, .info-text, .help-text {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 300 !important;
        }
        
        /* Table styling */
        .stTable, .dataframe {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Progress bars and status elements */
        .stProgress > div > div > div {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Radio buttons and checkboxes */
        .stRadio > label, .stCheckbox > label {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
        }
        
        /* File uploader */
        .stFileUploader label {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
        }
        
        /* Metric cards */
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-weight: 600 !important;
        }
        
        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
        }

        /* Enhanced responsive typography */
        @media (max-width: 768px) {
            body {
                font-size: 14px;
            }
            
            h1.kasuku-title {
                font-size: 2rem !important;
            }
            
            .stButton > button {
                font-size: 0.9rem !important;
            }
        }

        /* Improve readability with better line heights */
        .stMarkdown p {
            line-height: 1.6 !important;
        }
        
        .chat-bubble .message {
            line-height: 1.5 !important;
        }
        
        .card-text {
            line-height: 1.5 !important;
        }
        
        /* Toast notifications */
        .copy-toast {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            background-color: #4CAF50;
            color: white;
            border-radius: 4px;
            z-index: 10000;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { 
                transform: translateX(100%); 
                opacity: 0; 
            }
            to { 
                transform: translateX(0); 
                opacity: 1; 
            }
        }
        
        /* Button hover effects */
        .stButton > button {
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }
                /* Hide default Streamlit button styling for icon buttons */
        .icon-btn button {
            background: none !important;
            border: none !important;
            padding: 8px !important;
            min-width: auto !important;
            width: 40px !important;
            height: 40px !important;
            border-radius: 50% !important;
            color: #555 !important;
            transition: all 0.3s ease !important;
            box-shadow: none !important;
        }
        
        .icon-btn button:hover {
            background-color: rgba(0,0,0,0.08) !important;
            transform: scale(1.1) !important;
            box-shadow: none !important;
        }
        
        .icon-btn button:active {
            transform: scale(0.95) !important;
        }
        
        /* Specific icon button colors */
        .icon-btn.speak-btn button:hover {
            color: #2196F3 !important;
            background-color: rgba(33, 150, 243, 0.1) !important;
        }
        
        .icon-btn.copy-btn button:hover {
            color: #4CAF50 !important;
            background-color: rgba(76, 175, 80, 0.1) !important;
        }
        
        .icon-btn.save-btn button:hover {
            color: #FF9800 !important;
            background-color: rgba(255, 152, 0, 0.1) !important;
        }
        
        .icon-btn.delete-btn button:hover {
            color: #f44336 !important;
            background-color: rgba(244, 67, 54, 0.1) !important;
        }
        
        .icon-btn.discard-btn button:hover {
            color: #9E9E9E !important;
            background-color: rgba(158, 158, 158, 0.1) !important;
        }
        
        /* Material icons styling */
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            font-size: 24px !important;
            vertical-align: middle;
        }
        
        /* Icon button container */
        .icon-buttons-row {
            display: flex;
            gap: 4px;
            align-items: center;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(0,0,0,0.1);
        }
        
        /* st-copy button customization */
        div[data-testid="column"] .icon-btn button p {
            margin: 0 !important;
            padding: 0 !important;
        }
        /* Icon button size variants */
        

        
        /* Large icons (32px) */
        .icon-btn.size-large button {
            width: 56px !important;
            height: 56px !important;
            padding: 12px !important;
        }
        
        .icon-btn.size-large button svg,
        .icon-btn.size-large .material-symbols-outlined {
            font-size: 36px !important;
            width: 36px !important;
            height: 36px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_icon_button(icon_name, button_key, button_class, tooltip):
    """Render a Material Icon button with Streamlit"""
    return st.button(
        f":material/{icon_name}:",
        key=button_key,
        help=tooltip,
        use_container_width=False,
        type="tertiary"
    )

def login_page():
    """Enhanced login page with Space Grotesk and Material Icons"""
    
    # Apply comprehensive Space Grotesk styling with Material Icons
    st.markdown("""
    <style>
        /* Import Space Grotesk and Material Icons */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        
        /* Material Icons base styling */
        .material-icons {
            font-family: 'Material Icons';
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            vertical-align: middle;
            margin-right: 8px;
        }
        
        .material-icons.md-18 { font-size: 18px; }
        .material-icons.md-20 { font-size: 20px; }
        .material-icons.md-24 { font-size: 24px; }
        .material-icons.md-28 { font-size: 28px; }
        .material-icons.md-32 { font-size: 32px; }
        
        /* Apply to all elements in the login container */
        .main .block-container {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .login-main-title {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            text-align: center;
            color: #333;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .login-subtitle {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 500 !important;
            font-size: 1.2rem !important;
            text-align: center;
            color: #666;
            margin-bottom: 2rem !important;
        }
        
        .login-section-title {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.5rem !important;
            text-align: center;
            margin: 1.5rem 0 !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        /* Style all text inputs with Material Icons in labels */
        div[data-testid="stTextInput"] label {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            display: flex !important;
            align-items: center !important;
        }
        
        div[data-testid="stTextInput"] label .material-icons {
            font-size: 20px !important;
            margin-right: 6px !important;
        }
        
        div[data-testid="stTextInput"] input {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
            font-size: 1rem !important;
        }
        
        /* Style buttons with Material Icons */
        div[data-testid="stButton"] button {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            letter-spacing: -0.01em;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
        }
        
        /* Style form elements */
        .stForm {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        /* Demo section styling with Material Icons */
        .demo-section {
            font-family: 'Space Grotesk', sans-serif !important;
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 2rem;
            border-left: 4px solid #81C784;
        }
        
        .demo-title {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            color: #333;
            margin-bottom: 1rem !important;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .demo-credential {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 400 !important;
            margin: 0.5rem 0;
            padding: 0.3rem 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .demo-credential .material-icons {
            font-size: 18px;
            color: #666;
        }
        
        /* Success/error messages */
        .stAlert {
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .stAlert .material-icons {
            margin-right: 8px;
        }
        
        /* Custom icon styling for labels */
        .icon-label {
            display: flex;
            align-items: center;
            gap: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create three columns with the middle one containing the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Centered title and subtitle with Material Icons
        st.markdown("""
            <h1 class='login-main-title'>
            Kasuku 🦜
            </h1>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 class='login-subtitle'>Speech Transcription for Non Standard Speech</h4>", unsafe_allow_html=True)
    
        
        # Login form with Material Icons
        with st.form("login_form", clear_on_submit=False):
            # Custom label with Material Icon for email/phone
            email = st.text_input(
                "Email Address or Phone Number",
                placeholder="Enter your email or phone number",
                help="Enter your email address or phone number",
                label_visibility="collapsed"  # Hide default label since we have custom one
            )
            
            # Custom label with Material Icon for password
            password = st.text_input(
                "Password", 
                type="password", 
                placeholder="Enter your password",
                help="Enter your  password",
                label_visibility="collapsed"  # Hide default label
            )
            
            submit_button = st.form_submit_button(
                "Login",
                icon=":material/login:",
                type="primary", 
                use_container_width=True
            )
            
            if submit_button:
                if email and password:
                    is_valid, user_name = authenticate_user(email, password)
                    if is_valid:
                        st.session_state.authenticated = True
                        st.session_state.user_name = user_name
                        st.session_state.user_email = email
                        st.session_state.first_login = True
                        st.success(f"Welcome back, {user_name}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.error("Please enter proper credentials.")
        
        # Demo credentials section with Material Icons
        st.markdown("""
        <div class='demo-section' style='background-color: #FFEA99;'>
            <h4 class='demo-title'>
                <span class="material-icons">badge</span>
                Demo Credentials
            </h4>
            <p class='demo-credential'>
                <span class="material-icons">email</span>
                <strong>Email:</strong> alex@kasuku.com
            </p>
            <p class='demo-credential'>
                <span class="material-icons">vpn_key</span>
                <strong>Password:</strong> password
            </p>
            <p class='demo-credential'>
                <span class="material-icons">phone</span>
                <strong>Phone:</strong> 0712345678
            </p>
            <p style='font-family: Space Grotesk; font-size: 0.9rem; color: #666; margin-top: 1rem; display: flex; align-items: center; gap: 8px;'>
                <span class="material-icons" style="font-size: 18px;">info</span>
                Use these credentials to test the application features.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with navigation and enhanced TTS settings"""
    with st.sidebar:
        st.markdown('<h1 class="kasuku-title"><span style="color: #000000;">Kasuku</span> 🦜</h1>', unsafe_allow_html=True)
        
        st.markdown("##")
        
        # Navigation buttons
        if st.button(
            "Record Yourself",
            type="secondary" if st.session_state.current_view == 'Record Yourself' else "secondary",
            icon=":material/record_voice_over:",
            use_container_width=True,
            key="nav_home"
        ):
            st.session_state.current_view = 'Record Yourself'
            st.rerun()
        
        # History Button
        history_count = len(st.session_state.transcription_history)
        history_label = f"Saved Transcriptions ({history_count})" if history_count > 0 else "Saved Transcriptions"
        
        if st.button(
            history_label,
            type="secondary" if st.session_state.current_view == 'history' else "secondary",
            icon =":material/bookmark:",
            use_container_width=True,
            key="nav_history"
        ):
            st.session_state.current_view = 'history'
            st.rerun()
        
        st.markdown("##")
        
        # Language selection
        if st.session_state.current_view == 'Record Yourself':
            st.markdown("### :material/docs: Language to Transcribe")
            
            language_options = {
                "English": "en",
                "Swahili": "sw"
            }
            selected_language = st.selectbox(
                "Select Language",
                options=list(language_options.keys()),
                index=0,
                key="language_selector",
                label_visibility="collapsed"
            )
            language_code = language_options[selected_language]
        else:
            selected_language = "English"
            language_code = "en"
        
        st.markdown("##")
        
        # --- TTS SETTINGS ---
        # This is kept as it's used by our new Google TTS function
        st.markdown("### :material/volume_up: Text-to-Speech Settings")
        
        # Voice Selection
        st.selectbox(
            "Select Voice",
            options=["Female", "Male"], # These are logical names
            index=0,
            key="tts_voice_gender", # This session state is read by the speak buttons
            label_visibility="collapsed"
        )
        
        st.markdown("##")
        
        # User info and logout
        st.markdown("### :material/info: User Info")
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="font-size: 20px;">person</span>
            <span>{st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)
       
        st.markdown("##")
        
        if st.button("Logout", type="primary", icon=":material/logout:", use_container_width=True, key="sidebar_logout"):
            for key in ['authenticated', 'user_name', 'user_email', 'current_transcription', 
                       'current_transcription_language', 'current_audio_bytes', 'tts_voice_gender',
                       'tts_speech_rate', 'tts_voice_pitch', 'tts_engine']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    return selected_language, language_code

def render_transcription_history(search_query, language_filter, prefix=""):
    """Render transcription history with filtering and actions"""
    # Start scrollable container
    st.markdown('<div class="scrollable-history">', unsafe_allow_html=True)
    
    # Display filtered history
    if not st.session_state.transcription_history:
        st.info("No transcriptions yet")
    else:
        # Filter transcriptions
        filtered_history = filter_transcriptions(
            st.session_state.transcription_history, 
            search_query, 
            language_filter
        )
        
        # Display transcriptions in chat bubble style with actions
        for original_index, item in reversed(filtered_history):
            # Escape quotes in transcription for JavaScript
            escaped_transcription = item['transcription'].replace("'", "\\'").replace('"', '\\"').replace('`', '\\`')
            element_id = f"{prefix}_{original_index}"
            
            st.markdown(f"""
            <div class="chat-bubble">
                <div class="timestamp">{item['timestamp']}</div>
                <div class="language-tag">{item['language']}</div>
                <div class="message">{item['transcription']}</div>
                <div class="actions">
                    <button id="copy_{element_id}" class="copy-button" onclick="copyToClipboard_{element_id}()">
                        <span class="material-symbols-outlined" style="font-size: 16px;">content_copy</span>
                        Copy
                    </button>
                    <button class="delete-button" onclick="confirmDelete_{element_id}()">
                        <span class="material-symbols-outlined" style="font-size: 16px;">delete</span>
                        Delete
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    
    # End scrollable container
    st.markdown('</div>', unsafe_allow_html=True)

def render_history_grid():
    """Render transcription history in a vertical card format"""
    st.markdown('<h1 class="kasuku-title"> Saved Transcriptions </h1>', unsafe_allow_html=True)
    
    if not st.session_state.transcription_history:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; color: #666;'>
            <span class="material-symbols-outlined" style="font-size: 48px;">history</span>
            <h3>No transcriptions yet</h3>
            <p>Start recording to see your transcriptions here</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
   # Search and filter controls - top row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input(
            "Search transcriptions",
            icon=":material/search:",
            placeholder="Search by content...",
            key="history_search"
        )
    
    with col2:
        language_filter = st.selectbox(
            "Filter by Language",
            ["All", "English", "Swahili"],
            key="history_language_filter"
        )
    
    # Filter transcriptions
    filtered_history = filter_transcriptions(
        st.session_state.transcription_history,
        search_query,
        language_filter
    )
    
    # Clear All button - positioned below search/filter but above cards
    if filtered_history:
        # Create a centered container for the Clear All button
        clear_col1, clear_col2, = st.columns([2, 1])
        with clear_col2:
            if st.button("Clear All Transcriptions", 
                        type="secondary",
                        icon=":material/clear_all:",
                        use_container_width=True,
                        key="history_clear_all"):
                if st.session_state.transcription_history:
                    st.session_state.transcription_history = []
                    st.success("All transcriptions cleared!")
                    st.rerun()
    
    # Filter transcriptions
    filtered_history = filter_transcriptions(
        st.session_state.transcription_history,
        search_query,
        language_filter
    )
    
    if not filtered_history:
        st.info("No transcriptions match your search criteria.")
        return
    
    # Add CSS for the vertical card styling
    st.markdown("""
    <style>
        .transcription-cards-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .transcription-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #81C784;
            transition: all 0.3s ease;
            position: relative;
            min-height: 120px;
            resize: both;
            overflow: auto;
            width: 100%;
            max-width: 100%;
        }
        
        .transcription-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .card-language {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            color: #555;
        }
        
        .card-timestamp {
            font-size: 0.8rem;
            color: #888;
        }
        
        .card-content {
            margin-bottom: 1.2rem;
        }
        
        .card-text {
            font-size: 1rem;
            line-height: 1.5;
            color: #333;
            margin: 0;
            word-wrap: break-word;
        }
        
        .card-actions {
            display: flex;
            gap: 0.8rem;
            justify-content: flex-end;
            padding-top: 0.8rem;
            border-top: 1px solid #f0f0f0;
        }
        
        .card-button {
            background: none;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .copy-card-btn {
            background-color: #2196F3;
            color: white;
        }
        
        .copy-card-btn:hover {
            background-color: #1976D2;
            transform: translateY(-1px);
        }
        
        .delete-card-btn {
            background-color: #f44336;
            color: white;
        }
        
        .delete-card-btn:hover {
            background-color: #d32f2f;
            transform: translateY(-1px);
        }
        
        /* Resize handle styling */
        .transcription-card::-webkit-resizer {
            border-width: 2px;
            border-style: solid;
            border-color: transparent #81C784 #81C784 transparent;
        }
        
        /* Material icons styling */
        .material-symbols-outlined {
            font-size: 18px !important;
            vertical-align: middle;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Start the cards container
    st.markdown('<div class="transcription-cards-container">', unsafe_allow_html=True)
    
    # Display transcriptions vertically (newest first)
    filtered_history = list(reversed(filtered_history))
    
    for original_index, item in filtered_history:
        render_transcription_card(item, original_index)
    
    # Close the cards container
    st.markdown('</div>', unsafe_allow_html=True)

# --- UPDATED FUNCTION ---
def render_transcription_card(item, original_index):
    """Render a single transcription card with Material Icon buttons"""
    from st_copy import copy_button

    # Determine language settings
    if item['language'] == "English":
        border_color = "#E7440E"
        lang_code = "en"
    else:
        border_color = "#15D0E9"
        lang_code = "sw"
    
    transcription_text = item.get("transcription", "")
    
    # Display the card
    st.markdown(f"""
    <div class="transcription-card"
         style="border-left:4px solid {border_color};
                border-radius:8px;
                padding:16px;
                margin-bottom:16px;
                background:#D3FF98;
                box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div>
                <span style="font-weight:bold;">{item.get('language','')}</span>
            </div>
            <div style="font-size:0.8rem;color:#777;">{item.get('timestamp','')}</div>
        </div>
        <div>
            <p style="margin:0;font-size:1rem;">{transcription_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Icon buttons row
    cols = st.columns([0.4, 0.4, 0.4, 10], vertical_alignment="center")
    
    # Speak button
    with cols[0]:
        st.markdown('<div class="icon-btn speak-btn size-xlarge">', unsafe_allow_html=True)
        speak_button_clicked = st.button(
            ":material/volume_up:",
            key=f"speak_{original_index}",
            help="Speak",
            type="tertiary",
            use_container_width=False
        )
        
        if speak_button_clicked:
            with st.spinner("Generating speech..."):
                selected_gender = st.session_state.get('tts_voice_gender', 'Female')
                
                # 1. GET BASE64 DIRECTLY
                audio_base64, engine_used = text_to_speech(
                    transcription_text,
                    language=lang_code,
                    gender=selected_gender
                )
                
                if audio_base64:
                    # Save audio data to session state
                    audio_data_key = f"audio_{original_index}"
                    st.session_state[audio_data_key] = {
                        'base64': audio_base64,
                        'format': "mp3",
                        'gender': selected_gender,
                        'engine': engine_used
                        # No more 'file_path' or 'pending_cleanup'
                    }
                    
                    # 2. PLAY FILE using the stored base64 data
                    r = random.randint(0, 1000000) # Generate a random number
                    st.markdown(f"""
                    <audio autoplay data-run="{r}" style="display: none;">
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                    """, unsafe_allow_html=True)
                    st.toast(f"Playing ({selected_gender} voice)")
                    
                    # Store in main audio_data for potential reuse
                    if 'audio_data' not in st.session_state:
                        st.session_state.audio_data = {}
                    st.session_state.audio_data.update(st.session_state[audio_data_key])
                else:
                    st.error("Failed to generate speech.")

    # Copy button
    with cols[1]:
        st.markdown('<div class="icon-btn copy-btn">', unsafe_allow_html=True)
        copy_button(transcription_text, key=f"copy_{original_index}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Delete button
    with cols[2]:
        st.markdown('<div class="icon-btn delete-btn">', unsafe_allow_html=True)
        if st.button(
            ":material/delete:",
            key=f"delete_{original_index}",
            help="Delete",
            type="tertiary",
            use_container_width=False
        ):
            delete_transcription(original_index, st.session_state.transcription_history)
            st.toast("Deleted", icon="🗑️")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def stop_all_speech():
    """Stop all currently playing TTS"""
    # This function is fine as-is
    st.markdown("""
    <script>
        if (typeof speechSynthesis !== 'undefined' && speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }
    </script>
    """, unsafe_allow_html=True)
    

def render_main_interface(show_welcome=True):
    """Render the main transcription interface"""
    # This function is fine as-is
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if show_welcome:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
                <h3> Hello {st.session_state.user_name} 👋 </h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)
    
    return col1, col2, col3

# --- UPDATED FUNCTION ---
def render_transcription_result(transcription, selected_language):
    """Render the transcription result with Material Icon action buttons"""
    from st_copy import copy_button
    
    # Clean the transcription text
    import re
    import html
    
    def clean_transcription_text(text):
        if not text:
            return ""
        clean_text = re.sub('<.*?>', '', text)
        clean_text = html.unescape(clean_text)
        clean_text = re.sub(r'', '', clean_text, flags=re.DOTALL)
        clean_text = ' '.join(clean_text.split())
        return clean_text.strip()
    
    clean_transcription = clean_transcription_text(transcription)
    
    if not clean_transcription:
        clean_transcription = "Error: Could not extract transcribed text"
    
    lang_code = "sw" if selected_language == "Swahili" else "en"
    
    # Display transcription
    with st.container():
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; border-radius: 5px; padding: 20px; background-color: #D3FF98; margin: 10px 0;">
            <h4 style="color: #1A1A1A; margin: 0 0 10px 0;">{selected_language} Transcription Result : </h4>
            <p style="font-size: 18px; color: #1A1A1A; margin: 0; font-weight: 500; line-height: 1.5;">{html.escape(clean_transcription)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Icon action buttons
    cols = st.columns([0.5, 0.5, 0.5, 0.5, 6], vertical_alignment="center")
    
    # Speak
    with cols[0]:
        st.markdown('<div class="icon-btn speak-btn">', unsafe_allow_html=True)
        speak_button_clicked = st.button(":material/volume_up:", key="speak_btn", help="Speak", type="tertiary")
        
        if speak_button_clicked:
            if clean_transcription.strip():
                with st.spinner("Generating speech..."):
                    selected_gender = st.session_state.get('tts_voice_gender', 'Female')
                    
                    # 1. GET BASE64 DIRECTLY
                    audio_base64, engine_used = text_to_speech(
                        clean_transcription,
                        language=lang_code,
                        gender=selected_gender
                    )
                    
                    if audio_base64:
                        # Save audio data to session state
                        st.session_state.current_audio_data = {
                            'base64': audio_base64,
                            'format': "mp3",
                            'gender': selected_gender,
                            'engine': engine_used
                            # No more 'file_path' or 'pending_cleanup'
                        }
                        
                        # 2. PLAY FILE using the stored base64 data
                        r = random.randint(0,1000000) # Generate a random number
                        st.markdown(f"""
                        <audio autoplay data-run="{r}" style="display: none;">
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                        """, unsafe_allow_html=True)
                        st.toast(f"Playing ({selected_gender} {engine_used} voice)")
                        
                        # Store in main audio_data for potential reuse
                        if 'audio_data' not in st.session_state:
                            st.session_state.audio_data = {}
                        st.session_state.audio_data.update(st.session_state.current_audio_data)
                    else:
                        st.error("Failed to generate speech.")
            else:
                st.warning("No text to speak.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Copy
    with cols[1]:
        st.markdown('<div class="icon-btn copy-btn">', unsafe_allow_html=True)
        copy_button(clean_transcription, key="copy_main_result")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Save
    with cols[2]:
        st.markdown('<div class="icon-btn save-btn">', unsafe_allow_html=True)
        if st.button(":material/bookmark:", key="save_btn", help="Save", type="tertiary"):
            from backend import create_transcription_item

            transcription_item = create_transcription_item(
                clean_transcription,
                selected_language,
                st.session_state.user_name
            )
            st.session_state.transcription_history.append(transcription_item)
            st.session_state.current_transcription = None
            st.session_state.current_transcription_language = None
            st.toast("Saved!", icon="💾")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Discard
    with cols[3]:
        st.markdown('<div class="icon-btn discard-btn">', unsafe_allow_html=True)
        if st.button(":material/delete:", key="discard_btn", help="Discard", type="tertiary"):
            st.session_state.current_transcription = None
            st.session_state.current_transcription_language = None
            st.toast("Discarded", icon="🗑️")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def handle_transcription_actions():
    """Helper function to handle transcription actions in the main app flow"""
    # This function is fine as-is
    
    # Clear any lingering feedback messages after a delay
    if 'feedback_clear_time' not in st.session_state:
        st.session_state.feedback_clear_time = None
    
    # Auto-clear feedback after some time
    import time
    current_time = time.time()
    
    if (st.session_state.get('button_feedback') and 
        st.session_state.feedback_clear_time and 
        current_time - st.session_state.feedback_clear_time > 3):
        st.session_state.button_feedback = None
        st.session_state.feedback_clear_time = None