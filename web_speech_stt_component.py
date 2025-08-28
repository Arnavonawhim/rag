"""
Simple Web Speech API Component for Streamlit
"""

import streamlit as st
import streamlit.components.v1 as components

def stt_input():
    """
    Simple speech-to-text component using Web Speech API
    """
    
    html_code = """
    <div style="width: 100%; padding: 0;">
        <button id="voiceBtn" 
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
        <div id="voiceStatus" style="margin-top: 8px; font-size: 0.8rem; color: #666; min-height: 20px;"></div>
    </div>

    <script>
    (function() {
        const button = document.getElementById('voiceBtn');
        const status = document.getElementById('voiceStatus');
        let recognition = null;
        let isListening = false;

        // Check support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            button.innerHTML = '⚠️ Not Supported';
            button.disabled = true;
            status.innerHTML = 'Web Speech API not supported';
            return;
        }

        // Setup recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        button.onclick = function() {
            if (!isListening) {
                startListening();
            }
        };

        function startListening() {
            isListening = true;
            button.innerHTML = '🔴 Listening...';
            button.style.background = '#dc3545';
            status.innerHTML = 'Listening... Speak now!';
            
            recognition.start();
            
            setTimeout(() => {
                if (isListening) {
                    stopListening();
                }
            }, 10000);
        }

        function stopListening() {
            isListening = false;
            button.innerHTML = '🎤 Voice Input';
            button.style.background = '#ff4b4b';
            recognition.stop();
        }

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript.trim();
            status.innerHTML = 'Recognized: ' + transcript;
            
            // Store in sessionStorage for Streamlit to pick up
            sessionStorage.setItem('voice_transcript', transcript);
            sessionStorage.setItem('voice_timestamp', Date.now());
            
            stopListening();
        };

        recognition.onerror = function(event) {
            status.innerHTML = 'Error: ' + event.error;
            stopListening();
        };

        recognition.onend = function() {
            stopListening();
        };
    })();
    </script>
    """
    
    return components.html(html_code, height=80)
