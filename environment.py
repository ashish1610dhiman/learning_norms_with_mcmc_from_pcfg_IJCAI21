# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:33:21 2019

@author: dhias426
"""
#import matplotlib.pyplot as plt
import random
import numpy as np

class position():
    """ Class to represent position of objects """
    def __init__(self,x,y):
        #theta is in degreees
        self.x=x
        self.y=y 
    def get_distance(self,point):
        if isinstance(point,position):
            return (((self.x-point.x)**2+(self.y-point.y)**2)**0.5)
        else:
            print ("Point must be an instance of position")
            return (np.nan)
    def coordinates(self):
        return (self.x,self.y)
    def get_zone(self):
        if self.x<=-1/3:
            return (1)
        elif self.x<=1/3:
            return (2)
        else:
            return (3)
        

class an_object():
    """ Class to model objects """
    def __init__(self,obj_id,position,colour,shape,last_action=np.nan):
        self.obj_id=obj_id
        self.position=position
        self.colour=colour
        self.shape=shape
        self.last_action=last_action
        self.current_zone=self.position.get_zone()
    def describe(self):
        print("Object {}: color={},shape={},current_zone={},last_action={}".format(self.obj_id,self.colour,self.shape,self.current_zone,self.last_action))
    def _repr_(self):
        return "(Object {}: color={},shape={},current_zone={},last_action={})".format(self.obj_id,self.colour,self.shape,self.current_zone,self.last_action)

def polar_to_cartesian(position):
    from math import sin,cos,radians
    return(position.r*cos(radians(position.theta)),position.r*sin(radians(position.theta)))        
        
def create_env(N=20,seed=np.nan):
    """ Create N objects randomly in environment """
    colours=["r","g","b"]
    shapes=["square","circle","triangle"]
    if not np.isnan(seed):
        random.seed(seed)
    object_list=[]
    zones={i:-1+i*(2/3) for i,colour in enumerate(colours,1)}
    for i in range(N):
        # To prevent two point from being too close
        while (True):
            p=position(round(random.uniform(-1,1),2),round(random.uniform(-1,1),2))
            if len(object_list)>0:
                t=[int(p.get_distance(obj.position)<=0.1) for obj in object_list]
                if sum(t)==0:
                    break
            else:
                break
        c=colours[random.randint(0,2)]
        s=shapes[random.randint(0,2)]
        object_list.append(an_object(i+1,p,c,s))
    return (object_list,colours,shapes,zones)

# Indices in the env. object list are one less than the object IDs!
def get_obj(id,env):
    return env[0][id-1]


def plot_env(env,ax,itr=np.nan,legend=False,annotate=True):
    """ Helper function to plot environment """
    ax.set_xlim(-1.1,1.1)
    ax.set_ylim(-1.1,1.1)
    shape_code={"square":"s","circle":"o","triangle":"v"}
    for obj in env[0]:
        (x,y)=(obj.position.coordinates())
        if obj.last_action=="pickup":
            ax.scatter(x,y,c="white",marker=shape_code[obj.shape],facecolor="white",edgecolor=obj.colour,linewidths=0.97,alpha=0.7,label='_nolegend_')
            if annotate==True:
                ax.annotate(obj.obj_id,(x,y),(x+0.016,y+0.016),fontsize=7,weight="light")
        else:
            ax.scatter(x,y,c=obj.colour,marker=shape_code[obj.shape],label='_nolegend_')
            if annotate==True:
                ax.annotate(obj.obj_id,(x,y),(x+0.016,y+0.016),fontsize=7,weight="light")
    ax.set_xlabel("X_coordinate")
    ax.set_ylabel("Y_coordinate")
    for col,pt in env[-1].items():
        if legend==True:
            ax.axvspan(-2/3+pt,pt,color=env[1][col-1],alpha=0.097,label="Zone-{}".format(col))
        else:
            ax.axvspan(-2/3+pt,pt,color=env[1][col-1],alpha=0.07,label='_nolegend_')
    if type(itr)==float:
        ax.title.set_text("Current state of Simulated Environment\n Number of objects={}".format(len(env[0])))
    else:
        ax.title.set_text("{}\n Number of objects={}".format(itr,len(env[0])))
    if legend==True:
        ax.legend()

    
def plot_area(ax,target_area=np.nan,destination_area=np.nan):
    """ Helper function to plot target area """
    import matplotlib.patches as patches
    if type(target_area)==list:
        rect_t = patches.Rectangle((target_area[0].x,target_area[0].y),abs(target_area[0].x-target_area[1].x),
                           abs(target_area[0].y-target_area[1].y),linewidth=1,edgecolor='k',
                           facecolor=(32/255,178/255,170/255,0.25))
        ax.add_patch(rect_t)
    if type(destination_area)==list:
        rect_p = patches.Rectangle((destination_area[0].x,destination_area[0].y),abs(destination_area[0].x-destination_area[1].x),
                           abs(destination_area[0].y-destination_area[1].y),linewidth=1,edgecolor='k',
                           facecolor=(240/255,230/255,140/255,0.43))
        ax.add_patch(rect_p)
    



# =============================================================================
# fig,axs=plt.subplots(3,3,sharex=True, sharey=True,figsize=(14,9))
# plt.suptitle("Simulated Environment")
# counter=1
# for i in [0,1,2]:
#     for j in [0,1,2]:
#         env=create_env(seed=random.uniform(1,550))
#         plot_env(env,axs[i][j],counter)
#         counter+=1
# =============================================================================
    
    