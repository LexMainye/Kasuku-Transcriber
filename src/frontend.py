import streamlit as st
import random
from backend import authenticate_user, filter_transcriptions, delete_transcription,copy_transcription,create_transcription_item

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

    </style>
    """, unsafe_allow_html=True)

def copy_to_clipboard_js(text, element_id):
    """Generate JavaScript to copy text to clipboard"""
    return f"""
    <script>
        function copyToClipboard_{element_id}() {{
            const text = `{text}`;
            navigator.clipboard.writeText(text).then(function() {{
                // Show temporary success message
                const button = document.getElementById('copy_{element_id}');
                const originalText = button.innerHTML;
                button.innerHTML = '✓ Copied!';
                button.style.backgroundColor = '#4CAF50';
                setTimeout(function() {{
                    button.innerHTML = originalText;
                    button.style.backgroundColor = '#2196F3';
                }}, 2000);
            }}, function(err) {{
                console.error('Could not copy text: ', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
            }});
        }}
    </script>
    """

def delete_transcription_js(original_index, prefix):
    """Generate JavaScript to handle delete confirmation"""
    return f"""
    <script>
        function confirmDelete_{prefix}_{original_index}() {{
            if (confirm('Are you sure you want to delete this transcription?')) {{
                // Trigger the Streamlit button click
                const deleteButton = document.getElementById('delete_{prefix}_{original_index}');
                if (deleteButton) {{
                    deleteButton.click();
                }}
            }}
        }}
    </script>
    """

def clear_transcription_js():
    """Generate JavaScript to handle clear transcription"""
    return """
    <script>
        function clearTranscription() {
            // Find the transcription result container
            const resultContainer = document.querySelector('.success-box');
            if (resultContainer) {
                // Add a fade-out effect
                resultContainer.style.opacity = '0.5';
                resultContainer.style.transition = 'opacity 0.3s ease';
                
                // After a brief delay, trigger the Streamlit clear button
                setTimeout(function() {
                    const clearButton = document.getElementById('clear_transcription_button');
                    if (clearButton) {
                        clearButton.click();
                    }
                }, 300);
            }
        }
    </script>
    """

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
            Parrot Transcriber 🦜
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
                <strong>Phone:</strong> +254712345678
            </p>
            <p style='font-family: Space Grotesk; font-size: 0.9rem; color: #666; margin-top: 1rem; display: flex; align-items: center; gap: 8px;'>
                <span class="material-icons" style="font-size: 18px;">info</span>
                Use these credentials to test the application features.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Use this enhanced version
if __name__ == "__main__":
    login_page()

def render_sidebar():
    """Render the sidebar with navigation and settings"""
    with st.sidebar:
        st.markdown('<h1 class="kasuku-title"><span style="color: #000000;">Parrot Transcriber</span> 🦜</h1>', unsafe_allow_html=True)
        
        st.markdown("##")
        
        # New Transcirption Button with Google-style icon
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
        
        # Language selection (only show on home view)
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
            # Default values for history view
            selected_language = "English"
            language_code = "en"
        
        st.markdown("##")
        
        # User info section
        st.markdown("### :material/info: User Info")
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="font-size: 20px;">person</span>
            <span>{st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)
       
        st.markdown("##")
        
        # Logout button 
        if st.button("Logout", type="primary",icon=":material/logout:", use_container_width=True, key="sidebar_logout"):
            for key in ['authenticated', 'user_name', 'user_email']:
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
            
            # Inject the JS for this specific copy function
            st.markdown(copy_to_clipboard_js(escaped_transcription, element_id), unsafe_allow_html=True)
            
            # Inject the JS for delete confirmation
            st.markdown(delete_transcription_js(original_index, prefix), unsafe_allow_html=True)
    
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

def render_transcription_card(item, original_index):
    """Render a single transcription card in vertical layout"""
    # Determine language flag and color
    if item['language'] == "English":
        flag = "🇬🇧"
        border_color = "#D22B2B"  # Red for English
    else:
        flag = "🇹🇿"
        border_color = "#2196F3"  # Blue for Swahili
    
    # Escape transcription for JavaScript
    transcription_text = item.get("transcription", "")
    escaped_transcription = (
        transcription_text.replace("'", "\\'")
                          .replace('"', '\\"')
                          .replace("`", "\\`")
    )
    card_id = f"card_{original_index}"
    
    st.markdown(f"""
    <div id="{card_id}" class="transcription-card"
         style="border-left:4px solid {border_color};
                border-radius:8px;
                padding:16px;
                margin-bottom:16px;
                background:#D3FF98;
                box-shadow:0 2px 4px rgba(0,0,0,0.1);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div>
                <span style="font-size:1.2rem;">{flag}</span>
                <span style="font-weight:bold;margin-left:4px;">{item.get('language','')}</span>
            </div>
            <div style="font-size:0.8rem;color:#777;">{item.get('timestamp','')}</div>
        </div>
        <div>
            <p style="margin:0;font-size:1rem;">{transcription_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add JavaScript for card interactions
    st.markdown(f"""
    <script>
        function copyCardText_{card_id}() {{
            const text = `{escaped_transcription}`;
            navigator.clipboard.writeText(text).then(function() {{
                const button = document.querySelector('#{card_id} .copy-card-btn');
                const icon = button.querySelector('.material-symbols-outlined');
                const originalText = button.textContent;
                
                button.innerHTML = '<span class="material-symbols-outlined">check</span> Copied!';
                button.style.backgroundColor = '#4CAF50';
                
                setTimeout(function() {{
                    button.innerHTML = '<span class="material-symbols-outlined">content_copy</span> Copy';
                    button.style.backgroundColor = '#2196F3';
                }}, 2000);
            }});
        }}
        
        function deleteCard_{card_id}() {{
            if (confirm('Are you sure you want to delete this transcription?')) {{
                // Create a hidden Streamlit button to trigger the deletion
                const deleteButton = document.createElement('button');
                deleteButton.style.display = 'none';
                deleteButton.id = 'delete_trigger_{card_id}';
                document.body.appendChild(deleteButton);
                
                // Simulate a click to trigger Streamlit's callback
                deleteButton.click();
                
                // Hide the card with animation
                const card = document.getElementById('{card_id}');
                card.style.opacity = '0.5';
                card.style.transform = 'scale(0.95)';
                card.style.transition = 'all 0.3s ease';
                setTimeout(() => {{
                    card.style.display = 'none';
                }}, 300);
            }}
        }}
        
    </script>
    """, unsafe_allow_html=True)
    
    # Add a hidden Streamlit button for actual copying & deletion
    col1, col2, col3 = st.columns([1, 5, 1])  # Middle column is wider for spacing

    with col1:
        if st.button("Copy ", key=f"copy_{original_index}",icon=":material/content_copy:", help="Copy this transcription"):
            transcription_text = copy_transcription(original_index, st.session_state.transcription_history)
            if transcription_text:
                try:
                    import pyperclip
                    pyperclip.copy(transcription_text)
                    st.success("Copied to clipboard!")
                except ImportError:
                    # Fallback to JavaScript method
                    escaped_text = transcription_text.replace("'", "\\'").replace('"', '\\"').replace('`', '\\`')
                    st.markdown(f"""
                    <script>
                        navigator.clipboard.writeText("{escaped_text}");
                    </script>
                    """, unsafe_allow_html=True)
                    st.success("Copied to clipboard!")
            else:
                st.error("Transcription not found")
            st.rerun()

    with col3:  # Delete button in the rightmost column
        if st.button("Delete", key=f"delete_{original_index}",icon=":material/delete_forever:", help="Delete this transcription"):
            delete_transcription(original_index, st.session_state.transcription_history)
            st.rerun()
    

def render_main_interface(show_welcome=True):
    """Render the main transcription interface"""
    # Center title and add welcome message
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
    
        
        # Only show welcome message if show_welcome is True
        if show_welcome:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
                <h3> Hello {st.session_state.user_name} 👋 </h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Add empty space to maintain layout consistency
            st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)
    
    return col1, col2, col3

def render_transcription_result(transcription, selected_language):
    """Render the transcription result with copy, save, and discard functionality"""
    st.markdown("### Transcription Result")
    
    # Clean the transcription text - remove HTML tags if present
    import re
    import html
    
    def clean_transcription_text(text):
        if not text:
            return ""
        
        # Remove HTML tags
        clean_text = re.sub('<.*?>', '', text)
        
        # Decode HTML entities
        clean_text = html.unescape(clean_text)
        
        # Remove extra whitespace and comments
        clean_text = re.sub(r'<!--.*?-->', '', clean_text, flags=re.DOTALL)
        clean_text = ' '.join(clean_text.split())
        
        return clean_text.strip()
    
    # Clean the transcription
    clean_transcription = clean_transcription_text(transcription)
    
    # If still looks like HTML structure, try to extract meaningful content
    if not clean_transcription or len(clean_transcription) < 5:
        # Look for actual text content in the original
        lines = str(transcription).split('\n')
        for line in lines:
            line = line.strip()
            if (line and 
                not line.startswith('<') and 
                not line.startswith('<!--') and
                not any(css_word in line.lower() for css_word in ['style=', 'color:', 'font-', 'margin:', 'padding:']) and
                len(line) > 3):
                clean_transcription = line
                break
    
    # Final fallback
    if not clean_transcription:
        clean_transcription = "Error: Could not extract transcribed text"
    
    # Use Streamlit's success container instead of custom HTML
    with st.container():
        # Simple green border using CSS that definitely works
        st.markdown(f"""
        <div style="border: 2px solid #4CAF50; border-radius: 5px; padding: 20px; background-color: #D3FF98; margin: 10px 0;">
            <h4 style="color: #1A1A1A; margin: 0 0 10px 0;"> Transcribed Text ({selected_language}):</h4>
            <p style="font-size: 18px; color: #1A1A1A; margin: 0; font-weight: 500; line-height: 1.5;">{html.escape(clean_transcription)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Alternative: Use Streamlit's native success message if HTML still doesn't work
    # st.success(f"**Transcribed Text ({selected_language}):**\n\n{clean_transcription}")
    
    # Store clean transcription for buttons
    st.session_state.clean_transcription_for_buttons = clean_transcription
    
    # Create three columns for action buttons
    col1, col2, col3 = st.columns(3)
    
    # Initialize button states in session state if not exist
    if 'button_feedback' not in st.session_state:
        st.session_state.button_feedback = None
    
    with col1:
        copy_clicked = st.button(
            "Copy", 
            icon=":material/content_copy:", 
            use_container_width=True, 
            key="copy_transcription_btn",
            help="Copy transcription to clipboard"
        )
        
        if copy_clicked:
            # Use pyperclip if available, otherwise show the text to copy
            try:
                import pyperclip
                pyperclip.copy(clean_transcription)
                st.success("Copied to clipboard!")
            except ImportError:
                st.info(f"Copy this text: {clean_transcription}")
            
            st.session_state.button_feedback = "copied"
            # Don't rerun immediately to show the success message
    
    with col2:
        # Save button
        save_clicked = st.button(
            "Save", 
            icon=":material/save:", 
            use_container_width=True, 
            key="save_transcription_btn",
            help="Save transcription"
        )

        if save_clicked:
            # Create and save transcription item
            from backend import create_transcription_item

            transcription_item = create_transcription_item(
                transcription,
                selected_language,
                st.session_state.user_name
            )

            # Add to history
            st.session_state.transcription_history.append(transcription_item)

            # Clear current transcription from display
            st.session_state.current_transcription = None
            st.session_state.current_transcription_language = None

            # Set feedback state
            st.session_state.button_feedback = "saved"
            st.rerun()
    
    with col3:
        discard_clicked = st.button(
            "Discard", 
            icon=":material/delete_forever:", 
            use_container_width=True, 
            key="discard_transcription_btn",
            help="Discard transcription without saving"
        )
        
        if discard_clicked:
            st.session_state.current_transcription = None
            st.session_state.current_transcription_language = None
            st.session_state.button_feedback = "discarded"
            st.rerun()


def handle_transcription_actions():
    """Helper function to handle transcription actions in the main app flow"""
    # This can be called in your main app flow to ensure proper state management
    
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


def handle_transcription_actions():
    """Helper function to handle transcription actions in the main app flow"""
    # This can be called in your main app flow to ensure proper state management
    
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

