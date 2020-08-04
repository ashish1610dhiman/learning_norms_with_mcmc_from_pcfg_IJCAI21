# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:17:19 2019

@author: dhias426
"""
class pickup_action():
    def __init__(self,obj):
        self.obj=obj # Object on which action is to be performed
    def perform(self):
        if self.obj.last_action!="pickup":
            self.obj.last_action=="pickup"
            print ("Object picked up")
        else:
            print ("Object already picked up")
            
class move_action():
    def __init__(self,obj,new_position):
        self.obj=obj
        self.new_position=new_position
    def perform(self):
        if self.obj.last_action!="pickup":
            print ("Picking up object, since it was not picked up")
            pickup_action(self.obj).perform()
        self.obj.position=self.new_position
        self.obj.last_action="move"
        print ("Moved object to new position")
        

class throw_action():
    def __init__(self,obj,obj_list):
        self.obj=obj
        self.obj_list
    def perform(self):
        if self.obj.last_action!="pickup":
            print ("Picking up object, since it was not picked up")
            pickup_action(self.obj).perform()
        self.obj.last_action="throw"
        self.obj_list.remove(self.obj)
        print ("Trashing object")
        return (self.obj_list)


                
            
        