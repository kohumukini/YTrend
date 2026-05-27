import logging
import logging.config
from .flow import flow_pipeline


LOGGING_CONFIG = {
    "version": 1, 
    "disable_existing_loggers": True, 
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(message)s", 
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }, 
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        }
    }, 

    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler", 
            "level": "INFO", 
            "formatter": "simple", 
            "stream": "ext://sys.stdout", 
        }, 
        "stderr": {
            "class": "logging.StreamHandler", 
            "level": "ERROR", 
            "formatter": "detailed", 
            "stream": "ext://sys.stderr", 
        }, 
        "file": {
            # Selecting the handler class for files
            "class": "logging.FileHandler", 
            # Detailed formatting for documentation
            "level": "DEBUG", 
            "formatter": "detailed", 
            "filename": "app.log", 
            # Writing mode
            "mode": "a"
        }
    }, 
    "root": {
        "level": "DEBUG", 
        "handlers": [
            "stdout", 
            "stderr", 
            "file"
        ]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

if __name__ == "__main__": 
    try: 
        logger.info("Pipeline starting...")
        flow_pipeline()
        logger.info("Pipeline run successfully")
    except Exception as e: 
        logger.critical(f"Pipeline failed: Rendering Issue: {e}", exc_info = True)
        # exc info full traceback implementation