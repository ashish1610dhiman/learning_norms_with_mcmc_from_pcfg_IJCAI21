# -*- coding: utf-8 -*-
"""
Created on Fri May 24 17:00:04 2019

@author: dhias426
"""

from environment import *
from actions import *
from robot_task_2 import *
from rules_1_1 import print_rule

import matplotlib.pyplot as plt
import numpy as np
import pickle
from copy import deepcopy




with open ('rules.txt', 'rb') as fp:
    rules = pickle.load(fp)



env=create_env()
env_copy=deepcopy(env)
fig,ax=plt.subplots(figsize=(14,9))
plot_env(env,ax)
plot_area(ax,target_area)
plt.legend(["Target Area"])



fig,ax=plt.subplots(figsize=(14,9))
plot_env(env,ax)
target_area=[position(0.5,-0.75),position(1.0,0.45)]
destination_area=[position(-0.1,0.4),position(0.7,1)]
plot_area(ax,target_area,destination_area)
plt.legend(["Target Area","Destination Area"]);



task_2=task("move",["r","b"],["triangle","circle"],target_area,destination_area)
my_robot=robot(task_2,env)
df=my_robot.make_permutations([],2)
fig,ax=plt.subplots(figsize=(14,9))
plot_env(env,ax)
plot_area(ax,target_area,destination_area)
plt.legend(["Target Area","Destination Area"]);