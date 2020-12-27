"""
# Created by ashish1610dhiman at 27/12/20
Contact at ashish1610dhiman@gmail.com
"""


import sys
sys.path.append('src')


import yaml
import math
import pickle
import numpy as np
from pickle_wrapper import unpickle, pickle_it
import matplotlib.pyplot as plt



from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.algorithm_1_v4 import create_data
from mcmc_norm_learning.rules_4 import get_prob, get_log_prob
from mcmc_norm_learning.environment import position,plot_env
from mcmc_norm_learning.robot_task_new import task, robot, plot_task


with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

##Get default env
env = unpickle('data/env.pickle')


##Get default task
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


nc_obs= create_data(true_norm_exp,env,name=None,task=the_task,random_task=False,
                               num_actionable=np.nan,num_repeat=50,w_nc=0.1,verbose=False)

print (len(nc_obs))



