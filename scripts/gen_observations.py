import sys
sys.path.append('src')

import yaml
import shutil
import math
import pickle
import numpy as np
from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.algorithm_1_v4 import create_data
from mcmc_norm_learning.rules_4 import get_prob, get_log_prob
from mcmc_norm_learning.environment import position
from mcmc_norm_learning.robot_task_new import task, robot

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

true_norm_exp = params['true_norm']['exp']
num_observations = params['num_observations']
obs_data_set = params['obs_data_set']

colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area_parts = params['target_area'].replace(' ','').split(';')
target_area_part0 = position(*map(float, target_area_parts[0].split(',')))
target_area_part1 = position(*map(float, target_area_parts[1].split(',')))
target_area = (target_area_part0, target_area_part1)
print(target_area_part0.coordinates())
print(target_area_part1.coordinates())
the_task = task(colour_specific, shape_specific,target_area)

env = unpickle('data/env.pickle')

rob = robot(the_task,env)
actionable = rob.all_actionable()
print(actionable)

true_norm_prior = get_prob("NORMS",true_norm_exp) 
true_norm_log_prior = get_log_prob("NORMS",true_norm_exp) 

if math.isclose(true_norm_prior, 0):
    print(f'Stopping! True norm expression has near-zero prior ({true_norm_prior})\n')
# elif (num_observations == 100 and obs_data_set == 1):
#     shutil.copyfile('data/default_observations.pickle', 'data/observations.pickle')
else:
    observations = create_data(true_norm_exp,env,name=None,task=the_task,random_task=False,
                               num_actionable=np.nan,num_repeat=num_observations,verbose=False)
    pickle_it(observations, 'data/observations.pickle')
    

