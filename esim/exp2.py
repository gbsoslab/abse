import subprocess
import numpy as np
import random

total_experiments = 30
exp_results = []

'''
coord = []
for i in range(10):
	for j in range(10):
		coord.append((i, j))
random.shuffle(coord)

for i in range(50):
	print(f'rm.add_agent_to_region(0, ({coord[i][0]}, {coord[i][1]}), Agent(AgentOpt(0, {i}, "OBJ_GREED")))')

'''
for i in range(30):
	total_agent = 50
	proc = subprocess.Popen(['python', 'smart.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	out = proc.communicate()

	sim_end = out[0].decode('ascii').split('\r\n')[-2].split('|')[-1]
	left_agent = sim_end.split(":")[-1][1:-1]

	survived = total_agent - len(left_agent.split(','))
	exp_results.append(survived/float(total_agent))

print(f"mean:{np.mean(exp_results)}, stddev:{np.std(exp_results)}")
