import os
import json
import uuid
import wave
import sounddevice as sd
import soundfile as sf
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VoiceRegistration:
    def __init__(self):
        # Azure Speaker Recognition API configuration
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = os.getenv('AZURE_SPEECH_REGION')
        self.speech_endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
        
        if not self.speech_key:
            raise ValueError("Azure Speech Key must be set in .env file")
        
        # Set up the endpoint for Speaker Recognition API
        if self.speech_endpoint:
            self.api_endpoint = self.speech_endpoint
        elif self.speech_region:
            self.api_endpoint = f"https://{self.speech_region}.api.cognitive.microsoft.com"
        else:
            raise ValueError("Either AZURE_SPEECH_ENDPOINT or AZURE_SPEECH_REGION must be set in .env file")
        
        self.profiles_file = "speaker_profiles.json"
        self.profiles = self.load_profiles()
        
    def load_profiles(self):
        """Load existing speaker profiles from file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_profiles(self):
        """Save speaker profiles to file"""
        with open(self.profiles_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)
    
    def record_audio(self, duration=30, sample_rate=16000):
        """Record audio from microphone for specified duration"""
        print(f"\n🎤 Recording {duration} seconds of audio...")
        print("📝 Please read the provided text clearly and naturally.")
        print("⏰ Recording will start in 3 seconds...")
        
        for i in range(3, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
        
        print("🎙️  Recording started! Speak now...")
        
        # Record audio using sounddevice
        try:
            # Record audio
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            
            # Show progress while recording
            for i in range(duration):
                progress = (i + 1) / duration * 100
                print(f"\r⏳ Recording progress: {progress:.1f}%", end="", flush=True)
                time.sleep(1)
            
            print("\n✅ Recording completed!")
            
            # Wait for recording to finish
            sd.wait()
            
            return recording, sample_rate
            
        except Exception as e:
            print(f"❌ Error during recording: {e}")
            return None, sample_rate
    
    def save_audio_to_file(self, recording, sample_rate, filename):
        """Save recorded audio to WAV file"""
        try:
            # Save using soundfile
            sf.write(filename, recording, sample_rate, subtype='PCM_16')
            return True
        except Exception as e:
            print(f"❌ Error saving audio file: {e}")
            return False
    
    def get_enrollment_text(self):
        """Get the text to be read during voice enrollment"""
        return """Please read the following text clearly and naturally:

The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once. 

Voice recognition technology has advanced significantly in recent years, making it possible to identify speakers with remarkable accuracy. 

When creating a voice profile, it's important to speak clearly and at a natural pace. The system will analyze various characteristics of your voice including pitch, tone, and speech patterns.

This enrollment process typically takes about thirty seconds to complete. Please continue reading until the recording stops automatically.

