# Windows Installation Guide

This guide helps you install the Azure Speech Recognition project on Windows systems.

## Quick Fix for PyAudio Issues

### Option 1: Use pipwin (Recommended)

```bash
# Install pipwin first
pip install pipwin

# Install PyAudio using pipwin
pipwin install pyaudio
```

### Option 2: Use Pre-compiled Wheels

```bash
# Install PyAudio from a pre-compiled wheel
pip install pipwin
pipwin install pyaudio
```

### Option 3: Install Visual C++ Build Tools

If you prefer to compile from source:

1. Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. During installation, select "C++ build tools" workload
3. Then run: `pip install pyaudio`

### Option 4: Use Alternative Audio Library

The project now uses `sounddevice` instead of PyAudio, which should work better on Windows:

```bash
pip install -r requirements.txt
```

## Complete Installation Steps

1. **Install Python 3.7+** (if not already installed)
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **If you still get PyAudio errors**, try:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

4. **Set up your .env file**:
   - Copy `env_example.txt` to `.env`
   - Add your Azure credentials

5. **Test the installation**:
   ```bash
   python simple_speech_recognition.py
   ```

## Troubleshooting

### Microphone Permissions

1. Go to **Windows Settings** > **Privacy** > **Microphone**
2. Ensure "Allow apps to access your microphone" is **On**
3. Make sure your terminal/IDE is allowed

### Audio Device Issues

If you get audio device errors:

1. **Check your default microphone**:
   - Right-click the speaker icon in taskbar
   - Select "Open Sound settings"
   - Check your default input device

2. **Test your microphone**:
   - In Sound settings, click "Test your microphone"
   - Speak and check if the bar moves

### Alternative: Use the Simple Version

The `simple_speech_recognition.py` uses Azure's built-in microphone support and should work without PyAudio:

```bash
python simple_speech_recognition.py
```

## Common Error Messages

### "Microsoft Visual C++ 14.0 or greater is required"
- Use Option 1 or 2 above (pipwin)
- Or install Visual C++ Build Tools

### "No module named 'pyaudio'"
- The project now uses sounddevice instead
- Run: `pip install sounddevice`

### "No speech could be recognized"
- Check microphone permissions
- Ensure your microphone is working
- Try speaking louder

## Still Having Issues?

If you continue to have problems:

1. **Use the simple version**: `python simple_speech_recognition.py`
2. **Check your Azure credentials** in the `.env` file
3. **Verify your microphone** works in other applications
4. **Try running as administrator** if permission issues persist 