import logging

def setup_logger(verbose=False):
    level = logging.INFO if verbose else logging.ERROR
    logging.basicConfig(filename='app.log', level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def get_logger():
    return logging.getLogger(__name__)
