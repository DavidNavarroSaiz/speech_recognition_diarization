# Demo Guide: Speech Recognition with Diarization

This guide will walk you through testing the speech recognition with diarization system step by step.

## 🎯 Demo Overview

**Goal**: Demonstrate real-time speech transcription with speaker identification using a hybrid approach that combines Azure's diarization capabilities with local profile mapping.

## 📋 Prerequisites

Before starting the demo, ensure you have:

1. ✅ **Azure Speech Service** configured with valid credentials
2. ✅ **Python environment** with all dependencies installed
3. ✅ **Working microphone** for voice input
4. ✅ **Quiet environment** for clear audio recording
5. ✅ **`.env` file** with Azure credentials

## 🚀 Demo Steps

### Step 1: Verify Setup

First, let's ensure everything is working:

```bash
# Check if dependencies are installed
pip list | grep -E "(azure|sounddevice|soundfile)"

# Verify .env file exists
ls -la .env

# Test basic speech recognition
python continuos_speech_recognition.py
```

**Expected Output**: Should show Azure Speech Service connection and basic transcription.

### Step 2: Create Voice Profile

Create a speaker profile for demonstration:

```bash
python voice_registration.py
```

**Follow these steps**:
1. Choose option `1` (Create new speaker profile)
2. Enter name: `David` (or your preferred name)
3. Read the enrollment text clearly for 30 seconds
4. Wait for profile creation confirmation

**Expected Output**:
```
🎤 Creating speaker profile for: david
============================================================
📖 ENROLLMENT TEXT TO READ:
============================================================
Please read the following text clearly and naturally:

The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once.

Voice recognition technology has advanced significantly in recent years, making it possible to identify speakers with remarkable accuracy.

When creating a voice profile, it's important to speak clearly and at a natural pace. The system will analyze various characteristics of your voice including pitch, tone, and speech patterns.

This enrollment process typically takes about thirty seconds to complete. Please continue reading until the recording stops automatically.

Thank you for participating in this voice enrollment session.
============================================================

Press Enter when you're ready to start recording...

🎤 Recording 30 seconds of audio...
📝 Please read the provided text clearly and naturally.
⏰ Recording will start in 3 seconds...
   3...
   2...
   1...
🎙️  Recording started! Speak now...
⏳ Recording progress: 100.0%
✅ Recording completed!
💾 Audio saved to: temp_enrollment_david.wav
🔄 Creating speaker profile...
✅ Speaker profile created successfully for david
🆔 Profile ID: 351a5011-25f3-4dc3-a0b3-11e916b649a7
📁 Audio file: temp_enrollment_david.wav
📊 Status: Ready for speaker identification
🎉 Profile is ready for speaker identification!
💡 This profile will be used to map speaker IDs to names during transcription
```

### Step 3: Verify Profile Creation

Check that the profile was created successfully:

```bash
python voice_registration.py
```

Choose option `2` (List all speaker profiles)

**Expected Output**:
```
📋 Available Speaker Profiles (1 total):
============================================================
1. Name: david
   Profile ID: 351a5011-25f3-4dc3-a0b3-11e916b649a7
   Status: Ready
   Created: 2024-01-01T12:00:00.000000
   Audio file: temp_enrollment_david.wav
------------------------------------------------------------
```

### Step 4: Test Speaker Identification

Now test the speaker identification system:

```bash
python speaker_identification.py
```

Choose option `1` (List speaker profiles) to verify profiles are loaded.

**Expected Output**:
```
📋 Available Speaker Profiles (1 total):
============================================================
1. Name: david
   Profile ID: 351a5011-25f3-4dc3-a0b3-11e916b649a7
   Created: 2024-01-01T12:00:00.000000
------------------------------------------------------------
```

### Step 5: Real-time Transcription Demo

Choose option `3` (Real-time transcription) for the main demo.

**Demo Script**:
1. **Start speaking** when you see "SessionStarted event"
2. **Say**: "Hello, my name is David and I'm testing the speech recognition system"
3. **Continue speaking** naturally about any topic
4. **Observe** how the system identifies you as "david" instead of "Guest st-1"

