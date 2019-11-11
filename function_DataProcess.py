# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:36:02 2018

@author: chiilee
"""
import numpy as np


def moving_window_smooth(array,window_width):
    new_array=[]
    temp=int(window_width/2)    
    for kk in range(1,temp+1):
        new_array.append(array[kk-1])
    for kk in range(temp,len(array)-(temp)):
        q=sum(array[kk-temp:kk+temp+1])/window_width
        new_array.append(q)
    for kk in range((len(array)-temp+1),len(array)+1):
        new_array.append(array[kk-1])
    return new_array

def rate_calculating(data_array,time_array):
    #input= km / Myr
    #output= cm /yr
    new_data_array=[0]
    for kk in range(1,len(data_array)):
        q=(data_array[kk]-data_array[kk-1])/(time_array[kk]-time_array[kk-1])
        q=q*0.1       
        new_data_array.append(q)
    return new_data_array
    
   
#calculate magma production rate
def count_every_timestep(count_time_array,time_array):
#count_time_array= time-array of every markers in ranges
    count=[0]              #number was made in every time step
    for kk1 in range(0,len(time_array)-1):
        count.append(0)
        for kk2 in range(len(count_time_array)):
            if time_array[kk1]==count_time_array[kk2] and count_time_array[kk2]!=0:  
                count[kk1]=count[kk1]+1
    return count

def tick_function(orig_array,new_array,orig_array_limit,tick_interval):
    tick_location=[]
    temp=new_array[len(new_array)-1]
    for kk in range (0,len(orig_array)):
        if orig_array[kk]>orig_array_limit:
            temp=new_array[kk-1]
            break
    tick_value = np.arange(0,temp,tick_interval)
    for kk1 in range (0,len(tick_value)):
        for kk2 in range (0,len(new_array)):
            if new_array[kk2] > int(tick_value[kk1]):
                break
        ratio = (tick_value[kk1]-new_array[kk2-1])/(new_array[kk2]-new_array[kk2-1])
        v=orig_array[kk2-1]*(1-ratio)+orig_array[kk2]*ratio     
        tick_location.append(v)
    return tick_value,tick_location
