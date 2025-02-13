import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import logging
import os
from core.video_processor import VideoProcessor
from core.voice_cloner import VoiceCloner
from core.lip_sync import LipSyncProcessor
from config import (
	TEMP_DIR, LOG_DIR, LOG_FORMAT, LOG_FILE,
	SUPPORTED_LANGUAGES, SUPPORTED_VIDEO_FORMATS,
	SUPPORTED_AUDIO_FORMATS, check_dependencies
)

class VideoEditorApp:
	def __init__(self, root):
		self.root = root
		self.root.title("AI Video Editor")
		self.root.geometry("800x600")
		
		# Check dependencies first
		if not check_dependencies():
			messagebox.showerror("Error", "Missing required dependencies. Please install all requirements.")
			self.root.destroy()
			return
			
		# Setup logging first
		self.setup_logging()
		
		# Initialize processors with context managers
		try:
			self.video_processor = VideoProcessor(temp_dir=str(TEMP_DIR))
			self.voice_cloner = VoiceCloner()
			self.lip_sync = LipSyncProcessor()
		except Exception as e:
			self.logger.error(f"Failed to initialize processors: {str(e)}")
			messagebox.showerror("Initialization Error", f"Failed to initialize: {str(e)}")
			self.root.destroy()
			return
		
		# Create UI
		self.create_ui()
		
		# Initialize variables
		self.initialize_variables()
		
		# Register cleanup
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		
	def setup_logging(self):
		"""Configure logging with settings from config."""
		LOG_DIR.mkdir(exist_ok=True)
		logging.basicConfig(
			level=logging.INFO,
			format=LOG_FORMAT,
			handlers=[
				logging.StreamHandler(),
				logging.FileHandler(LOG_FILE)
			]
		)
		self.logger = logging.getLogger(__name__)

	def create_ui(self):
		# Create main frame with better layout
		main_frame = ttk.Frame(self.root, padding="10")
		main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		
		# File selection with better validation
		self._create_file_section(main_frame)
		
		# Language selection with dropdown
		self._create_language_section(main_frame)
		
		# Progress and status
		self._create_progress_section(main_frame)

	def _create_file_section(self, parent):
		# Input video
		ttk.Label(parent, text="Input Video:").grid(row=0, column=0, sticky=tk.W)
		ttk.Entry(parent, textvariable=self.input_video_path, width=50).grid(row=0, column=1, padx=5)
		ttk.Button(parent, text="Browse", command=self.browse_input_video).grid(row=0, column=2)
		
		# Reference audio
		ttk.Label(parent, text="Reference Audio:").grid(row=1, column=0, sticky=tk.W)
		ttk.Entry(parent, textvariable=self.reference_audio_path, width=50).grid(row=1, column=1, padx=5)
		ttk.Button(parent, text="Browse", command=self.browse_reference_audio).grid(row=1, column=2)
		
		# Output path
		ttk.Label(parent, text="Output Path:").grid(row=2, column=0, sticky=tk.W)
		ttk.Entry(parent, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5)
		ttk.Button(parent, text="Browse", command=self.browse_output_path).grid(row=2, column=2)

	def _create_language_section(self, parent):
		# Language frame
		lang_frame = ttk.LabelFrame(parent, text="Language Settings", padding="5")
		lang_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
		
		# Source language
		ttk.Label(lang_frame, text="Source Language:").grid(row=0, column=0, sticky=tk.W)
		source_combo = ttk.Combobox(lang_frame, textvariable=self.source_lang, width=15)
		source_combo['values'] = list(self.supported_languages.keys())
		source_combo.grid(row=0, column=1, padx=5)
		
		# Target language
		ttk.Label(lang_frame, text="Target Language:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
		target_combo = ttk.Combobox(lang_frame, textvariable=self.target_lang, width=15)
		target_combo['values'] = list(self.supported_languages.keys())
		target_combo.grid(row=0, column=3, padx=5)

	def _create_progress_section(self, parent):
		# Progress frame
		progress_frame = ttk.LabelFrame(parent, text="Progress", padding="5")
		progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
		
		# Progress bar
		self.progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
		self.progress.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
		
		# Status label
		self.status_label = ttk.Label(progress_frame, text="Ready")
		self.status_label.grid(row=1, column=0, columnspan=2)
		
		# Process button
		ttk.Button(parent, text="Start Processing", command=self.start_processing).grid(
			row=5, column=0, columnspan=3, pady=10)

	def browse_input_video(self):
		"""Browse for input video with supported formats."""
		filetypes = [("Video files", f"*{ext}") for ext in SUPPORTED_VIDEO_FORMATS]
		filename = filedialog.askopenfilename(filetypes=filetypes)
		if filename:
			self.input_video_path.set(filename)

	def browse_reference_audio(self):
		"""Browse for reference audio with supported formats."""
		filetypes = [("Audio files", f"*{ext}") for ext in SUPPORTED_AUDIO_FORMATS]
		filename = filedialog.askopenfilename(filetypes=filetypes)
		if filename:
			self.reference_audio_path.set(filename)

	def browse_output_path(self):
		filename = filedialog.asksaveasfilename(defaultextension=".mp4",
											  filetypes=[("MP4 files", "*.mp4")])
		if filename:
			self.output_path.set(filename)

	def update_status(self, message, progress_value=None):
		self.status_label.config(text=message)
		if progress_value is not None:
			self.progress['value'] = progress_value
		self.root.update_idletasks()

	def initialize_variables(self):
		"""Initialize all UI variables using config settings."""
		self.input_video_path = tk.StringVar()
		self.reference_audio_path = tk.StringVar()
		self.output_path = tk.StringVar()
		self.source_lang = tk.StringVar(value="en")
		self.target_lang = tk.StringVar(value="hi")
		self.processing = False
		self.supported_languages = SUPPORTED_LANGUAGES


	def on_closing(self):
		"""Handle application cleanup on closing."""
		try:
			if self.processing:
				if not messagebox.askokcancel("Quit", "Processing is in progress. Do you want to quit?"):
					return
			self.cleanup()
			self.root.destroy()
		except Exception as e:
			self.logger.error(f"Error during cleanup: {str(e)}")
			self.root.destroy()

	def cleanup(self):
		"""Clean up resources."""
		try:
			if hasattr(self, 'video_processor'):
				self.video_processor.cleanup()
			if hasattr(self, 'voice_cloner'):
				self.voice_cloner.cleanup()
			if hasattr(self, 'lip_sync'):
				self.lip_sync.cleanup()
			self.logger.info("All resources cleaned up")
		except Exception as e:
			self.logger.error(f"Cleanup failed: {str(e)}")

	def process_video(self):
		"""Process video with proper resource management."""
		self.processing = True
		try:
			# Create temp directory for processing
			TEMP_DIR.mkdir(exist_ok=True)

			
			# Load video
			self.update_status("Loading video...", 10)
			video = self.video_processor.load_video(self.input_video_path.get())
			
			# Extract audio
			self.update_status("Extracting audio...", 20)
			audio_path = self.video_processor.extract_audio(video, "temp/temp_audio.wav")
			
			# Transcribe audio
			self.update_status("Transcribing audio...", 30)
			transcription = self.video_processor.transcribe_audio(audio_path)
			
			# Translate text
			self.update_status("Translating text...", 40)
			translated_text = self.video_processor.translate_text(
				transcription['text'],
				self.source_lang.get(),
				self.target_lang.get()
			)
			
			# Clone voice
			self.update_status("Cloning voice...", 60)
			dubbed_audio = self.voice_cloner.clone_voice(
				translated_text,
				self.reference_audio_path.get(),
				"temp/dubbed_audio.wav",
				self.target_lang.get()
			)
			
			# Lip sync
			self.update_status("Synchronizing lips...", 80)
			self.lip_sync.sync_audio_with_lips(
				self.input_video_path.get(),
				dubbed_audio,
				self.output_path.get()
			)
			
			self.update_status("Processing complete!", 100)
			messagebox.showinfo("Success", "Video processing completed successfully!")
			
		except Exception as e:
			self.logger.error(f"Processing failed: {str(e)}")
			messagebox.showerror("Error", f"Processing failed: {str(e)}")
			self.update_status("Processing failed")
		finally:
			self.processing = False
			self.progress['value'] = 0
			try:
				# Cleanup temp files
				for file in TEMP_DIR.glob("*"):
					file.unlink()

			except Exception as e:
				self.logger.error(f"Failed to cleanup temp directory: {str(e)}")

	def start_processing(self):
		if not all([self.input_video_path.get(), self.reference_audio_path.get(), 
				   self.output_path.get()]):
			messagebox.showerror("Error", "Please select all required files")
			return
			
		# Run processing in a separate thread
		threading.Thread(target=self.process_video, daemon=True).start()

def main():
	root = tk.Tk()
	app = VideoEditorApp(root)
	root.mainloop()

if __name__ == "__main__":
	main()