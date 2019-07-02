# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:05:23 2019

@author: dhias426
"""

def aggregate(directory,order_plan):
    import os
    from itertools import product
    import sys
    import pandas as pd
    files=os.listdir("./permutations/"+directory)
    files=[x for x in files if "jpeg" not in x]
    try:
        os.mkdir("./action_profile/"+directory+"/")
        print ("Creating directory to store Action plans")
    except:
        print ("Directory already available")
    #Find number of subtasks
    num_subtasks=max(order_plan.keys())
    subtask_files=[]
    for subtask in range(1,int(num_subtasks)+1):
        subtask_files.append([file for file in files if "subtask_{}".format(subtask) in file])
    total_combinations=list(product(*subtask_files))
    print("Total combinations possible={}".format(str(len(total_combinations))))
    action_plans=pd.DataFrame()
    original = sys.stdout
    for counter,combination in enumerate(total_combinations,1):
        plan=[]
        tci=1
        print ("Genrating Action profile for combination={}".format(counter))
        sys.stdout = open('./action_profile/'+directory+'/action_profile_{}.txt'.format(str(counter)), 'x')
        for i in range(0,int(num_subtasks)):
            print (combination[i][:-4])
        print()
        for i in range(int(num_subtasks)):
            temp=order_plan[i+1][combination[i].split("__")[-1][:-4]]
            plan=plan+list(temp[0:-1])
            tci=tci*float(temp.iloc[-1].split("=")[-1])
            file=open('./permutations/'+directory+'/'+combination[i])
            lines=file.readlines()
            for line in lines:
                if "object" in line:
                    if "not picked" not in line:
                        print (line)
        plan.append("tci={:.3f}".format(tci))
        action_plans["combination_{}".format(str(counter))]=plan
        sys.stdout=original
    action_plans.to_csv('./action_profile/'+directory+'/'+"Action_plan_{}.csv".format(directory.split('/')[1]))
    return (action_plans)



if __name__== "__main__":
    import sys
    if len(sys.argv)!=2:
        print("Wrong number of arguments")
    else:
        directory=sys.argv[1]
        aggregate(directory)