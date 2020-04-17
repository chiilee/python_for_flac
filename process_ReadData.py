# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 15:42:00 2019

@author: chiilee
"""

import sys
sys.path.append("/home/chiilee/flac-DD/181215/util")
sys.path.append("/home/chiilee/code")
sys.path.append("/home/chiilee/code/git-code")
import os
import function_DataProcess as cd
import function_DataInOut as ip

#----------------------------
#          SETTING
#----------------------------
inputpath='/home/chiilee/data/feb2020/stand/'
outputpath='/home/chiilee/Pic/stand/'
foldername='s0.01-'
vts=600

#others
stop_timing=8#80*0.05
time_length=18
Ltime_length=1200
#'''
#--------------------------------------------------------------------------------#
path = inputpath+foldername
os.chdir(path)
results_dir = os.path.abspath(outputpath+foldername)
if not os.path.isdir(results_dir):
       os.makedirs(results_dir)
import function_ReadData as rd
vts_numbers=vts-1

#-------------------------------------------
print ('>>>>> read & save data <<<<<')
#-------------------------------------------
time=rd.read_time(vts_numbers)
ip.save_1array('D_time',path,time)

trench_index,trench_location=rd.read_trench_location(vts_numbers)
trench_retreat_rate=cd.rate_calculating(trench_location,time)
trench_retreat_rate=cd.moving_window_smooth(trench_retreat_rate,15)
trench_retreat_rate=cd.moving_window_smooth(trench_retreat_rate,15)
ip.save_1array('D_trench_index',path,trench_index)
ip.save_1array('D_trench_location',path,trench_location)
ip.save_1array('D_retreat',path,trench_retreat_rate)

subductingV=rd.read_downgoing_plate_velocity(trench_index,vts_numbers)
subductingV=cd.moving_window_smooth(subductingV,15)
subductingV=cd.moving_window_smooth(subductingV,15)
ip.save_1array('D_subductingV',path,subductingV)

Ltime=rd.read_subductingL(time,subductingV,trench_retreat_rate)
ip.save_1array('D_Ltime',path,Ltime)

dip=rd.read_slab_dip(vts_numbers,100,200)
dip=cd.moving_window_smooth(dip,15)
ip.save_1array('D_dip100_200',path,dip)

BA_extension=rd.read_backarc_extensionL(time,trench_retreat_rate)
BA_extension=cd.moving_window_smooth(BA_extension,7)
ip.save_1array('D_BA',path,BA_extension)

rx,rz,rt=rd.read_rifting_location(vts_numbers)
ip.save_3array('D_rifting',path,rx,rz,rt)

nrx=ip.read_data('D_rifting',path,1)
nrz=ip.read_data('D_rifting',path,2)
nrt=ip.read_data('D_rifting',path,3)
rx=[]
rz=[]
rt=[]
for kk in range (len(nrx)):
    rx.append(nrx[len(nrx)-kk-1])
    rz.append(nrz[len(nrz)-kk-1])
    rt.append(nrt[len(nrt)-kk-1])
rift_count=[0]             
for kk1 in range(0,len(time)-1):
  rift_count.append(0)
  for kk2 in range(len(rt)):
       if time[kk1]<rt[kk2] and time[kk1+1]>=rt[kk2] and rt[kk2]!=0:
          rift_count[kk1]=rift_count[kk1]+1*1.25*5/9
rift_count=cd.moving_window_smooth(rift_count,15)
rift_count=cd.moving_window_smooth(rift_count,7)
ip.save_1array('D_rift_count',path,rift_count)

mx=ip.read_data('D_melt',path,2)
mt=ip.read_data('D_melt',path,4)
mlabel=ip.read_data('D_melt',path,7)
mz=ip.read_data('D_melt',path,8)
allmelt_count=[0]             
basaltmelt_count=[0]
perimelt_count=[0]
for kk1 in range(0,len(time)-1):
  allmelt_count.append(0)
  for kk2 in range(len(mt)):
       if time[kk1]<mt[kk2] and time[kk1+1]>mt[kk2] and mt[kk2]!=0:  
          allmelt_count[kk1]=allmelt_count[kk1]+1*2*5/9            
for kk1 in range(0,len(time)-1):
  basaltmelt_count.append(0)
  for kk2 in range(len(mt)):
       if time[kk1]<mt[kk2] and time[kk1+1]>mt[kk2] and mt[kk2]!=0 and mlabel[kk2]==1:  
          basaltmelt_count[kk1]=basaltmelt_count[kk1]+1*2*5/9           
for kk1 in range(0,len(time)-1):
  perimelt_count.append(0)
  for kk2 in range(len(mt)):
       if time[kk1]<mt[kk2] and time[kk1+1]>mt[kk2] and mt[kk2]!=0 and mlabel[kk2]==3:  
          perimelt_count[kk1]=perimelt_count[kk1]+1*2*5/9
allmelt_count=cd.moving_window_smooth(allmelt_count,15)
allmelt_count=cd.moving_window_smooth(allmelt_count,7)
basaltmelt_count=cd.moving_window_smooth(basaltmelt_count,15)
basaltmelt_count=cd.moving_window_smooth(basaltmelt_count,7)
perimelt_count=cd.moving_window_smooth(perimelt_count,15)
perimelt_count=cd.moving_window_smooth(perimelt_count,7)
ip.save_3array('D_melt_count',path,allmelt_count,basaltmelt_count,perimelt_count)


#'''

#'''
