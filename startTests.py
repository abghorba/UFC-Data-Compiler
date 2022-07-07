import pytest
import os
import sys


if len(sys.argv) != 2:
    raise Exception("Correct usage: python startTests.py <test_name>")

args = sys.argv[1:]
test_to_run = args[0]

# Since we use argparse in ufc_scraper.py we will get a system error
# unless we clear the arguments here first
sys.argv = [sys.argv[0]]

pytest.main([os.getcwd() + f"/tests/{test_to_run}.py", "-s", "-v"])
