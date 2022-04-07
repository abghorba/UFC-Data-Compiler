import logging
import pytest
import os

from datetime import datetime

log_filename = datetime.now().strftime("%d%m%Y%H%M%S") + f"-unit_tests"
log_filepath = os.getcwd() + f"/logs/{log_filename}.log"

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(module)s.py - %(funcName)s - [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(log_filepath),
                                logging.StreamHandler()])

pytest.main([os.getcwd() + f"/tests/unit_tests.py", "-v"])
