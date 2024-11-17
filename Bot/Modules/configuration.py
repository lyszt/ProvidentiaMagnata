import logging
import os

class Initialize:
    def __init__(self):
        pass
    def makeLogs(self):
        LOG_FILE = 'providence.log'
        if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
            os.remove(LOG_FILE)
        logging.basicConfig(filename='providence.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s'
                            ,datefmt="%H:%M:%S")
        logging.FileHandler('providence.log')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
