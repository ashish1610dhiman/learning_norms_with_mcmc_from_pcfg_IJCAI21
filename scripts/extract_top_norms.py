import sys
sys.path.append('src')

import yaml
from pickle_wrapper import unpickle, pickle_it
from mcmc_norm_learning.environment import position
from mcmc_norm_learning.robot_task_new import task
from mcmc_norm_learning.algorithm_1_v4 import to_tuple
from mcmc_norm_learning.mcmc_performance import performance
from collections import Counter

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

def calc_precision_and_recall(posterior_sample, env, task1, true_expression, repeat=10000):
    learned_expressions=Counter(map(to_tuple, posterior_sample))
    info = f"Number of unique Norms in sequence={len(learned_expressions)}"
    n = 829 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! <<<<<<<<<<< Change back to smaller number !!!! ****
    info += f"Top {n} norms:\n"
    for freq,expression in learned_expressions.most_common(n):
        info += f"Freq. {freq}"
        info += f"{expression}\n"
    # Calculate precision and recall of top_n norms from learned expressions
    pr_result=performance(task1,env,true_expression,learned_expressions,
                          folder_name="temp",file_name="top_norm",
                          top_n=n,beta=1,repeat=repeat,verbose=False)
    #pr_result.head()
    return pr_result, info

posterior_sample = unpickle('data/posterior.pickle')
env = unpickle('data/env.pickle')
pr_result, info = calc_precision_and_recall(posterior_sample, env, the_task, true_expression)
with open('metrics/precision_recall.txt', 'w') as f:
    f.write(info)
    f.write("\n")
    f.write(pr_result.to_string())