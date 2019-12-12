# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:12:35 2019

@author: dhias426
"""

from rules_4 import *

def get_elem(a,E):
    """ Helper function, get the elem at index a of expression """
    from copy import deepcopy
    sub_exp=deepcopy(E)
    temp_rule_dict=rule_dict["NORMS"].copy()
    if len(a)==0:
        return ("NORMS",sub_exp)
    for counter,index in enumerate(a,1):
        if isinstance(index,str):
            print("get_elem found index elt. {} of type str in index {}".format(index, a))
        non_terminal=temp_rule_dict[sub_exp[0]][index-1]
        temp_rule_dict=rule_dict[non_terminal]
        sub_exp=sub_exp[index] 
    return (non_terminal,sub_exp)


def join(a,my_sub):
    """ Helper function, joins my sub at a """
    a_=a[:-1]
    temp=list(my_sub[a_])
    temp_=list(temp[-1])
    temp_[a[-1]-1]=my_sub[a]
    temp[-1]=tuple(temp_)
    my_sub[a_]=tuple(temp)

def generate_subtrees(expression):
    """ Helper function for create vector """
    from algorithm_2_utilities import generate_A
    from mcmc_convergence_utilities import get_elem
    uni_trees=[]
    Ae=list(generate_A(expression))
    for a in Ae:
        nt,sub_exp=get_elem(a,expression)
        end=tuple(rule_dict[nt][sub_exp[0]])
        if len(end)==0:
            end=sub_exp[1]
        uni_trees.append(tuple([nt,sub_exp[0],end]))
    my_sub={a:uni_tree for a,uni_tree in zip(Ae,uni_trees)}
    for i in range(1,len(Ae)):
        a=Ae[-i]
        if len(a)>0:
           join(a,my_sub)
    return (my_sub)

def create_vector(expression,verbose=False):
    """ Create vector out of the passed expression """
    from collections import Counter
    from mcmc_convergence_utilities import generate_subtrees
    from time import time
    s=time()
    sub_trees=generate_subtrees(expression).values()
    v=Counter(sub_trees)
    if verbose==True:
        print ("Time to create vector={:.7f}".format(time()-s))
    return (v)
    
    
        
    
    