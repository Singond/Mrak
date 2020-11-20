import logging

logger = logging.getLogger("Mrak")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)-5s %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
