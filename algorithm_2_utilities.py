# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:35:38 2019

@author: dhias426
"""

from robot_task_new import all_compliant
from working import history_matches_cond
from rules_4 import zones_set

def generate_index(expression,q_dict):
    """ Generate Index of nodes in expression , it starts from 1 """
    label=expression[0]
    #print (label)
    if label in q_dict.keys():
        return ([])
    else:
        sub_expressions=[x for x in expression[1:]]
        return ([i+1]+ list(generate_index(sub_expressions[i],q_dict)) for i in range(len(sub_expressions)))
    
#b=list(generate_index(rules))

def sub_A(indices,p=[]):
    """ Generates A for a branch of A """
    """ 1st element of indices should be int for this to work """
    #print ("indices=",indices)
    #print ("p=",p)
    if type(p)==int:
        A=[]
        p=[p]
    else:
        if len(p)==0:
            A=[p]
        else:
            A=[]
    for elem in indices:
        #print ("elem=",elem)
        if type(elem)==int:
            A.append(p+[elem])
            p=A[-1]
        else:
            if len(elem)==1:
                #print ("check1")
                A.append(p+elem)
            else:
                #print ("check2\n")
                if [] in A:
                    A=A+sub_A(elem,indices[0])
                else:
                    A=A+sub_A(elem,A[-1])
        #print ("A=",A)
    return (A)

def generate_A(expression, root_label=[]):
    if hasattr(expression, "__len__") and not isinstance(expression, str):
        yield root_label
        if len(expression) > 1:
            for i,e in enumerate(expression[1:], 1):
                for a in generate_A(e, root_label+[i]):
                    yield a

""" def generate_A(expression,q_dict): """
""" Generate A (set of nodes) for the expression """
"""    from algorithm_2_utilities import generate_index,sub_A
    indices=(generate_index(expression,q_dict))
    Ae=[[]]
    for sub_index in indices:
        b=sub_A(sub_index)
        b.remove([])
        Ae=Ae+b
    final=[tuple(x) for x in Ae]
    return (final) """


def sever(a,expression,rule_dict):
    """ Sever the expression at node a"""
    from copy import deepcopy

    exp_copy=deepcopy(expression)
    sub_expression=exp_copy
    temp_rule_dict=rule_dict["NORMS"].copy()
    code="exp_copy"
    my_str="HOLE"
    if len(a)==0:
        exp_copy=["HOLE"]
        non_terminal="NORMS"
        return (non_terminal,exp_copy)
    for counter,index in enumerate(a,1):
        if counter==len(a):
            code=code+".__setitem__({},{})".format(index,"my_str")
        else:
            code=code+".__getitem__({})".format(index)
        non_terminal=temp_rule_dict[sub_expression[0]][index-1]
        temp_rule_dict=rule_dict[non_terminal]
        sub_expression=sub_expression[index]  
    eval(code)
    return (non_terminal,exp_copy)
    
def fill_hole(a,E_hole,E_sub):
    """ Replace HOlE with E_sub in E_hole at node a"""
    from copy import deepcopy
    E_hole_copy=deepcopy(E_hole)
    code="E_hole_copy"
    if len(a)==0:
        return(E_sub)
    for counter,index in enumerate(a,1):
        if counter==len(a):
            code=code+".__setitem__({},{})".format(index,E_sub)
        else:
            code=code+".__getitem__({})".format(index)
    eval(code)
    return (E_hole_copy)

def violations(execution, expression, task, env):
    ac = all_compliant(expression, task, env, "foo")
    for i, move in enumerate(execution):
        assert move[0][0]=="pickup"
        oid = move[0][1]
        

def violations(norms,env):
    """ Returns a dict with key as object_id and value,
    as a list of all apossible violations of norm on that object """
    from verify_action_4 import check_pro_or_per,check_per,check_obl
    violations={}
    my_dict={x:norms[x] for x in range(1,len(norms))}
    obl_norms={norm_no:norm for (norm_no,norm) in my_dict.items() if norm[0]=="Obl"}
    pro_norms={norm_no:norm for (norm_no,norm) in my_dict.items() if norm[0]=="Pro"}
    per_norms={norm_no:norm for (norm_no,norm) in my_dict.items() if norm[0]=="Per"}
    for obj in env[0]:
        #print (obj.obj_id,obj.colour,obj.shape)
        viol_zones=list(env[3].keys())
        ob_viol=[]
        """ Pickup stage """
        #check if pickup is prohibited and no permission
        pro_flag,pro_zone,key=check_pro_or_per(obj,"pickup",pro_norms)
        per_flag,per_zone,key=check_pro_or_per(obj,"pickup",per_norms)
        if pro_flag==1: #Prohibition exists
            if per_flag==0:
                ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones]
            else:
                if pro_zone != per_zone:
                   ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones] 
        """ Putdown stage """
        #check for obl and permission
        obl_flag,obl_zone,key=check_obl(obj,obl_norms)
        per_flag,per_zone,key=check_pro_or_per(obj,"putdown",per_norms)
        if obl_flag==1:
            viol_zones.remove(int(obl_zone))
            if per_flag==0:
                ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones]
            else:
                if per_zone!=obl_zone:
                    viol_zones.remove(int(per_zone))
                ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones]
        #check for pro and permission
        pro_flag,pro_zone,key=check_pro_or_per(obj,"putdown",pro_norms)
        per_flag,per_zone,key=check_pro_or_per(obj,"putdown",per_norms)
        viol_zones=list(env[3].keys())
        if pro_flag==1: #Prohibition exists
            if per_flag==0:
                ob_viol.append((("pickup",obj.obj_id),("putdown",obj.obj_id,int(pro_zone))))
            else:
                if pro_zone!=per_zone:
                    ob_viol.append((("pickup",obj.obj_id),("putdown",obj.obj_id,int(pro_zone))))
        if len(ob_viol)>0:
            violations[obj.obj_id]=ob_viol
    return (violations)   


def Likelihood(expression,task,executions,env,w_normative=1.0):
    """ Calculate log-Likelihhod of expression in data
    Violation function is called on env inside
    Empty expression (i.e. norms) can be passed """
    from numpy import log
    log_lik = 0
    ac = all_compliant(expression, task, env, "foo")
    #print("ac in Likelihood: {}".format(ac))
    for ex in executions:
        #print("Execution seen by Likelihood: ", ex)
        w_normative=float(w_normative)
        num_zones = len(zones_set())
        for ex in executions:
            lik_ex_normative = 1
            for i,move in enumerate(ex):
                oid = move[0][1]
                possible_moves = ac[oid]
                #print("Possible moves at pos. {}: {}".format(i,possible_moves))
                zone_options = {
                    pm.putdown[2]
                    for pm in possible_moves
                    if pm.unless == None or not history_matches_cond(ex[max(i-len(pm.unless),0):i], pm.unless, env)
                }
                num_poss_zones = len(zone_options)
                #if num_poss_zones < len(possible_moves):
                    #print("Likelihood: unless constraint reduced num. options to {} (refined options: {})".format(num_poss_zones, zone_options))
                assert move[1][0]=="putdown"
                move_zone = move[1][2]
                violated = not move_zone in zone_options
                if violated:
                    #print("Violation: move zone {} not in {}".format(move_zone, zone_options))
                    lik_ex_normative *= 0.000000001 # To make log(zero) work
                else:
                    lik_ex_normative *= 1/num_poss_zones
            lik_ex_non_normative = 1/(num_zones**len(ex)) if w_normative != 1.0 else 0
            lik_ex = w_normative*lik_ex_normative + (1-w_normative)*(lik_ex_non_normative)
            log_lik += log(lik_ex)
    return log_lik


# =============================================================================
# def count_actionable_obj(robot):
#     actionable_objects=[]
#     (x1,y1)=robot.task.target_area[0].coordinates()
#     (x2,y2)=robot.task.target_area[1].coordinates()
#     for obj in robot.env[0]:
#         if (x1<=obj.position.x<=x2):
#             if (y1<=obj.position.y<=y2):
#                 if obj.colour in robot.task.colour_specific:
#                     if obj.shape in robot.task.shape_specific:
#                         actionable_objects.append(obj)
#     return(len(actionable_objects),actionable_objects)
# =============================================================================   
