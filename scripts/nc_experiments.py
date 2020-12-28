"""
# Created by ashish1610dhiman at 28/12/20
Contact at ashish1610dhiman@gmail.com
"""

import sys
from pathlib import Path

script_path = Path(__file__)
bas_dir = script_path.parent.parent
sys.path.append('{}/src'.format(bas_dir))

import os
import csv
import yaml
import tqdm
import math
import pickle
import numpy as np
import pandas as pd
import itertools
import operator
from pathlib import Path
import argparse
from operator import concat, itemgetter
import matplotlib.pyplot as plt
import dask
from joblib import Parallel, delayed
from dask.distributed import Client
from collections import defaultdict
from functools import reduce
from operator import concat, itemgetter
import ast

from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.algorithm_1_v4 import to_tuple
from mcmc_norm_learning.algorithm_1_v4 import create_data
from mcmc_norm_learning.rules_4 import get_prob, get_log_prob
from mcmc_norm_learning.environment import position, plot_env
from mcmc_norm_learning.robot_task_new import task, robot, plot_task
from mcmc_norm_learning.algorithm_1_v4 import algorithm_1, over_dispersed_starting_points
from mcmc_norm_learning.mcmc_convergence import prepare_sequences, calculate_R
from mcmc_norm_learning.rules_4 import q_dict, rule_dict, get_log_prob
from algorithm_2_utilities import Likelihood
from mcmc_norm_learning.mcmc_performance import performance
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('-exp', metavar='exp_no', type=str, nargs='+', help='Experiment directory', default="exp0")
parser.add_argument('-w_nc', metavar='w_nc', type=int, nargs='+', help='w non-compliance', default=None)

exp_no = parser.parse_args().exp
w_nc = parser.parse_args().w_nc

output_dir = f"{bas_dir}/data_nc/{exp_no}/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(f"{bas_dir}/params_nc.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

""" Step 1: Default Environment and params"""

##Get default env
env = unpickle(f'{bas_dir}/data/env.pickle')

##Get default task
true_norm_exp = params['true_norm']['exp']
num_observations = params['num_observations']
obs_data_set = params['obs_data_set']

if w_nc == None:
    w_nc = params["w_nc"]
n = params['n']
m = params['m']
rf = params['rf']
rhat_step_size = params['rhat_step_size']
top_n = params["top_norms_n"]

colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area_parts = params['target_area'].replace(' ', '').split(';')
target_area_part0 = position(*map(float, target_area_parts[0].split(',')))
target_area_part1 = position(*map(float, target_area_parts[1].split(',')))
target_area = (target_area_part0, target_area_part1)
print(target_area_part0.coordinates())
print(target_area_part1.coordinates())
the_task = task(colour_specific, shape_specific, target_area)

fig, axs = plt.subplots(1, 2, figsize=(9, 4), dpi=100);
plot_task(env, axs[0], "Initial Task State", the_task, True)
axs[1].text(0, 0.5, "\n".join([str(x) for x in true_norm_exp]), wrap=True)
axs[1].axis("off")
axs[1].title.set_text("True Norm")
plt.savefig(f"{output_dir}/nc_hist.jpg")
plt.close()

""" Step 2: Gen Observations """

obs = nc_obs = create_data(true_norm_exp, env, name=None, task=the_task, random_task=False,
                           num_actionable=np.nan, num_repeat=num_observations, w_nc=w_nc, verbose=False)
true_norm_prior = get_prob("NORMS", true_norm_exp)
true_norm_log_prior = get_log_prob("NORMS", true_norm_exp)
print(f"For True Norm, prior={true_norm_prior}, log_prior={true_norm_log_prior}")

""" Step 3: Gen MCMC chains """

num_chains = math.ceil(m / 2)
starts, info = over_dispersed_starting_points(num_chains, obs, env, \
                                              the_task, time_threshold=math.inf, w_normative=(1 - w_nc))

with open(f'{output_dir}/starts_info_nc.txt', 'w') as chain_info:
    chain_info.write(info)


@dask.delayed
def delayed_alg1(obs, env, the_task, q_dict, rule_dict, start, rf, max_iters, w_nc):
    exp_seq, log_likelihoods = algorithm_1(obs, env, the_task, q_dict, rule_dict,
                                           "dummy value", start=start, relevance_factor=rf, \
                                           max_iterations=max_iters, w_normative=1 - w_nc, verbose=False)
    log_posteriors = [None] * len(exp_seq)
    for i in range(len(exp_seq)):
        exp = exp_seq[i]
        ll = log_likelihoods[i]
        log_prior = get_log_prob("NORMS", exp)  # Note: this imports the rules dict from rules_4.py
        log_posteriors[i] = log_prior + ll
    return {'chain': exp_seq, 'log_posteriors': log_posteriors}


def delayed_alg1_joblib(start_i):
    alg1_result = delayed_alg1(obs=obs, env=env, the_task=the_task, q_dict=q_dict, \
                               rule_dict=rule_dict, start=start_i, rf=rf, \
                               max_iters=4 * n, w_nc=w_nc).compute()
    return (alg1_result)


chains_and_log_posteriors = []
chains_and_log_posteriors = Parallel(verbose=2, n_jobs=-1 \
                                     )(delayed(delayed_alg1_joblib)(starts[run]) \
                                       for run in tqdm.tqdm(range(num_chains), desc="Loop for Individual Chains"))

