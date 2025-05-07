
import os
from datetime import datetime

# def setup_logging(log_dir='logs', level=logging.INFO):
#     # Create timestamped log file name
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     log_file = os.path.join(log_dir, f"app_{timestamp}.log")

#     # Ensure log directory exists
#     os.makedirs(log_dir, exist_ok=True)

#     # Configure logging
#     logging.basicConfig(
#         level=level,
#         format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#         handlers=[
#             logging.FileHandler(log_file, mode='w'),
#             logging.StreamHandler()
#         ]
#     )
    
        
import logging

def setup_logging(log_dir='logs', level=logging.INFO):
    # Configure the root logger
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"app_{timestamp}.log")
    
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(level=logging.INFO, filename=log_file, filemode="a",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Optional: Add a console handler for debugging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Add the console handler to the root logger
    logging.getLogger().addHandler(console_handler)

    logging.info(f"Log file created: {log_file}")
