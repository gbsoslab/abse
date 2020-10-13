import contexts
from adev.scenario_manager import *
from adev.region_manager import UniRegionManager
from adev.agent import Agent, AgentOpt

from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.system_message import SysMessage
from evsim.definition import *

from config import *

scm = ScenarioManager('evac.sce')
config =scm.get_config()

se = SystemSimulator()
se.register_engine(config['engineName'], SIMULATION_MODE, TIME_DENSITY)

#print(scm.get_example_scenario())
rm = UniRegionManager()

# Regions
for region in scm.get_regions():
	rm.add_region_to_building(region['rid'], (region['regionSize'][0], region['regionSize'][1]))
	for entry in region['entries']:
		rm.add_entry_point_to_region(region['rid'], entry['en_id'], (entry['coord'][0],entry['coord'][1]))
		rm.add_entry_point_to_region(region['rid'], entry['en_id'], (entry['coord'][0], entry['coord'][1]))
	for exit in region['exits']:
		rm.add_exit_point_to_region(region['rid'], entry['ex_id'], (entry['coord'][0],entry['coord'][1]))
		rm.add_exit_point_to_region(region['rid'], exit['ex_id'], (exit['coord'][0], exit['coord'][1]))

# Agents
for agent in scm.get_agents():
	if agent['type'] == 'Normal':
		rm.add_agent_to_region(agent['rid'], (agent['coord'][0], agent['coord'][1]), Agent(AgentOpt(agent['rid'], agent['aid'], agent['strategy'])))


building = rm.get_building(config['instance_time'], config['destroy_time'], config['simName'], config['engineName'])

se.get_engine(config['engineName']).insert_input_port("agent_in")
se.get_engine(config['engineName']).insert_output_port("agent_out")

se.get_engine(config['engineName']).register_entity(building)

se.get_engine(config['engineName']).simulate()