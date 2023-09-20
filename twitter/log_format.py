import logging

def setup_logger():
    """ Function sets up logger and logging capabilities: organize messages
        - Logger log levels: Debug, Info, Warn, Error, Critial, Fatal
        Returns logger object with custom template to print logs/msgs to devs in console
    """
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG) # SET log level

    # Create log handler and formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter) # Add formatter to handler
    logger.addHandler(handler) # Add handler to logger
    return logger
