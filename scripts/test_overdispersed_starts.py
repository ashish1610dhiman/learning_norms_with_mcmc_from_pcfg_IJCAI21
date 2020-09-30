import sys
sys.path.append('src')

import yaml
import pickle
from pickle_wrapper import pickle_it, unpickle
from mcmc_norm_learning.algorithm_1_v4 import over_dispersed_starting_points
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.environment import position
import pprint

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area_parts = params['target_area'].replace(' ','').split(';')
target_area_part0 = position(*map(float, target_area_parts[0].split(',')))
target_area_part1 = position(*map(float, target_area_parts[1].split(',')))
target_area = (target_area_part0, target_area_part1)
true_expression = params['true_norm']['exp']

env = unpickle('data/env.pickle')
the_task = task(colour_specific, shape_specific,target_area)
obs = unpickle('data/observations.pickle')
num_starts = 5
odsp, info = over_dispersed_starting_points(num_starts,obs,env,the_task)
print(info)
print('E0s:\n')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(odsp)
