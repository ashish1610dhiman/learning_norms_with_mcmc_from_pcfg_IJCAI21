# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:35:38 2019

@author: dhias426
"""

from algorithm_2_utilities import generate_A,sever,fill_hole,Likelihood
from relevance import is_relevant
from numpy import random,exp,log,isnan
from rules_4 import expand,expand_probability
from cosine_sim import cos_theta

#expression=expand("NORMS")
#TO DO: Remove arg. q_dict - no longer used
def generate_new_expression(expression,data,task1,q_dict,rule_dict,env,relevance_factor=0.5,sim_threshold=0,similarity_penalty=1,w_normative=1):
    """ Version with jumping distribution change """
    #print ("Original_expression")
    #print_expression(expression)
    #Step 2
    Ae=list(generate_A(expression))
    a=random.choice(Ae)
    #print ("Node chosen={}".format(a))
    #Step 3
    non_terminal,E_hole=sever(a,expression,rule_dict)
    #Step_4
    E_sub=expand(non_terminal)
    #p_E_sub=get_prob(non_terminal,E_sub)
    #Step_5
    E_new=fill_hole(a,E_hole,E_sub)
    #prior_E=expand_probability("NORMS",expression)
    #prior_E_new=expand_probability("NORMS",E_new)
    #print ("\nNew_expression")
    #print_expression(E_new)
    #Step_6
    old_log_lik = Likelihood(expression,task1,data,env,w_normative)
    #Step_7
    new_log_lik = Likelihood(E_new,task1,data,env,w_normative)
    print ("Old Expression: Log-Likelihood={}".format(old_log_lik))
    print ("New Expression: Log-Likelihood={}".format(new_log_lik))
    #Step_8
    Ae_new=list(generate_A(E_new))
    #Adjusting for relevance of norms
    """
    if isnan(relevance_factor)==False:
        if is_relevant(expression,task1,env)==False:
            old_log_lik+=log(relevance_factor)
        if is_relevant(E_new,task1,env)==False:
            print ("E_new is not relevant")
            new_log_lik+=log(relevance_factor)
    """
    # Adjusting for similarity between W and E'
    """
    sim=cos_theta(expression,E_new)
    adjusting_factor=1
    if sim>=sim_threshold:
        adjusting_factor=similarity_penalty
    print ("Adjusting factor:{}".format(adjusting_factor))
    """
    log_lik_no_norm = Likelihood([],task1,data,env,w_normative)
    if isnan(relevance_factor)==False:
        p_accept_adjust_numerator_log = log(relevance_factor) if new_log_lik <= log_lik_no_norm else 0
        p_accept_adjust_denominator_log = log(relevance_factor) if old_log_lik <= log_lik_no_norm else 0
        factor_log = p_accept_adjust_numerator_log - p_accept_adjust_denominator_log
    else:
        factor_log = 0
    print("log(factor) = {}".format(factor_log))
    # p_accept = min(1, factor * ((len(Ae)) / len(Ae_new)) * new_log_lik / old_log_lik)
    log_p_accept = min(0, factor_log + log(len(Ae)) - log(len(Ae_new)) + new_log_lik - old_log_lik)
    print("log(p_accept)={:.7f}".format(log_p_accept))
    #Step 9
    r_log=log(random.uniform())
    if r_log < log_p_accept:
        print ("E_new accepted")
        return (E_new)
    else:
        print ("E_new rejected")
        return (expression)
