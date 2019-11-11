# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:28:34 2018

@author: chiilee
"""
import numpy as np

def save_1array(title,path,array1):
    f = open(path +"/"+ title + ".txt",'w')
    for kk in range(len(array1)):
        f.write('%f\n'%array1[kk])
    f.close()  
    
def save_2array(title,path,array1,array2):
    f = open(path +"/"+ title + ".txt",'w')
    for kk in range(len(array1)):
        f.write('%f '%array1[kk])
        f.write('%f\n'%array2[kk])
    f.close()     

def save_3array(title,path,array1,array2,array3):
    f = open(path +"/"+ title + ".txt",'w')
    for kk in range(len(array1)):
        f.write('%f '%array1[kk])
        f.write('%f '%array2[kk])
        f.write('%f\n'%array3[kk])
    f.close()  

def save_4array(title,path,array1,array2,array3,array4):
    f = open(path +"/"+ title + ".txt",'w')
    for kk in range(len(array1)):
        f.write('%f '%array1[kk])
        f.write('%f '%array2[kk])
        f.write('%f '%array3[kk])
        f.write('%f\n'%array4[kk])
    f.close()  

def save_5array(title,path,array1,array2,array3,array4,array5):
    f = open(path +"/"+ title + ".txt",'w')
    for kk in range(len(array1)):
        f.write('%f '%array1[kk])
        f.write('%f '%array2[kk])
        f.write('%f '%array3[kk])
        f.write('%f '%array4[kk])
        f.write('%f\n'%array5[kk])
    f.close()  

def read_data1(title,path):
    temp1=np.loadtxt(path+"/"+title+".txt")
    return temp1

def read_data(title,path,column_index):
    temp1=np.loadtxt(path+"/"+title+".txt")
    temp2=temp1[:,(column_index-1)]
    return temp2
