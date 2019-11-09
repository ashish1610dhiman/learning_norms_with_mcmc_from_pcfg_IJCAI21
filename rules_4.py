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
#from numpy import nan
    
rule_dict={}
rule_dict["NORMS"]={"Norms":["NORM1","NORM2"]}
rule_dict["NORM1"]={"Obl":["COND","ZONE"],
                    "Pro":["ACTION","COLOUR","SHAPE","ZONE"]}
rule_dict["NORM2"]={"Per":["ACTION","COLOUR","SHAPE","ZONE"]}

rule_dict["COND"]={"Moved":["COLOUR","SHAPE","ZONE","COND"],
                   "Next-Move":["COLOUR","SHAPE"]}
rule_dict["ZONE"]={"Zone":[]}
rule_dict["ACTION"]={"Action":[]}
rule_dict["COLOUR"]={"Colour":[]}
rule_dict["SHAPE"]={"Shape":[]}

p_dict={}
p_dict["NORMS"]={"Norms":1}
p_dict["NORM1"]={"Obl":1/2,"Pro":1/2}
p_dict["NORM2"]={"Per":1}
p_dict["COND"]={"Moved":1/2,"Next-Move":1/2}

p_dict["ZONE"]={"Zone":1}
p_dict["ACTION"]={"Action":1}
p_dict["COLOUR"]={"Colour":1}
p_dict["SHAPE"]={"Shape":1}

q_dict={"Colour":{"r":1/4,"g":1/4,"b":1/4,"any":1/4},
        "Shape":{"triangle":1/4,"square":1/4,"circle":1/4,"any":1/4},
        "Action":{"pickup":1/2,"putdown":1/2},
        "Zone":{'1':1/4,'2':1/4,'3':1/4,'any':1/4}}

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
    """ Get probabilities of expanding in form of recusrive list """
    nts=rule_dict[non_terminal][expression[0]]
    if is_not_recursive(nts)==0:
            return ([p_dict[non_terminal][expression[0]]]+[expand_probability(nt,expression[i]) for i,nt in enumerate(nts,1)])
    else:
        return (q_dict[expression[0]][expression[1]])
        

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
    from operator import mul
    from functools import reduce
    from rules_3 import flatten_all,expand_probability
    b=expand_probability(non_terminal,expression)
    if type(b)==list:
        return (reduce(mul,flatten_all(b)))
    else:
        return (b)

# Converts (e.g.) ['Moved', ['Colour', 'any'], ['Shape', 'any'], ['Zone', '1'], ['Moved', ['Colour', 'r'], ['Shape', 'square'], ['Zone', '2'], ['Next-Move', ['Colour', 'g'], ['Shape', 'square']]]]
# to:
# [['Moved', ['Colour', 'any'], ['Shape', 'any'], ['Zone', '1']],
#  ['Moved', ['Colour', 'r'], ['Shape', 'square'], ['Zone', '2']],
#  ['Next-Move', ['Colour', 'g'], ['Shape', 'square']] ]
def separate_conds(cond, prev_cond=[]):
    if cond[0] == 'Next-Move':
        return prev_cond + [cond]
    assert cond[0] == 'Moved'
    return separate_conds(cond[4:][0], prev_cond + [cond[0:4]])

def print_rule(rule,counter):
    """ Helper function to print a rule """
    print ("------------------------------------------------")
    print ("                NORM Number={}".format(str(counter)))
    print ("------------------------------------------------")
    if rule[0]=="Per":
        print ("   > PERMISSION: action "+rule[1][1].lower())
        print ("     for colour "+rule[2][1].lower()+", shape "+rule[3][1].lower()+', and zone '+rule[4][1])
    elif rule[0]=="Pro":
        print ("   > PROHIBITION: action "+rule[1][1].lower())
        print ("     for colour "+rule[2][1].lower()+", shape "+rule[3][1].lower()+', and zone '+rule[4][1])
    else:
        cond = rule[1]
        conds_list = separate_conds(cond)
        next_move_cond = conds_list[-1]
        print ("   > OBLIGATION:")
        print ("     put in zone "+rule[2][1].upper()+" if handling colour "+next_move_cond[1][1].upper()+" and shape "+next_move_cond[2][1].upper())
        if len(conds_list) > 1:
            print ("     and history is ")
            for c in conds_list[:-1]:
                print(c)

def print_expression(expression):
    """ Helper function to print a expression """
    for i in range(1,len(expression)):
        print_rule(expression[i],i)
        

#rules=expand("NORMS")