import streamlit as st
import random
from backend import authenticate_user, filter_transcriptions, delete_transcription,copy_transcription,create_transcription_item

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
        /* Add these styles to your load_css() function */

        /* Navigation button styling */
        .stButton > button[data-testid="baseButton-primary"] {
            font-family: 'Satoshi', sans-serif;
            font-weight: 700;
            width: 100%;
            background-color: #81C784 !important;
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin: 0.25rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Transcription card styling */
        .transcription-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
            min-height: 180px;
            display: flex;
            flex-direction: column;
        }

        .transcription-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
            border-color: #81C784;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #f0f0f0;
        }

        .card-language {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-flag {
            font-size: 1.2rem;
        }

        .card-lang-text {
            font-weight: 600;
            color: #81C784;
            font-size: 0.85rem;
        }

        .card-timestamp {
            font-size: 0.7rem;
            color: #666;
            text-align: right;
            line-height: 1.2;
        }

        .card-content {
            flex: 1;
            margin: 0.5rem 0;
        }

        .card-text {
            font-size: 0.9rem;
            line-height: 1.4;
            color: #333;
            margin: 0;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .card-actions {
            display: flex;
            justify-content: flex-end;
            gap: 0.5rem;
            margin-top: auto;
            padding-top: 0.5rem;
            border-top: 1px solid #f0f0f0;
        }

        .card-button {
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }

        .card-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }

        .copy-card-btn {
            background: #2196F3;
        }

        .copy-card-btn:hover {
            background: #1976D2;
        }

        .expand-card-btn {
            background: #FF9800;
        }

        .expand-card-btn:hover {
            background: #F57C00;
        }

        .delete-card-btn {
            background: #f44336;
        }

        .delete-card-btn:hover {
            background: #d32f2f;
        }

        .card-button .material-symbols-outlined {
            font-size: 18px;
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }

        .card-full-text {
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 2px solid #81C784;
            animation: slideDown 0.3s ease;
        }

        .full-text-content {
            background: #f8f9fa;
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 3px solid #81C784;
        }

        .full-text-content p {
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.5;
            color: #333;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Grid responsive layout */
        @media (max-width: 768px) {
            .transcription-card {
                margin: 0.25rem 0;
                min-height: 160px;
            }
            
            .card-actions {
                gap: 0.25rem;
            }
            
            .card-button {
                width: 32px;
                height: 32px;
            }
            
            .card-button .material-symbols-outlined {
                font-size: 16px;
            }
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
        st.markdown("<h1 style='text-align: center;'>Kasuku Transcriber 🦜</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Speech Transcription for Non Standard Speech</h4>", unsafe_allow_html=True)
        
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
                        st.session_state.first_login = True  # Set first login flag
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
    """Render the sidebar with navigation and settings"""
    with st.sidebar:
        st.markdown('<h1 class="kasuku-title"><span style="color: #000000;">Kasuku Transcriber</span> 🦜</h1>', unsafe_allow_html=True)
        
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
                background:#fff;
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
    col1, col2, col3 = st.columns([1, 6, 1])  # Middle column is wider for spacing

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
                <h3>Hello {st.session_state.user_name} 👋</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Add empty space to maintain layout consistency
            st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)
    
    return col1, col2, col3

def render_transcription_result(transcription, selected_language):
    """Render the transcription result with copy, save, and discard functionality"""
    st.markdown("### Transcription Result")
    
    # Display result in a styled container
    st.markdown(f"""
    <div class="success-box">
        <strong>Transcribed Text ({selected_language}):</strong><br>
        <p style="font-size: 1.2rem; margin-top: 0.5rem; font-weight: 500; color: #2d5016;">{transcription}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for action buttons
    col1, col2, col3 = st.columns(3)
    
    # Initialize button states in session state if not exist
    if 'button_feedback' not in st.session_state:
        st.session_state.button_feedback = None
    
    with col1:
        # Copy button
        copy_clicked = st.button(
            "Copy", 
            icon=":material/content_copy:", 
            use_container_width=True, 
            key="copy_transcription_btn",
            help="Copy transcription to clipboard"
        )
        
        if copy_clicked:
            # JavaScript to copy to clipboard
            # Escape the transcription text outside the f-string to avoid backslash issues
            escaped_text = transcription.replace('`', '\\`').replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <script>
                if (navigator.clipboard) {{
                    navigator.clipboard.writeText(`{escaped_text}`).then(function() {{
                        console.log('Text copied to clipboard');
                    }});
                }} else {{
                    // Fallback for older browsers
                    var textArea = document.createElement("textarea");
                    textArea.value = `{escaped_text}`;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                }}
            </script>
            """, unsafe_allow_html=True)
            
            st.session_state.button_feedback = "copied"
            st.rerun()
    
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
        # Discard button
        discard_clicked = st.button(
            "Discard", 
            icon=":material/delete_forever:", 
            use_container_width=True, 
            key="discard_transcription_btn",
            help="Discard transcription without saving"
        )
        
        if discard_clicked:
            # Clear current transcription from display
            st.session_state.current_transcription = None
            st.session_state.current_transcription_language = None
            
            # Set feedback state
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

