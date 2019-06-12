# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:43:38 2019

@author: dhias426
"""

import numpy as np



class task():
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
    #import matplotlib.pyplot as plt
    from numpy import nan
    from environment import plot_env,plot_area
    plot_env(env,ax,itr,legend=False,annotate=annotate_choice)
    plot_area(ax,task.target_area,nan)
    ax.legend(["Target Area"])

class robot():
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
    def perform_task(self,rules,name):
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
        print ("Found {} actionable objects".format(str(num_actionable_obj)))
        if (num_actionable_obj)==0:
            return (nan)
        original = sys.stdout
        try:
            os.mkdir("./permutations/")
            print ("Creating directory to store permutations")
        except:
            print ("Directory already available")
        order=random.choice(actionable_objects,num_actionable_obj,replace=False)
        print ("Order of Acting:",[x.obj_id for x in order])
        sys.stdout = open('./permutations/'+name+'.txt', 'x')
        print("Generated Actions for plan")
        action_list=[]
        for obj1 in order:
            """ Perform pickup action """
            pro_flag,pro_zone,key=verify_action(obj1,"prohibition","pickup",rules)
            if pro_flag==1: #If action is prohibited
                print ("Picing-up {}-{} object from Zone={} prohibited by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,key))
                per_flag,per_zone,key=verify_action(obj1,"permission","pickup",rules)
                if per_flag==1 and pro_zone==per_zone: #If permission exists
                    print ("Picking-up {}-{} object from Zone={} permitted by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,key))
                    pickup_action(obj1).perform()
                    action_list.append(("pickup",obj1.obj_id))
                else:
                    print ("Action skipped")
                    continue
            else:
                pickup_action(obj1).perform()
                action_list.append(("pickup",obj1.obj_id))
            """ Perform putdown action """
            if obj1.last_action=="pickup": #Proceed to put down
                obl_flag,new_zone,key=verify_action(obj1,"obligation","putdown",rules)
                if obl_flag==1: #If obligation exists
                    print ("Putting-down {}-{} object in Zone-{} obligated by Norm-{}".format(obj1.colour,obj1.shape,new_zone,key))
                    putdown_action(obj1,new_zone,self.task.target_area,self.env[3]).perform()
                    action_list.append(("putdown",obj1.obj_id,int(new_zone)))
                else:
                    pro_flag,pro_zone,key=verify_action(obj1,"prohibition","putdown",rules)
                    possible_zones=list(deepcopy(self.env[3]).keys())
                    if pro_flag==1: #If putting down is prohibited in pro_zone
                        print ("Putting down {}-{} object in Zone-{} prohibited by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,key))
                        per_flag,per_zone,key=verify_action(obj1,"permission","putdown",rules)
                        if per_flag==1 and pro_zone==per_zone:
                            print ("Permission provided for putting down {}-{} object in Zone-{}  by Norm-{}".format(obj1.colour,obj1.shape,per_zone,key))
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
        sys.stdout.close()
        sys.stdout=original
        return (action_list)
    def do_task(self,rules,permutation,copy_flag):
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
            pro_flag,pro_zone,key=verify_action(obj1,"prohibition","pickup",rules)
            if pro_flag==1: #If action is prohibited
                print ("Picing-up {}-{} object from Zone={} prohibited by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,key))
                per_flag,per_zone,key=verify_action(obj1,"permission","pickup",rules)
                if per_flag==1 and pro_zone==per_zone: #If permission exists
                    print ("Picking-up {}-{} object from Zone={} permitted by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,key))
                    pickup_action(obj1).perform()
                    action_list.append(("pickup",obj1.obj_id))
                else:
                    continue
            else:
                pickup_action(obj1).perform()
                action_list.append(("pickup",obj1.obj_id))
            """ Perform putdown action """
            if obj1.last_action=="pickup": #Proceed to put down
                obl_flag,new_zone,key=verify_action(obj1,"obligation","putdown",rules)
                if obl_flag==1: #If obligation exists
                    print ("Putting-down {}-{} object in Zone-{} obligated by Norm-{}".format(obj1.colour,obj1.shape,new_zone,key))
                    putdown_action(obj1,new_zone,self.task.target_area,self.env[3]).perform()
                    action_list.append(("putdown",obj1.obj_id,new_zone))
                else:
                    pro_flag,pro_zone,key=verify_action(obj1,"prohibition","putdown",rules)
                    possible_zones=list(deepcopy(self.env[3]).keys())
                    if pro_flag==1: #If putting down is prohibited in pro_zone
                        print ("Putting down {}-{} object in Zone-{} prohibited by Norm-{}".format(obj1.colour,obj1.shape,pro_zone,key))
                        per_flag,per_zone,key=verify_action(obj1,"permission","putdown",rules)
                        if per_flag==1 and pro_zone==per_zone:
                            print ("Permission provided for putting down {}-{} object in Zone-{}  by Norm-{}".format(obj1.colour,obj1.shape,per_zone,key))
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
        """ Make permutations over of objects in Target Area """
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
            print ("Creating directory to store permutations")
        except:
            print ("Directory already available")
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
        
            
        
        