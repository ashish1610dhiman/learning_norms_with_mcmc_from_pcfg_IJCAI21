# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:17:19 2019

@author: dhias426
"""

import weakref

class pickup_action():
    def __init__(self,obj):
        self.obj=obj # Object on which action is to be performed
        self.id=weakref.ref(obj)
    def perform(self):
        if self.obj.last_action!="pickup":
            self.id().last_action="pickup"
            print ("{}-{}:object-{} picked up".format(self.obj.colour,self.obj.shape,self.obj.obj_id))
        else:
            print ("{}-{}:object-{} already picked up".format(self.obj.colour,self.obj.shape,self.obj.obj_id))

class putdown_action():
    def __init__(self,obj,new_zone,ta,zone_dict):
        from environment import position
        import random
        self.obj=obj
        self.new_zone=new_zone
        y1=ta[0].y
        y2=ta[1].y
        y_new=random.uniform(-1,1)
        while y1<=y_new<=y2:
            y_new=random.uniform(-1,1)
        self.new_position=position(random.uniform(zone_dict[int(new_zone)]-2/3,zone_dict[int(new_zone)]),y_new)
        self.id=weakref.ref(obj)
    def perform(self):
        from actions import pickup_action
        if self.obj.last_action!="pickup":
            print ("Picking up {}-{}:object-{}, since it was not picked up".format(self.obj.colour,self.obj.shape,self.obj.obj_id))
            pickup_action(self.obj).perform()
        self.id().position=self.new_position
        self.id().last_action="put_down"
        self.id().current_zone=self.new_zone
        print ("Object {}:{}-{} put-down in zone-{}\n".format(self.obj.colour,self.obj.shape,self.obj.obj_id,self.new_zone))


            
# =============================================================================
# class move_action():
#     def __init__(self,obj,new_position):
#         self.obj=obj
#         self.new_position=new_position
#         self.id=weakref.ref(obj)
#     def perform(self):
#         from actions import pickup_action
#         if self.obj.last_action!="pickup":
#             print ("Picking up {}-{} object, since it was not picked up".format(self.obj.colour,self.obj.shape))
#             pickup_action(self.obj).perform()
#         self.id().position=self.new_position
#         self.id().last_action="move"
#         print ("Moved {}-{} object to new position\n".format(self.obj.colour,self.obj.shape))
#         
# 
# class throw_action():
#     def __init__(self,throw_obj_list,obj_list):
#         self.throw_obj_list=throw_obj_list
#         self.obj_list=obj_list
#     def perform(self):
#         from actions import pickup_action
#         for obj in self.throw_obj_list:
#             id1=weakref.ref(obj)
#             if obj.last_action!="pickup":
#                 print ("Picking up {}-{} object, since it was not picked up".format(obj.colour,obj.shape))
#                 pickup_action(obj).perform()
#             if obj in self.obj_list:
#                 id1().last_action="throw"
#                 self.obj_list.remove(obj)
#                 print ("Throwing {}-{} object\n".format(obj.colour,obj.shape))
#             #return (self.obj_list)
#             else:
#                 print ("{}-{} object not in list\n".format(obj.colour,obj.shape))
# =============================================================================


                
            
        