pickle_it(chains_and_log_posteriors, f'{output_dir}/chains_and_log_posteriors.pickle')

""" Step 4: Pass to analyse chains """

with open(f'{output_dir}/chain_posteriors_nc.csv', 'w', newline='') as csvfile, \
        open(f'{output_dir}/chain_info.txt', 'w') as chain_info:
    chain_info.write(f'Number of chains: {len(chains_and_log_posteriors)}\n')
    chain_info.write(f'Length of each chain: {len(chains_and_log_posteriors[0]["chain"])}\n')

    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(('chain_number', 'chain_pos', 'expression', 'log_posterior'))
    exps_in_chains = [None] * len(chains_and_log_posteriors)
    for i, chain_data in enumerate(chains_and_log_posteriors):  # Consider skipping first few entries
        chain = chain_data['chain']
        log_posteriors = chain_data['log_posteriors']
        exp_lp_pairs = list(zip(chain, log_posteriors))

        exps_in_chains[i] = set(map(to_tuple, chain))

        # print(sorted(log_posteriors, reverse=True))

        lps_to_exps = defaultdict(set)
        for exp, lp in exp_lp_pairs:
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

        changed_exp_indices = [i for i in range(1, len(chain)) if chain[i] != chain[i - 1]]
        print(f'Writing {len(exp_lp_pairs)} rows to CSV file\n')
        csv_writer.writerows(
            ((i, j, chain_lp_pair[0], chain_lp_pair[1]) for j, chain_lp_pair in enumerate(exp_lp_pairs)))

    all_exps = set(itertools.chain(*exps_in_chains))
    chain_info.write(f'Total num. distinct exps across all chains (including warm-up): {len(all_exps)}\n')

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
csvfile.close()
chain_info.close()

result = pd.read_csv(f"{output_dir}/chain_posteriors_nc.csv")

log_post_no_norm = Likelihood(["Norms", ["No-Norm"]], the_task, obs, env, w_normative=1 - w_nc)
log_post_true_norm = Likelihood(true_norm_exp, the_task, obs, env, w_normative=1 - w_nc)

print(f"log_post_no_norm={log_post_no_norm},log_post_true_norm={log_post_true_norm}")

print(result.groupby("chain_number")[["log_posterior"]].agg(['min', 'max', 'mean', 'std']))

hist_plot = result['log_posterior'].hist(by=result['chain_number'], bins=10)
plt.savefig(f"{output_dir}/nc_hist.jpg")
plt.close()

grouped = result.groupby('chain_number')[["log_posterior"]]
ncols = 2
nrows = int(np.ceil(grouped.ngroups / ncols))
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 5 * nrows), sharey=False)
for (key, ax) in zip(grouped.groups.keys(), axes.flatten()):
    grouped.get_group(key).plot(ax=ax)
    ax.axhline(y=log_post_no_norm, label="No Norm", c='r')
    ax.axhline(y=log_post_true_norm, label="True Norm", c='g')
    ax.title.set_text("For chain={}".format(key))
    ax.legend()
plt.savefig(f"{output_dir}/cnc_movement.jpg")
plt.close()


""" Step 5: Convergence Tests """

def conv_test(chains):
    convergence_result, split_data = calculate_R(chains, rhat_step_size)
    with open(f'{output_dir}/conv_test_nc.txt', 'w') as f:
        f.write(convergence_result.to_string())
    return reduce(concat, split_data)


chains = list(map(itemgetter('chain'), chains_and_log_posteriors))
posterior_sample = conv_test(prepare_sequences(chains, warmup=True))
pickle_it(posterior_sample, f'{output_dir}/posterior_nc.pickle')

""" Step 6: Extract Top Norms """

learned_expressions=Counter(map(to_tuple, posterior_sample))

top_norms_with_freq = learned_expressions.most_common(top_n)
top_norms = list(map(operator.itemgetter(0), top_norms_with_freq))

exp_posterior_df = pd.read_csv(f'{output_dir}/chain_posteriors_nc.csv', usecols=['expression','log_posterior'])
exp_posterior_df = exp_posterior_df.drop_duplicates()
exp_posterior_df['post_rank'] = exp_posterior_df['log_posterior'].rank(method='dense',ascending=False)
exp_posterior_df.sort_values('post_rank', inplace=True)
exp_posterior_df['expression'] = exp_posterior_df['expression'].transform(ast.literal_eval)
exp_posterior_df['expression'] = exp_posterior_df['expression'].transform(to_tuple)

print(exp_posterior_df)

def log_posterior(exp, exp_lp_df):
    return exp_lp_df.loc[exp_lp_df['expression'] == exp]['log_posterior'].iloc[0]


with open(f'{output_dir}/precision_recall_nc.txt', 'w') as f:
    f.write(f"Number of unique Norms in sequence={len(learned_expressions)}\n")
    f.write(f"Top {top_norms} norms:\n")
    for expression,freq in top_norms_with_freq:
        f.write(f"Freq. {freq}, lp {log_posterior(expression, exp_posterior_df)}: ")
        f.write(f"{expression}\n")
    f.write("\n")


# pr_result=performance(the_task,env,true_norm_exp,learned_expressions,
#                         folder_name="temp",file_name="top_norm",
#                         top_n=n,beta=1,repeat=100000,verbose=False)
