# -*- coding: utf-8 -*-
"""
Created on Fri May 17 13:43:38 2019

@author: dhias426
"""

import numpy as np



class task():
    def __init__(self,task_type,colour_specific=np.nan,shape_specific=np.nan,target_area=np.nan,destination_area=np.nan):
        self.task_type=task_type
        self.colour_specific=colour_specific
        self.shape_specific=shape_specific
        self.target_area=target_area
        self.destination_area=destination_area
    def print_task(self):
        print ("---------------------------------")
        print (self.task_type.upper())
        print(self.colour_specific)
        print(self.shape_specific)
        print ("---------------------------------")

def plot_task(plt,env,ax,itr,task):
    #import matplotlib.pyplot as plt
    from environment import plot_env,plot_area
    plot_env(env,ax,itr,legend=False)
    plot_area(ax,task.target_area,task.destination_area)
    if task.task_type=='move':
        plt.legend(["Target Area","Destination Area"])
    else:
        plt.legend(["Target Area"])

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
    def do_task(self,rules,permutation,copy_flag):
        from actions import throw_action,move_action,pickup_action
        from environment import position
        from verify_action import verify_action
        import random
        from copy import deepcopy,copy
        from numpy import nan
        flag=1
        empty_rules=(len(rules)==0)
        action_list=[]
        if self.task.task_type=="move":
            (x3,y3)=self.task.destination_area[0].coordinates()
            (x4,y4)=self.task.destination_area[1].coordinates()
            for obj in permutation:
                if empty_rules==False:
                    flag,junk,key=verify_action(obj,self.task.task_type,rules)
                #print ("flag="+str(flag))
                if flag==1:
                    if copy_flag==0:
                        obj1=deepcopy(obj)
                    else:
                        obj1=obj
                    x_new=((x3+x4)/2)+random.uniform(-(x4-x3)/2,(x4-x3)/2)
                    y_new=((y3+y4)/2)+random.uniform(-(y4-y3)/2,(y4-y3)/2)
                    move_action(obj1,position(x_new,y_new)).perform()
                    action_list.append(("move",obj1.obj_id,obj1.position.coordinates()))
                else:
                    print ("Norm:{} invoked on {}-{} object".format(key,obj.colour,obj.shape))
                    print ("{} action on {}-{} object skipped\n".format("Move",obj.colour,obj.shape))
        elif self.task.task_type=="throw":
            for obj in permutation:
                if empty_rules==False:
                    flag,junk,key=verify_action(obj,self.task.task_type,rules)
                if flag==1:
                    temp_env=copy(self.env[0])
                    if copy_flag==0:
                        obj1=obj
                    else:
                        obj1=obj
                        temp_env=self.env[0]
                    throw_action([obj1],temp_env).perform()
                    action_list.append(("throw",obj1.obj_id,nan))
                else:
                    print ("Norm:{} invoked on {}-{} object".format(key,obj.colour,obj.shape))
                    print ("{} action on {}-{} object skipped\n".format("Trash",obj.colour,obj.shape))
        else:
            for obj in permutation:
                if empty_rules==False:
                    (flag,task,key)=verify_action(obj,self.task.task_type,rules)
                else:
                    flag=0
                if copy_flag==0:
                    obj1=obj
                    temp_env=copy(self.env[0])
                else:
                    obj1=obj
                    temp_env=self.env[0]
                if flag==1:
                    pickup_action(obj1).perform()
                    action_list.append(("pickup",obj.obj_id,nan))
                    print ("Norm:{} invoked on {}-{} object(s)".format(key,obj.colour,obj.shape))
                    if task=="move":
                        move_action(obj1,position(random.uniform(-2/3+self.env[-1][obj.colour],self.env[-1][obj.colour]),random.uniform(-1,1))).perform()
                        action_list.append(("move",obj1.obj_id,obj1.position.coordinates()))
                    if task=="trash":
                        throw_action([obj1],temp_env).perform()
                        action_list.append(("throw",obj1.obj_id,nan))
                if flag==0:
                    #print ("ABC")
                    pickup_action(obj1).perform()
                    action_list.append(("pickup",obj.obj_id,nan))
                    print ()
        return (action_list)
    def make_permutations(self,rules,subtask,folder):
        import sys
        from itertools import permutations
        from task_completion_index import tci
        from shutil import rmtree
        from stat import S_IWUSR
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
        print ("{} Permutations possible for subtask={}".format(str(len(permutation_list)),str(subtask)))
        task_df=pd.DataFrame()
        original = sys.stdout
        try:
            os.mkdir("./permutations/"+folder+"/")
            print ("Creating directory to store permutations")
        except:
            print ("Directory already available")
        for counter,permutation in enumerate(permutation_list,1):
            #print ("\nWriting actions for permutaion={} to file".format(str(counter)))
            sys.stdout = open('./permutations/'+folder+"/"+'subtask_{}__permutation_{}.txt'.format(str(subtask),str(counter)), 'x')
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
        
            
        
        