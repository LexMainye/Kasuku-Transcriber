import streamlit as st
from backend import authenticate_user, filter_transcriptions, delete_transcription

def load_css():
    """Load custom CSS styling for the application"""
    st.markdown("""
    <style>
        /* Import Google Material Symbols */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        
        /* Import Satoshi font */
        @import url('https://api.fontshare.com/v2/css?f[]=satoshi@900,700,500,400&display=swap');
        
        /* Apply Satoshi font to all text */
        * {
            font-family: 'Satoshi', sans-serif;
        }
        
        /* Title styling with Satoshi */
        h1.kasuku-title {
            font-family: 'Satoshi', sans-serif;
            font-weight: 900;
            font-size: 2.5rem;
            text-align: center;
            color: #333;
            letter-spacing: -0.02em;
        }
        
        /* Updated Button styling with different colors for actions */
        .stButton > button[data-testid="baseButton-secondary"] {
            font-family: 'Satoshi', sans-serif;
            font-weight: 700;
            width: 100%;
            background-color: #ff4b4b !important;  /* Red color for danger actions */
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
        
        /* Hover effect for danger buttons */
        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background-color: #ff6b6b !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }
        
        /* Primary button style (for Transcribe button) */
        .stButton > button[data-testid="baseButton-primary"] {
            font-family: 'Satoshi', sans-serif;
            font-weight: 700;
            width: 100%;
            background-color: #81C784 !important;  /* Light green for primary actions */
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Hover effect for primary buttons */
        .stButton > button[data-testid="baseButton-primary"]:hover {
            background-color: #A5D6A7 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }
        
        /* Copy button styling */
        .copy-button {
            background-color: #2196F3 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.3rem 0.8rem !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            margin: 0.2rem !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 4px !important;
        }
        
        .copy-button:hover {
            background-color: #1976D2 !important;
            transform: translateY(-1px) !important;
        }
        
        /* Delete button styling for individual items */
        .delete-button {
            background-color: #f44336 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.3rem 0.8rem !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            margin: 0.2rem !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 4px !important;
        }
        
        .delete-button:hover {
            background-color: #d32f2f !important;
            transform: translateY(-1px) !important;
        }
        
        /* Clear transcription button styling */
        .clear-transcription-button {
            background-color: #f44336 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            margin: 0.2rem !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 4px !important;
            margin-left: 10px !important;
        }
        
        .clear-transcription-button:hover {
            background-color: #d32f2f !important;
            transform: translateY(-1px) !important;
        }
        
        /* Add spacing between buttons */
        .stButton {
            margin: 0.5rem 0;
        }
        
        /* Remove green colors from other elements */
        .main-header, .greeting-message, .info-box, .success-box,
        .user-info, .scrollable-history, .chat-message {
            border-color: #dee2e6;
            background-color: #f8f9fa;
            color: inherit;
        }
        
        .chat-language {
            color: #666;
        }
        
        .stTextInput > div > div > input {
            border-color: #dee2e6 !important;
        }
        
        .stTextInput > div > div > input:focus {
            box-shadow: 0 0 0 2px rgba(0,0,0,0.1) !important;
            border-color: #666 !important;
        }
        
        /* Apply Satoshi to specific elements */
        .streamlit-expanderHeader,
        .stTextInput label,
        .stSelectbox label,
        .stMarkdown,
        .stText {
            font-family: 'Satoshi', sans-serif !important;
        }
        
        /* Language icon styling */
        .language-icon {
            font-family: 'Material Symbols Outlined';
            font-size: 24px;
            vertical-align: middle;
            margin-right: 8px;
        }
        
        /* Search icon styling */
        .search-icon {
            font-family: 'Material Symbols Outlined';
            font-size: 24px;
            vertical-align: middle;
            margin-right: 8px;
            color: #666;
        }
        
        /* Container for search input with icon */
        .search-container {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        /* Filter icon styling */
        .filter-icon {
            font-family: 'Material Symbols Outlined';
            font-size: 24px;
            vertical-align: middle;
            margin-right: 8px;
            color: #666;
        }
        
        /* Container for filter with icon */
        .filter-container {
            display: flex;
            align-items: center;
            margin: 1rem 0;
        }
        
        /* Updated delete icon styling */
        .delete-container {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: -8px;  /* Adjust spacing */
        }
        
        .material-symbols-outlined.delete-icon {
            font-family: 'Material Symbols Outlined';
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            font-size: 24px;
            color: #ff4b4b;
            vertical-align: middle;
        }
        
        /* Material Symbols button styling */
        .material-button {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
        }
        
        .material-button .material-symbols-outlined {
            font-family: 'Material Symbols Outlined' !important;
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
            font-size: 20px !important;
            line-height: 1 !important;
        }
        
        /* Chat bubble styling with action buttons */
        .chat-bubble {
            background-color: white;
            border-radius: 15px;
            padding: 0.8rem;
            margin: 0.5rem 0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            border-left: 3px solid #81C784;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .chat-bubble:hover {
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
            transform: translateX(2px);
        }
        
        .chat-bubble .timestamp {
            font-size: 0.7rem;
            color: #666;
            margin-bottom: 0.2rem;
        }
        
        .chat-bubble .language-tag {
            font-size: 0.8rem;
            color: #81C784;
            font-weight: 600;
            margin-bottom: 0.3rem;
        }
        
        .chat-bubble .message {
            font-size: 0.9rem;
            line-height: 1.4;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .chat-bubble .actions {
            display: flex;
            justify-content: flex-end;
            gap: 0.5rem;
            margin-top: 0.5rem;
            padding-top: 0.5rem;
            border-top: 1px solid #eee;
        }
        
        /* Scrollable container styling */
        .scrollable-history {
            max-height: 400px;
            overflow-y: auto;
            padding-right: 10px;
            margin: 1rem 0;
        }
        
        /* Updated floating accessibility button */
        .floating-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background-color: white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .floating-button[data-active="true"] {
            background-color: #81C784;
        }
        
        .floating-button[data-active="true"] .accessibility-icon {
            color: white;
        }
        
        .floating-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .accessibility-icon {
            font-family: 'Material Symbols Outlined';
            font-size: 24px;
            color: #333;
            transition: color 0.3s ease;
        }
        
        /* Screen reader tooltip */
        .screen-reader-tooltip {
            position: fixed;
            bottom: 80px;
            right: 20px;
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
            display: none;
            pointer-events: none;
        }
        
        .floating-button:hover + .screen-reader-tooltip {
            display: block;
        }

        /* Success message styling */
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 0.5rem;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
            margin: 0.5rem 0;
            font-size: 0.9rem;
        }
        
        /* Success box styling */
        .success-box {
            background-color: #f8f9fa;
            border: 2px solid #81C784;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        /* Button container for transcription result */
        .transcription-buttons {
            display: flex;
            justify-content: flex-start;
            gap: 10px;
            margin-top: 1rem;
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
    """Display centered login page in main content area"""
    # Create three columns with the middle one containing the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Centered title and subtitle
        st.markdown("<h1 style='text-align: center;'>Kasuku ASR 🦜</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Speech Recognition for Non Standard Speech</h4>", unsafe_allow_html=True)
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Centered login header
        st.markdown("<h3 style='text-align: center;'>Login</h3>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            email = st.text_input("Email Address or Phone Number", placeholder="Enter your email or phone number")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_button:
                if email and password:
                    is_valid, user_name = authenticate_user(email, password)
                    if is_valid:
                        st.session_state.authenticated = True
                        st.session_state.user_name = user_name
                        st.session_state.user_email = email
                        st.success(f"Welcome, {user_name}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                else:
                    st.error("Please enter both email and password.")
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Demo credentials centered
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### Demo Access")
        st.markdown("**Email:** alex@kasuku.com")
        st.markdown("**Password:** password")
        st.markdown("**Phone:** +254712345678")
        st.markdown("</div>", unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with language selection and history"""
    with st.sidebar:
        # Language selection with icon
        st.markdown("""
        ### <span class="language-icon">language</span> Language
        """, unsafe_allow_html=True)
        
        language_options = {
            "English ": "en",
            "Swahili ": "sw"
        }
        selected_language = st.selectbox(
            "Select Language",
            options=list(language_options.keys()),
            index=0,
            key="language_selector",
            label_visibility="collapsed"
        )
        language_code = language_options[selected_language]
        
        st.markdown("---")
        
        # Transcription History in sidebar with scrollable container
        st.markdown("### Transcription History")
        
        # Search and filter in sidebar with icon
        st.markdown("""
        <div class="search-container">
            <span class="search-icon">search</span>
            <span>Search</span>
        </div>
        """, unsafe_allow_html=True)
        
        search_query = st.text_input(
            "Search transcriptions",
            placeholder="Search transcriptions...",
            key="sidebar_search",
            label_visibility="collapsed"
        )
        
        # Add filter section with icon
        st.markdown("""
        <div class="filter-container">
            <span class="filter-icon">filter_alt</span>
            <span>Filter</span>
        </div>
        """, unsafe_allow_html=True)
        
        language_filter = st.selectbox(
            "Filter by",
            ["All", "English (Kenya)", "Swahili (Kenya)"],
            key="sidebar_language_filter",
            label_visibility="collapsed"
        )
        
        # Display transcription history
        render_transcription_history(search_query, language_filter, "sidebar")
        
        # Clear all button
        col_clear, col_spacer = st.columns([2, 1])
        with col_clear:
            if st.button(
                "Clear All Transcriptions",
                type="secondary",
                use_container_width=True,
                key="clear_history"
            ):
                st.session_state.transcription_history = []
                st.rerun()

        st.markdown("---")
        
        # User info section
        st.markdown("### User Info")
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="font-size: 20px;">person</span>
            <span>{st.session_state.user_name}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", type="secondary", use_container_width=True, key="sidebar_logout"):
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

def add_screen_reader_js():
    """Add screen reader functionality JavaScript"""
    return """
    <script>
        function speak(text, shouldCancel = false) {
            if ('speechSynthesis' in window) {
                if (shouldCancel) {
                    window.speechSynthesis.cancel();
                    return;
                }
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 1;
                utterance.pitch = 1;
                window.speechSynthesis.speak(utterance);
            }
        }

        function toggleScreenReader() {
            const button = document.querySelector('#accessibilityButton');
            const icon = button.querySelector('.accessibility-icon');
            
            if (button.getAttribute('data-active') === 'true') {
                speak('', true);  // Cancel any ongoing speech
                button.setAttribute('data-active', 'false');
                button.style.backgroundColor = 'white';
                icon.style.color = '#333';
            } else {
                button.setAttribute('data-active', 'true');
                button.style.backgroundColor = '#81C784';
                icon.style.color = 'white';
                
                // Collect all visible text
                const textElements = document.querySelectorAll('.chat-bubble .message, .stMarkdown p, .stText p');
                let textToRead = [];
                
                textElements.forEach(el => {
                    if (el.offsetParent !== null) {  // Check if element is visible
                        textToRead.push(el.textContent);
                    }
                });
                
                speak(textToRead.join('. '));
            }
        }

        // Keyboard shortcut
        document.addEventListener('keydown', (e) => {
            if (e.altKey && e.key === 'r') {
                toggleScreenReader();
            }
        });
    </script>
    """

def add_accessibility_features():
    """Add accessibility features like screen reader"""
    st.markdown(add_screen_reader_js(), unsafe_allow_html=True)
    st.markdown(f"""
        <div class="floating-button" 
             onclick="toggleScreenReader()" 
             id="accessibilityButton"
             data-active="false">
            <span class="material-symbols-outlined accessibility-icon">accessibility_new</span>
        </div>
        <div class="screen-reader-tooltip">
            Screen Reader Available (Alt + R)
        </div>
    """, unsafe_allow_html=True)

def render_main_interface():
    """Render the main transcription interface"""
    # Center title and add welcome message
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="kasuku-title">Kasuku ASR 🦜</h1>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
            <h3>Hello {st.session_state.user_name} 👋</h3>
        </div>
        """, unsafe_allow_html=True)
    
    return col1, col2, col3

def render_transcription_result(transcription, selected_language):
    """Render the transcription result with copy and clear functionality"""
    st.markdown("### Transcription Result")
    
    # Display result with copy button
    escaped_transcription = transcription.replace("'", "\\'").replace('"', '\\"').replace('`', '\\`')
    result_id = "main_result"
    
    st.markdown(f"""
    <div class="success-box">
    <strong>Transcribed Text ({selected_language}):</strong><br>
    <p style="font-size: 1.2rem; margin-top: 0.5rem; font-weight: 500; color: #2d5016;">{transcription}</p>
    <div class="transcription-buttons">
        <button id="copy_{result_id}" class="copy-button" onclick="copyToClipboard_{result_id}()" style="font-size: 1rem; padding: 0.5rem 1rem;">
            <span class="material-symbols-outlined" style="font-size: 18px;">content_copy</span>
            Copy Transcription
        </button>
        <button class="clear-transcription-button" onclick="clearTranscription()">
            <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
            Clear Transcription
        </button>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inject the JS for the main result copy function
    st.markdown(copy_to_clipboard_js(escaped_transcription, result_id), unsafe_allow_html=True)
    
    # Inject the JS for clear transcription function
    st.markdown(clear_transcription_js(), unsafe_allow_html=True)