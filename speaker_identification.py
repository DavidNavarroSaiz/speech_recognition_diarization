import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

class SpeakerIdentification:
    def __init__(self):
        # Azure Speech Service configuration
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = os.getenv('AZURE_SPEECH_REGION')
        self.speech_endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
        
        if not self.speech_key:
            raise ValueError("Azure Speech Key must be set in .env file")
        
        self.profiles_file = "speaker_profiles.json"
        self.profiles = self.load_profiles()
        
        # Initialize Azure Speech SDK
        self._initialize_speech_config()
        
    def load_profiles(self):
        """Load existing speaker profiles from file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _initialize_speech_config(self):
        """Initialize Azure Speech SDK configuration for diarization"""
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
        
    def get_speaker_name(self, speaker_id):
        """Get speaker name from profile ID"""
        if speaker_id in self.profiles:
            return self.profiles[speaker_id]["name"]
        return f"Guest {speaker_id[-4:]}"  # Fallback to guest with last 4 chars
    
    def list_profiles(self):
        """List all available speaker profiles"""
        if not self.profiles:
            print("\n📋 No speaker profiles found.")
            print("💡 Please run voice_registration.py first to create profiles.")
            return
        
        print(f"\n📋 Available Speaker Profiles ({len(self.profiles)} total):")
        print("=" * 60)
        for i, (profile_id, profile_info) in enumerate(self.profiles.items(), 1):
            print(f"{i}. Name: {profile_info['name']}")
            print(f"   Profile ID: {profile_id}")
            print(f"   Created: {profile_info['created_date']}")
            print("-" * 60)
    
    def _conversation_transcriber_recognition_canceled_cb(self, evt: speechsdk.SessionEventArgs):
        """Callback for canceled recognition"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] ❌ Canceled event')
    
    def _conversation_transcriber_session_stopped_cb(self, evt: speechsdk.SessionEventArgs):
        """Callback for session stopped"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] 🛑 SessionStopped event')
    
    def _conversation_transcriber_transcribed_cb(self, evt: speechsdk.SpeechRecognitionEventArgs):
        """Callback for final transcribed results with speaker identification"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Get speaker name from profile if available
            speaker_id = evt.result.speaker_id
            speaker_name = self.get_speaker_name(speaker_id)
            
            print(f'\n[{timestamp}] ✅ TRANSCRIBED:')
            print(f'👤 Speaker: {speaker_name}')
            print(f'💬 Text: {evt.result.text}')
            print(f'⏱️  Offset: {evt.result.offset}')
            print(f'⏱️  Duration: {evt.result.duration}')
            print()
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print(f'\n[{timestamp}] ❌ NOMATCH: Speech could not be TRANSCRIBED: {evt.result.no_match_details}')
    
    def _conversation_transcriber_transcribing_cb(self, evt: speechsdk.SpeechRecognitionEventArgs):
        """Callback for intermediate transcription results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Get speaker name from profile if available
        speaker_id = evt.result.speaker_id
        speaker_name = self.get_speaker_name(speaker_id)
        
        print(f'[{timestamp}] 🔄 TRANSCRIBING:')
        print(f'👤 Speaker: {speaker_name}')
        print(f'💬 Text: {evt.result.text}')
    
    def _conversation_transcriber_session_started_cb(self, evt: speechsdk.SessionEventArgs):
        """Callback for session started"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f'[{timestamp}] 🚀 SessionStarted event')
    
    def transcribe_file(self, audio_file_path):
        """Perform speech recognition with speaker identification from an audio file"""
        print(f"\n🎵 Starting transcription with speaker identification")
        print(f"📁 File: {audio_file_path}")
        print("=" * 60)
        
        if not self.profiles:
            print("⚠️  No speaker profiles found. Speakers will be identified as 'Guest X'")
            print("💡 Run voice_registration.py to create speaker profiles for better identification.")
        
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
                print(f'[{timestamp}] 🛑 CLOSING on {evt}')
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
            
            print("\n✅ Transcription completed!")
            
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
            raise
    
    def transcribe_microphone(self):
        """Perform real-time speech recognition with speaker identification from microphone"""
        print("\n🎤 Starting real-time transcription with speaker identification")
        print("🎙️  Using default microphone")
        print("⏹️  Press Ctrl+C to stop")
        print("=" * 60)
        
        if not self.profiles:
            print("⚠️  No speaker profiles found. Speakers will be identified as 'Guest X'")
            print("💡 Run voice_registration.py to create speaker profiles for better identification.")
        
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
                print(f'[{timestamp}] 🛑 CLOSING on {evt}')
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
            print("\n⏹️  Stopping transcription...")
            conversation_transcriber.stop_transcribing_async()
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
            raise

def main():
    """Main function for speaker identification"""
    print("🎤 Azure Speaker Identification System")
    print("=" * 45)
    
    # Check environment variables
    if not os.getenv('AZURE_SPEECH_KEY'):
        print("❌ Error: Please set AZURE_SPEECH_KEY in your .env file")
        print("See env_example.txt for reference")
        return
    
    if not os.getenv('AZURE_SPEECH_ENDPOINT') and not os.getenv('AZURE_SPEECH_REGION'):
        print("❌ Error: Please set either AZURE_SPEECH_ENDPOINT or AZURE_SPEECH_REGION in your .env file")
        print("See env_example.txt for reference")
        return
    
    try:
        # Create speaker identification instance
        identification = SpeakerIdentification()
        
        while True:
            print("\n📋 Choose an option:")
            print("1. List speaker profiles")
            print("2. Transcribe audio file")
            print("3. Real-time transcription (microphone)")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                identification.list_profiles()
                
            elif choice == "2":
                audio_file = input("Enter the path to your audio file: ").strip()
                if not os.path.exists(audio_file):
                    print(f"❌ Error: File '{audio_file}' not found")
                    continue
                identification.transcribe_file(audio_file)
                
            elif choice == "3":
                identification.transcribe_microphone()
                
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 