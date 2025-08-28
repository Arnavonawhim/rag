"""
Web Speech API Component for Streamlit
Provides browser-native speech recognition without Python dependencies
"""

import streamlit as st
import streamlit.components.v1 as components

def stt_input(language='en-US', key=None):
    """
    Create a speech-to-text input component using Web Speech API
    
    Args:
        language (str): Language code for speech recognition
        key (str): Unique key for the component
    
    Returns:
        str: Transcribed text or None
    """
    
    # Generate unique key if not provided
    if key is None:
        key = f"stt_input_{id(language)}"
    
    # HTML and JavaScript for Web Speech API
    html_code = f"""
    <div id="{key}_container" style="width: 100%; padding: 0;">
        <button id="{key}_btn" 
                style="width: 100%; 
                       height: 2.5rem; 
                       background: #ff4b4b; 
                       color: white; 
                       border: none; 
                       border-radius: 4px; 
                       cursor: pointer;
                       font-size: 0.9rem;
                       font-weight: 500;">
            🎤 Voice Input
        </button>
        <div id="{key}_status" style="margin-top: 8px; font-size: 0.8rem; color: #666;"></div>
    </div>

    <script>
    (function() {{
        const button = document.getElementById('{key}_btn');
        const status = document.getElementById('{key}_status');
        let recognition = null;
        let isListening = false;

        // Check Web Speech API support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
            button.innerHTML = '⚠️ Not Supported';
            button.disabled = true;
            status.innerHTML = 'Web Speech API not supported in this browser';
            return;
        }}

        // Initialize Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = '{language}';

        button.addEventListener('click', function() {{
            if (!isListening) {{
                startListening();
            }} else {{
                stopListening();
            }}
        }});

        function startListening() {{
            isListening = true;
            button.innerHTML = '🔴 Listening...';
            button.style.background = '#dc3545';
            status.innerHTML = 'Listening... Speak now!';
            
            recognition.start();
            
            // Auto-stop after 10 seconds
            setTimeout(() => {{
                if (isListening) {{
                    stopListening();
                }}
            }}, 10000);
        }}

        function stopListening() {{
            isListening = false;
            button.innerHTML = '🎤 Voice Input';
            button.style.background = '#ff4b4b';
            status.innerHTML = '';
            
            if (recognition) {{
                recognition.stop();
            }}
        }}

        recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            status.innerHTML = `Recognized: ${{transcript}}`;
            
            // Send result to Streamlit
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: transcript
            }}, '*');
            
            stopListening();
        }};

        recognition.onerror = function(event) {{
            console.error('Speech recognition error:', event.error);
            status.innerHTML = `Error: ${{event.error}}`;
            stopListening();
        }};

        recognition.onend = function() {{
            stopListening();
        }};
    }})();
    </script>
    """
    
    # Return the component result
    return components.html(html_code, height=80, key=key)

def create_voice_input_fallback():
    """
    Fallback voice input using existing Python-based solution
    """
    if st.button("🎤 Voice Input (Python)", use_container_width=True):
        st.info("Using Python-based voice recognition...")
        # This would use your existing voice_utils functions
        return None
    return None
