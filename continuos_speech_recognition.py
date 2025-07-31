import os
import time
from datetime import datetime
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

class SimpleSpeechRecognition:
    def __init__(self):
        # Azure Speech Service configuration
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = os.getenv('AZURE_SPEECH_REGION')
        # self.speech_endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
        
        # Initialize Azure Speech SDK
        self._initialize_speech_config()
        
    def _initialize_speech_config(self):
        """Initialize Azure Speech SDK configuration"""
        if not self.speech_key or not self.speech_region:
            raise ValueError("Azure Speech Key and Region must be set in .env file")
        
       
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )
        
        # Configure speech recognition settings
        self.speech_config.speech_recognition_language = "en-US"
        self.speech_config.enable_continuous_recognition = True
        self.speech_config.enable_dictation = True
        
        # Optional: Enable detailed logging (commented out to avoid issues)
        # self.speech_config.set_property(
        #     speechsdk.PropertyId.SpeechServiceConnection_LogFilename, 
        #     "speech_log.txt"
        # )
        
    def _recognized_callback(self, evt):
        """Callback for recognized speech"""
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Recognized: {evt.result.text}")
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print(f"No speech could be recognized: {evt.result.no_match_details}")
    
    def _recognizing_callback(self, evt):
        """Callback for intermediate recognition results"""
        current_text = evt.result.text
        if current_text:
            print(f"Recognizing: {current_text}", end='\r')
    
    def _canceled_callback(self, evt):
        """Callback for canceled recognition"""
        print(f"Recognition canceled: {evt.result.cancellation_details.reason}")
        if evt.result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.result.cancellation_details.error_details}")
    
    def _session_started_callback(self, evt):
        """Callback for session started"""
        print("Speech recognition session started")
    
    def _session_stopped_callback(self, evt):
        """Callback for session stopped"""
        print("Speech recognition session stopped")
    
    def start_recognition(self):
        """Start real-time speech recognition using default microphone"""
        print("Starting real-time speech recognition...")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        try:
            # Create audio config using default microphone
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            
            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Connect callbacks
            speech_recognizer.recognized.connect(self._recognized_callback)
            speech_recognizer.recognizing.connect(self._recognizing_callback)
            speech_recognizer.canceled.connect(self._canceled_callback)
            speech_recognizer.session_started.connect(self._session_started_callback)
            speech_recognizer.session_stopped.connect(self._session_stopped_callback)
            
            # Start continuous recognition
            speech_recognizer.start_continuous_recognition()
            
            # Keep the program running
            while True:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping speech recognition...")
            speech_recognizer.stop_continuous_recognition()
        except Exception as e:
            print(f"Error during recognition: {e}")

def main():
    """Main function"""
    print("Azure Simple Real-Time Speech Recognition")
    print("=" * 45)
    
    # Check environment variables
    if not os.getenv('AZURE_SPEECH_KEY') or not os.getenv('AZURE_SPEECH_REGION'):
        print("Error: Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION in your .env file")
        print("See env_example.txt for reference")
        return
    
    try:
        # Create and start speech recognition
        recognizer = SimpleSpeechRecognition()
        recognizer.start_recognition()
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 