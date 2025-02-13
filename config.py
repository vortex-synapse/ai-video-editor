"""Configuration settings for AI Video Editor"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
TEMP_DIR = BASE_DIR / "temp"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
TEMP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Model settings
WHISPER_MODEL_TYPE = "base"
TTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"

# Supported languages
SUPPORTED_LANGUAGES = {
	'en': 'English',
	'es': 'Spanish',
	'fr': 'French',
	'de': 'German',
	'hi': 'Hindi',
	'ja': 'Japanese',
	'ko': 'Korean',
	'zh': 'Chinese'
}

# File settings
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav"]

# Processing settings
MAX_RETRIES = 3
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for file operations

# Logging settings
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOG_DIR / 'ai_video_editor.log'

# Check for required external dependencies
def check_dependencies():
	"""Check if required external dependencies are available."""
	try:
		import cv2
		import numpy
		import torch
		import whisper
		import mediapipe
		import tensorflow
		from TTS.api import TTS
		return True
	except ImportError as e:
		print(f"Missing dependency: {str(e)}")
		return False