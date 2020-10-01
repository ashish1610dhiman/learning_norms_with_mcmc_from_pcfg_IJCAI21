import sys
sys.path.append('src')

from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.mcmc_convergence import prepare_sequences, calculate_R
from operator import itemgetter
import yaml

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
rhat_step_size = params['rhat_step_size']

def conv_test(chains):
    convergence_result, split_data = calculate_R(chains, rhat_step_size)
    print(convergence_result.to_string())

chains_and_log_likelihoods = unpickle('data/chains_and_log_likelihoods.pickle')
chains = list(map(itemgetter('chain'), chains_and_log_likelihoods))
conv_test(prepare_sequences(chains, warmup=False))