**Expected Output**:
```
🎤 Starting real-time transcription with speaker identification
🎙️  Using default microphone
⏹️  Press Ctrl+C to stop
============================================================
[10:52:43] 🚀 SessionStarted event
🔍 Debug: New speaker 'st-1' mapped to 'david'
[10:52:47] 🔄 TRANSCRIBING:
👤 Speaker: david
💬 Text: hello my name is

[10:52:49] ✅ TRANSCRIBED:
👤 Speaker: david
💬 Text: Hello my name is David and I'm testing the speech recognition system.
⏱️  Offset: 27600000
⏱️  Duration: 23200000

[10:52:51] 🔄 TRANSCRIBING:
👤 Speaker: david
💬 Text: this is working really well

[10:52:52] ✅ TRANSCRIBED:
👤 Speaker: david
💬 Text: This is working really well.
⏱️  Offset: 57100000
⏱️  Duration: 31600000
```

## 🎭 Demo Scenarios

### Scenario 1: Single Speaker
- **Setup**: One voice profile created
- **Test**: Speak naturally for 1-2 minutes
- **Expected**: All speech attributed to the registered speaker name

### Scenario 2: Multiple Speakers (Future Enhancement)
- **Setup**: Multiple voice profiles created
- **Test**: Have different people speak
- **Expected**: Each speaker mapped to their respective profile

### Scenario 3: No Profiles
- **Setup**: Delete all profiles
- **Test**: Run speaker identification
- **Expected**: All speakers shown as "Guest X"

## 🔍 Key Features to Demonstrate

### 1. Real-time Transcription
- **Feature**: Live speech-to-text conversion
- **Demo**: Speak naturally and watch text appear in real-time
- **Highlight**: Low latency and accurate transcription

### 2. Speaker Diarization
- **Feature**: Identifies different speakers
- **Demo**: Show how system distinguishes between speakers
- **Highlight**: Azure's advanced diarization capabilities

### 3. Local Profile Mapping
- **Feature**: Maps speaker IDs to user-defined names
- **Demo**: Show "david" instead of "Guest st-1"
- **Highlight**: Custom speaker identification without cloud profiles

### 4. Intermediate Results
- **Feature**: Shows transcription progress
- **Demo**: Observe real-time updates as you speak
- **Highlight**: Responsive user experience

## 🐛 Troubleshooting Demo Issues

### Issue 1: "No speaker profiles found"
**Solution**: Run voice registration first and create a profile

### Issue 2: Still showing "Guest st-1"
**Solution**: 
1. Check `speaker_profiles.json` exists
2. Verify profile was created successfully
3. Restart speaker identification script

### Issue 3: Poor transcription quality
**Solutions**:
- Use better microphone
- Speak more clearly
- Reduce background noise
- Check internet connection

### Issue 4: Azure authentication errors
**Solutions**:
- Verify `.env` file credentials
- Check Azure Speech Service is active
- Ensure correct region/endpoint

## 📊 Demo Metrics

### Success Criteria
- ✅ Profile creation completes without errors
- ✅ Speaker identification shows registered name
- ✅ Real-time transcription works smoothly
- ✅ No Azure authentication errors

### Performance Indicators
- **Latency**: < 2 seconds for transcription
- **Accuracy**: > 90% transcription accuracy
- **Speaker Mapping**: Correct name assignment
- **Stability**: No crashes or errors

## 🎯 Demo Conclusion

### What We've Demonstrated
1. **Azure Speech SDK Integration** - Seamless cloud-based transcription
2. **Speaker Diarization** - Automatic speaker identification
3. **Local Profile Management** - Custom speaker mapping
4. **Real-time Processing** - Live speech recognition
5. **Hybrid Architecture** - Combining cloud and local capabilities

### Current Limitations
1. **Simple Speaker Assignment** - First speaker gets first profile
2. **No Voice Verification** - Profiles not validated against voice characteristics
3. **Limited to Local Mapping** - No true biometric speaker recognition

### Future Possibilities
1. **Azure Speaker Recognition** - When available again
2. **Local ML Models** - Custom speaker identification
3. **Multi-Speaker Support** - Enhanced mapping algorithms
4. **Voice Biometrics** - True voice print creation

## 📝 Demo Notes

### For Presenters
- Have backup microphone ready
- Test setup before presentation
- Prepare sample speech content
- Have troubleshooting steps ready

### For Audience
- Ask questions about the technology
- Request different demo scenarios
- Discuss potential applications
- Explore limitations and alternatives

---

**Demo Duration**: 10-15 minutes  
**Technical Level**: Intermediate  
**Prerequisites**: Basic Python knowledge, Azure familiarity 