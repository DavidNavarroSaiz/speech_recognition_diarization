# Speech Recognition with Diarization Project

A Python-based speech recognition system that combines Azure Cognitive Services Speech SDK with speaker diarization capabilities. This project demonstrates how to implement real-time speech transcription with speaker identification.

## 🎯 Project Overview

This project consists of two main components:
1. **Voice Registration System** - Records and stores speaker profiles
2. **Speaker Identification System** - Performs real-time transcription with speaker mapping

## ⚠️ Important Notice: Azure Speaker Recognition Limitations

**As of June 2024, Azure Speaker Recognition is a Limited Access feature with paused registrations.**

- Microsoft has paused all new registrations for the Speaker Recognition Limited Access program
- This affects the ability to use Azure's official Speaker Recognition API for voice profile creation
- The project currently uses a hybrid approach combining Azure's diarization with local profile mapping

## 🏗️ Architecture

### Current Implementation (Hybrid Approach)
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Voice         │    │   Azure Speech   │    │   Speaker       │
│ Registration    │───▶│   SDK            │───▶│ Identification  │
│ (Local)         │    │   (Diarization)  │    │ (Local Mapping) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Components

1. **`voice_registration.py`** - Voice profile creation and management
2. **`speaker_identification.py`** - Real-time transcription with speaker mapping
3. **`speaker_profiles.json`** - Local storage for speaker profiles
4. **`continuos_speech_recognition.py`** - Basic speech recognition (reference)

## 🚀 Features

### ✅ Implemented Features
- **Real-time speech transcription** using Azure Speech SDK
- **Speaker diarization** - identifies different speakers in conversation
- **Local voice profile management** - create, list, and delete speaker profiles
- **Microphone recording** for voice enrollment (30-second sessions)
- **Speaker mapping** - maps Azure speaker IDs to user-defined names
- **Multiple input sources** - microphone and audio files

### 🔄 Current Limitations
- **No Azure Speaker Recognition API** - limited to local profile mapping
- **Simple speaker assignment** - first detected speaker gets first profile
- **No voice verification** - profiles are not validated against actual voice characteristics

## 📋 Prerequisites

### Required Software
- Python 3.7+
- Azure Cognitive Services Speech SDK
- Audio recording capabilities

### Required Dependencies
```
azure-cognitiveservices-speech==1.34.0
sounddevice==0.4.6
soundfile==0.12.1
python-dotenv==1.0.0
requests==2.31.0
```

### Azure Setup
1. **Azure Speech Service** - Required for transcription and diarization
2. **Environment Variables** - Set up `.env` file with Azure credentials

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd speech_recognition_diarization
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file with your Azure credentials:
```env
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
# Optional: AZURE_SPEECH_ENDPOINT=your_custom_endpoint_here
```

### 4. Windows-Specific Setup
For Windows users, follow the installation guide in `WINDOWS_INSTALL.md`.

## 📖 Usage Guide

### Step 1: Create Voice Profiles
```bash
python voice_registration.py
```

**Process:**
1. Choose option 1: "Create new speaker profile"
2. Enter speaker name (e.g., "David")
3. Read the provided enrollment text for 30 seconds
4. Profile is saved locally with a unique ID

**Enrollment Text:**
```
The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once.

Voice recognition technology has advanced significantly in recent years, making it possible to identify speakers with remarkable accuracy.

When creating a voice profile, it's important to speak clearly and at a natural pace. The system will analyze various characteristics of your voice including pitch, tone, and speech patterns.

This enrollment process typically takes about thirty seconds to complete. Please continue reading until the recording stops automatically.

Thank you for participating in this voice enrollment session.
```

### Step 2: Perform Speaker Identification
```bash
python speaker_identification.py
```

**Options:**
1. **List profiles** - View all registered speakers
2. **Transcribe file** - Process audio files with speaker identification
3. **Real-time transcription** - Live microphone transcription with speaker mapping

### Step 3: Real-time Usage
1. Choose option 3 for real-time transcription
2. Speak naturally - the system will:
   - Transcribe your speech in real-time
   - Identify you as the first registered speaker
   - Show intermediate and final results

## 🔧 Technical Details

### Speaker Mapping Logic
```python
def get_speaker_name(self, speaker_id):
    # First speaker detected → First profile in list
    # Second speaker detected → Second profile (if available)
    # Additional speakers → "Guest X" naming
```

