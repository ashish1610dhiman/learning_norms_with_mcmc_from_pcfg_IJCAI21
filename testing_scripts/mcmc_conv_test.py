# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:28:44 2019

@author: dhias426
"""

from environment import *
from rules_3 import *
from robot_task_new import *
from algorithm_1 import create_data

from copy import deepcopy
from numpy import nan
import matplotlib.pyplot as plt

env=create_env(N=30)
expression=expand("NORMS")
print_expression(expression)

target_area=[position(-0.25,-1),position(0.25,-0.4)]
task1=task(colour_specific=['g','b'],shape_specific='square',target_area=target_area)
fig,ax=plt.subplots(figsize=(8,6))
plot_task(env,ax,"Clearing the area",task1,True)

action_profile_with_norms=create_data(task1,expression,env,"with_norms",num_repeat=500)

data_with_norms=[]
for itr,ap in action_profile_with_norms.items():
    for i in range(0,int(len(ap)/2)):
        data_with_norms.append(tuple([ap[i],ap[i+1]]))
print ("Data with norms")
print(data_with_norms[0:5])

from algorithm_1 import algorithm_1,to_tuple

import seaborn as sns
from collections import Counter
import os
import sys

print ("Generating sequence for data with norms")
exp_seq_with,lik_list_with=algorithm_1(data_with_norms,env,q_dict,rule_dict,filename="mcmc_test/mcmc_report_with_norms",max_iterations=50000)
