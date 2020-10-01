import sys
sys.path.append('src')

import yaml
import pickle
from pickle_wrapper import pickle_it, unpickle
from algorithm_2_utilities import Likelihood
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.environment import position

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area_parts = params['target_area'].replace(' ','').split(';')
target_area_part0 = position(*map(float, target_area_parts[0].split(',')))
target_area_part1 = position(*map(float, target_area_parts[1].split(',')))
target_area = (target_area_part0, target_area_part1)

true_expression = params['true_norm']['exp']
the_task = task(colour_specific, shape_specific,target_area)
obs = unpickle('data/observations.pickle')
env = unpickle('data/env.pickle')

ll_no_norm = Likelihood([],the_task,obs,env)
ll_true_exp = Likelihood(true_expression,the_task,obs,env)
learned_exp = ['Norms', ['Obl', ['Moved', ['Colour', 'b'], ['Shape', 'any'], ['Zone', '2'], ['Next-Move', ['Colour', 'b'], ['Shape', 'any']]], ['Zone', '2']], ['Per', ['Action', 'putdown'], ['Colour', 'any'], ['Shape', 'square'], ['PerZone', '1']]]
ll_learned_exp = Likelihood(learned_expression,the_task,obs,env)

print("Log likelihood of observations given no norm: {ll_no_norm}\n")
print("Log likelihood of observations given true exp.: {ll_true_exp}\n")
print("Log likelihood of observations given learned exp.: {ll_learned_exp}\n")



# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint()
