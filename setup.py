#!/usr/bin/env python3
"""
Setup script for Azure Real-Time Speech Recognition
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return
    
    print("Creating .env file...")
    try:
        shutil.copy("env_example.txt", ".env")
        print("✓ .env file created from template")
        print("⚠️  Please edit .env file with your Azure credentials")
    except FileNotFoundError:
        print("✗ env_example.txt not found")
        sys.exit(1)

def check_azure_credentials():
    """Check if Azure credentials are set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    speech_region = os.getenv('AZURE_SPEECH_REGION')
    
    if not speech_key or speech_key == "your_azure_speech_key_here":
        print("⚠️  Azure Speech Key not configured in .env file")
        return False
    
    if not speech_region or speech_region == "your_azure_region_here":
        print("⚠️  Azure Speech Region not configured in .env file")
        return False
    
    print("✓ Azure credentials configured")
    return True

def main():
    """Main setup function"""
    print("Azure Real-Time Speech Recognition Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Check Azure credentials
    credentials_ok = check_azure_credentials()
    
    print("\nSetup complete!")
    if not credentials_ok:
        print("\nNext steps:")
        print("1. Edit .env file with your Azure Speech Service credentials")
        print("2. Run: python simple_speech_recognition.py")
    else:
        print("\nYou're ready to go!")
        print("Run: python simple_speech_recognition.py")

if __name__ == "__main__":
    main() 