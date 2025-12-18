"""Advanced Logging with Rotation - Extended"""
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import sys
from pathlib import Path
from datetime import datetime

def setup_advanced_logger(name='data_pipeline'):
    """Setup logger with multiple handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler (INFO and above)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        '%(asctime)s - %(levelname)-8s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console.setFormatter(console_fmt)
    
    # Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # File handler with size rotation
    file_handler = RotatingFileHandler(
        log_dir / 'pipeline.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_fmt)
    
    # Daily rotating handler
    daily_handler = TimedRotatingFileHandler(
        log_dir / 'daily.log',
        when='midnight',
        interval=1,
        backupCount=30
    )
    daily_handler.setLevel(logging.INFO)
    daily_handler.setFormatter(file_fmt)
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.addHandler(daily_handler)
    
    return logger

# Example usage
if __name__ == '__main__':
    logger = setup_advanced_logger()
    
    logger.debug("Debug message - detailed info")
    logger.info("Pipeline started")
    logger.warning("Warning - check this")
    logger.error("Error occurred")
    logger.critical("Critical issue!")
    
    # Simulate pipeline steps
    for i in range(5):
        logger.info(f"Processing batch {i+1}/5")
    
    logger.info("Pipeline completed successfully")
    
    print("\n✅ Logs written to:")
    print("   - logs/pipeline.log (all levels, size-rotated)")
    print("   - logs/daily.log (daily rotation)")
