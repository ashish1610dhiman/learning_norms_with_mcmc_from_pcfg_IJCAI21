# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:35:38 2019

@author: dhias426
"""

#expression=expand("NORMS")

def generate_new_expression(expression,data,task1,q_dict,rule_dict,env,relevance_factor=0.5,w_normative=1):
    from algorithm_2_utilities import generate_A,sever,fill_hole,Likelihood
    from relevance import is_relevant
    from numpy import random,exp,log
    from rules_3 import expand
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
    old_log_lik=Likelihood(expression,data,env,w_normative)
    #Step_7
    new_log_lik=Likelihood(E_new,data,env,w_normative)
    print ("Old Likelihood={}".format(exp(old_log_lik)))
    print ("New Likelihood={}".format(exp(new_log_lik)))
    #Step_8
    Ae_new=generate_A(E_new,q_dict)
    if is_relevant(expression,task1,env)==False:
        old_log_lik+=log(relevance_factor)
    if is_relevant(E_new,task1,env)==False:
        new_log_lik+=log(relevance_factor)
    p_accept=min(1,(len(Ae)/len(Ae_new))*exp(new_log_lik-old_log_lik))
    print("p_accept={:.7f}".format(p_accept))
    #Step 9
    r=random.uniform()
    if r<p_accept:
        print ("E_new accepted")
        return (E_new)
    else:
        print ("E_new rejected")
        return (expression)
