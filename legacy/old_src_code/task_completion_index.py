# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:34:20 2019

@author: dhias426
"""
def in_target_area(obj,task):
    (x1,y1)=(task.target_area[0].x,task.target_area[0].y)
    (x2,y2)=(task.target_area[1].x,task.target_area[1].y)
    if (x1<=obj.position.x<=x2):
        if (y1<=obj.position.y<=y2):
            if obj.colour in task.colour_specific:
                if obj.shape in task.shape_specific:
                    return (1)
    return (0)


def in_dest_area(obj,task):
    (x3,y3)=(task.destination_area[0].x,task.destination_area[0].y)
    (x4,y4)=(task.destination_area[1].x,task.destination_area[1].y)
    if (x3<=obj.position.x<=x4):
        if (y3<=obj.position.y<=y4):
            if obj.colour in task.colour_specific:
                if obj.shape in task.shape_specific:
                    return (1)
    return (0)



def tci(task,env,num_actionable_obj):
    from task_completion_index import in_target_area
    not_cleared=0
    for obj in env[0]:
        if in_target_area(obj,task):
            not_cleared=+1
        return (1-(not_cleared/num_actionable_obj))
                
        
            
        
                
        