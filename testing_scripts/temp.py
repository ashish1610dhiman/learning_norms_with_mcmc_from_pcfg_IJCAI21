# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:29:33 2019

@author: dhias426
"""

import matplotlib.pyplot as plt
r1=[]
g1=[]
b1=[]
for i in range(1,1001):
    r1.append(sum(r[:i])/i)
    g1.append(sum(g[:i])/i)
    b1.append(sum(b[:i])/i)

    
plt.plot(range(1,1001),r1,label="Average Probability of r showing up",color='r',linestyle="--",marker=".",alpha=0.5)
plt.plot(range(1,1001),g1,label="Average Probability of g showing up",color='g',linestyle="--",marker=".",alpha=0.5)
plt.plot(range(1,1001),b1,label="Average Probability of b showing up",color='b',linestyle="--",marker=".",alpha=0.5)
plt.axhline(0.33,c="k",label="0.33")
plt.xlabel("Number of Trials")
plt.ylabel("Average Probability")
plt.legend()
