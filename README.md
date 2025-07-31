# Azure Real-Time Speech Recognition

This project implements real-time speech recognition using Azure Cognitive Services Speech SDK. It provides two different approaches for capturing audio and performing speech recognition with console output.

## Features

- Real-time speech recognition using Azure Cognitive Services
- Continuous recognition with intermediate results
- Console output with timestamps
- Support for multiple languages
- Error handling and logging
- Two implementation approaches:
  - **Simple**: Uses Azure's built-in microphone support
  - **Advanced**: Custom audio processing with sounddevice

## Prerequisites

1. **Azure Speech Service**: You need an Azure Speech Service resource
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a new Speech Service resource
   - Note down your **Key** and **Region**

2. **Python 3.7+**: Make sure you have Python installed

3. **Microphone**: A working microphone for audio input

## Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `env_example.txt` to `.env`
   - Fill in your Azure credentials:
   ```
   AZURE_SPEECH_KEY=your_azure_speech_key_here
   AZURE_SPEECH_REGION=your_azure_region_here
   ```

## Usage

### Simple Implementation (Recommended for beginners)

This version uses Azure's built-in microphone support and is easier to set up:

```bash
python simple_speech_recognition.py
```

### Advanced Implementation

This version provides more control over audio processing:

```bash
python real_time_speech_recognition.py
```

### Output Example

```
Azure Real-Time Speech Recognition
==========================================
Starting real-time speech recognition...
Press Ctrl+C to stop
--------------------------------------------------
Speech recognition session started
Recognizing: Hello world
[14:30:25] Recognized: Hello world
Recognizing: This is a test
[14:30:28] Recognized: This is a test
```

## Configuration Options

You can customize the behavior by modifying the `.env` file:

```env
# Azure Speech Service Configuration
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=your_region_here

# Optional: Custom endpoint for custom speech models
AZURE_SPEECH_ENDPOINT=https://your-custom-endpoint.cognitiveservices.azure.com/

# Audio Configuration (for advanced implementation)
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_CHUNK_SIZE=1024
```

## Language Support

To change the recognition language, modify the `speech_recognition_language` in the code:

```python
self.speech_config.speech_recognition_language = "en-US"  # English
self.speech_config.speech_recognition_language = "es-ES"  # Spanish
self.speech_config.speech_recognition_language = "fr-FR"  # French
# ... and many more
```

## Troubleshooting

### Common Issues

1. **"No module named 'azure.cognitiveservices.speech'"**
   - Run: `pip install azure-cognitiveservices-speech`

2. **"No module named 'sounddevice'"**
   - Run: `pip install sounddevice`

3. **"Azure Speech Key and Region must be set"**
   - Make sure your `.env` file exists and contains the correct credentials

4. **"No speech could be recognized"**
   - Check your microphone permissions
   - Ensure your microphone is working
   - Try speaking louder or more clearly

5. **Audio quality issues**
   - Adjust the `AUDIO_SAMPLE_RATE` in your `.env` file
   - Try different `AUDIO_CHUNK_SIZE` values

### Windows-specific Issues

1. **PyAudio installation problems**:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

2. **Microphone permissions**:
   - Go to Windows Settings > Privacy > Microphone
   - Ensure your app has microphone access

### macOS-specific Issues

1. **Microphone permissions**:
   - Go to System Preferences > Security & Privacy > Privacy > Microphone
   - Add your terminal/IDE to the allowed apps

## Advanced Features

### Custom Speech Models

If you have a custom speech model, you can use it by setting the `AZURE_SPEECH_ENDPOINT` in your `.env` file.

### Logging

The application creates a `speech_log.txt` file with detailed Azure Speech Service logs for debugging.

### Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues
- Invalid credentials
- Audio device problems
- Recognition errors

## Security Notes

- Never commit your `.env` file to version control
- Keep your Azure Speech Service key secure
- Consider using Azure Key Vault for production applications

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.