### Profile Storage Format
```json
{
  "profile_id": {
    "name": "David",
    "profile_id": "uuid-string",
    "created_date": "2024-01-01T12:00:00",
    "audio_file": "temp_enrollment_david.wav",
    "enrollment_status": "Ready",
    "enrollments_count": 1,
    "speech_length_sec": 30.0,
    "remaining_speech_sec": 0.0
  }
}
```

### Azure Speech SDK Configuration
- **Language**: English (en-US)
- **Service**: ConversationTranscriber for diarization
- **Audio**: 16kHz, 16-bit PCM format

## 🔮 Future Enhancements

### When Azure Speaker Recognition Becomes Available
1. **True Voice Verification** - Use Azure's Speaker Recognition API
2. **Voice Print Creation** - Generate actual voice biometrics
3. **Multi-Speaker Enrollment** - Support for multiple voice samples per speaker
4. **Confidence Scoring** - Speaker identification confidence levels

### Alternative Approaches
1. **Local Voice Recognition** - Implement local speaker identification
2. **Machine Learning Models** - Train custom speaker identification models
3. **Voice Activity Detection** - Improve speaker segmentation
4. **Multi-Modal Identification** - Combine voice with other biometrics

## 🐛 Troubleshooting

### Common Issues

#### 1. Audio Recording Problems
```bash
# Windows: Install Visual C++ Build Tools
# Linux: Install portaudio
sudo apt-get install portaudio19-dev
```

#### 2. Azure Authentication Errors
- Verify `.env` file contains correct credentials
- Check Azure Speech Service is active
- Ensure region/endpoint configuration is correct

#### 3. Speaker Not Recognized
- Ensure profile was created successfully
- Check `speaker_profiles.json` exists and contains data
- Verify microphone permissions

#### 4. Transcription Quality Issues
- Use high-quality microphone
- Ensure quiet environment
- Speak clearly and at normal pace
- Check internet connection for Azure services

### Debug Information
The system provides debug output showing:
- Speaker ID mapping process
- Profile loading status
- Azure service connection status

## 📊 Performance Considerations

### Current Limitations
- **Speaker Assignment**: Simple sequential mapping
- **Voice Quality**: Depends on recording environment
- **Real-time Latency**: Network-dependent for Azure services

### Optimization Tips
- Use wired microphone for better audio quality
- Ensure stable internet connection
- Close unnecessary applications during recording
- Use quiet environment for voice enrollment

## 🔒 Privacy and Security

### Data Storage
- **Local Storage**: All profiles stored locally in `speaker_profiles.json`
- **Audio Files**: Temporary enrollment files (can be deleted)
- **No Cloud Storage**: Voice data not uploaded to external services

### Best Practices
- Regularly delete temporary audio files
- Secure your `.env` file with Azure credentials
- Be aware of microphone permissions
- Consider data retention policies

## 📚 API Reference

### VoiceRegistration Class
```python
class VoiceRegistration:
    def create_speaker_profile(name)      # Create new voice profile
    def list_profiles()                   # List all profiles
    def delete_profile(profile_id)        # Delete specific profile
    def get_profile_by_name(name)         # Find profile by name
```

### SpeakerIdentification Class
```python
class SpeakerIdentification:
    def transcribe_microphone()           # Real-time transcription
    def transcribe_file(audio_file)       # File transcription
    def list_profiles()                   # List available profiles
    def get_speaker_name(speaker_id)      # Map speaker ID to name
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### Testing
- Test with different audio qualities
- Verify speaker mapping accuracy
- Check error handling
- Validate Azure service integration

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 📞 Support

### Getting Help
- Check troubleshooting section above
- Review Azure Speech Service documentation
- Verify environment configuration

### Azure Support
- [Azure Speech Service Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/)
- [Speaker Recognition FAQ](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/speaker-recognition-overview)

## 🔄 Version History

### v1.0.0 (Current)
- Basic speech recognition with diarization
- Local voice profile management
- Real-time transcription capabilities
- Hybrid speaker mapping system

### Planned Features
- Enhanced speaker identification algorithms
- Multi-language support
- Improved audio processing
- Better error handling and recovery

---

**Note**: This project demonstrates the current state of speech recognition technology and the challenges of implementing speaker identification without access to specialized APIs. It serves as a foundation for future development when Azure Speaker Recognition becomes more widely available.