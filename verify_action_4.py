# -*- coding: utf-8 -*-
"""
Created on Fri May 24 09:39:30 2019

@author: dhias426
"""
from rules_4 import pro_or_per_colour, pro_or_per_shape, pro_or_per_action,\
                    pro_or_per_zone, separate_conds, obl_zone,\
                    next_move_colour, next_move_shape

def check_pro_or_per(obj,task_type,norms):
    """ Helper function, Check if task performed on obj matches target of Prohibition or Permission norm """
    from numpy import nan
    #Return 1 if matching prohibition or permission exists
    for key,rule in norms.items():
        if pro_or_per_colour(rule)==obj.colour:
            if pro_or_per_shape(rule)==obj.shape:
                if pro_or_per_action(rule)==task_type:
                    return (1,pro_or_per_zone(rule),key)
    return (0,nan,nan)


def check_obl(obj,norms):
    """ Helper function, Check if task can be performed on obj given Obligatory norms """
    from numpy import nan
    #Return 1 if obligation matches obj
    for key,rule in norms.items():
        cond = rule[1]
        conds_list = separate_conds(cond)
        next_move = conds_list[-1]
        if next_move_shape(next_move)==obj.shape:
            if next_move_colour(next_move)==obj.colour:
                return (1,obl_zone(rule),key)
                break
    return (0,nan,nan)
        
    
def verify_action(obj,check,task_type,rules):
    """ Check if action can be performed given Norms """
    from numpy import nan
    #print ("Check")
    rule_dict={x:rules[x] for x in range(1,len(rules))}
    if len(rules)==0:
        return (0,nan,nan)
    obl_norms={norm_no:norm for (norm_no,norm) in rule_dict.items() if norm[0]=="Obl"}
    pro_norms={norm_no:norm for (norm_no,norm) in rule_dict.items() if norm[0]=="Pro"}
    per_norms={norm_no:norm for (norm_no,norm) in rule_dict.items() if norm[0]=="Per"}
    if check=="prohibition":
        return (check_pro_or_per(obj,task_type,pro_norms))
    elif check=="permission":
        return (check_pro_or_per(obj,task_type,per_norms))
    else:
        return (check_obl(obj,obl_norms))
    
# =============================================================================
# def verify_action(obj,task_type,rules):
#     from verify_action import check_pro,check_per,check_obl
#     from numpy import nan
#     #return 1 if action is allowed by per,pro norms
#     #Seperate the 3 types of norms
#     rule_dict={x:rules[x] for x in range(1,len(rules))}
#     obl_norms={norm_no:norm for (norm_no,norm) in rule_dict.items() if norm[0]=="Obl"}
#     pro_norms={norm_no:norm for (norm_no,norm) in rule_dict.items() if norm[0]=="Pro"}
#     per_norms={norm_no:norm for (norm_no,norm) in rule_dict.items() if norm[0]=="Per"}
#     #Check if action is prohibited
#     if len(pro_norms)>0:
#         flag_pro,key_pro=check_pro(obj,task_type,pro_norms)
#     else:
#         flag_pro=0 #Since no prohibition, task does not vioalte any
#         key_pro=nan
#     if len(per_norms)>0:
#         flag_per,key_per=check_per(obj,task_type,per_norms)
#     else:
#         flag_per=0 #Since no permission, task can not be permitted
#         key_per=nan
#     #print ("pro,per={},{}".format(str(flag_pro),str(flag_per)))
#     if task_type=="pickup":
#         if len(obl_norms)>0:
#             flag_obl,task,key_obl=check_obl(obj,obl_norms)
#         else:
#             flag_obl=0
#             task=nan
#             key_obl=nan
#         if flag_obl==1:
#             return (1,task,key_obl)
#         else:
#             return (0,task,key_obl)
#     if (flag_pro==1):#Action is prohibited
#         if flag_per==1: #Does exception exist
#             return(1,nan,str(key_per)+"_"+str(key_per))
#         else:
#             return(0,nan,key_pro)
#     else:
#         return (1,nan,key_pro)
#     
# =============================================================================
