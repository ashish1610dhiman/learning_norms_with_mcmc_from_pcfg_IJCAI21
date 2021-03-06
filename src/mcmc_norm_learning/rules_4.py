# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:51:03 2019

@author: dhias426
"""

"""
File defines the PCFG and other helper functions

Naming Convention:
Non-Terminal Symbols are Capitalized
1st letter of label is capitalized
Terminal Symbols are in small-case

rule_dict[non-terminal]={label1:[set of Nhk],label2:[set of Nhk]}

p_dict[non-terminal]={T_ik:P[T_ik]}

q_dict[non-recursive-rule-label]={diff_options:P[diff_actions]}
"""

import math
from operator import add, mul
from functools import reduce
#from numpy import nan

    
rule_dict={}
rule_dict["NORMS"]={"No-norm":[],
                    "Norms":["NORM1","NORM2"],
                    "Norm":["NORM1"]}
rule_dict["NORM1"]={"Obl":["COND","ZONE"],
                    "Pro":["ACTION","COLOUR","SHAPE","ZONE"]}
rule_dict["NORM2"]={"Per":["ACTION","COLOUR","SHAPE","PERZONE"]}

rule_dict["COND"]={"Moved":["COLOUR","SHAPE","ZONE","COND"],
                   "Next-Move":["COLOUR","SHAPE"]}
rule_dict["PERZONE"]={"PerZone":[]}
rule_dict["ZONE"]={"Zone":[]}
rule_dict["ACTION"]={"Action":[]}
rule_dict["COLOUR"]={"Colour":[]}
rule_dict["SHAPE"]={"Shape":[]}

p_dict={}
p_dict["NORMS"]={"No-norm": 0.5,"Norms":0.25,"Norm":0.25}
p_dict["NORM1"]={"Obl":1/2,"Pro":1/2}
p_dict["NORM2"]={"Per":1}
p_dict["COND"]={"Moved":1/3,"Next-Move":2/3}
p_dict["ZONE"]={"Zone":1}
p_dict["PERZONE"]={"PerZone":1}
p_dict["ACTION"]={"Action":1}
p_dict["COLOUR"]={"Colour":1}
p_dict["SHAPE"]={"Shape":1}

q_dict={"Colour":{"r":1/6,"g":1/6,"b":1/6,"any":1/2},
        "Shape":{"triangle":1/6,"square":1/6,"circle":1/6,"any":1/2},
        "Action":{"putdown":1},
        "Zone":{'1':1/3,'2':1/3,'3':1/3},
        "PerZone":{'1':1/6,'2':1/6,'3':1/6,'any':1/2},
        "No-norm": {'true':1}}

def colours_set():
    return {'r','g','b'}

def shapes_set():
    return {'triangle','square','circle'}

def zones_set():
    return {'1','2','3'}

def is_not_recursive(Rik):
    return (len(Rik)==0)

def sample(my_dict):
    from numpy.random import choice
    a=list(my_dict.keys())
    if (len(a)==1):
        return (a[0])
    else:
        p=[my_dict[key] for key in a]
        assert abs(sum(p)-1)<=0.05, "Proabilities don't add up to one"
        return (str(choice(a,1,True,p)[0]))

def expand(non_terminal):
    """ Function to expand the given non-terminal symbol as per the PCFG rules """
    from rules_3 import is_not_recursive
    from rules_3 import sample
    #Randomly chose rule for non-terminal
    chosen_rule=sample(p_dict[non_terminal])
    #print (chosen_rule)
    if is_not_recursive(rule_dict[non_terminal][chosen_rule]):
        return ([chosen_rule,sample(q_dict[chosen_rule])])
    else:
        return ([chosen_rule] + [expand(nt) for nt in rule_dict[non_terminal][chosen_rule]])

def expand_probability(non_terminal,expression):
    """ Get probabilities of expanding in form of recursive list """
    nts=rule_dict[non_terminal][expression[0]]
    if is_not_recursive(nts)==0:
            return ([p_dict[non_terminal][expression[0]]]+[expand_probability(nt,expression[i]) for i,nt in enumerate(nts,1)])
    else:
        return p_dict[non_terminal][expression[0]] * q_dict[expression[0]][expression[1]]
        

def flatten_all(iterable):
    """ Helper function to flatten a recursive list """
    for elem in iterable:
        if not isinstance(elem, list):
            yield elem
        else:
            for x in flatten_all(elem):
                yield x

def get_prob(non_terminal,expression):
    """ Returns the probability(Prior) of the given non-terinal expanding to the given expression """
    b=expand_probability(non_terminal,expression)
    if type(b)==list:
        return reduce(mul,flatten_all(b))
    else:
        return b

def get_log_prob(non_terminal,expression):
    """ Returns the log probability(Prior) of the given non-terinal expanding to the given expression """
    b=expand_probability(non_terminal,expression)
    if type(b)==list:
        return reduce(add,map(math.log, flatten_all(b)))
    else:
        return math.log(b)

# separate_conds:
# Converts (e.g.) ['Moved', ['Colour', 'any'], ['Shape', 'any'], ['Zone', '1'], ['Moved', ['Colour', 'r'], ['Shape', 'square'], ['Zone', '2'], ['Next-Move', ['Colour', 'g'], ['Shape', 'square']]]]
# to:
# [['Moved', ['Colour', 'any'], ['Shape', 'any'], ['Zone', '1']],
#  ['Moved', ['Colour', 'r'], ['Shape', 'square'], ['Zone', '2']],
#  ['Next-Move', ['Colour', 'g'], ['Shape', 'square']] ]
def separate_conds(cond, prev_cond=[]):
    if cond[0] == 'Next-Move':
        return prev_cond + [cond]
    assert cond[0] == 'Moved' #Unit condition
    return separate_conds(cond[4:][0], prev_cond + [cond[0:4]])

def obl_conds(rule):
    cond = rule[1]
    conds_list = separate_conds(cond)
    hist_conds = conds_list[0:-1]
    next_move_cond = conds_list[-1]
    return hist_conds, next_move_cond

def print_rule(rule,counter):
    """ Helper function to print a rule """
    print ("------------------------------------------------")
    print ("                NORM Number={}".format(str(counter)))
    print ("------------------------------------------------")
    if rule[0]=="Per":
        print ("   > PERMISSION: action "+pro_or_per_action(rule))
        print ("     for colour "+pro_or_per_colour(rule)+", shape "+pro_or_per_shape(rule)+' and zone '+pro_or_per_zone(rule))
    elif rule[0]=="Pro":
        print ("   > PROHIBITION: action "+pro_or_per_action(rule))
        print ("     for colour "+pro_or_per_colour(rule)+", shape "+pro_or_per_shape(rule)+' and zone '+pro_or_per_zone(rule))
    else:
        hist_conds, next_move_cond = obl_conds(rule)
        print ("   > OBLIGATION:")
        print ("     put in zone "+obl_zone(rule)+" if handling colour "+next_move_colour(next_move_cond)+" and shape "+next_move_shape(next_move_cond))
        if len(hist_conds) > 0:
            print ("     and history is ")
            for c in hist_conds:
                print("     ",c)

def pro_or_per_action(rule):
    return rule[1][1]

def pro_or_per_colour(rule):
    return rule[2][1]

def pro_or_per_shape(rule):
    return rule[3][1]

def pro_or_per_zone(rule):
    return rule[4][1]

def obl_zone(rule):
    return rule[2][1]

def moved_colour(moved_cond):
    return moved_cond[1][1]

def moved_shape(moved_cond):
    return moved_cond[2][1]

def moved_zone(moved_cond):
    return moved_cond[3][1]

def next_move_colour(next_move):
    return next_move[1][1]

def next_move_shape(next_move):
    return next_move[2][1]

def print_expression(expression):
    """ Helper function to print a expression """
    for i in range(1,len(expression)):
        print_rule(expression[i],i)
        

#rules=expand("NORMS")