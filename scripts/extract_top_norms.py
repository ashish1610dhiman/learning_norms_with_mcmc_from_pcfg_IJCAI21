import sys
sys.path.append('src')

import yaml
from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.environment import position
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.algorithm_1_v4 import to_tuple
from mcmc_norm_learning.mcmc_performance import performance
from collections import Counter
import operator
import pickle
import pickle_wrapper
import pandas as pd
import ast

with open("params.yaml", 'r') as fd:
    params = yaml.safe_load(fd)

colour_specific = params['colour_specific']
shape_specific = params['shape_specific']
target_area_parts = params['target_area'].replace(' ','').split(';')
target_area_part0 = position(*map(float, target_area_parts[0].split(',')))
target_area_part1 = position(*map(float, target_area_parts[1].split(',')))
target_area = (target_area_part0, target_area_part1)
the_task = task(colour_specific, shape_specific,target_area)
true_expression = params['true_norm']['exp']

posterior_sample = unpickle('data/posterior.pickle')
learned_expressions=Counter(map(to_tuple, posterior_sample))
n = 20
top_norms_with_freq = learned_expressions.most_common(n)
top_norms = list(map(operator.itemgetter(0), top_norms_with_freq))
pickle_it(top_norms, 'data/top_norms.pickle')

env = unpickle('data/env.pickle')

exp_posterior_df = pd.read_csv('metrics/chain_posteriors.csv', usecols=['expression','log_posterior'])
exp_posterior_df = exp_posterior_df.drop_duplicates()
exp_posterior_df['post_rank'] = exp_posterior_df['log_posterior'].rank(method='dense',ascending=False)
exp_posterior_df.sort_values('post_rank', inplace=True)
exp_posterior_df['expression'] = exp_posterior_df['expression'].transform(ast.literal_eval)
exp_posterior_df['expression'] = exp_posterior_df['expression'].transform(to_tuple)

def log_posterior(exp, exp_lp_df):
    return exp_lp_df.loc[exp_lp_df['expression'] == exp]['log_posterior'].iloc[0]

with open('metrics/precision_recall.txt', 'w') as f:
    f.write("Number of unique Norms in sequence={len(learned_expressions)}\n")
    f.write(f"Top {n} norms:\n")
    for expression,freq in top_norms_with_freq:
        f.write(f"Freq. {freq}, lp {log_posterior(expression, exp_posterior_df)}: ")
        f.write(f"{expression}\n")
    f.write("\n")

# Calculate precision and recall of top_n norms from learned expressions
pr_result=performance(the_task,env,true_expression,learned_expressions,
                        folder_name="temp",file_name="top_norm",
                        top_n=n,beta=1,repeat=50000,verbose=False)

with open('metrics/precision_recall.txt', 'a') as f:
    f.write(pr_result.to_string())