Thank you for participating in this voice enrollment session."""
    
    def create_speaker_profile(self, name):
        """Create a speaker profile using voice enrollment"""
        print(f"\n🎤 Creating speaker profile for: {name}")
        
        # Show enrollment text
        print("\n" + "="*60)
        print("📖 ENROLLMENT TEXT TO READ:")
        print("="*60)
        print(self.get_enrollment_text())
        print("="*60)
        
        input("\nPress Enter when you're ready to start recording...")
        
        try:
            # Record audio
            recording, sample_rate = self.record_audio(duration=30)
            
            if recording is None:
                print("❌ Recording failed. Please try again.")
                return None
            
            # Save to temporary file
            temp_audio_file = f"temp_enrollment_{name.lower().replace(' ', '_')}.wav"
            if not self.save_audio_to_file(recording, sample_rate, temp_audio_file):
                print("❌ Failed to save audio file.")
                return None
            
            print(f"💾 Audio saved to: {temp_audio_file}")
            
            # Create speaker profile using Azure Speaker Recognition API
            print("🔄 Creating speaker profile with Azure...")
            
            # Step 1: Create a new speaker profile
            profile_id = self.create_speaker_profile_api()
            
            if not profile_id:
                print("❌ Failed to create speaker profile")
                if os.path.exists(temp_audio_file):
                    os.remove(temp_audio_file)
                return None
            
            print(f"✅ Speaker profile created with ID: {profile_id}")
            
            # Step 2: Enroll the voice sample
            print("🔄 Enrolling voice sample...")
            enrollment_result = self.enroll_voice_sample_api(profile_id, temp_audio_file)
            
            if enrollment_result:
                # Save profile info
                self.profiles[profile_id] = {
                    "name": name,
                    "profile_id": profile_id,
                    "created_date": datetime.now().isoformat(),
                    "audio_file": temp_audio_file,
                    "enrollment_status": enrollment_result.get("enrollmentStatus", "Unknown"),
                    "enrollments_count": enrollment_result.get("enrollmentsCount", 0),
                    "speech_length_sec": enrollment_result.get("enrollmentsSpeechLengthInSec", 0),
                    "remaining_speech_sec": enrollment_result.get("remainingEnrollmentsSpeechLengthInSec", 20)
                }
                self.save_profiles()
                
                print(f"✅ Speaker profile created successfully for {name}")
                print(f"🆔 Profile ID: {profile_id}")
                print(f"📁 Audio file: {temp_audio_file}")
                print(f"📊 Enrollment Status: {enrollment_result.get('enrollmentStatus', 'Unknown')}")
                print(f"📊 Speech Length: {enrollment_result.get('enrollmentsSpeechLengthInSec', 0):.1f}s")
                print(f"📊 Remaining: {enrollment_result.get('remainingEnrollmentsSpeechLengthInSec', 20):.1f}s")
                
                if enrollment_result.get("enrollmentStatus") == "Enrolled":
                    print("🎉 Profile is ready for speaker identification!")
                else:
                    print("⚠️  Profile needs more enrollment audio to be ready for identification")
                
                return profile_id
            else:
                print("❌ Failed to enroll voice sample")
                # Clean up temp file
                if os.path.exists(temp_audio_file):
                    os.remove(temp_audio_file)
                return None
                
        except Exception as e:
            print(f"❌ Error creating speaker profile: {e}")
            # Clean up temp file
            if 'temp_audio_file' in locals() and os.path.exists(temp_audio_file):
                os.remove(temp_audio_file)
            return None
    
    def list_profiles(self):
        """List all available speaker profiles"""
        if not self.profiles:
            print("\n📋 No speaker profiles found.")
            return
        
        print(f"\n📋 Available Speaker Profiles ({len(self.profiles)} total):")
        print("=" * 60)
        for i, (profile_id, profile_info) in enumerate(self.profiles.items(), 1):
            print(f"{i}. Name: {profile_info['name']}")
            print(f"   Profile ID: {profile_id}")
            print(f"   Created: {profile_info['created_date']}")
            print(f"   Audio file: {profile_info.get('audio_file', 'N/A')}")
            print("-" * 60)
    
    def delete_profile(self, profile_id):
        """Delete a speaker profile"""
        if profile_id in self.profiles:
            name = self.profiles[profile_id]["name"]
            del self.profiles[profile_id]
            self.save_profiles()
            print(f"✅ Deleted profile for {name}")
        else:
            print(f"❌ Profile ID {profile_id} not found")
    
    def get_profile_by_name(self, name):
        """Get profile ID by name"""
        for profile_id, profile_info in self.profiles.items():
            if profile_info["name"].lower() == name.lower():
                return profile_id
        return None
    
    def create_speaker_profile_api(self):
        """Create a new speaker profile using Azure Speaker Recognition API"""
        url = f"{self.api_endpoint}/speaker-recognition/identification/text-independent/profiles"
        params = {"api-version": "2021-09-05"}
        headers = {
            "Ocp-Apim-Subscription-Key": self.speech_key,
            "Content-Type": "application/json"
        }
        data = {"locale": "en-us"}
        
        try:
            response = requests.post(url, params=params, headers=headers, json=data)
            
            if response.status_code == 201:
                profile_info = response.json()
                profile_id = profile_info.get("profileId")
                print(f"✅ Profile created successfully: {profile_id}")
                return profile_id
            else:
                print(f"❌ Failed to create profile. Status: {response.status_code}")
                print(f"Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating speaker profile: {e}")
            return None
    
    def enroll_voice_sample_api(self, profile_id, audio_file_path):
        """Enroll a voice sample to an existing speaker profile"""
        url = f"{self.api_endpoint}/speaker-recognition/identification/text-independent/profiles/{profile_id}/enrollments"
        params = {"api-version": "2021-09-05"}
        headers = {
            "Ocp-Apim-Subscription-Key": self.speech_key,
            "Content-Type": "audio/wav; codecs=audio/pcm"
        }
        
        try:
            # Read the audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            response = requests.post(url, params=params, headers=headers, data=audio_data)
            
            if response.status_code == 201:
                enrollment_info = response.json()
                print(f"✅ Voice sample enrolled successfully")
                return enrollment_info
            else:
                print(f"❌ Failed to enroll voice sample. Status: {response.status_code}")
                print(f"Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error enrolling voice sample: {e}")
            return None
    
    def get_profile_status_api(self, profile_id):
        """Get the status of a speaker profile"""
        url = f"{self.api_endpoint}/speaker-recognition/identification/text-independent/profiles/{profile_id}"
        params = {"api-version": "2021-09-05"}
        headers = {
            "Ocp-Apim-Subscription-Key": self.speech_key
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get profile status. Status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting profile status: {e}")
            return None

def main():
    """Main function for voice registration"""
    print("🎤 Azure Voice Registration System")
    print("=" * 40)
    
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
        # Create voice registration instance
        registration = VoiceRegistration()
        
        while True:
            print("\n📋 Choose an option:")
            print("1. Create new speaker profile")
            print("2. List all speaker profiles")
            print("3. Delete speaker profile")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n=== Create New Speaker Profile ===")
                name = input("Enter speaker name: ").strip()
                
                if not name:
                    print("❌ Name cannot be empty.")
                    continue
                
                # Check if name already exists
                existing_profile = registration.get_profile_by_name(name)
                if existing_profile:
                    print(f"⚠️  A profile for '{name}' already exists.")
                    overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
                    if overwrite != 'y':
                        continue
                    # Delete existing profile
                    registration.delete_profile(existing_profile)
                
                print(f"\n🎤 Voice Registration for: {name}")
                print("📋 Requirements:")
                print("- 30 seconds of clear speech")
                print("- Read the provided text naturally")
                print("- Ensure quiet environment")
                print("- Speak at normal volume")
                
                ready = input("\nAre you ready to start? (y/n): ").strip().lower()
                if ready != 'y':
                    print("Registration cancelled.")
                    continue
                
                registration.create_speaker_profile(name)
                
            elif choice == "2":
                registration.list_profiles()
                
            elif choice == "3":
                registration.list_profiles()
                if registration.profiles:
                    try:
                        profile_num = int(input("\nEnter the number of the profile to delete: ").strip())
                        profile_ids = list(registration.profiles.keys())
                        if 1 <= profile_num <= len(profile_ids):
                            profile_id = profile_ids[profile_num - 1]
                            name = registration.profiles[profile_id]["name"]
                            confirm = input(f"Are you sure you want to delete {name}'s profile? (y/n): ").strip().lower()
                            if confirm == 'y':
                                registration.delete_profile(profile_id)
                        else:
                            print("❌ Invalid profile number.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
                
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