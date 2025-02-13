"""
AI Video Editor - Main Entry Point
"""

import sys
import logging
from pathlib import Path
from system_check import run_system_check

def setup_environment():
	"""Setup environment for the application."""
	# Add project root to Python path
	project_root = Path(__file__).parent
	if str(project_root) not in sys.path:
		sys.path.insert(0, str(project_root))

def main():
	"""Main entry point for the application."""
	try:
		setup_environment()
		
		# Run system checks first
		if not run_system_check():
			print("System check failed. Please check the logs and install required dependencies.")
			sys.exit(1)
			
		from main import main as app_main
		app_main()
	except Exception as e:
		logging.error(f"Application failed to start: {str(e)}")
		sys.exit(1)

if __name__ == "__main__":
	main()
