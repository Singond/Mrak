import sys
import argparse
from mrak.core import Mrak, ConfigNotFoundException
from mrak.log import logger
from mrak import systray

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--config-file")
    args = parser.parse_args()

    logger.info("Starting Mrak")
    logger.debug("Parsed arguments: %s", args)
    try:
        if "config_file" in args:
            m = Mrak(args.config_file)
        else:
            m = Mrak()
    except ConfigNotFoundException:
        logger.error("No configuration file found")
        sys.exit(10)

    systray.run(m)

    logger.info("Quitting Mrak")
