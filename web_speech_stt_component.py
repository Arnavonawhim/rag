"""
Web Speech API Component for Streamlit
Provides browser-native speech recognition without Python dependencies
"""

import streamlit as st
import streamlit.components.v1 as components

def stt_input(language='en-US', key='stt_default'):
    """
    Create a speech-to-text input component using Web Speech API
    
    Args:
        language (str): Language code for speech recognition
        key (str): Unique key for the component
    
    Returns:
        str: Transcribed text or None
    """
    
    # HTML and JavaScript for Web Speech API
    html_code = f"""
    <div id="stt_container" style="width: 100%; padding: 0;">
        <button id="stt_btn" 
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
        <div id="stt_status" style="margin-top: 8px; font-size: 0.8rem; color: #666; min-height: 20px;"></div>
    </div>

    <script>
    (function() {{
        // Prevent multiple initializations
        if (window.sttInitialized) return;
        window.sttInitialized = true;
        
        const button = document.getElementById('stt_btn');
        const status = document.getElementById('stt_status');
        let recognition = null;
        let isListening = false;

        // Check Web Speech API support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
            button.innerHTML = '⚠️ Not Supported';
            button.disabled = true;
            status.innerHTML = 'Web Speech API not supported';
            return;
        }}

        // Initialize Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = '{language}';
        recognition.maxAlternatives = 1;

        button.addEventListener('click', function() {{
            if (!isListening) {{
                startListening();
            }} else {{
                stopListening();
            }}
        }});

        function startListening() {{
            try {{
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
            }} catch (error) {{
                console.error('Start listening error:', error);
                status.innerHTML = 'Error starting microphone';
                stopListening();
            }}
        }}

        function stopListening() {{
            isListening = false;
            button.innerHTML = '🎤 Voice Input';
            button.style.background = '#ff4b4b';
            
            if (recognition) {{
                try {{
                    recognition.stop();
                }} catch (error) {{
                    console.error('Stop recognition error:', error);
                }}
            }}
        }}

        recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript.trim();
            status.innerHTML = `Recognized: ${{transcript}}`;
            
            // Send result back to Streamlit
            const iframe = window.frameElement;
            if (iframe) {{
                iframe.contentWindow.parent.postMessage({{
                    type: 'streamlit:componentValue',
                    key: '{key}',
                    value: transcript
                }}, '*');
            }}
            
            // Also try direct method
            if (window.parent && window.parent !== window) {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: transcript
                }}, '*');
            }}
            
            stopListening();
        }};

        recognition.onerror = function(event) {{
            console.error('Speech recognition error:', event.error);
            let errorMsg = 'Recognition error';
            if (event.error === 'no-speech') {{
                errorMsg = 'No speech detected';
            }} else if (event.error === 'network') {{
                errorMsg = 'Network error';
            }} else if (event.error === 'not-allowed') {{
                errorMsg = 'Microphone access denied';
            }}
            status.innerHTML = errorMsg;
            stopListening();
        }};

        recognition.onend = function() {{
            if (isListening && status.innerHTML === 'Listening... Speak now!') {{
                status.innerHTML = 'No speech detected';
            }}
            stopListening();
        }};
    }})();
    </script>
    """
    
    # Create component and handle return value
    try:
        component_value = components.html(html_code, height=80)
        return component_value
    except Exception as e:
        st.error(f"Voice component error: {{e}}")
        return None
