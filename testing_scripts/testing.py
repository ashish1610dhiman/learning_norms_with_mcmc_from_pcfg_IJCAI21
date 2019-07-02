# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:15:42 2019

@author: dhias426
"""

from environment import *
from rules_3 import *
from robot_task_new import *
from algorithm_1_v2 import create_data,algorithm_1,to_tuple
from mcmc_performance import performance
from algorithm_2_utilities import Likelihood
from algorithm_2 import generate_new_expression

import seaborn as sns
from collections import Counter
import os
import sys
from copy import deepcopy
from numpy import nan
import matplotlib.pyplot as plt
import time
import pickle

env=create_env(N=40)
fig,ax=plt.subplots(figsize=(8,6))
plot_env(env,ax,legend=True)

with open('my_env2.sv', 'wb') as fp:
    pickle.dump(env, fp)

true_expression=expand("NORMS")
print_expression(true_expression)

# =============================================================================
with open('my_env2.sv', 'wb') as fp:
    pickle.dump(env, fp)
    
with open('my_exp2.sv', 'wb') as fp:
    pickle.dump(true_expression, fp)
    
with open('my_data2.sv', 'wb') as fp:
    pickle.dump(data, fp)
    


 with open ('my_exp.sv', 'rb') as fp:
     true_expression = pickle.load(fp)
 
 with open ('my_env.sv', 'rb') as fp:
   env = pickle.load(fp)
   
with open('my_data.sv', 'rb') as fp:
   data = pickle.load(fp)    
# =============================================================================
    



target_area=[position(-0.25,-0.8),position(0.4,-0.35)]
task1=task(colour_specific=np.nan,shape_specific=np.nan,target_area=target_area)
fig,ax=plt.subplots(figsize=(8,6))
plot_task(env,ax,"Clearing the highlighted area",task1,True)

s=time.time()
action_profile_with_norms=create_data(task1,true_expression,env,"my_test2",num_repeat=500,verbose=False)
print ("Time Taken to complete job={:.2f}s\n".format(time.time()-s))

data=[]
for itr,ap in action_profile_with_norms.items():
    for i in range(0,int(len(ap)/2)):
        data.append(tuple([ap[2*i],ap[2*i+1]]))
print ("Data Generated:")
for i in range(10):
    print(data[i])
    

with open('my_data.sv', 'wb') as fp:
    pickle.dump(data, fp)


from algorithm_1_v2 import algorithm_1 as algorithm_1_len 
from algorithm_1_v3 import algorithm_1 as algorithm_1_str

from algorithm_1_v4 import algorithm_1 as algorithm_1_len 
rf=0.5

s=time.time()
print ("Generating sequence")
exp_seq_with_s,lik_list_with=algorithm_1_len(data,env,task1,true_expression,q_dict,rule_dict,
                                       filename="mcmc_test/my_test/cosine_1",
                                       sim_threshold=0.25,similarity_penalty=0.8,
                                       relevance_factor=rf,max_iterations=50000,verbose=False)
print ("\nTime Taken to complete job={:.2f}s\n".format(time.time()-s))

s=time.time()
print ("Generating sequence")
exp_seq_with_l,lik_list_with=algorithm_1_len(data,env,task1,true_expression,q_dict,rule_dict,
                                       filename="mcmc_test/my_test/lenient_1",
                                       relevance_factor=rf,max_iterations=50000,verbose=False)
print ("\nTime Taken to complete job={:.2f}s\n".format(time.time()-s))


#strict inequality
learned_expressions_s=Counter(map(to_tuple,exp_seq_with_s[int(len(exp_seq_with)/2)+1:]))
print ("Number of unique Norms in sequence={}".format(len(learned_expressions_s)))
#result2=performance(task1,env,true_expression,learned_expressions,name="test3",top_n=nan,beta=1,verbose=False)
#result2

#lenient inequality
learned_expressions_l=Counter(map(to_tuple,exp_seq_with_l[int(len(exp_seq_with)/2)+1:]))
print ("Number of unique Norms in sequence={}".format(len(learned_expressions_l)))
#result1=performance(task1,env,true_expression,learned_expressions,name="test2",top_n=nan,beta=1,verbose=False)
#result1

# =============================================================================
# learned_expressions=Counter(map(to_tuple,exp_seq_with))
# print ("Number of unique Norms in sequence={}".format(len(learned_expressions)))
# result2=performance(task1,env,true_expression,learned_expressions,name="test2",top_n=np.nan,beta=1,verbose=False)
# result2
# =============================================================================


# =============================================================================
# top=learned_expressions.most_common()
# t_with=sum(learned_expressions.values())
# exists = os.path.isfile('./mcmc_test/my_test/top_norms2.2.txt')
# if exists==True:
#     os.remove('./mcmc_test/my_test/top_norms2.2.txt')
# original = sys.stdout
# for i in range(len(top)):
#     exp=top[i]
#     if (i%10==0):
#         print("Rank:{} Norm has relative frequency={:.3f}%".format(i+1,exp[1]*100/t_with))
#     sys.stdout = open('./mcmc_test/my_test/top_norms2.2.txt', 'a+')
#     print("\n\n\n************Rank:{}, %-Frequency={:.3f}%**********".format(i+1,exp[1]*100/t_with))
#     print_expression(exp[0])
#     print("*************************************************")
#     sys.stdout=original
# 
# =============================================================================


sns.set_style("darkgrid")
fig,ax=plt.subplots(1, 2, sharex=False, sharey=False,figsize=(14,10))
fig.suptitle('Frequency of Norms in the generated sequence for relevance_factor={}'.format(rf))

t_l=sum(learned_expressions_l.values())
ax[0].plot([x*100/t_l for x in sorted(learned_expressions_l.values())],"o-",c=(250/255,93/255,130/255,0.7),markerfacecolor=(250/255,18/255,72/255,0.77))
ax[0].set_ylabel("%-Frequency in sample of size={}".format(t1))
ax[0].set_xlabel("Descending Rank of Norms from a total of {} Norms".format(len(learned_expressions_l)))
ax[0].title.set_text("Weak Inequality check for E_0:\nlog_Likelihood(expression)>=log_Likelihood(No-Norm)")
obl_rank1=[] #Ascending order Rank
for rank,x in enumerate(learned_expressions_l.most_common(),1):
    if x[0][1][0] =="Obl":
        obl_rank1.append(rank)
for rank in obl_rank1:
    ax[0].scatter(x=len(learned_expressions_l)-rank,
               y=sorted(learned_expressions_l.values())[len(learned_expressions_l)-rank]*100/t_l,
               c='green',s=151,marker='p',alpha=0.88,label='Obligatory,Rank={}'.format(rank))
ax[0].legend()
    #ax[0].annotate(xy=(len(learned_expressions_l)-rank,sorted(learned_expressions_l.values())[len(learned_expressions_l)-rank]*100/t_l),
      #xytext=(3,1),textcoords='offset points',color='green',fontsize=11.5,style='italic',s="Obl, Rank={}".format(rank))

#Strict inequality
t_s=sum(learned_expressions_s.values())
ax[1].plot([x*100/t for x in sorted(learned_expressions_s.values())],"o-",c=(250/255,93/255,130/255,0.7),markerfacecolor=(250/255,18/255,72/255,0.77))
ax[1].set_ylabel("Frequency in sample of size={}".format(t_s))
ax[1].set_xlabel("Descending Rank of Norms from a total of {} Norms".format(len(learned_expressions_s)))
ax[1].title.set_text("Strict Inequality check for E_0:\nlog_Likelihood(expression)>log_Likelihood(No-Norm)")
obl_rank=[] #Ascending order Rank
for rank,x in enumerate(learned_expressions_s.most_common(),1):
    if x[0][1][0] =="Obl":
        obl_rank.append(rank)
for rank in obl_rank:
    ax[1].scatter(x=len(learned_expressions_s)-rank,
               y=sorted(learned_expressions_s.values())[len(learned_expressions_s)-rank]*100/t_s,
               c="green",s=151,marker='p',alpha=0.88,label='Obligatory,Rank={}'.format(rank))
ax[1].legend()
    #ax[1].annotate(xy=(len(learned_expressions_s)-rank,sorted(learned_expressions_s.values())[len(learned_expressions_s)-rank]*100/t_s),
      #xytext=(3,4),textcoords='offset points',color='green',fontsize=11.5,style='italic',s="Obl, Rank={}".format(rank))










original = sys.stdout
a=open('./mcmc_test/my_test/start_name1.txt', 'a+')
sys.stdout = a
print ("--------------------------------------------------")
E_0=expand("NORMS")
print_expression(E_0)
print ("Lik={}".format(exp(Likelihood(E_0,data,env,w_normative=1))))
print ("--------------------------------------------------")
s=time.time()
while ((time.time()-s)<200):
    if exp(Likelihood(E_0,data,env,w_normative=1))>0:
        print ("--------------------------------------------------")
        print_expression(E_0)
        print ("Lik={}".format(exp(Likelihood(E_0,data,env,w_normative=1))))
        print ("--------------------------------------------------")
        break
    else:
        print ("--------------------------------------------------")
        E_0=expand("NORMS")
        print_expression(E_0)
        print ("Lik={}".format(exp(Likelihood(E_0,data,env,w_normative=1))))
        print ("--------------------------------------------------")
sys.stdout=original
a.close()
