# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:42:05 2019

@author: dhias426
"""

def dot(E1_vec,E2_vec):
    # Find common keys in two expressions
    common_keys=set(E1_vec.keys()) & set(E2_vec.keys())
    ans=0
    for key in common_keys:
        ans+=(E1_vec[key]*E2_vec[key])
    return (ans)

def cos_theta(E1,E2):
    # Find Cos_theta between two expressions
    from mcmc_convergence_utilities import create_vector
    E1_vec=create_vector(E1,verbose=True)
    E2_vec=create_vector(E2,verbose=True)
    norm_E1=dot(E1_vec,E1_vec)**0.5
    norm_E2=dot(E2_vec,E2_vec)**0.5
    num=dot(E1_vec,E2_vec)
    return (num/(norm_E1*norm_E2))
    