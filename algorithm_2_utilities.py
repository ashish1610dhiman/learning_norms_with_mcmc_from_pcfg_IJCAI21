# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:35:38 2019

@author: dhias426
"""

#from rules_3 import is_not_recursive

def generate_index(expression,q_dict):
    """ Generate Index of nodes in expression , it starts from 1 """
    label=expression[0]
    #print (label)
    sub_expressions=[x for x in expression[1:]]
    if label in q_dict.keys():
        return ([])
    else:
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

def generate_A(expression,q_dict):
    """ Generate A (set of nodes) for the expression """
    from algorithm_2_utilities import generate_index,sub_A
    indices=(generate_index(expression,q_dict))
    Ae=[[]]
    for sub_index in indices:
        b=sub_A(sub_index)
        b.remove([])
        Ae=Ae+b
    final=[tuple(x) for x in Ae]
    return (final)


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



def violation(norms,env):
    """ Returns a dict with key as object_id and value,
    as a list of all apossible violations of norm on that object """
    from verify_action_4 import check_pro,check_per,check_obl
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
        pro_flag,pro_zone,key=check_pro(obj,"pickup",pro_norms)
        per_flag,per_zone,key=check_per(obj,"pickup",per_norms)
        if pro_flag==1: #Prohibition exists
            if per_flag==0:
                ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones]
            else:
                if pro_zone != per_zone:
                   ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones] 
        """ Putdown stage """
        #check for obl and permission
        obl_flag,obl_zone,key=check_obl(obj,obl_norms)
        per_flag,per_zone,key=check_per(obj,"putdown",per_norms)
        if obl_flag==1:
            viol_zones.remove(int(obl_zone))
            if per_flag==0:
                ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones]
            else:
                if per_zone!=obl_zone:
                    viol_zones.remove(int(per_zone))
                ob_viol=ob_viol+[(("pickup",obj.obj_id),("putdown",obj.obj_id,zone)) for zone in viol_zones]
        #check for pro and permission
        pro_flag,pro_zone,key=check_pro(obj,"putdown",pro_norms)
        per_flag,per_zone,key=check_per(obj,"putdown",per_norms)
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


def Likelihood(expression,data,env,w_normative=1.0):
    """ Calculate log-Likelihhod of expression in data
    Violation function is called on env inside
    Empty expression (i.e. norms) can be passed """
    from algorithm_2_utilities import violation
    from numpy import log
    #calculate |K|
    mod_K=len(env[3])
    #Find Vioalations
    violations=violation(expression,env)
    log_likelihood_data=0
    w_normative=float(w_normative)
    for x in data:
        #Each x expresses only 1 object
        obj_id=x[0][1]
        lik_non_norm=1/mod_K
        if obj_id in violations.keys():
            if x in violations[obj_id]:
                lik_norm=0.000000001 # To make log(zero) work
                #print ("check1")
            else:
                lik_norm=1/(mod_K-len(violations[obj_id]))
                #print ("check2")
        else:
            lik_norm=1/mod_K
            #print ("check3")
        likelihood_x=w_normative*lik_norm+(1-w_normative)*(lik_non_norm)
        log_likelihood_data+=log(likelihood_x)
    return (log_likelihood_data)
        


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
