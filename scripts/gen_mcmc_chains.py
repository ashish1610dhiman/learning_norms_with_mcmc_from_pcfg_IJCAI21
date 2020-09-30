import sys
sys.path.append('src')

import yaml
from tqdm.notebook import trange
import pickle
import csv
import math
from mcmc_norm_learning.rules_4 import q_dict, rule_dict, get_prob
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.algorithm_1_v4 import algorithm_1, over_dispersed_starting_points
from mcmc_norm_learning.environment import position
from pickle_wrapper import unpickle, pickle_it
import dask
from dask.distributed import Client

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

n = params['n']
m = params['m']
rf = params['rf']
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

num_chains = int(m/2+1)
starts, info = over_dispersed_starting_points(num_chains,obs,env,the_task,time_threshold=math.inf)
with open('metrics/chain_info.txt', 'w') as chain_info:
    chain_info.write(info)

@dask.delayed
def delayed_alg1(obs,env,the_task,q_dict,rule_dict,start,rf,max_iters):
    exp_seq,log_likelihoods = algorithm_1(obs,env,the_task,q_dict,rule_dict,
                                        "dummy value",
                                        start = start,
                                        relevance_factor=rf,max_iterations=max_iters,verbose=False)
    log_posteriors = [None]*len(exp_seq)
    for i in range(len(exp_seq)):
        exp = exp_seq[i]
        ll = log_likelihoods[i]
        prior = get_prob("NORMS",exp) # Note: this imports the rules dict from rules_4.py
        log_posteriors[i] = math.log(prior) + ll

    return {'chain': exp_seq, 'log_likelihoods': log_posteriors} #!!!!! *** Deliberately misnaming 2nd key name for now

with open('metrics/chain_likelihoods.csv', 'w', newline='') as cl_csvfile:
    chains_and_log_likelihoods=[]
    for i in trange(1,num_chains,desc="Loop for Individual Chains"):
        chains_and_log_likelihoods.append(
            delayed_alg1(obs,env,the_task,q_dict,rule_dict,starts[i],rf,4*n))
    pickle_it(dask.compute(*chains_and_log_likelihoods), 'data/chains_and_log_likelihoods.pickle')
