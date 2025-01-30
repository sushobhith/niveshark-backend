import logging
from datetime import datetime
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
  os.makedirs("logs")

# Configure logging
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  handlers=[
      # File handler for all logs
      logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
      # Console handler
      logging.StreamHandler()
  ]
)

# Create logger
logger = logging.getLogger(__name__) 