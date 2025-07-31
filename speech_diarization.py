import os
import time
from datetime import datetime
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

class SpeechDiarization:
    def __init__(self):
        # Azure Speech Service configuration
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = os.getenv('AZURE_SPEECH_REGION')
        self.speech_endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
        
        # Initialize Azure Speech SDK
        self._initialize_speech_config()
        
    def _initialize_speech_config(self):
        """Initialize Azure Speech SDK configuration for diarization"""
        if not self.speech_key:
            raise ValueError("Azure Speech Key must be set in .env file")
        
        # Use endpoint if available, otherwise use region
        if self.speech_endpoint:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                endpoint=self.speech_endpoint
            )
        elif self.speech_region:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.speech_region
            )
        else:
            raise ValueError("Either AZURE_SPEECH_ENDPOINT or AZURE_SPEECH_REGION must be set in .env file")
        
        # Configure speech recognition settings for diarization
        self.speech_config.speech_recognition_language = "en-US"
        
    def _conversation_transcriber_recognition_canceled_cb(self, evt: speechsdk.SessionEventArgs):
        """Callback for canceled recognition"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] Canceled event')
    
    def _conversation_transcriber_session_stopped_cb(self, evt: speechsdk.SessionEventArgs):
        """Callback for session stopped"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] SessionStopped event')
    
    def _conversation_transcriber_transcribed_cb(self, evt: speechsdk.SpeechRecognitionEventArgs):
        """Callback for final transcribed results with speaker identification"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'\n[{timestamp}] TRANSCRIBED:')
        
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f'\tText: {evt.result.text}')
            print(f'\tSpeaker ID: {evt.result.speaker_id}')
            print(f'\tOffset: {evt.result.offset}')
            print(f'\tDuration: {evt.result.duration}')
            print()
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print(f'\tNOMATCH: Speech could not be TRANSCRIBED: {evt.result.no_match_details}')
    
    def _conversation_transcriber_transcribing_cb(self, evt: speechsdk.SpeechRecognitionEventArgs):
        """Callback for intermediate transcription results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] TRANSCRIBING:')
        print(f'\tText: {evt.result.text}')
        print(f'\tSpeaker ID: {evt.result.speaker_id}')
    
    def _conversation_transcriber_session_started_cb(self, evt: speechsdk.SessionEventArgs):
        """Callback for session started"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] SessionStarted event')
    
    def recognize_from_file(self, audio_file_path):
        """Perform speech recognition with diarization from an audio file"""
        print(f"Starting speech recognition with diarization from file: {audio_file_path}")
        print("=" * 60)
        
        try:
            # Create audio config from file
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
            
            # Create conversation transcriber
            conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            transcribing_stop = False
            
            def stop_cb(evt: speechsdk.SessionEventArgs):
                """Callback that signals to stop continuous recognition upon receiving an event"""
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f'[{timestamp}] CLOSING on {evt}')
                nonlocal transcribing_stop
                transcribing_stop = True
            
            # Connect callbacks to the events fired by the conversation transcriber
            conversation_transcriber.transcribed.connect(self._conversation_transcriber_transcribed_cb)
            conversation_transcriber.transcribing.connect(self._conversation_transcriber_transcribing_cb)
            conversation_transcriber.session_started.connect(self._conversation_transcriber_session_started_cb)
            conversation_transcriber.session_stopped.connect(self._conversation_transcriber_session_stopped_cb)
            conversation_transcriber.canceled.connect(self._conversation_transcriber_recognition_canceled_cb)
            
            # Stop transcribing on either session stopped or canceled events
            conversation_transcriber.session_stopped.connect(stop_cb)
            conversation_transcriber.canceled.connect(stop_cb)
            
            # Start transcribing
            conversation_transcriber.start_transcribing_async()
            
            # Wait for completion
            while not transcribing_stop:
                time.sleep(0.5)
            
            # Stop transcribing
            conversation_transcriber.stop_transcribing_async()
            
            print("\nTranscription completed!")
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise
    
    def recognize_from_microphone(self):
        """Perform real-time speech recognition with diarization from microphone"""
        print("Starting real-time speech recognition with diarization from microphone...")
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            # Create audio config using default microphone
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            
            # Create conversation transcriber
            conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            transcribing_stop = False
            
            def stop_cb(evt: speechsdk.SessionEventArgs):
                """Callback that signals to stop continuous recognition upon receiving an event"""
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f'[{timestamp}] CLOSING on {evt}')
                nonlocal transcribing_stop
                transcribing_stop = True
            
            # Connect callbacks to the events fired by the conversation transcriber
            conversation_transcriber.transcribed.connect(self._conversation_transcriber_transcribed_cb)
            conversation_transcriber.transcribing.connect(self._conversation_transcriber_transcribing_cb)
            conversation_transcriber.session_started.connect(self._conversation_transcriber_session_started_cb)
            conversation_transcriber.session_stopped.connect(self._conversation_transcriber_session_stopped_cb)
            conversation_transcriber.canceled.connect(self._conversation_transcriber_recognition_canceled_cb)
            
            # Stop transcribing on either session stopped or canceled events
            conversation_transcriber.session_stopped.connect(stop_cb)
            conversation_transcriber.canceled.connect(stop_cb)
            
            # Start transcribing
            conversation_transcriber.start_transcribing_async()
            
            # Keep the program running until interrupted
            while not transcribing_stop:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping transcription...")
            conversation_transcriber.stop_transcribing_async()
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise

def main():
    """Main function"""
    print("Azure Speech Recognition with Diarization")
    print("=" * 45)
    
    # Check environment variables
    if not os.getenv('AZURE_SPEECH_KEY'):
        print("Error: Please set AZURE_SPEECH_KEY in your .env file")
        print("See env_example.txt for reference")
        return
    
    if not os.getenv('AZURE_SPEECH_ENDPOINT') and not os.getenv('AZURE_SPEECH_REGION'):
        print("Error: Please set either AZURE_SPEECH_ENDPOINT or AZURE_SPEECH_REGION in your .env file")
        print("See env_example.txt for reference")
        return
    
    try:
        # Create speech diarization instance
        diarization = SpeechDiarization()
        
        # Ask user for input method
        print("\nChoose input method:")
        print("1. Audio file")
        print("2. Microphone (real-time)")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            # Get audio file path
            audio_file = input("Enter the path to your audio file: ").strip()
            if not os.path.exists(audio_file):
                print(f"Error: File '{audio_file}' not found")
                return
            diarization.recognize_from_file(audio_file)
            
        elif choice == "2":
            # Start real-time recognition from microphone
            diarization.recognize_from_microphone()
            
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 