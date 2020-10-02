import sys
sys.path.append('src')

import yaml
import pickle
from pickle_wrapper import pickle_it, unpickle

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
n = params['n']

chain_length = 4*n

chains_and_log_posteriors = unpickle('data/chains_and_log_posteriors.pickle')

for i,chain_data in enumerate(chains_and_log_posteriors):
    log_posteriors = chain_data['log_posteriors']
    print(f'Chain {i} log posteriors: \n{log_posteriors[chain_length-1000:]}\n')
