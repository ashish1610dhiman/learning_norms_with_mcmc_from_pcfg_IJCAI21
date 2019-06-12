# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:51:03 2019

@author: dhias426
"""

"""
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
rule_dict["NORM1"]={"Obl":["SUB_ACTION1","SUB_ACTION2"],
                     "Pro":["ACTION","CONDITION",]}
rule_dict["NORM2"]={"Per":["ACTION","CONDITION"]}


rule_dict["SUB_ACTION1"]={"If":["CONDITION","NA1"]}
rule_dict["SUB_ACTION2"]={"Then":["NA2","ZONE"]}
rule_dict["NA1"]={"1st_Action":[]}
rule_dict["NA2"]={"2nd_Action":[]}
rule_dict["ZONE"]={"Zone":[]}

rule_dict["CONDITION"]={"On":["COLOUR_CONDITION","SHAPE_CONDITION"]}
rule_dict["COLOUR_CONDITION"]={"Colour":[]}
rule_dict["SHAPE_CONDITION"]={"Shape":[]}
rule_dict["ACTION"]={"Perform":["ZONE","NORMATIVE_ACTION"]}
rule_dict["NORMATIVE_ACTION"]={"Action":[]}


p_dict={}
p_dict["NORMS"]={"Norms":1}
p_dict["NORM1"]={"Obl":1/2,"Pro":1/2}
p_dict["NORM2"]={"Per":1}
p_dict["SUB_ACTION1"]={"If":1}
p_dict["SUB_ACTION2"]={"Then":1}
p_dict["NA1"]={"1st_Action":1}
p_dict["NA2"]={"2nd_Action":1}
p_dict["ZONE"]={"Zone":1}
p_dict["ACTION"]={"Perform":1}
p_dict["CONDITION"]={"On":1}
p_dict["COLOUR_CONDITION"]={"Colour":1}
p_dict["SHAPE_CONDITION"]={"Shape":1}
p_dict["NORMATIVE_ACTION"]={"Action":1}


q_dict={"Colour":{"r":1/3,"g":1/3,"b":1/3},
        "Shape":{"triangle":1/3,"square":1/3,"circle":1/3},
        "Action":{"pickup":1/2,"putdown":1/2},
        "1st_Action":{"pickup":1},
        "2nd_Action":{"putdown":1},
        "Zone":{'1':1/3,'2':1/3,'3':1/3}}


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
    """ Return probability of each label as per prior probabilities """
    nts=rule_dict[non_terminal][expression[0]]
    if is_not_recursive(nts)==0:
            return ([p_dict[non_terminal][expression[0]]]+[expand_probability(nt,expression[i]) for i,nt in enumerate(nts,1)])
    else:
        return (q_dict[expression[0]][expression[1]])
        

def flatten_all(iterable):
    """ Flatten a nested list """
    for elem in iterable:
        if not isinstance(elem, list):
            yield elem
        else:
            for x in flatten_all(elem):
                yield x

def get_prob(non_terminal,expression):
    """ Return probability of non-terminal expanding to the given expression as per prior probabilities """
    from operator import mul
    from functools import reduce
    from rules_3 import flatten_all,expand_probability
    b=expand_probability(non_terminal,expression)
    if type(b)==list:
        return (reduce(mul,flatten_all(b)))
    else:
        return (b)
    
def print_rule(rule,counter):
    print ("------------------------------------------------")
    print ("                NORM Number={}".format(str(counter)))
    print ("------------------------------------------------")
    if rule[0]=="Per":
        print ("   > PERMITTED to "+rule[1][2][1].upper())
        print ("     "+rule[2][1][1].upper()+"-"+rule[2][2][1].upper()+'s in ZONE-'+rule[1][1][1])
    elif rule[0]=="Pro":
        print ("   > PROHIBITED to "+rule[1][2][1].upper())
        print ("     "+rule[2][1][1].upper()+"-"+rule[2][2][1].upper()+'s in ZONE-'+rule[1][1][1])
    else:
        print ("   > OBLIGATORY to")
        print ("     "+rule[2][1][1].upper()+" "+rule[1][1][1][1].upper()+"-"+rule[1][1][2][1].upper()+'s in ZONE-'+rule[2][2][1])
        print ("     if you "+rule[1][2][1].upper()+" "+rule[1][1][1][1].upper()+"-"+rule[1][1][2][1].upper()+'s') 
    
def print_expression(expression):
    from rules_3 import print_rule
    for i in range(1,len(expression)):
        print_rule(expression[i],i)

#rules=expand("NORMS")   

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
