from core import Mrak
from log import logger
import systray

logger.info("Starting Mrak")
m = Mrak("../test/testconfig.yaml")
systray.run(m)
logger.info("Quitting Mrak")
