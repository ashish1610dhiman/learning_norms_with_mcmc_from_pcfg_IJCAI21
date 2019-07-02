# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:16:30 2019

@author: dhias426
"""
from environment import *
from actions import *
from robot_task_3 import *
from rules_3 import print_rule,expand
from combine_subtask import aggregate

import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations
import pickle
from copy import deepcopy


with open ('my_rules.txt', 'rb') as fp:
    rules = pickle.load(fp)
    
env=create_env(N=25,seed=25)
env_copy_super=deepcopy(env)
# For Pickup Subtask
target_area_p=[position(-0.3,-0.3),position(0.3,0.3)]
sub_task_p=task("pickup",["g","b"],np.nan,target_area_p,np.nan)

# For Move Subtask
target_area_m=[position(-0.5,0),position(0.2,1)]
destination_area_m=[position(-1,0.4),position(-0.7,1)]
sub_task_m=task("move",["r","b"],["triangle","circle"],target_area_m,destination_area_m)

# For Throw Subtask
target_area_t=[position(-0.9,0.25),position(-0.1,0.9)]
sub_task_t=task("throw",np.nan,["square","circle"],target_area_t,np.nan)
#Create a dict of tasks and visualise them
task_dict={"p":sub_task_p,"m":sub_task_m,"t":sub_task_t}
possible_orders=list(permutations(task_dict.keys())) #possible order of completing a task;
order_plans={}
for order in possible_orders:
    env_copy=deepcopy(env)
    print ("\nThe chosen order is:",order)
    sub_task_plans={}
    for i,subtask_key in enumerate(order,1):
        print ("Subtask={}".format(i))
        task_dict[subtask_key].print_task()
        fig,ax=plt.subplots(1, 2, sharex=True, sharey=True,figsize=(14,10))
        plot_task(env_copy,ax[0],"For:{}\nBefore the Sub-Task_{}".format(order,i),task_dict[subtask_key])
        sub_task_plans[i]=robot(task_dict[subtask_key],env_copy).make_permutations(rules,i,"C/{}_{}_{}".format(order[0],order[1],order[2]))
        plot_task(env_copy,ax[1],"For:{}\nAfter the Sub-Task_{}".format(order,i),task_dict[subtask_key])
        plt.savefig("./permutations/C/{}_{}_{}/subtask_{}_effect.jpeg".format(order[0],order[1],order[2],i))
        plt.close()
    order_plans[order]=sub_task_plans
    
#Aggregate action plans for individual subtasks for each order
B={}
m1=0
for order in possible_orders:
    order_plan=order_plans[order]
    B[order]=aggregate("C/{}_{}_{}".format(order[0],order[1],order[2]),order_plan)
    m1+=B[order].shape[1]