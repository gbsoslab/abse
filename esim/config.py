# SIMULATION_MODE
SIMULATION_MODE = 'VIRTUAL_TIME'

# SIMULATION_MODEL
TIME_DENSITY=1
MODEL_TIME_REQ=1

# Network UI Feature
NETWORK_UI_FLAG = False
NETWORK_HOST_ADDR = "127.0.0.1"
NETWORK_HOST_PORT = 19612
NETWORK_UPDATE_FREQ = 1

IPWORKS_LICENSE = ""

# REPORT Feature
REPORT_FLAG = True
REPORT_FREQ = 1
REPORT_TO_NETWORK = False
REPORT_TO_CONSOLE = True

import os
if os.path.isfile("./instance/config.py"):
	from instance.config import *