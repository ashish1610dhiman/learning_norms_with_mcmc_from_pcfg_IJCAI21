import sys
sys.path.append('src')

import mcmc_norm_learning
import yaml
import shutil

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

true_norm_exp = params['true_norm']['exp']
target_area_str = params['target_area']
num_observations = params['num_observations']
obs_data_set = params['obs_data_set']

if (num_observations == 100 and 
    obs_data_set == 1
   ):
    shutil.copyfile('data/default_observations.pickle', 'data/observations.pickle')
else:
    print('To do: generate new observations')
    

