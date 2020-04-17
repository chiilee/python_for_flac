# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:24:19 2019

@author: chiilee
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

def find_interpolate(X,Y,deltaX):    
    newX = np.arange(0,max(X),deltaX)
    newY = [0]*len(newX)
    
    for kk1 in range(0,len(newX)-1):
        for kk2 in range(0,len(X)-1):
            if newX[kk1]>=X[kk2] and newX[kk1]<X[kk2+1]:
                ratio=(newX[kk1]-X[kk2])/(X[kk2+1]-X[kk2])
                newY[kk1]=Y[kk2]*(1-ratio)+Y[kk2+1]*ratio
    return newX,newY

def weak_strenght(D,T,fv,fys):
    S=[]
    SW=[]
    
    epsilon=1e-15
    g=9.8
    R=8.315
    
    for kk in range(len(D)):
        if D[kk]<=10:
            #phase=7,OC
            cohesion=4e+7/10
            phi=30/2
            density=2880
            A=1.25e-1
            n=3.05
            E=3.76e+5
        else:
            #phase=4, olivine
            cohesion=4e+7/10
            phi=30/2
            density=3300
            A=7.00e+4
            n=3.00
            E=6.00e+5
        eta=0.25*(4/(3*A))**(1/n)*epsilon**((1-n)/n)*math.exp(E/(n*R*(T[kk]+273)))*fv
        if (eta > 3e+27): 
            eta=3e+27
        if (eta < 1e+19) :
            eta=1e+19
        sigma_visc=2*eta*epsilon
        sigma_plast=cohesion+math.tan(math.radians(phi))*density*(D[kk]*1e+3)*g
        #sigma_plast2=cohesion*fys
        sigma_plast2=sigma_plast*fys            
        #sigma_plast2=cohesion*fys+math.tan(math.radians(3))*density*(D[kk]*1e+3)*g 
        S.append(min(sigma_visc,sigma_plast)*1e-6)
        SW.append(min(sigma_visc,sigma_plast2)*1e-6)
    return S,SW
  
t_rate =np.arange(0,1400,200)
depth_rate=[0,8,16,26,37,50,72]
D,T=find_interpolate(depth_rate,t_rate,0.1)
  
  
fig1_1=plt.figure(figsize=(5,8))
ax1 = fig1_1.add_subplot(111)
#ax2 = ax1.twiny()

S1_,S1=weak_strenght(D,T,1,1)
S2_,S2=weak_strenght(D,T,1,0.5)
S3_,S3=weak_strenght(D,T,0.5,1)
S4_,S4=weak_strenght(D,T,0.5,0.5)

line1 = ax1.plot(S1_ , D, '-', color='#CC0000', label = 'Orig.',  lw=4)
line2 = ax1.plot(S1, D, '-',color='#FF5511', label = 'fv=1  , fys=1',  lw=2)
line3 = ax1.plot(S2, D, '-',color='#227700', label = 'fv=1  , fys=0.5',  lw=2)
line4 = ax1.plot(S3, D, '--',color='#0066FF', label = 'fv=0.5, fys=1',  lw=2)
line5 = ax1.plot(S4, D, '--',color='#7700BB', label = 'fv=0.5, fys=0.5',  lw=2)

# added these three lines
lines = line1+line2+line3+line4+line5
labs = [l.get_label() for l in lines]
ax1.legend(lines, labs, loc=4,fontsize=15) 

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax1.grid()
ax1.set_xlabel("Strength (MPa)", fontsize=20)
ax1.set_xlim(0,400)
ax1.set_ylabel(r"Depth (km)", fontsize=20)
ax1.set_ylim(30,0)
plt.text(260,2,r'$\epsilon$=1e-15',fontsize=20)
#ax2.set_xlabel(r"length (km)")
#ax2.set_ylim(0,5000)