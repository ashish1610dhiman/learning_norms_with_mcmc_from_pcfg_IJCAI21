import sys
sys.path.append('src')
import yaml
from tqdm.notebook import trange
import pickle
import csv
from mcmc_norm_learning.rules_4 import q_dict, rule_dict
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.algorithm_1_v4 import algorithm_1
from mcmc_norm_learning.environment import position

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
print(target_area)

def unpickle(path):
    with open(path, 'rb') as fp:
        result = pickle.load(fp)
        print("Unpickled 1st element for '{}' is {}\n".format(path, result[0]))
        return result

def pickle_it(x, path):
    with open(path, 'wb') as fp:
        pickle.dump(x, fp)

true_expression = params['true_norm']['exp']
env = unpickle('data/env.pickle')

the_task = task(colour_specific, shape_specific,target_area)

obs = unpickle('data/observations.pickle')

with open('metrics/chain_likelihoods.csv', 'w', newline='') as csvfile:
    chains=[]
    writer = csv.writer(csvfile)
    writer.writerow(('chain_number', 'chain_pos', 'likelihood'))
    for i in trange(1,int(m/2+1),desc="Loop for Individual Chains"):
        print ("\n:::::::::::::::::::: FOR SEQUENCE {} ::::::::::::::::::::".format(i))
        exp_seq,likelihoods = algorithm_1(obs,env,the_task,q_dict,rule_dict,
                                        "demo/convergence/report_for_chain_{}_x".format(i),
                                        relevance_factor=rf,max_iterations=4*n,verbose=False)
        chains.append(exp_seq)
        writer.writerows(((i,j,likelihood) for j,likelihood in enumerate(likelihoods)))
    pickle_it(chains, 'data/chains.pickle')
