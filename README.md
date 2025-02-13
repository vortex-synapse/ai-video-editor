# AI Video Editor

An advanced AI-powered video editing tool that provides automated dubbing, translation, voice cloning, and lip-sync capabilities.

## Features

- **Video Processing**: Load and process video files in various formats
- **Audio Extraction**: Extract audio from video files
- **Speech Recognition**: Convert audio to text using OpenAI's Whisper
- **Text Translation**: Translate text between multiple languages
- **Voice Cloning**: Clone voices for natural-sounding dubbing
- **Lip Synchronization**: Sync dubbed audio with video lip movements
- **Real-time Processing**: Support for real-time video stream processing
- **Multi-language Support**: Support for multiple languages in translation and dubbing
- **User-friendly Interface**: Easy-to-use graphical interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vortex-synapse/ai-video-editor.git
cd ai-video-editor
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python -m ai_video_editor
```

2. Using the GUI:
   - Select input video file
   - Choose reference audio for voice cloning
   - Set source and target languages
   - Choose output path
   - Click "Start Processing"

## Project Structure

```
ai_video_editor/
├── core/                    # Core processing modules
│   ├── video_processor.py   # Video processing functionality
│   ├── voice_cloner.py      # Voice cloning and synthesis
│   └── lip_sync.py         # Lip synchronization processing
├── tests/                   # Test suite
│   ├── test_core.py        # Core components tests
│   └── __init__.py         # Test package initialization
├── config.py               # Configuration settings
├── main.py                 # Main application and GUI
├── __main__.py            # Entry point
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Testing

Run the test suite:
```bash
python -m unittest discover tests
```

## Requirements


- Python 3.8+
- CUDA-capable GPU (recommended for faster processing)
- Required Python packages listed in requirements.txt

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Hindi (hi)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI Whisper for speech recognition
- Coqui TTS for voice synthesis
- MediaPipe for face mesh detection
- MoviePy for video processing
