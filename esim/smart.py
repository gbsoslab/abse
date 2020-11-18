import contexts
import sys,os

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *

from adev.clock import Clock
from adev.agent import Agent, AgentOpt
from adev.region_manager import RegionManager, UniRegionManager

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
	

rm = UniRegionManager()
rm.add_region_to_building(0, (10, 10))
# handle entry points 
rm.add_entry_point_to_region(0, 0, (4,4))
# handle exit points 
rm.add_exit_point_to_region(0, 0, (0, 4))
rm.add_exit_point_to_region(0, 1, (4, 0))

rm.add_building_exit(0, 0)
rm.add_building_exit(0, 1)

rm.add_agent_to_region(0, (1, 1), Agent(AgentOpt(0, 0, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (3, 7), Agent(AgentOpt(0, 1, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (9, 7), Agent(AgentOpt(0, 2, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (4, 7), Agent(AgentOpt(0, 3, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (0, 3), Agent(AgentOpt(0, 4, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (7, 7), Agent(AgentOpt(0, 5, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (2, 5), Agent(AgentOpt(0, 6, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (6, 9), Agent(AgentOpt(0, 7, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (2, 4), Agent(AgentOpt(0, 8, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (6, 6), Agent(AgentOpt(0, 9, "OBJ_SMART")))                                                                                                 
rm.add_agent_to_region(0, (3, 8), Agent(AgentOpt(0, 10, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (6, 8), Agent(AgentOpt(0, 11, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (7, 9), Agent(AgentOpt(0, 12, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (2, 1), Agent(AgentOpt(0, 13, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (1, 0), Agent(AgentOpt(0, 14, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (9, 3), Agent(AgentOpt(0, 15, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (0, 0), Agent(AgentOpt(0, 16, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (6, 0), Agent(AgentOpt(0, 17, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (9, 5), Agent(AgentOpt(0, 18, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 2), Agent(AgentOpt(0, 19, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (0, 9), Agent(AgentOpt(0, 20, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (3, 2), Agent(AgentOpt(0, 21, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (9, 1), Agent(AgentOpt(0, 22, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 6), Agent(AgentOpt(0, 23, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (7, 5), Agent(AgentOpt(0, 24, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 9), Agent(AgentOpt(0, 25, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 3), Agent(AgentOpt(0, 26, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (3, 0), Agent(AgentOpt(0, 27, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (7, 2), Agent(AgentOpt(0, 28, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (6, 3), Agent(AgentOpt(0, 29, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (3, 3), Agent(AgentOpt(0, 30, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (1, 6), Agent(AgentOpt(0, 31, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (3, 1), Agent(AgentOpt(0, 32, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (7, 1), Agent(AgentOpt(0, 33, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (2, 6), Agent(AgentOpt(0, 34, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (0, 2), Agent(AgentOpt(0, 35, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (8, 7), Agent(AgentOpt(0, 36, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (4, 9), Agent(AgentOpt(0, 37, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (9, 0), Agent(AgentOpt(0, 38, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (1, 2), Agent(AgentOpt(0, 39, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (2, 2), Agent(AgentOpt(0, 40, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (3, 6), Agent(AgentOpt(0, 41, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 0), Agent(AgentOpt(0, 42, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 1), Agent(AgentOpt(0, 43, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (5, 7), Agent(AgentOpt(0, 44, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (8, 8), Agent(AgentOpt(0, 45, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (1, 4), Agent(AgentOpt(0, 46, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (1, 7), Agent(AgentOpt(0, 47, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (4, 3), Agent(AgentOpt(0, 48, "OBJ_SMART")))                                                                                                
rm.add_agent_to_region(0, (3, 9), Agent(AgentOpt(0, 49, "OBJ_SMART")))  

#rm.add_agent_to_region(0, (29, 29), Agent(AgentOpt(0, 0, "OBJ_GREED")))
#rm.add_agent_to_region(0, (2,2), Agent(AgentOpt(0, 8, "OBJ_GREED")))
#rm.add_agent_to_region(0, (2,2), Agent(AgentOpt(0, 7, "OBJ_GREED")))

#rm.connect_region(0, 0, 1, 0)

building = rm.get_building(0, 100, "evacuation", "sname")

se.get_engine("sname").insert_input_port("agent_in")
se.get_engine("sname").insert_output_port("agent_out")

se.get_engine("sname").register_entity(building)

se.get_engine("sname").simulate()
