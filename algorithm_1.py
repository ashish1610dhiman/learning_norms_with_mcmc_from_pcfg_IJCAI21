# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:38:10 2019

@author: dhias426
"""
from rules_3 import *
from environment import *
from robot_task_new import *
from copy import deepcopy
from numpy import nan,random
import matplotlib.pyplot as plt
from collections import Counter

def to_tuple(expression):
    """ Converts a nested list to nested tuple """
    my_tup=tuple()
    for elem in expression:
        if type(elem)!=list:
            my_tup=my_tup+tuple([elem])
        else:
            my_tup=my_tup+tuple([to_tuple(elem)])
    return (my_tup)


def algorithm_1(data,env,q_dict,rule_dict,filename="mcmc_reort",max_iterations=1000000):
    """ Implementation of algorithm 1 given in Bayesian Synthesis paper """
    from algorithm_2_utilities import Likelihood
    from algorithm_2 import generate_new_expression
    from rules_3 import expand,print_expression
    import sys
    import os.path
    #Generate E0
    E_0=expand("NORMS")
    while(True):
        if Likelihood(E_0,data,env)>0:
            break
        else:
            #print(Likelihood(E_0,data,env))
            E_0=expand("NORMS")
    print ("E0 chosen is:")
    print_expression(E_0)
    sequence=[E_0]
    lik_list=[]
    lik_list.append(Likelihood(sequence[-1],data,env))
    original = sys.stdout
    exists = os.path.isfile('./{}.txt'.format(filename))
    if exists==True:
        os.remove('./{}.txt'.format(filename))
    for i in range(1,max_iterations+1):
        print ("\n--------------Iteration={}--------------".format(i))
        sys.stdout = open('./{}.txt'.format(filename), 'a+')
        print ("\n--------------Iteration={}--------------".format(i))
        print_expression(sequence[-1])
        lik_list.append(Likelihood(sequence[-1],data,env))
        sequence.append(generate_new_expression(sequence[-1],data,q_dict,rule_dict,env))
        print ("----------------------------------------")
        sys.stdout=original
    return (sequence,lik_list)
    

env=create_env(N=30)
sns.set_style("white")
fig,ax=plt.subplots(figsize=(8,6))
plot_env(env,ax,legend=True)

data=[]
for i in range(100):
    z=random.choice([1,2,3],p=[0.45,0.5,0.05])
    o=random.choice([2,5,12,18,15])
    data.append((("pickup",o),("putdown",o,z)))
    


from algorithm_2_utilities import violation

E_0=expand("NORMS")
print_expression(E_0)
v=violation(E_0,env)



exp_seq,lik_list=algorithm_1(data,env,q_dict,rule_dict,filename="mcmc_report4",max_iterations=50000)
print ("Order of Improvement in Likelihood={:.2E}".format(max(lik_list)/min(lik_list)))

learned_norms=Counter(map(to_tuple,exp_seq))
t=sum(learned_norms.values())

top=learned_norms.most_common()[:50]
exists = os.path.isfile('./top_norms.txt')
if exists==True:
    os.remove('./top_norms.txt')
original = sys.stdout
for i in range(len(top)):
    exp=top[i]
    print("Rank:{} Norm has relative frequency={:.3f}%".format(i+1,exp[1]*100/t))
    sys.stdout = open('./top_norms.txt', 'a+')
    print("\n\n\n************Rank:{}, %-Frequency={:.3f}%**********".format(i+1,exp[1]*100/t))
    print_expression(exp[0])
    print("*************************************************")
    sys.stdout=original


import seaborn as sns
sns.set_style("darkgrid")
#sns.relplot(x="Different Norms", y="Frequency", kind="line", data=learned_norms)
fig,ax=plt.subplots(figsize=(8,6))
plt.plot(sorted(learned_norms.values()),"o-",c=(250/255,93/255,130/255,0.7),markerfacecolor=(250/255,18/255,72/255,0.77))
plt.ylabel("Frequency in sample of size={}".format(t))
plt.xlabel("Index of Norms from a total of {} Norms".format(len(learned_norms)))
plt.title("Frequency of Norms")
