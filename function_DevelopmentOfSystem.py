# -*- coding: utf-8 -*-
"""
Created on Wed May  8 20:22:53 2019

@author: chiilee

sub function  for plot_Develoopment.py
the most of function need: related parameters and the last vts number

"""

import sys
sys.path.append("/home/chiilee/git-flac/flac/util")
import numpy as np
import math
import flac
import flacmarker2vtk
fl=flac. Flac()

slab_phase=[1,3,7,19,5,13]
flacmarker2vtk.xmin=600
flacmarker2vtk.xmax=1800
flacmarker2vtk.zmin=-210
flacmarker2vtk.zmax=50

start_vts=1
L1=1000
L2=-200

def read_strenght(model_steps,trench_index,fys):
# calculate the cumulative strenght above 50 km
# cumulative strenght: GPa.m

    print ('caulate strenght profile')
    total_stress=[]
    dis=[]
    time=[]
    
    L=np.arange(L2,L1,5)
    for step in range(start_vts,model_steps+1):
        print(fl.time[step],'Myr')
       
        xmesh,zmesh=fl.read_mesh(step)
        x_len,z_len=xmesh.shape
        chamber=fl.read_chamber(step)
        vis = fl.read_visc(step)
        strainrate = fl.read_srII(step)
        pressure = fl.read_pres(step)
        den= fl.read_density(step)
        tem = fl.read_temperature(step)
        
        trench_location=xmesh[trench_index[step-1],0]        
        for kk in range (0,z_len):
                if zmesh[0,kk] > -50:
                    Z=kk                   
        for kk1 in range (0,len(L)):            
            for kk in range(0,x_len):
                if xmesh[kk,0] < (trench_location-L[kk1]):
                    X=kk        
                    
            total_Pn=0
            for kk in range(0,Z):
                if kk>0:
                    Pn=den[X,kk]*((zmesh[0,kk-1]-zmesh[0,kk])*1e+3)*9.8
                    total_Pn=total_Pn+Pn
                stressvis = 2*pow(10,strainrate[X,kk])*pow(10,vis[X,kk])
                stressy = 4e7 + 0.577* total_Pn
                if (chamber[X,kk]>0.24):
                    stressy= stressy*fys
                P=min(stressvis,stressy)
                if kk>0:
                    total_P=total_P+ P*(zmesh[0,kk-1]-zmesh[0,kk])*1e+3
                else:
                    total_P=P
            
            total_stress.append(math.log10(total_P*1e-9))
            dis.append(L[kk1])
            time.append(fl.time[step])

    return total_stress, dis, time

    
def read_topo(model_steps,trench_index):
    print ('caulate topo')
    topo=[]
    dis=[]
    time=[]
    
    L=np.arange(L2,L1,5)
    for step in range(start_vts,model_steps+1):
        print(fl.time[step],'Myr')
       
        xmesh,zmesh=fl.read_mesh(step)
        x_len,z_len=xmesh.shape
        #chamber=fl.read_chamber(step)
        trench_location=xmesh[trench_index[step-1],0]    
                 
        for kk1 in range (0,len(L)):
            
            for kk in range(0,x_len):
                if xmesh[kk,0] < (trench_location-L[kk1]):
                    X=kk        
                    
            topo.append(zmesh[X,0]-zmesh[0,0])
            dis.append(L[kk1])
            time.append(fl.time[step])
            #print(depth,stress,total_stress)

    return topo, dis, time  

def read_phase(model_steps,trench_index):
    print ('read surface phase')
    phase=[]
    dis=[]
    time=[]
    
    L=np.arange(L2,L1,5)
    for step in range(start_vts,model_steps+1):
        print(fl.time[step],'Myr')
       
        xmesh,zmesh=fl.read_mesh(step)
        x_len,z_len=xmesh.shape
        Phase=fl.read_phase(step)
        trench_location=xmesh[trench_index[step-1],0]    

                    
        for kk1 in range (0,len(L)):           
            for kk in range(0,x_len):
                if xmesh[kk,0] < (trench_location-L[kk1]):
                    X=kk        
                    
            phase.append(Phase[X,0])
            dis.append(L[kk1])
            time.append(fl.time[step])
    return phase, dis, time  


def read_meltvol(model_steps,trench_index,depth):
    print ('caulate M profile at',depth,' km' )
    chamberM=[]
    dis=[]
    time=[]
    
    L=np.arange(L2,L1,5)
    for step in range(start_vts,model_steps+1):
        print(fl.time[step],'Myr')
       
        xmesh,zmesh=fl.read_mesh(step)
        x_len,z_len=xmesh.shape
        chamber=fl.read_chamber(step)
        
        trench_location=xmesh[trench_index[step-1],0]        
        for kk in range (0,z_len):
                if zmesh[0,kk] > -1*depth:
                    Z=kk            
                    
        for kk1 in range (0,len(L)):
            
            for kk in range(0,x_len):
                if xmesh[kk,0] < (trench_location-L[kk1]):
                    X=kk        
                    
            chamberM.append(chamber[X,Z])
            dis.append(L[kk1])
            time.append(fl.time[step])
            #print(depth,stress,total_stress)

    return chamberM, dis, time
    
def read_srII(model_steps,trench_index,depth):
    print ('caulate strain rate profile at',depth, ' km' )
    srII=[]
    dis=[]
    time=[]
    
    L=np.arange(L2,L1,5)
    for step in range(start_vts,model_steps+1):
        print(fl.time[step],'Myr')
       
        xmesh,zmesh=fl.read_mesh(step)
        x_len,z_len=xmesh.shape
        sII=fl.read_srII(step)
        
        trench_location=xmesh[trench_index[step-1],0]       
        
        for kk in range (0,z_len):
                depth11 = zmesh[0,0]-zmesh[0,kk]
                if depth11 < depth:
                    Z=kk            
                #print(Z,zmesh[0,0]-zmesh[0,Z])    
        for kk1 in range (0,len(L)):
            
            for kk in range(0,x_len):
                if xmesh[kk,0] < (trench_location-L[kk1]):
                    X=kk        
                    
            srII.append(sII[X,Z])
            dis.append(L[kk1])
            time.append(fl.time[step])
            #print(depth,stress,total_stress)

    return srII, dis, time