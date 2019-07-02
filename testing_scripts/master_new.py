# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:16:26 2019

@author: dhias426
"""

from environment import *
from rules_3 import *
from robot_task_new import *
from copy import deepcopy
from numpy import nan
import matplotlib.pyplot as plt

env=create_env(N=30)
env_copy=deepcopy(env)

#fig,ax=plt.subplots(1, 2, sharex=True, sharey=True,figsize=(14,10))
fig,ax=plt.subplots(figsize=(8,6))
plot_env(env,ax,legend=True)

rules=expand("NORMS")
for i in [1,2]:
    print_rule(rules[i],i)
    
    
target_area=[position(-1,-0.9),position(-0.4,-0.2)]
task1=task(colour_specific=np.nan,shape_specific=np.nan,target_area=target_area)
fig,ax=plt.subplots(figsize=(8,6))
plot_task(env,ax,"Clearing the area",task1,True)

name="wo_rules"
env_copy=deepcopy(env)
fig,ax=plt.subplots(1, 2, sharex=True, sharey=True,figsize=(14,10))
plot_task(env_copy,ax[0],"Before clearing (w/o rules)",task1,True)
ap1=robot(task1,env_copy).perform_task([],name)
plot_task(env_copy,ax[1],"After clearing (w/o rules)",task1,True)
plt.savefig("./permutations/{}.jpeg".format(name))
plt.close()


name="with_rules"
env_copy=deepcopy(env)
fig,ax=plt.subplots(1, 2, sharex=True, sharey=True,figsize=(14,10))
plot_task(env_copy,ax[0],"Before clearing (with rules)",task1,True)
ap2=robot(task1,env_copy).perform_task(rules,name)
plot_task(env_copy,ax[1],"After clearing (with rules)",task1,True)
plt.savefig("./permutations/{}.jpeg".format(name))
plt.close()

""" ALgorithm 2 testing""""
#fig,ax=plt.subplots(1, 2, sharex=True, sharey=True,figsize=(14,10))
env=create_env(N=30)
env_copy=deepcopy(env)
target_area=[position(-1,-0.9),position(-0.4,-0.2)]
task1=task(colour_specific=np.nan,shape_specific=np.nan,target_area=target_area)
fig,ax=plt.subplots(figsize=(8,6))
plot_task(env,ax,"Clearing the area",task1,True)
norms=expand("NORMS")
print_expression(norms)

