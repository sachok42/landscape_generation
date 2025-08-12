import logging
from logging.handlers import RotatingFileHandler
import os

def create_logger(name, log_file, level=logging.INFO, max_bytes=1048576, backup_count=5):
	"""
	Creates and configures a logger that writes to a specific file.
	
	Args:
		name (str): Name of the logger (usually __name__)
		log_file (str): Path to the log file
		level (int): Logging level (default: logging.INFO)
		max_bytes (int): Max log file size before rotation (default: 1MB)
		backup_count (int): Number of backup logs to keep (default: 5)
		
	Returns:
		logging.Logger: Configured logger instance
	"""
	# Create logger
	logger = logging.getLogger(name)
	logger.setLevel(level)
	
	# Create logs directory if it doesn't exist
	log_dir = os.path.dirname(log_file)
	if log_dir and not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	# Create rotating file handler
	handler = RotatingFileHandler(
		log_file,
		maxBytes=max_bytes,
		backupCount=backup_count
	)
	
	# Create formatter
	formatter = logging.Formatter(
		'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	handler.setFormatter(formatter)
	
	# Add handler to logger if not already added
	if not any(
		isinstance(h, RotatingFileHandler) and h.baseFilename == os.path.abspath(log_file)
		for h in logger.handlers
	):
		logger.addHandler(handler)
	
	return logger

# Example usage
if __name__ == "__main__":
	# Create different loggers for different purposes
	app_logger = create_logger("myapp", "logs/application.log")
	db_logger = create_logger("database", "logs/database.log", level=logging.DEBUG)
	error_logger = create_logger("errors", "logs/errors.log", level=logging.ERROR)
	
	# Log some messages
	app_logger.info("Application started")
	db_logger.debug("Database connection established")
	error_logger.error("Critical error occurred!")