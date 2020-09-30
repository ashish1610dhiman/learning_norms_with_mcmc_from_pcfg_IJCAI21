# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:12:35 2019

@author: dhias426
"""

from mcmc_convergence_utilities import create_vector
from collections import Counter
#from copy import deepcopy
import time
import pandas as pd
from math import log
from tqdm import tnrange, tqdm_notebook

def calculate_variance(sequence_list):
    """ Return within and between sequence variance for a list of sequences """
    m=len(sequence_list)
    sequence_means={}
    sequence_variance={}
    for j,sequence in enumerate(sequence_list,1):
        n=len(sequence)
        sequence_vector=list(map(create_vector,sequence))
        seq_sum=sum(sequence_vector,Counter())
        sequence_means[j]=Counter({key:value/n for key,value in seq_sum.items()})
        s_j=0
        for i,X in enumerate(sequence_vector):
            X1=X.copy()
            X1.subtract(sequence_means[j])
            t=sum([value**2 for value in X1.values()])
            s_j=s_j+t
        sequence_variance[j]=s_j/(n-1)
    net_mean=sum(sequence_means.values(),Counter())
    net_mean=Counter({key:value/m for key,value in net_mean.items()})
    W=sum(sequence_variance.values())/m
    B=0
    for sequence_mean in sequence_means.values():
        sequence_mean_=sequence_mean.copy()
        sequence_mean_.subtract(net_mean)
        t=sum([value**2 for value in sequence_mean_.values()])
        B=B+t
    B=n*B/(m-1)
    return (W,B)


def prepare_sequences(sequence_list,warmup=True,split=True):
    """ Helper function to discard warmup and split remaining halves """
    if warmup==True:
        wo_warmup=[sequence[int(len(sequence)/2)+1:] for sequence in sequence_list]
    else:
        wo_warmup=sequence_list
    split_halves=[]
    if split==True:
        for seq in wo_warmup:
            split_halves.append(seq[:int(len(seq)/2)])
            split_halves.append(seq[int(len(seq)/2):])
    else:
        split_halves=wo_warmup
    return (split_halves)

def calculate_R(split_halves,step_size):
    """ Calculate R coefficient """
    result={"iterations":[],"R":[],"within_seq_var":[],"between_seq_var":[],"var_over_est":[]}
    counter=0
    flag=0
    n=len(split_halves[0])
    tot=int(log(n/step_size,2))+2
    for i in tnrange(tot,desc="Progress"):
        if flag==1:
            counter+=counter
        else:
            counter+=step_size
            flag=1
        counter=min(n,counter)
        s=time.time()
        print ("\nCalculating Variance for 1st {} iterations".format(counter))
        my_seq=[sequence[:counter] for sequence in split_halves]
        print(f'Temp. check: seq length is {len(my_seq[0])}')
        W,B=calculate_variance(my_seq)
        result["iterations"].append(counter)
        result["within_seq_var"].append(W)
        result["between_seq_var"].append(B)
        result["var_over_est"].append(((n-1)/n)*W+(1/n)*B)
        result["R"].append((result["var_over_est"][-1]/W)**0.5)
        print ("Time taken for job={:.1f}s".format(time.time()-s))
    result=pd.DataFrame(result)
    return (result, split_halves)
#W,B=calculate_variance(sequence_list)

#import pickle

#with open('env_convergence.txt', 'wb') as fp:
    #pickle.dump(env, fp)
    
            
            
        
        
    
    
    
        
    
    