# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:43:38 2019

@author: dhias426
"""

import numpy as np
from collections import namedtuple
from contextlib import redirect_stdout
from working import *
from itertools import product
import numpy as np
import random


PossMove = namedtuple("PossMove", ['pickup','putdown','unless'])
PossMove.__new__.__defaults__ = (None,None,None) # Just use 'defaults' param above if using Python 3.7 or above

class task():
    """ Class to model the task """
    def __init__(self,colour_specific=np.nan,shape_specific=np.nan,target_area=np.nan):
        self.task_type="clear"
        self.colour_specific=colour_specific
        self.shape_specific=shape_specific
        self.target_area=target_area
    def print_task(self):
        print ("---------------------------------")
        print (self.task_type.upper())
        print(self.colour_specific)
        print(self.shape_specific)
        print ("---------------------------------")

def plot_task(env,ax,itr,task,annotate_choice):
    """ Helper function to plot the task """
    #import matplotlib.pyplot as plt
    from numpy import nan
    from environment import plot_env,plot_area
    plot_env(env,ax,itr,legend=False,annotate=annotate_choice)
    plot_area(ax,task.target_area,nan)
    ax.legend(["Area to clear"])

class robot():
    """ Class to model the robot """
    def __init__(self,task,env):
        import numpy as np
        self.task=task
        self.env=env
        if type(self.task.colour_specific)!=list:
            try:
                if np.isnan(self.task.colour_specific):
                    self.task.colour_specific=self.env[1]
            except:
                self.task.colour_specific=[self.task.colour_specific]
        if type(self.task.shape_specific)!=list:
            try:
                if np.isnan(self.task.shape_specific):
                    #print (self.task.shape_specific)
                    self.task.shape_specific=self.env[2]
            except:
                self.task.shape_specific=[self.task.shape_specific]
    def all_actionable(self):
        """ Returns object-ids of all actionable objects for a task """
        actionable_objects=[]
        (x1,y1)=self.task.target_area[0].coordinates()
        (x2,y2)=self.task.target_area[1].coordinates()
        for obj in self.env[0]:
            if (x1<=obj.position.x<=x2):
                if (y1<=obj.position.y<=y2):
                    if obj.colour in self.task.colour_specific:
                        if obj.shape in self.task.shape_specific:
                            actionable_objects.append(obj.obj_id)
        return (actionable_objects)

    def perform_task(self,rules,name,verbose=True):
        ac_dict = all_compliant(rules,self.task,self.env,name,verbose)
        if verbose:
            print("ac_dict: ", ac_dict)
        ums = list(unless_moves(ac_dict))
        if verbose:
            print("Unless moves: ", ums)
        
        objects = list(ac_dict.keys())
        num_objects = len(objects)
        compliant_exec = False
        while not compliant_exec:
            p = np.random.permutation(objects)
            if verbose:
                print("permutation: ", p)
            for exe in gen_moves_from_all_compliant_dict(p, ac_dict):
                if verbose:
                    print("Considering execution: ", exe)
                matched_constraint = False
                for um in ums:
                    if verbose:
                        print("Checking unless constraint: ", um)
                    constrained_obj = um[0]
                    constraint_history_length = len(um[2])
                    assert isinstance(constraint_history_length, int)
                    if verbose:
                        print("Constrained history length: ", constraint_history_length)
                    co_index = np.argwhere(p==constrained_obj)[0][0]
                    if verbose:
                        print("Constrained object is at index {} of execution".format(co_index))
                    assert exe[co_index][1][2] in zones_set()
                    assert set(um[1]) < zones_set()
                    if verbose:
                        print("exec's zone for constrained obj: ", exe[co_index][1][2])
                        print("Unless constraint triggering zones: ", um[1])
                        print("Exec. puts {} in {} (it is in {}?)".format(um[0], exe[co_index][1][2], um[1]))
                    if exe[co_index][1][2] not in um[1]: # exec's zone for constrained object doesn't matche a zone of the unless constraint
                        continue
                    sub_exec = exe[max(co_index-constraint_history_length,0):co_index]
                    if verbose:
                        print("Calling history_matches_cond({}, {}, ...)".format(sub_exec, um[2]))
                    if history_matches_cond(sub_exec, um[2], self.env):
                        if verbose:
                            print("Matched!")
                        matched_constraint = True
                        break
                if not matched_constraint:
                    return exe
            if verbose:
                print("Trying another permutation")      
        assert compliant_exec == True
        return None # Will never get here due to the assert

    # Old version kept for reference
    """ def perform_task(self,rules,name,verbose=True):
        # Return one out of all possible compliant action plan given norms 
        import sys
        from actions import pickup_action,putdown_action
        from verify_action_4 import verify_action
        from copy import deepcopy
        import os
        from numpy import nan,random
        actionable_objects=[]
        (x1,y1)=self.task.target_area[0].coordinates()
        (x2,y2)=self.task.target_area[1].coordinates()
        for obj in self.env[0]:
            if (x1<=obj.position.x<=x2):
                if (y1<=obj.position.y<=y2):
                    if obj.colour in self.task.colour_specific:
                        if obj.shape in self.task.shape_specific:
                            actionable_objects.append(obj)
        num_actionable_obj=len(actionable_objects)
        if verbose==True:
            print ("Found {} actionable objects".format(str(num_actionable_obj)))
        if (num_actionable_obj)==0:
            return (nan)
        original = sys.stdout
        try:
            os.mkdir("./"+name[:-len(name.split("/")[-1])])
            if verbose==True:
                print ("Creating directory to store permutations")
        except:
            if verbose==True:
                print ("Directory already available")
        order=random.choice(actionable_objects,num_actionable_obj,replace=False)
        if verbose==True:
            print ("Order of Acting:",[x.obj_id for x in order])
        sys.stdout = open('./'+name+'.txt', 'x')
        print("Generated Actions for plan")
        action_list=[]
        for obj1 in order:
            # Perform pickup action
            pro_flag,pro_zone,rule=verify_action(obj1,"prohibition","pickup",rules)
            if pro_flag==1: #If action is prohibited
                print ("Picking-up {}-{} object from Zone={} prohibited by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                per_flag,per_zone,rule=verify_action(obj1,"permission","pickup",rules)
                if per_flag==1 and pro_zone==per_zone: #If permission exists
                    print ("Picking-up {}-{} object from Zone={} permitted by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                    pickup_action(obj1).perform()
                    action_list.append(("pickup",obj1.obj_id))
                else:
                    print ("Action skipped")
                    continue
            else:
                pickup_action(obj1).perform()
                action_list.append(("pickup",obj1.obj_id))
            # Perform putdown action
            if obj1.last_action=="pickup": #Proceed to put down
                possible_zones=list(deepcopy(self.env[3]).keys())
                print("Possible zones: ")
                obl_flag,obl_zone,rule=verify_action(obj1,"obligation","putdown",rules)
                if obl_flag==1: #If obligation exists
                    print ("Putting-down {}-{} object in Zone-{} obligated by norm {}".format(obj1.colour,obj1.shape,obl_zone,rule))
                    per_flag,per_zone,rule=verify_action(obj1,"permission","putdown",rules)
                    if per_flag==1:
                        print ("But Putting-down {}-{} object in Zone-{} permitted by norm {}".format(obj1.colour,obj1.shape,per_zone,rule))
                        putdown_action(obj1,int(random.choice([obl_zone,per_zone])),self.task.target_area,self.env[3]).perform()
                        action_list.append(("putdown",obj1.obj_id,obj1.current_zone))
                    else:
                        putdown_action(obj1,obl_zone,self.task.target_area,self.env[3]).perform()
                        action_list.append(("putdown",obj1.obj_id,obl_zone))
                else:
                    pro_flag,pro_zone,rule=verify_action(obj1,"prohibition","putdown",rules)
                    if pro_flag==1: #If putting down is prohibited in pro_zone
                        print ("Putting down {}-{} object in Zone-{} prohibited by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                        per_flag,per_zone,rule=verify_action(obj1,"permission","putdown",rules)
                        if per_flag==1 and pro_zone==per_zone:
                            print ("Permission provided for putting down {}-{} object in Zone-{} by norm {}".format(obj1.colour,obj1.shape,per_zone,rule))
                            putdown_action(obj1,random.choice(possible_zones),self.task.target_area,self.env[3]).perform()
                            action_list.append(("putdown",obj1.obj_id,obj1.current_zone))
                        else:
                            # possible_zones.remove(int(pro_zone))
                            putdown_action(obj1,random.choice(possible_zones),self.task.target_area,self.env[3]).perform()
                            action_list.append(("putdown",obj1.obj_id,obj1.current_zone))
                    else:
                        #print ("I am King")
                        putdown_action(obj1,random.choice(possible_zones),self.task.target_area,self.env[3]).perform()
                        action_list.append(("putdown",obj1.obj_id,obj1.position.get_zone()))            
        sys.stdout.close()
        sys.stdout=original
        return (action_list) """


    def do_task(self,rules,permutation,copy_flag):
        """ Called by make permutations """
        from actions import pickup_action,putdown_action
        #from environment import position
        from verify_action_4 import verify_action
        import random
        from copy import deepcopy
        #from numpy import nan
        action_list=[]
        for obj in permutation:
            if copy_flag==0:
                obj1=deepcopy(obj)
            else:
                obj1=obj
            """ Perform pickup action """
            pro_flag,pro_zone,rule=verify_action(obj1,"prohibition","pickup",rules)
            if pro_flag==1: #If action is prohibited
                print ("Picing-up {}-{} object from Zone={} prohibited by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                per_flag,per_zone,rule=verify_action(obj1,"permission","pickup",rules)
                if per_flag==1 and pro_zone==per_zone: #If permission exists
                    print ("Picking-up {}-{} object from Zone={} permitted by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                    pickup_action(obj1).perform()
                    action_list.append(("pickup",obj1.obj_id))
                else:
                    continue
            else:
                # pickup_action(obj1).perform()
                action_list.append(("pickup",obj1.obj_id))
            """ Perform putdown action """
            if obj1.last_action=="pickup": #Proceed to put down
                obl_flag,new_zone,rule=verify_action(obj1,"obligation","putdown",rules)
                if obl_flag==1: #If obligation exists
                    print ("Putting-down {}-{} object in Zone-{} obligated by Norm-{}".format(obj1.colour,obj1.shape,new_zone,rule))
                    putdown_action(obj1,new_zone,self.task.target_area,self.env[3]).perform()
                    action_list.append(("putdown",obj1.obj_id,new_zone))
                else:
                    pro_flag,pro_zone,rule=verify_action(obj1,"prohibition","putdown",rules)
                    possible_zones=list(deepcopy(self.env[3]).keys())
                    if pro_flag==1: #If putting down is prohibited in pro_zone
                        print ("Putting down {}-{} object in Zone-{} prohibited by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,rule))
                        per_flag,per_zone,rule=verify_action(obj1,"permission","putdown",rules)
                        if per_flag==1 and pro_zone==per_zone:
                            print ("Permission provided for putting down {}-{} object in Zone-{} by norm {}".format(obj1.colour,obj1.shape,per_zone,rule))
                            putdown_action(obj1,random.choice(possible_zones),self.task.target_area,self.env[3]).perform()
                            action_list.append(("putdown",obj1.obj_id,new_zone))
                        else:
                            possible_zones.remove(pro_zone)
                            putdown_action(obj1,random.choice(possible_zones),self.task.target_area,self.env[3]).perform()
                            action_list.append(("putdown",obj1.obj_id,new_zone))
                    else:
                        #print ("I am King")
                        putdown_action(obj1,random.choice(possible_zones),self.task.target_area,self.env[3]).perform()
                        action_list.append(("putdown",obj1.obj_id,obj1.position.get_zone()))
        return (action_list)
    def make_permutations(self,rules,folder):
        """ Make permutations over of objects in Target Area and return possible action plans """
        import sys
        from itertools import permutations
        from task_completion_index import tci
        #from shutil import rmtree
        #from stat import S_IWUSR
        import pandas as pd
        import os
        from numpy import nan
        actionable_objects=[]
        (x1,y1)=self.task.target_area[0].coordinates()
        (x2,y2)=self.task.target_area[1].coordinates()
        for obj in self.env[0]:
            if (x1<=obj.position.x<=x2):
                if (y1<=obj.position.y<=y2):
                    if obj.colour in self.task.colour_specific:
                        if obj.shape in self.task.shape_specific:
                            actionable_objects.append(obj)
        num_actionable_obj=len(actionable_objects)
        print ("Found {} actionable objects".format(str(num_actionable_obj)))
        if (num_actionable_obj)==0:
            return (nan)
        permutation_list=list(permutations(actionable_objects)).copy()
        #perm_list_copy=perm_list.copy()
        print ("{} Permutations possible for given task".format(str(len(permutation_list))))
        task_df=pd.DataFrame()
        original = sys.stdout
        try:
            os.mkdir("./permutations/"+folder+"/")
            #print ("Creating directory to store permutations")
        except:
            pass
            #print ("Directory already available")
        for counter,permutation in enumerate(permutation_list,1):
            #print ("\nWriting actions for permutaion={} to file".format(str(counter)))
            sys.stdout = open('./permutations/'+folder+"/"+'permutation_{}.txt'.format(str(counter)), 'x')
            print("Generated Actions for permutation={}\n".format(str(counter)))
            task_df["permutation_{}".format(str(counter))]=self.do_task(rules,permutation,counter==len(permutation_list))
            sys.stdout.close()
            sys.stdout=original
        print ("-------------------------------------------")
        tci_val=tci(self.task,self.env,num_actionable_obj)
        task_df = task_df.append({"permutation_{}".format(str(i)) : "tci={:.2f}".format(tci_val) for i in range(1,counter+1)} , ignore_index=True)
        print ("       Task Completion Index={:.2f}".format(tci_val))
        print ("-------------------------------------------")
        return (task_df)
#TODO Non compliant = All- All_Compliant maybe
def all_compliant(rules,task,env,name,verbose=False):
    """ Return all possible compliant action given norms/rules """
    import sys
    from actions import pickup_action,putdown_action
    from verify_action_4 import verify_action
    from copy import deepcopy
    import os
    from numpy import nan,random
    from collections import defaultdict
    from rules_4 import obl_conds
    
    actionable_objects=[]
    (x1,y1)=task.target_area[0].coordinates()
    (x2,y2)=task.target_area[1].coordinates()
    for obj in env[0]:
        if (x1<=obj.position.x<=x2):
            if (y1<=obj.position.y<=y2):
                if obj.colour in task.colour_specific:
                    if obj.shape in task.shape_specific:
                        actionable_objects.append(obj)
    num_actionable_obj=len(actionable_objects)
    if verbose==True:
        print("Rules: ", rules)
        print ("Found {} actionable objects".format(str(num_actionable_obj)))
    if (num_actionable_obj)==0:
        return (nan)
    try: 
        #os.mkdir("./"+name[:-len(name.split("/")[-1])])
        if verbose==True:
            print ("Creating directory to store permutations")
    except:
        if verbose==True:
            print ("Directory already available")
    #Order of object action is chosen randomly everytime
    order=random.choice(actionable_objects,num_actionable_obj,replace=False)
    #if verbose==True:
        # print ("Order of Acting:",[x.obj_id for x in order])
    # with open('./'+name+'.txt', 'w') as f: # Mode was x. Why?
    # with redirect_stdout(f):
    action_pairs_by_obj=defaultdict(set)
    possible_zones_init=set(map(str, deepcopy(env[3]).keys()))
    for obj1 in order:
        oid = obj1.obj_id
        possible_zones=set(possible_zones_init)
        """ Perform pickup action """
        pro_flag,pro_zone,rule=verify_action(obj1,"prohibition","pickup",rules)
        if pro_flag==1: #If action is prohibited
            # print ("Picking-up {}-{} object from Zone={} prohibited by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
            per_flag,per_zone,rule=verify_action(obj1,"permission","pickup",rules)
            per_zones = possible_zones if per_zone == 'any' else {per_zone}
            if per_flag==1 and pro_zone in per_zones:  #If permission exists and overrides prohibition
                pass
                # print ("Picking-up {}-{} object from Zone={} permitted by norm: {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                # pickup_action(obj1).perform()
            else:
                #print ("Action skipped")
                continue
        else:
            pass # Was: pickup_action(obj1).perform() #This is needed to set obj1.last_action t0 "pickup"
        """ Perform putdown action """
        if True: # Was: obj1.last_action=="pickup": #Proceed to put down
            obl_flag,obl_zone,obl_rule = verify_action(obj1,"obligation","putdown",rules)
            if obl_flag==1: #If obligation exists
                #print ("Putting-down {}-{} object in Zone-{} obligated by norm {}".format(obj1.colour,obj1.shape,obl_zone,obl_rule))
                per_flag,per_zone,rule=verify_action(obj1,"permission","putdown",rules)
                if per_flag==1:
                    #print ("But Putting-down {}-{} object in Zone-{} permitted by norm {}".format(obj1.colour,obj1.shape,per_zone,rule))
                    per_zones = possible_zones if per_zone == 'any' else {per_zone}
                    # putdown_action(obj1,int(random.choice(tuple({obl_zone}|per_zones))),task.target_area,env[3]).perform()
                else:
                    per_zones = set()
                    # putdown_action(obj1,obl_zone,task.target_area,env[3]).perform()
                hist_conds, _ = obl_conds(obl_rule)
                for z in possible_zones:
                    if z in {obl_zone} | per_zones:
                        action_pairs_by_obj[oid].add(PossMove(("pickup",obj1.obj_id), ("putdown",obj1.obj_id,z)))
                    else:
                        action_pairs_by_obj[oid].add(PossMove(("pickup",obj1.obj_id), ("putdown",obj1.obj_id,z), unless=lists_to_tuples(hist_conds)))
            else:
                pro_flag,pro_zone,rule=verify_action(obj1,"prohibition","putdown",rules)
                if pro_flag==1: #If putting down is prohibited in pro_zone
                    # print ("Putting down {}-{} object in Zone-{} prohibited by norm {}".format(obj1.colour,obj1.shape,pro_zone,rule))
                    per_flag,per_zone,rule=verify_action(obj1,"permission","putdown",rules)
                    per_zones = possible_zones if per_zone == 'any' else {per_zone}
                    if per_flag==1 and pro_zone in per_zones:
                        pass
                        # print ("Permission provided for putting down {}-{} object in Zone-{} by norm {}".format(obj1.colour,obj1.shape,per_zone,rule))
                        # putdown_action(obj1,random.choice(tuple(possible_zones)),task.target_area,env[3]).perform()
                    else:
                        # print("removing {} from possible_zones: {}".format(pro_zone, possible_zones))
                        possible_zones.remove(pro_zone)
                        # putdown_action(obj1,random.choice(tuple(possible_zones)),task.target_area,env[3]).perform()
                #else:
                    #print ("I am King")
                    # putdown_action(obj1,random.choice(tuple(possible_zones)),task.target_area,env[3]).perform()
                #For all complying paths
                for z in possible_zones:
                    action_pairs_by_obj[oid].add(PossMove(("pickup",obj1.obj_id), ("putdown",obj1.obj_id,z)))
    return action_pairs_by_obj

def lists_to_tuples(x):
    if isinstance(x, list):
        return tuple(map(lists_to_tuples, x))
    else:
        return x

def gen_moves_from_all_compliant_dict(obj_order, compliant_moves_dict):
    move_options_in_order = [ list(map(lambda pm: (pm.pickup,pm.putdown), shuffled(compliant_moves_dict[o])))  for o in obj_order ]
    #print("Move options in order: ", move_options_in_order)
    for execution in product(*move_options_in_order):
        yield execution
        
def shuffled(seq):
    l = list(seq)
    random.shuffle(l)
    return l

        