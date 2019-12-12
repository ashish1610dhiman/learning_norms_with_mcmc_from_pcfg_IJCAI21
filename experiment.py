from environment import *
from rules_4 import *
from robot_task_new import *
from algorithm_1_v4 import create_data,algorithm_1,to_tuple
from mcmc_performance import performance
from mcmc_convergence import prepare_sequences,calculate_R
#import matplotlib.pyplot as plt
from collections import Counter
import pickle
import time
#import seaborn as sns
import os
import sys
from tqdm import tnrange, tqdm_notebook
from functools import reduce
from operator import concat
from rules_4 import q_dict, rule_dict

def gen_data_for_conv_test(data, env, task1):
    n=500 #Length of sequence after discarding warm-up part and splitting in half
    m=10 #Number of sequences after splitting in half
    rf=0.6

    chains=[]
    for i in tnrange(1,int(m/2+1),desc="Loop for Individual Chains"):
        print ("\n:::::::::::::::::::: FOR SEQUENCE {} ::::::::::::::::::::".format(i))
        exp_seq,lik_list = algorithm_1(data,env,task1,q_dict,rule_dict,
                                      "demo/convergence/report_for_chain_{}_x".format(i),
                                      relevance_factor=rf,max_iterations=4*n,verbose=False)
        chains.append(exp_seq)
    pickle_it(sequence_list, './experiment/sequence_list.sv')
    return chains

def conv_test(chains):
    convergence_result,split_data = calculate_R(chains,50)
    print(convergence_result)
    return reduce(concat, split_data)

def unpickle(path):
    with open(path, 'rb') as fp:
        result = pickle.load(fp)
        print("Unpickled 1st element for '{}' is {}\n".format(path, result[0]))
        return result

def pickle_it(x, path):
    with open(path, 'wb') as fp:
        pickle.dump(x, fp)
     
def calc_precision_and_recall(posterior_sample, env, task1, true_expression, repeat=10000):
    learned_expressions=Counter(map(to_tuple, posterior_sample))
    print("Number of unique Norms in sequence={}".format(len(learned_expressions)))
    print("Top 5 norms:")
    for freq,expression in learned_expressions.most_common(5):
        print("Freq. {}".format(freq))
        print(expression,"\n")
    # Calculate precision and recall of top_n norms from learned expressions
    pr_result=performance(task1,env,true_expression,learned_expressions,
                          folder_name=None,file_name="top_norm",
                          top_n=5,beta=1,repeat=repeat,verbose=False)
    pr_result.head()

def read_scenario():
    true_expression = unpickle('./demo/demo_exp.sv')
    env = unpickle('./demo/demo_env.sv')
    target_area=[position(-0.8,0.7),position(0.25,0.99)]
    task1 = task(colour_specific=env[1],shape_specific=env[2],target_area=target_area)
    return env,task1,true_expression

def read_observations():
    return(unpickle('./demo/demo_data.sv'))
    
if __name__ == "__main__":
    env,task1,true_expression = read_scenario()
    if sys.argv[1] == "pr":
        posterior_sample = unpickle('./experiment/posterior_sample.sv')
        calc_precision_and_recall(posterior_sample, env, task1, true_expression)
    elif sys.argv[1] == "convtest":
        if os.path.exists('./experiment/sequence_list.sv'):
            chains = unpickle('./experiment/sequence_list.sv')
        else:
            chains = gen_data_for_conv_test(data, env, task1)
        posterior_sample = conv_test(prepare_sequences(chains, warmup=True))
        pickle_it(posterior_sample, './experiment/posterior_sample.sv')
    else:
        print("Invalid argument")
        print(rule_dict)
