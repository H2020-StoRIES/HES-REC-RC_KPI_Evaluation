import logging
import os
import time
log_file = f"app_{time.strftime('%Y%m%d%H%M%S')}.log"
def setup_logging(log_directory="logs", log_file= log_file, level=logging.INFO):
    os.makedirs(log_directory, exist_ok=True)  # Create log directory if it doesn't exist
    log_path = os.path.join(log_directory, log_file)
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_path),
                            logging.StreamHandler()  # Also log to stderr/console
                        ])