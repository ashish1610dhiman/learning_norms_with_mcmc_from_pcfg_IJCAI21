import sys
sys.path.append('src')

import yaml
import pickle
from pickle_wrapper import pickle_it, unpickle
import argparse
from algorithm_2_utilities import Likelihood
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.environment import position

parser = argparse.ArgumentParser(description='Generate log likelihood of observations given specified norm expressions')
parser.add_argument('norm_types', metavar='NT', type=str, nargs='+',
                    help='enter none, true and/or top, separated by spaces')

args = parser.parse_args()
requested_expressions = args.norm_types

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area_parts = params['target_area'].replace(' ','').split(';')
target_area_part0 = position(*map(float, target_area_parts[0].split(',')))
target_area_part1 = position(*map(float, target_area_parts[1].split(',')))
target_area = (target_area_part0, target_area_part1)

the_task = task(colour_specific, shape_specific,target_area)
obs = unpickle('data/observations.pickle')
env = unpickle('data/env.pickle')

if 'none' in requested_expressions:
    ll_no_norm = Likelihood([],the_task,obs,env)
    print(f"Log likelihood of observations given no norm: {ll_no_norm}\n")
if 'true' in requested_expressions:
    true_expression = params['true_norm']['exp']
    ll_true_exp = Likelihood(true_expression,the_task,obs,env)
    print(f"Log likelihood of observations given true exp.: {ll_true_exp}\n")
if 'top' in requested_expressions:
    top_norm = unpickle('data/top_norms.pickle')[0]
    ll_top_norm = Likelihood(top_norm,the_task,obs,env)
    print(f"Log likelihood of observations given top norm.: {ll_top_norm}\n")
