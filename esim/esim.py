import contexts
import sys,os

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *
import numpy as np

from adev.clock import Clock
from adev.agent import Agent, AgentOpt
from adev.region_manager import RegionManager

import random
# Simulation Configuration
se = SystemSimulator()

se.register_engine("sname", SIMULATION_MODE, TIME_DENSITY)

# NETWORK_LIBRARY
if NETWORK_UI_FLAG:
	from ipworks import *
	from evsim.network_manager import NetworkManager

	udp_lib = UDPPort()
	udp_lib.runtime_license = IPWORKS_LICENSE
	#ipport = IPPort()
	#ipport.runtime_license = IPWORKS_LICENSE
	net_manager = NetworkManager()
	net_manager.register_network_library(udp_lib)
	#net_manager.register_network_library(ipport)
	#net_manager.connect(NETWORK_HOST_ADDR, NETWORK_HOST_PORT)
	

rm = RegionManager()
rm.add_region_to_building(0, (10, 10), 4)
rm.add_region_to_building(1, (10, 10), 4)
# handle entry points 
rm.add_entry_point_to_region(0, 0, (9,5))
rm.add_entry_point_to_region(1, 0, (9,5))
# handle exit points 
rm.add_exit_point_to_region(0, 0, (0, 5))
rm.add_exit_point_to_region(1, 0, (0, 5))


for i in range(400):
	region = random.randint(0,1)
	x_coord = random.randint(0, 9)
	y_coord = random.randint(0, 9)
	rm.add_agent_to_region(region, (x_coord, y_coord), Agent(AgentOpt(region, i, "OBJ_GREED")))

#rm.add_agent_to_region(0, (29, 29), Agent(AgentOpt(0, 0, "OBJ_GREED")))
#rm.add_agent_to_region(0, (2,2), Agent(AgentOpt(0, 8, "OBJ_GREED")))
#rm.add_agent_to_region(0, (2,2), Agent(AgentOpt(0, 7, "OBJ_GREED")))

rm.connect_region(0, 0, 1, 0)

building = rm.get_building(0, 3000, "evacuation", "sname")



se.get_engine("sname").insert_input_port("agent_in")
se.get_engine("sname").insert_output_port("agent_out")

se.get_engine("sname").register_entity(building)

se.get_engine("sname").simulate()