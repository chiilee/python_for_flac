# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:04:37 2019

@author: chiilee
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#time(Myr), vel(cm/yr)
time=[0,2.5,7.5,12.5,17.5,22.5,27.5,32.5,37.5,42.5,47.5]
vel=[0,35,21,2,3,4,12,13,12,10,4]
#vel =[0,32,16,1,1,5,10.5,9,8,10,6] #mariana1500
#vel =[0,18,4,6.5,4,9,11,7,8,8,6]#mariana2000

print(len(time),len(vel))

def find_vel(time,vel,deltaT):    
    T = np.arange(0,max(time),deltaT)
    V = [0]*len(T)
    
    for kk1 in range(0,len(T)-1):
        for kk2 in range(0,len(time)-1):
            if T[kk1]>=time[kk2] and T[kk1]<time[kk2+1]:
                ratio=(T[kk1]-time[kk2])/(time[kk2+1]-time[kk2])
                V[kk1]=vel[kk2]*(1-ratio)+vel[kk2+1]*ratio
    return T,V

def find_len (time,vel):
    #INPUT:time(Myr), vel(cm/yr)
    #OUTPUT:len(km)    
    L = [0]
    templ = 0
    
    for kk in range(1,len(time)):
        l=(time[kk]-time[kk-1])*vel[kk]*1e+6*1e-5
        templ=templ+l
        L.append(templ)
    return L


T,V = find_vel(time,vel,0.1)
L = find_len(T,V)

fig1_1=plt.figure(figsize=(8,4))
ax1 = fig1_1.add_subplot(111)
ax2 = ax1.twinx()

line1 = ax1.plot(T, V, '-r', label = 'convergence rate',  lw=2)
line2 = ax2.plot(T, L, '-g', label = 'subducting length',  lw=2)

# added these three lines
lines = line1+line2
labs = [l.get_label() for l in lines]
ax1.legend(lines, labs, loc=2) 

ax2.grid()
ax1.set_xlabel("Time (Myr))")
ax1.set_xlim(0,max(time))
ax1.set_ylabel(r"velocity (cm/yr)")
ax1.set_ylim(0,35)
ax2.set_ylabel(r"length (km)")
ax2.set_ylim(0,5000)


