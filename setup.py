from setuptools import setup, find_packages

setup(
	name="ai_video_editor",
	version="1.0.0",
	packages=find_packages(),
	install_requires=[
		'moviepy>=1.0.3',
		'openai-whisper>=1.0.0',
		'googletrans==3.1.0a0',
		'gTTS>=2.3.1',
		'opencv-python>=4.7.0',
		'numpy>=1.24.0',
		'torch>=2.0.0',
		'torchaudio>=2.0.0',
		'tensorflow>=2.12.0',
		'mediapipe>=0.10.0',
		'TTS>=0.13.0',
		'librosa>=0.10.0',
		'scipy>=1.10.0'
	],
	entry_points={
		'console_scripts': [
			'ai_video_editor=ai_video_editor.main:main',
		],
	}
)