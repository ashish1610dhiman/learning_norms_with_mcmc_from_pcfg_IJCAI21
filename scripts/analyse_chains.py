import sys
sys.path.append('src')

from pickle_wrapper import unpickle, pickle_it
import csv
from mcmc_norm_learning.mcmc_convergence import prepare_sequences
from mcmc_norm_learning.algorithm_1_v4 import to_tuple
from collections import defaultdict
import itertools
import operator
import yaml

# discard warmup and split remaining halves
#posterior_sample = prepare_sequences(chains, warmup=True)

chains_and_log_likelihoods = unpickle('data/chains_and_log_likelihoods.pickle')

with open('metrics/chain_likelihoods.csv', 'w', newline='') as csvfile, \
     open('metrics/chain_info.txt', 'w') as chain_info:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(('chain_number', 'chain_pos', 'expression', 'log_likelihood'))
    exps_in_chains = [None]*len(chains_and_log_likelihoods)
    for i,chain_data in enumerate(chains_and_log_likelihoods): # Consider skipping first few entries
        chain = chain_data['chain']
        log_likelihoods = chain_data['log_likelihoods']
        chain_ll_pairs = list(zip(chain,log_likelihoods))

        exps_in_chains[i] = set(map(to_tuple, chain))

        print(sorted(log_likelihoods, reverse=True))

        lls_to_exps = defaultdict(set)
        for exp,ll in chain_ll_pairs:
            lls_to_exps[ll].add(to_tuple(exp))

        num_exps_in_chain = len(exps_in_chains[i])

        print(lls_to_exps.keys())
        print('\n')

        chain_info.write(f'Num. expressions in chain {i}: {num_exps_in_chain}\n')
        decreasing_lls = sorted(lls_to_exps.keys(), reverse=True)
        chain_info.write("Expressions by decreasing log likelihood\n")
        for ll in decreasing_lls:
            chain_info.write(f'll = {ll} [{len(lls_to_exps[ll])} exps]:\n')
            for exp in lls_to_exps[ll]:
                chain_info.write(f'    {exp}\n')
            chain_info.write('\n')
        chain_info.write('\n')

        changed_exp_indices = [i for i in range(1,len(chain)) if chain[i] != chain[i-1]]
        print(f'Writing {len(chain_ll_pairs)} rows to CSV file\n')
        csv_writer.writerows(((i,j,chain_ll_pair[0],chain_ll_pair[1]) for j,chain_ll_pair in enumerate(chain_ll_pairs)))

    all_exps = set(itertools.chain(*exps_in_chains))
    chain_info.write(f'Total num. distinct exps across all chains: {len(all_exps)}\n')

    with open("params.yaml", 'r') as fd:
        params = yaml.safe_load(fd)
    true_norm_exp = params['true_norm']['exp']
    true_norm_tuple = to_tuple(true_norm_exp)
    
    chain_info.write(f'True norm in tuple: {true_norm_tuple in all_exps}\n')

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

    