"""System check utility for AI Video Editor"""

import sys
import pkg_resources
import subprocess
from pathlib import Path
import logging
from config import LOG_FORMAT, LOG_FILE, LOG_DIR

def setup_logging():
	"""Setup logging for system checks."""
	LOG_DIR.mkdir(exist_ok=True)
	logging.basicConfig(
		level=logging.INFO,
		format=LOG_FORMAT,
		handlers=[
			logging.StreamHandler(),
			logging.FileHandler(LOG_FILE)
		]
	)
	return logging.getLogger(__name__)

def check_python_version():
	"""Check if Python version meets requirements."""
	required_version = (3, 8)
	current_version = sys.version_info[:2]
	return current_version >= required_version

def check_gpu_support():
	"""Check for GPU support."""
	try:
		import torch
		return torch.cuda.is_available()
	except ImportError:
		return False

def check_ffmpeg():
	"""Check if FFmpeg is installed."""
	try:
		subprocess.run(['ffmpeg', '-version'], capture_output=True)
		return True
	except FileNotFoundError:
		return False

def check_dependencies():
	"""Check all required dependencies."""
	logger = setup_logging()
	requirements_file = Path(__file__).parent / 'requirements.txt'
	
	if not requirements_file.exists():
		logger.error("requirements.txt not found")
		return False
		
	required = pkg_resources.parse_requirements(requirements_file.open())
	installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
	missing = []
	
	for package in required:
		package_name = str(package.req.name)
		if package_name not in installed:
			missing.append(package_name)
			
	return len(missing) == 0, missing

def run_system_check():
	"""Run all system checks."""
	logger = setup_logging()
	checks = {
		"Python Version": check_python_version(),
		"GPU Support": check_gpu_support(),
		"FFmpeg": check_ffmpeg()
	}
	
	deps_ok, missing_deps = check_dependencies()
	checks["Dependencies"] = deps_ok
	
	all_passed = all(checks.values())
	
	if all_passed:
		logger.info("All system checks passed")
	else:
		logger.error("System checks failed:")
		for check, passed in checks.items():
			if not passed:
				if check == "Dependencies":
					logger.error(f"Missing dependencies: {', '.join(missing_deps)}")
				else:
					logger.error(f"{check} check failed")
					
	return all_passed

if __name__ == "__main__":
	sys.exit(0 if run_system_check() else 1)