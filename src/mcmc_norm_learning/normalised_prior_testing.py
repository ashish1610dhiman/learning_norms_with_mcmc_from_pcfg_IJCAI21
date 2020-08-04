# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 13:56:55 2019

@author: dhias426
"""

from rules_3 import *
import numpy as np
from collections import Counter

""" Script to check Normalised Prior Condition given in
 Supplementary material of Bayesian Synthesis Paper.
 Naming Convention is same as that given in the supplemntary material"""

#List all Non_terminal symbols
nt_dict={ct:c for ct,c in enumerate(rule_dict.keys())}

# M is the expectation_matrix

M=np.zeros(shape=(len(nt_dict),len(nt_dict)))

for i in nt_dict.keys():
    N_i=nt_dict[i]
    for j in nt_dict.keys():
        N_j=nt_dict[j]
       # ri=len(p_dict[N_i])
        m_ij=0
        for k,production in enumerate(p_dict[N_i],1):
            p_ik=p_dict[N_i][production]
            n_ikj=Counter(rule_dict[N_i][production])[N_j]
            m_ij+=(p_ik*n_ikj)
        M[i][j]=m_ij
        
LA=np.linalg 
eig_values, eig_vectors = LA.eig(M)

check_list=[abs(val)<1 for val in eig_values]

if check_list.count(False)>0:
    print ("Normalised Prior Condition not satisfied")
else:
    print ("Normalised Prior Condition is satisfied")
    
if __name__ == "__main__":
    print ("Test Result for Normalised Prior given in Supplementary material" )
            
