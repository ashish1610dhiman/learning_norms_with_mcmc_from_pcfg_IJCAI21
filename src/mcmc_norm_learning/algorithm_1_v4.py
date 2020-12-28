# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:38:10 2019

@author: dhias426
"""
from rules_4 import *
from copy import deepcopy
import numpy as np
from numpy import nan,exp,random,isnan
from algorithm_2_utilities import Likelihood
from algorithm_2_v2 import generate_new_expression
from mcmc_convergence import calculate_variance
from mcmc_convergence_utilities import create_vector
from robot_task_new import robot,plot_task
#from relevance import is_relevant
import sys
import os.path
import time
import math
from tqdm import tqdm, tnrange, tqdm_notebook
import os,glob,random
from collections import Counter, defaultdict
import dask
from dask.distributed import Client

def to_tuple(expression):
    """ Convert nested list to nested tuple """
    my_tup=tuple()
    for elem in expression:
        if type(elem)!=list:
            my_tup=my_tup+tuple([elem])
        else:
            my_tup=my_tup+tuple([to_tuple(elem)])
    return (my_tup)


def random_task_func(env,num_actionable,c1,s1):
    """ Generate random task on environment """
    #num_actionable deifnes the number of objects in the target_area
    from robot_task_new import task,robot
    from environment import position
    from random import uniform
    while(True):
        (a,b)=(uniform(-1,1),uniform(-1,1))
        (c,d)=(uniform(a,1),uniform(b,1))
        target_area=[position(a,b),position(c,d)]
        task1=task(colour_specific=c1,shape_specific=s1,target_area=target_area)
        actionable=len(robot(task1,deepcopy(env)).all_actionable())
        if actionable>0:
            if np.isnan(num_actionable):
                break
            elif num_actionable==actionable:
                break
    return (task1)

def create_data(expression,env,name=None,task=np.nan,random_task=False,limit_task_scope=False,
	num_actionable=np.nan,num_repeat=500,w_nc=0.0,verbose=True):
    """ Function to create data from either given task or randomised tasks """
    #print ("Generating action-profile data for case {}".format(name))
    action_profile={}
    #Empty the required directories
    if name != None:
        import matplotlib.pyplot as plt
        for folder in ["action_profiles","env_states"]:
            for f in glob.glob("./{}/{}/*".format(name,folder)):
                os.chmod(f, 0o777)
                os.remove(f)
    #for itr in tnrange(num_repeat,desc="Repetition of Task"):
    for itr in tqdm(range(num_repeat),desc="Repetition of Task"):
        #time.sleep(0.01) # WHY IS THIS HERE?
        env_copy=deepcopy(env)
        if name != None:
            fig,ax=plt.subplots(1, 2, sharex=True, sharey=True,figsize=(14,10))
        #Generate random task with actionable objects specified (random if specidied np.nan)
        if random_task==True:
        	if limit_task_scope==True:
        		c=random.choice(env[1])
        		s=random.choice(env[2])
        	else:
        		c=np.nan
        		s=np.nan
        	task=random_task_func(env,num_actionable,c,s)
        if name != None:
            plot_task(env_copy,ax[0],"Before clearing ({})".format(name),task,True)
        if verbose==True:
            print ("For repetition={} of task".format(itr+1))
        action_profile[itr+1]=robot(task,env_copy,w_nc\
                                    ).perform_task(expression,"./{}/action_profiles/itr_{}".format(name,itr+1),\
                                                   verbose);
        if name != None:
            plot_task(env_copy,ax[1],"After clearing ({})".format(name),task,True)
            plt.savefig("./{}/env_states/itr_{}.png".format(name,itr+1))
            plt.close()
    return list(action_profile.values())

def gen_E0(data,env,task1,w_normative=1,time_threshold=1000,verbose=False):
    #Generate E0
    E_0=expand("NORMS")
    s=time.time()
    time_flag=0
    iterations = 0
    log_lik_null=Likelihood([],task1,data,env,w_normative)
    while((time.time()-s)<time_threshold):
        iterations += 1
        time_flag=1
        log_lik = Likelihood(E_0,task1,data,env,w_normative)
        if log_lik > log_lik_null:
        # if log_lik > log_lik_null:
            """ Compared to log(Lik(no_norm) because for large sequences exp(log_Lik) gets to zero"""
            """ >= be cause we do rejection sampling for relevant norms below """
            print(log_lik)
            break
            """ if isnan(relevance_factor):
                break
            else:
                if (is_relevant(E_0,task1,env)==False):
                    if (random.uniform()>relevance_factor):
                        break
                else:
                    if (random.uniform()<=relevance_factor):
                        break """
        else:
            if verbose:
                print(log_lik)
                print("Trying another E0")
            E_0=expand("NORMS")
            time_flag=0
    print("Time to initialise E_0={:.4f}s".format(time.time()-s))
    if time_flag==0:
        print ("Stopping Algorithm, Not able to initialise E_0 in given time_threshold")
        return (nan,nan)
    return (E_0, iterations)

def over_dispersed_starting_points(num_starts,data,env,task1,multiplier=10,w_normative=1,time_threshold=1000):
    n = multiplier*num_starts
    gen_E0_results = [dask.delayed(gen_E0)(data,env,task1,w_normative,time_threshold) for _ in range(n)]
    gen_E0_results = dask.compute(*gen_E0_results)
    unzipped = list(zip(*gen_E0_results))
    candidate_starts = unzipped[0]
    iterations_list = unzipped[1]
    avg_iterations = sum(iterations_list)/n
    start_vectors = list(map(create_vector,candidate_starts))
    vector_sum = sum(start_vectors,Counter())
    mean_vector = Counter({key:value/n for key,value in vector_sum.items()})
    # Rank start_vectors by dist. from mean
    start_dist_pairs = []
    for i in range(n):
        start = candidate_starts[i]
        svec = start_vectors[i]
        diff = svec.copy()
        diff.subtract(mean_vector)
        dist_squared = sum([value**2 for value in diff.values()])
        start_dist_pairs.append((dist_squared, start))
    start_dist_pairs.sort(key=lambda x: x[0], reverse=True)
    info = (
        f'Number of chains requested: {num_starts}\n'
        f'Number of candidate starts generated: {n}\n'
        f'Average iterations to find E0: {avg_iterations}\n'
        f'Distances of starts from mean: {[math.sqrt(pair[0]) for pair in start_dist_pairs]}\n'
    )
    return ([start for d,start in start_dist_pairs[:num_starts]], info)

def algorithm_1(data,env,task1,q_dict,rule_dict,filename="mcmc_report",start=None,sim_threshold=0,similarity_penalty=1,relevance_factor=0.5,time_threshold=1000,max_iterations=1000,w_normative=1,verbose=False,resume=None):  
    """ For testing algorithm v_2 also similarity factor included """
    if resume != None:
        sequence0, lik_list0 = resume
        sequence = list(sequence0)
        lik_list = list(lik_list0)
        E_0 = sequence[-1]
    elif start != None:
        E_0 = start
        sequence=[E_0]
        lik_list = [Likelihood(E_0,task1,data,env,w_normative)]
    else:
        E_0, E_0_iterations = gen_E0(data,env,task1,w_normative,time_threshold)
        if verbose:
            print (f"E0 chosen is (after {E_0_iterations}):")
            print_expression(E_0)
        sequence=[E_0]
        lik_list=[]
        #lik_list.append(exp(Likelihood(sequence[-1],task1,data,env,w_normative)))
        lik_list.append(Likelihood(sequence[-1],task1,data,env,w_normative))
    # original = sys.stdout
    # exists = os.path.isfile('./{}.txt'.format(filename))
    #if exists==True:
    #    os.remove('./{}.txt'.format(filename))
    log_lik_no_norm = Likelihood([],task1,data,env,w_normative)
    #for i in tnrange(1,max_iterations,desc="Length of Sequence"):
    for i in tqdm(range(1,max_iterations),desc="Length of Sequence"):
        if verbose:
            print ("\n--------------Iteration={}--------------".format(i))
        #sys.stdout = open('./{}.txt'.format(filename), 'a+')
        if verbose and i==1:
            print ("\n-----------E0 chosen is:---------------")
            print_expression(E_0)
            print ("----------------------------------------")
        #print ("\n\n===========================Iteration={}===========================".format(i))
        new_expression = generate_new_expression(sequence[-1],data,task1,q_dict,rule_dict,env,log_lik_no_norm,relevance_factor,sim_threshold,similarity_penalty,w_normative)
        sequence.append(new_expression)
        #print_expression(sequence[-1])
        #lik_list.append(exp(Likelihood(sequence[-1],task1,data,env,w_normative)))
        lik_list.append(Likelihood(sequence[-1],task1,data,env,w_normative))
        #print ("===================================================================")
        #sys.stdout=original
    return (sequence,lik_list)
    

# =============================================================================
# env=create_env(N=30)
# sns.set_style("white")
# fig,ax=plt.subplots(figsize=(8,6))
# plot_env(env,ax,legend=True)
# 
# data=[]
# for i in range(100):
#     z=random.choice([1,2,3],p=[0.45,0.5,0.05])
#     o=random.choice([2,5,12,18,15])
#     data.append((("pickup",o),("putdown",lik_ex_normative
#     
# 
# 
# from algorithm_2_utilities import violation
# 
# E_0=expand("NORMS")
# print_expression(E_0)
# v=violation(E_0,env)
# 
# 
# 
# exp_seq,lik_list=algorithm_1(data,env,q_dict,rule_dict,filename="mcmc_report4",max_iterations=50000)
# print ("Order of Improvement in Likelihood={:.2E}".format(max(lik_list)/min(lik_list)))
# 
# learned_norms=Counter(map(to_tuple,exp_seq))
# t=sum(learned_norms.values())
# 
# top=learned_norms.most_common()[:50]
# exists = os.path.isfile('./top_norms.txt')
# if exists==True:
#     os.remove('./top_norms.txt')
# original = sys.stdout
# for i in range(len(top)):
#     exp=top[i]
#     print("Rank:{} Norm has relative frequency={:.3f}%".format(i+1,exp[1]*100/t))
#     sys.stdout = open('./top_norms.txt', 'a+')
#     print("\n\n\n************Rank:{}, %-Frequency={:.3f}%**********".format(i+1,exp[1]*100/t))
#     print_expression(exp[0])
#     print("*************************************************")
#     sys.stdout=original
# 
# 
# imlik_ex_normativeeaborn as sns
# sns.set_style("darkgrid")
# #sns.relplot(x="Different Norms", y="Frequency", kind="line", data=learned_norms)
# fig,ax=plt.subplots(figsize=(8,6))
# plt.plot(sorted(learned_norms.values()),"o-",c=(250/255,93/255,130/255,0.7),markerfacecolor=(250/255,18/255,72/255,0.77))
# plt.ylabel("Frequency in sample of size={}".format(t))
# plt.xlabel("Index of Norms from a total of {} Norms".format(len(learned_norms)))
# plt.title("Frequency of Norms")
# 
# =============================================================================

if __name__ == '__main__':
    client = Client()