# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:36:42 2018

@author: chiilee
"""

import sys
sys.path.append("/home/chiilee/git-flac/flac/util")
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

'''
simple function which can help to read the parameters
'''
def read_depth(z_array,x_index,z_index):
# get the deep of mesh(x,z)
    depth=z_array[x_index,0]-z_array[x_index,z_index]
    return depth
    
def read_area(xmesh,zmesh,x_index,z_index):
# get the total area of element(x,z) 

#    1(i,j) --------------- 2(i+1,j)
#           |             |
#           |    area     |
#           |             |
#  4(i,j+1) --------------- 3(i+1,j+1)   
#
    x1 = xmesh[x_index,z_index]
    y1 = zmesh[x_index,z_index]
    x2 = xmesh[x_index,z_index+1]
    y2 = zmesh[x_index,z_index+1]
    x3 = xmesh[x_index+1,z_index+1]
    y3 = zmesh[x_index+1,z_index+1]
    x4 = xmesh[x_index+1,z_index]
    y4 = zmesh[x_index+1,z_index]
    area1 = ((x1-x2)*(y3-y2))-((x3-x2)*(y1-y2))
    area2 = ((x1-x4)*(y3-y4))-((x3-x4)*(y1-y4))    
    area = (abs(area1)+abs(area2))*0.5           

    return area
    
    
def mxmz_adjust(mx,mi,mj,mt,time)  :
# adjust to sort by time

    mz=[]
    for kk in range(0,len(mx)): 
        for  kk2 in range(0,len(time)-1):
            if mt[kk]>time[kk2] and mt[kk]<time[kk2+1]:
                step=kk2+1
        xmesh,zmesh=fl.read_mesh(step)
        mx[kk]=mx[kk]*1e-3
        mz.append(read_depth(zmesh,mi[kk],mj[kk])*-1)
    return mx,mz
'''
read data from flac data to which used to draw figures
the most of function need: related parameters and the last vts number
the data will be a 1D list: value in each vts (from 1/or started_vts to last vts number)
'''    
def read_time(model_steps):
# get the model time list 

    timestep=[]
    for step in range(start_vts,model_steps+1):
        timestep.append(fl.time[step])
    return timestep


def read_downgoing_plate_velocity(trench_index,model_steps):
# get the means of area velocity on the subducting plate beside the trench (W15xD20 grid) 
   
    vel_total=[]
    for step in range(start_vts,model_steps+1):
        vx,vz=fl.read_vel(step)
        x_len,z_len=vx.shape
        total_vx=0
        
        if step<=3:
            total_vz=0.
        else:    
            for kk1 in range(min(x_len-2,trench_index[step-1]+10),min(x_len-1,trench_index[step-1]+25)):
                for kk2 in range(20,40):
                    total_vx=total_vx+vx[kk1,kk2]/20./(min(x_len,trench_index[step-1]+25)-min(x_len-1,trench_index[step-1]+10))
        total_v=(total_vx**2)**0.5
        vel_total.append(total_v)
    return vel_total


def read_trench_location (model_steps):
# get the trench location

    print ("record trench location")
    trench_Xindex=[]    
    trench_location=[]
    Xtmp=0
    for step in range(start_vts,model_steps+1):
        
        xmesh,zmesh=fl.read_mesh(step)
        xmesh_surf=xmesh[:,0]
        zmesh_surf=zmesh[:,0]
     
        ztmp=1000
        for s in range (0,len(xmesh_surf)):
            if step>=20:
                if zmesh_surf[s]<=ztmp and (Xtmp-50)<xmesh_surf[s] and xmesh_surf[s]<(Xtmp+50):
                    xtmp=xmesh_surf[s]
                    ztmp=zmesh_surf[s]
                    trench_index=s
            else:
                if zmesh_surf[s]<=ztmp :
                    xtmp=xmesh_surf[s]
                    ztmp=zmesh_surf[s]
                    trench_index=s
        Xtmp=xtmp
        trench_Xindex.append(trench_index)
        trench_location.append(Xtmp)
    for kk in range(0,20):
        trench_Xindex[kk]=trench_Xindex[16]
        trench_location[kk]=trench_location[16]
    return trench_Xindex, trench_location
     
     
def read_subductingL(time,subductingV,trench_retreat_rate):
# get the subducted length from subduction velcoity and trench retreat rate

    timeL=len(time)
    L=[0]
    temp = 0
    for kk in range(1,timeL):
        length=(time[kk]-time[kk-1])*1e+6*(subductingV[kk]+trench_retreat_rate[kk])*1e-3*1e-2
        temp = temp+length
        L.append(temp)
    return L


def read_backarc_extensionL(time,trench_retreat_rate):
# the extension lenght of back arc basin = (trench retreat rate)*(time) 

    timeL=len(time)
    L=[0]
    temp = 0
    for kk in range(1,timeL):
        length=(time[kk]-time[kk-1])*1e+6*trench_retreat_rate[kk]*1e-3*1e-2
        temp = temp+length
        L.append(temp)
    return L

  
def read_slab_dip(model_steps,depth1,depth2):
# read the dip of dip between depth1 and depth2(as the input parameters)

    print ('record dip (',depth1,'-',depth2,'km)')
    dip=[]    
    for step in range(start_vts,model_steps+1):
        xmesh,zmesh=fl.read_mesh(step)
        x_len,z_len=xmesh.shape
        phase=fl.read_phase(step)        
        zmesh_B=zmesh[0,:]

        temp=0 # when here's no slab between depth1 and depth2, both two depth will be shallower 
        depth2_temp=depth2+5
        while temp<=0:
            depth2_temp=depth2_temp-5
            for kk in range(0,z_len-1):
                # find z-index in depth2 -> j2
                if (read_depth(zmesh,0,kk)>depth2_temp):
                    j2=kk
                    break
            for kk in range(0,x_len-1):
                if phase[kk,j2] in slab_phase:
                    i2=kk          
                    temp=5
                    break
        if (depth2_temp-20)<=depth1:
            depth1_temp=depth2_temp-20
        else:
            depth1_temp=depth1       
        for kk in range(0,z_len-1):
            # find z-index in depth2 -> j2
            if (read_depth(zmesh,0,kk)<depth1_temp):
                j1=kk
            else:
                break
            # find x-index of surface of slab in depth2 -> i2
            for kk in range(0,x_len-1):
                if phase[kk,j1] in slab_phase:
                    i1=kk
                    break  
        detla_x=abs(xmesh[i1,j1]-xmesh[i2,j2])
        detla_z=abs(zmesh[i1,j1]-zmesh[i2,j2])
        di=math.degrees(math.atan(detla_z/detla_x))
        dip.append(di)
    return dip
        
        
def read_partialmeltingrate(model_steps):
#how many partial melting markers producted in a time step 

    print ('record melting porduce rate')
    melting_produce=[]
    melting_count=[]
    for step in range(start_vts,model_steps+1):
        countmarker=fl.read_countmarker(step)
        meltingmarker=fl.read_meltingmarker(step)
        xmesh,zmesh=fl.read_mesh(step)
        nx=len(countmarker)
        nz=len(countmarker[1,:])
        
        produce_rate=0
        count=0
        for kki in range(1,nx):
            for kkj in range(1,nz):
                if meltingmarker[kki,kkj]>0:
                    count=count+meltingmarker[kki,kkj]
                    produce_rate=produce_rate+(meltingmarker[kki,kkj]/countmarker[kki,kkj]*read_area(xmesh,zmesh,kki,kkj))
        melting_count.append(count)
        melting_produce.append(produce_rate)
    return melting_produce, melting_count
      
       
def read_wedgevis(model_steps,depth,trench_index):
# mean viscosity in the area (triangle above slab, max depth = input parameter)    
    
    print ('record average viscosity of wedge (',depth,'km above)')
    wedgevis=[0,0,0,0,0,0,0,0,0]    
    for step in range(start_vts+9,model_steps+1):
        total_area=0
        total_visc=0
        xmesh,zmesh=fl.read_mesh(step)
        phase=fl.read_phase(step)  
        x_len,z_len=xmesh.shape
        visc=fl.read_visc(step)

        temp=0 # when here's no slab at depth, change depth shallower 
        depth_temp=depth+5
        while temp<=0:
            depth_temp=depth_temp-5
            for kk in range(0,z_len-1):
                # find z-index in depth -> j
                if (read_depth(zmesh,0,kk)>depth_temp):
                    j=kk           
                    break
            for kk in range(0,x_len-1):
                # find x-index of surface of slab in depth -> i
                # defined of slab: basalt(1/3/7), eclogite(13), metasediment(5)
                if phase[kk,j] in slab_phase:
                    i=kk          
                    temp=5
                    break
        kkj=j
        for kki in range(i,trench_index[step-1]-7):   
            kkj_left=kkj
            kkj=10
            temp=0
            while temp<=0:
                if phase[kki,kkj] in slab_phase:
                    temp=5
                    break
                else:
                    total_area=total_area+read_area(xmesh,zmesh,kki,kkj)
                    total_visc=total_visc+(visc[kki,kkj]*read_area(xmesh,zmesh,kki,kkj))
                kkj=kkj+1
                if kkj>kkj_left:
                    temp=5
                    break
        if total_area==0:
            wedgevis.append(0)
        else:
            wedgevis.append(total_visc/total_area)
    return wedgevis

        
def read_rifting_location(model_steps):
# get the location of rifting (mantle -> basalt)
    rifting_x = [0,0]
    rifting_z = [0,0]
    rifting_t = [0,0]
    ph_3 = []
    phase3_list=[4,8]
    for step in range(model_steps,start_vts-1,-1):
        x,z,age,ph,ID = fl.read_markers(step)
        x,z,age,ph,ID = flacmarker2vtk.filter_marker(x,z,age,ph,ID)
        ID_key = dict(zip(ID, [j for j in range(len(ID))] ))    
           
        exist_ph_3 = [val for val in ph_3 if val in ID]               

        for iph_id in exist_ph_3:
             if ph[ ID_key[iph_id] ] in phase3_list:
                 rifting_z.append(z[ID_key[iph_id]])
                 rifting_x.append(x[ID_key[iph_id]] )
                 rifting_t.append(fl.time[step])
 
        ph_3 = []
        for j in range(len(ID)):
             if ph[j] == 3:
                 ph_3.append(ID[j])        
 
                 
    return rifting_x, rifting_z, rifting_t
    
