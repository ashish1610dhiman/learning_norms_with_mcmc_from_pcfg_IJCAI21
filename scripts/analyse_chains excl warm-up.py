import sys
sys.path.append('src')

from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.mcmc_convergence import prepare_sequences
from mcmc_norm_learning.algorithm_1_v4 import to_tuple
from collections import defaultdict
import itertools
import operator
import yaml
import math

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)
m = params['m']
num_chains = math.ceil(m/2)

chains_and_log_posteriors = unpickle('data/chains_and_log_posteriors.pickle')[:num_chains]

with open('metrics/chain_info_no_warmup.txt', 'w') as chain_info:
    chain_info.write(f'Number of chains: {len(chains_and_log_posteriors)}\n')
    chain_length = len(chains_and_log_posteriors[0]["chain"])
    print(f'Chain length: {chain_length}')
    chain_info.write(f'Length of each chain: {chain_length}\n')
    
    exps_in_chains = [None]*len(chains_and_log_posteriors)
    for i,chain_data in enumerate(chains_and_log_posteriors): # Consider skipping first few entries
        chain = chain_data['chain'][:int(chain_length/2)]
        log_posteriors = chain_data['log_posteriors'][:int(chain_length/2)]
        exp_lp_pairs = list(zip(chain,log_posteriors))

        exps_in_chains[i] = set(map(to_tuple, chain))

        print(sorted(log_posteriors, reverse=True))

        lps_to_exps = defaultdict(set)
        for exp,lp in exp_lp_pairs:
            lps_to_exps[lp].add(to_tuple(exp))

        num_exps_in_chain = len(exps_in_chains[i])

        print(lps_to_exps.keys())
        print('\n')

        chain_info.write(f'Num. expressions in chain {i}: {num_exps_in_chain}\n')
        decreasing_lps = sorted(lps_to_exps.keys(), reverse=True)
        chain_info.write("Expressions by decreasing log posterior\n")
        for lp in decreasing_lps:
            chain_info.write(f'lp = {lp} [{len(lps_to_exps[lp])} exps]:\n')
            for exp in lps_to_exps[lp]:
                chain_info.write(f'    {exp}\n')
            chain_info.write('\n')
        chain_info.write('\n')

    all_exps = set(itertools.chain(*exps_in_chains))
    chain_info.write(f'Total num. distinct exps across all chains (including warm-up): {len(all_exps)}\n')

    with open("params.yaml", 'r') as fd:
        params = yaml.safe_load(fd)
    true_norm_exp = params['true_norm']['exp']
    true_norm_tuple = to_tuple(true_norm_exp)
    
    chain_info.write(f'True norm in some chain(s): {true_norm_tuple in all_exps}\n')

    num_chains_in_to_exps = defaultdict(set)
    for exp in all_exps:
        num_chains_in = operator.countOf(map(operator.contains, 
                                                exps_in_chains,
                                                (exp for _ in range(len(exps_in_chains)))
                                            ),
                                        True)
        num_chains_in_to_exps[num_chains_in].add(exp)
    for num in sorted(num_chains_in_to_exps.keys(), reverse=True):
        chain_info.write(f'Out of {len(exps_in_chains)} chains ...\n')
        chain_info.write(f'{len(num_chains_in_to_exps[num])} exps are in {num} chains.\n')

    