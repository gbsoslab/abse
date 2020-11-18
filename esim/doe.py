import contexts
import subprocess
import numpy as np
import random
import copy


total_experiments = 30
exp_results = []

def gen_random_agents(x, y, agent_number):
	coord = []
	for i in range(x):
		for j in range(y):
			coord.append((i, j))
	random.shuffle(coord)
	return (coord[0:agent_number], agent_number)

def gen_quadrant_agents(x, y, agent_number, quadrant):
	coord = []
	gened_agent = 0

	if quadrant == 1:
		for i in range(int(x*0.3), x):
			for j in range(0, int(y*0.7)):
				coord.append((i, j))

		gened_agent = (x-int(x*0.3)) * int(y*0.7)
	elif quadrant == 2:
		for i in range(0, int(x*0.7)):
			for j in range(0, int(y*0.7)):
				coord.append((i, j))

		gened_agent = (int(x*0.7)) * int(y*0.7)
	elif quadrant == 3:
		for i in range(0, int(x*0.7)):
			for j in range(int(y*0.3), y):
				coord.append((i, j))
		gened_agent = int(x*0.7) * (y-int(y*0.3))
	elif quadrant == 4:
		for i in range(int(x*0.3), x):
			for j in range(int(y*0.3), y):
				coord.append((i, j))
		gened_agent = (x-int(x*0.3)) * (y-int(y*0.3))

	random.shuffle(coord)
	if agent_number < gened_agent:
		return (coord[0:agent_number], agent_number)
	else:
		return (coord[0:gened_agent], gened_agent)

import yaml
scenario = {'sceVersion': 'sce/v1',\
						 'sceType': 'EvacSim',\
						 'scenario':{\
						 	'regions':[],\
						 	'building':{\
						 	'exits':[],\
						 	},\
						 	'agents':[\
						 			],\
						 	},\
						 'config':{\
						 		'simName':'evacuation',\
						 		'engineName':'sname',\
					 			'instance_time':0, \
					 			'destroy_time':1000,\
					 			'rand_seed':1
						 	}
						 }

scenario_template = copy.deepcopy(scenario)

regions = [(10, 10), (5, 20), (20, 5)]
exits = [ [(0, 4)], [(0,0), (0, 4)], [(0,4), (4, 0)], [(0, 0), (0, 4), (0, 9)]]
agents = [25, 50, 75]
spawn_pattern = [0, 1, 2, 3, 4]
agent_type = [0, 0.25, 0.5, 0.75, 100]

import os

if not os.path.isdir('./scenario'):
	os.mkdir('./scenario')
	
rid = 0
for r in regions:
	for eid, ex in enumerate(exits):
		for aNum, ag in enumerate(agents):
			for sPattern, sp in enumerate(spawn_pattern):
				for aType, ag_type in enumerate(agent_type):
					scenario['scenario']['regions'].append({'rid':rid, 'regionSize':[r[0], r[1]], 'entries':[{'en_id':0, 'coord':[4, 4]}], 'exits':[]})
					for idx, item in enumerate(ex):
						scenario['scenario']['regions'][rid]['exits'].append({'ex_id':idx, 'coord':[item[0], item[1]]}) 
						scenario['scenario']['building']['exits'].append({'eid':idx, 'rid':rid})

					if sp == 0:
						alist, ag = gen_random_agents(r[0], r[1], ag)
						for aid, coord in enumerate(alist):
							if random.uniform(0, 1) < ag_type:
								scenario['scenario']['agents'].append({'rid':0, 'aid':aid, 'coord':[coord[0], coord[1]], 'type':'Normal', 'strategy': 'OBJ_GREED'})
							else:
								scenario['scenario']['agents'].append({'rid':0, 'aid':aid, 'coord':[coord[0], coord[1]], 'type':'Normal', 'strategy': 'OBJ_SMART'})
					else:
						alist, ag = gen_quadrant_agents(r[0], r[1], ag, sp)
						for aid, coord in enumerate(alist):
							if random.uniform(0, 1) < ag_type:
								scenario['scenario']['agents'].append({'rid':0, 'aid':aid, 'coord':[coord[0], coord[1]], 'type':'Normal', 'strategy': 'OBJ_GREED'})
							else:
								scenario['scenario']['agents'].append({'rid':0, 'aid':aid, 'coord':[coord[0], coord[1]], 'type':'Normal', 'strategy': 'OBJ_SMART'})
												
					dir_path = f"scenario/{r[0]}X{r[1]}_ep[{eid}]_an[{ag}]_sp[{sPattern}]_at[{aType}]/"
					
					if not os.path.isdir(dir_path):
						os.mkdir(dir_path)

					for rs in range(30):
						with open(dir_path + f"{r[0]}X{r[1]}_ep[{eid}]_an[{aNum}]_sp[{sPattern}]_at[{aType}]_rs[{rs}].sce", 'w') as f:
							scenario['config']['rand_seed'] = rs
							yaml.dump(scenario, f)
							
					scenario = copy.deepcopy(scenario_template)