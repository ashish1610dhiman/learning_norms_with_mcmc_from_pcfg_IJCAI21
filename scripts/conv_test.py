import sys
sys.path.append('src')

import yaml
import pickle
from pickle_wrapper import unpickle, pickle_it
from functools import reduce
from operator import concat
from mcmc_norm_learning.mcmc_convergence import prepare_sequences, calculate_R

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
rhat_step_size = params['rhat_step_size']

def conv_test(chains):
    convergence_result, split_data = calculate_R(chains, rhat_step_size)
    with open('metrics/conv_test.txt', 'w') as f:
        f.write(convergence_result.to_string())
    return reduce(concat, split_data)
    
chains = unpickle('data/chains.pickle')
posterior_sample = conv_test(prepare_sequences(chains, warmup=True))
pickle_it(posterior_sample, 'data/posterior.pickle')
