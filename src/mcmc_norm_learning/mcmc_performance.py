	# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 09:46:55 2019

@author: dhias426
"""

import numpy as np
from robot_task_new import all_compliant
from algorithm_1_v4 import create_data

def calculate_pr(true,predicted):
	""" Calculate precision and recall from true and predicted data """
	#true=[(true[2*i],true[2*i+1]) for i in range(int(len(true)/2))]
	#predicted=[(predicted[2*i],predicted[2*i+1]) for i in range(int(len(predicted)/2))]
	true=set(true)
	predicted=set(predicted)
	true_inter_pred=true & predicted
	
	print("Identical sets: {}".format(true == predicted))
	print(f"Num. distinct executions in observations: {len(true)}\n")
	print(f"Num. distinct executions given learned exp.: {len(predicted)}\n")
	print(f"Size of intersection: {len(true_inter_pred)}")
	
	return((len(true_inter_pred)/len(predicted)),(len(true_inter_pred)/len(true)))
  
def performance(task1,env,true_expression,learned_expressions,folder_name="top_exp",file_name="top_exp",top_n=np.nan,beta=1,repeat=1000,verbose=True):
	# Generate all possible action plans from true and leanrned expression (each in learned expressions)  and subsequently calculate precision and recall
	import pandas as pd
	from copy import deepcopy
	from mcmc_performance import calculate_pr
	print(f"True expression passed to performance(...): {true_expression}")
	#Genearte original data from the task
	#true_data=all_compliant(true_expression,task1,deepcopy(env),"{}/precision_recall/true_{}".format(folder_name,file_name),verbose=False)
	true_data = create_data(true_expression,env,name=None,task=task1,random_task=False,
                num_actionable=np.nan,num_repeat=repeat,verbose=False)
	print(f"true_data[0]: {true_data[0]}")
	#Sort the learned expresions and select top_n out of them
	if np.isnan(top_n):
	    top_n=len(learned_expressions)
	top_expressions=learned_expressions.most_common()[:top_n]
	t=sum([exp[1] for exp in top_expressions])
	result={"norm_rank":[],"weight":[],"precision":[],"recall":[],"F_{}".format(beta):[]}
	#Calculate Precison/Recall
	for rank,exp in enumerate(top_expressions,1):
		print("Calculting P&R for exp {} at rank {}".format(exp,rank))
		result["norm_rank"].append(rank)
		result["weight"].append(exp[1]/t)
		#predicted_data=all_compliant(exp[0],task1,deepcopy(env),"{}/precision_recall/{}_{}".format(folder_name,file_name,rank),verbose=False)
		predicted_data = create_data(exp[0],env,name=None,task=task1,random_task=False,
                num_actionable=np.nan,num_repeat=repeat,verbose=False)
		print(f"predicted_data[0]: {predicted_data[0]}")
		p,r=calculate_pr(true_data,predicted_data)
		result["precision"].append(p)
		result["recall"].append(r)
		result["F_{}".format(beta)].append((1+beta**2)*(p*r)/(r+p*beta**2))
	#Calculate Precision and Recall for the weighted norms
	result=pd.DataFrame(result)
	result=result[["norm_rank","weight","precision","recall","F_{}".format(beta)]]
	temp=pd.DataFrame()
	temp["norm_rank"]=["net"]
	temp["weight"]=sum(result["weight"])
	temp["precision"]=[sum(result.weight*result.precision)]
	temp["recall"]=[sum(result.weight*result.recall)]
	temp["F_{}".format(beta)]=[sum(result.weight*result["F_{}".format(beta)])]
	result=result.append(temp,ignore_index=True)
	#if verbose==True:
	print (result)
	return (result)
    
    
    