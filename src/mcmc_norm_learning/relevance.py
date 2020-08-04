# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 18:14:10 2019

@author: dhias426
"""


def is_relevant(expression,task1,env,verbose=False):
    """ Return True if task is relevant to expression """
    from copy import deepcopy
    from robot_task_new import robot
    from algorithm_2_utilities import violation
    #Find all the actionable objects of the task in norm
    actionable_objects=robot(task1,deepcopy(env)).all_actionable()
    #Find all the violations of the norm on task
    violations=violation(expression,env)
    violation_objects=set(list(violations.keys()))
    actionable_objects=set(actionable_objects)
    relevant=len(violation_objects & actionable_objects)>0
    if verbose==True:
        print ("Number of actionable objects for given task on environment:{}".format(len(actionable_objects)))
        print ("The task is relevant:{}".format(relevant))
    return (relevant)