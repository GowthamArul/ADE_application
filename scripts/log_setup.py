import logging
import os
import time

def init_logger():
    # Create log directory if it doesn't exist
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Set up logging
    log_file = os.path.join(log_directory, f'{time.strftime("%Y%m%d_%H%M%S")}_app.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
