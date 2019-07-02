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

    
rule_dict={}
rule_dict["NORM"]={"Obl":["SUB_ACTION1","SUB_ACTION2"],
         "Pro":["CONDITION","NORMATIVE_ACTION"],
         "Per":["CONDITION","NORMATIVE_ACTION"]}
rule_dict["SUB_ACTION1"]={"If":["CONDITION","NA1"]}
rule_dict["SUB_ACTION2"]={"Then":["NA2"]}
rule_dict["NA1"]={"1st_Action":[]}
rule_dict["NA2"]={"2nd_Action":[]}
rule_dict["CONDITION"]={"Cond":["COLOUR_CONDITION","SHAPE_CONDITION"]}
rule_dict["COLOUR_CONDITION"]={"Colour":[]}
rule_dict["SHAPE_CONDITION"]={"Shape":[]}
rule_dict["NORMATIVE_ACTION"]={"Action":[]}

p_dict={}
p_dict["NORM"]={"Obl":1/3,"Pro":1/3,"Per":1/3}
p_dict["SUB_ACTION1"]={"If":1}
p_dict["SUB_ACTION2"]={"Then":1}
p_dict["NA1"]={"1st_Action":1}
p_dict["NA2"]={"2nd_Action":1}
p_dict["CONDITION"]={"Cond":1}
p_dict["COLOUR_CONDITION"]={"Colour":1}
p_dict["SHAPE_CONDITION"]={"Shape":1}
p_dict["NORMATIVE_ACTION"]={"Action":1}


q_dict={"Colour":{"r":0.3,"g":0.3,"b":0.3,"np.nan":0.1},
        "Shape":{"triangle":0.3,"square":0.3,"circle":0.3,"np.nan":0.1},
        "Action":{"pickup":1/3,"move":1/3,"trash":1/3},
        "1st_Action":{"pickup":1},
        "2nd_Action":{"move":1/2,"trash":1/2}}


def is_recursive(Rik):
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
    from rules_1_1 import is_recursive
    from rules_1_1 import sample
    #Randomly chose rule for non-terminal
    chosen_rule=sample(p_dict[non_terminal])
    #print (chosen_rule)
    if is_recursive(rule_dict[non_terminal][chosen_rule]):
        return ([chosen_rule,sample(q_dict[chosen_rule])])
    else:
        return ([chosen_rule] + [expand(nt) for nt in rule_dict[non_terminal][chosen_rule]])
    
def print_rule(rule,counter):
    print ("------------------------------------------------")
    print ("                NORM Number={}".format(str(counter)))
    print ("------------------------------------------------")
    if rule[0]=="Per":
        print ("    PERMITTED to")
        print ("    "+rule[2][1].upper()+" "+rule[1][1][1].upper()+"-"+rule[1][2][1].upper()+'s')
    elif rule[0]=="Pro":
        print ("    PROHIBITED to")
        print ("    "+rule[2][1].upper()+" "+rule[1][1][1].upper()+"-"+rule[1][2][1].upper()+'s')
    else:
        print ("    OBLIGATORY to")
        print ("    "+rule[2][1][1].upper()+" "+rule[1][1][1][1].upper()+"-"+rule[1][1][2][1].upper()+'s')
        print ("    if you "+rule[1][2][1].upper()+" "+rule[1][1][1][1].upper()+"-"+rule[1][1][2][1].upper()+'s') 
    print ("")
    


#expand("NORM")   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
