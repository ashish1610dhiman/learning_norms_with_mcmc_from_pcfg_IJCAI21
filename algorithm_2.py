# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:35:38 2019

@author: dhias426
"""

#expression=expand("NORMS")

def generate_new_expression(expression,data,q_dict,rule_dict,env):
    """ Implementation of algorithm 2 given in the Bayesian Synthesis Paper """
    from algorithm_2_utilities import generate_A,sever,fill_hole,Likelihood
    from numpy import random
    from rules_3 import print_expression,expand
    #print ("Original_expression")
    #print_expression(expression)
    #Step 2
    Ae=generate_A(expression,q_dict)
    a=random.choice(Ae)
    print ("Node chosen={}".format(a))
    #Step 3
    non_terminal,E_hole=sever(a,expression,rule_dict)
    #Step_4
    E_sub=expand(non_terminal)
    #p_E_sub=get_prob(non_terminal,E_sub)
    #Step_5
    E_new=fill_hole(a,E_hole,E_sub)
    #print ("\nNew_expression")
    #print_expression(E_new)
    #Step_6
    old_lik=Likelihood(expression,data,env)
    #Step_7
    new_lik=Likelihood(E_new,data,env)
    print ("Old Likelihood={}".format(old_lik))
    print ("New Likelihood={}".format(old_lik))
    #Step_8
    Ae_new=generate_A(E_new,q_dict)
    p_accept=min(1,(len(Ae)/len(Ae_new))*(new_lik/old_lik))
    #Step 9
    r=random.uniform()
    if r<p_accept:
        print ("E_new accepted")
        return (E_new)
    else:
        print ("E_new rejected")
        return (expression)
