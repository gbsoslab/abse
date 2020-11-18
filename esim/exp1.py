import subprocess
import numpy as np
import random
import os
import platform

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
avg_time = []
with open('exp_results.csv', "w") as f:
	for _dir in os.listdir('./scenario'):
		base = os.path.join('./scenario', _dir)
		print(base)
		for sce in os.listdir(base):
			print("\t", sce)
			file_path = os.path.join(base, sce)
			if platform.system() == 'Windows':
				proc = subprocess.Popen(['python', 'uni_esim.py', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
			else:
				proc = subprocess.Popen(['python3', 'uni_esim.py', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
			out = proc.communicate()

			sim_end = out[0].decode('ascii').split('\r\n')
			avg_time.append(float(sim_end[0].split(":")[-1]))
			exp_results.append(float(sim_end[1].split(",")[1].split(":")[-1])/float(sim_end[1].split(",")[0].split(":")[-1]))

		f.write(f"{_dir}, {_dir.split('_')[0]}, {_dir.split('_')[1]}, {_dir.split('_')[2]}, {_dir.split('_')[3]}, {_dir.split('_')[4]},{np.mean(avg_time)}, {np.mean(exp_results)}, {np.std(exp_results)}\n")
		
		avg_time.clear()
		exp_results.clear()