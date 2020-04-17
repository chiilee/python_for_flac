# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:41:38 2019

@author: chiilee
"""
import numpy as np
import sys
import os
import function_DataInOut as ip
sys.path.append("/home/chiilee/code/git-code")
sys.path.append("/home/chiilee/git-flac/flac/util")

inputpath='/home/chiilee/data/'
foldername=['test']
path='/home/chiilee/data/'
#grouptype=[1]
#groupcolor=[]
os.chdir(inputpath)

def getfinalvts(path):
    finalvts=1
    if os.path.isfile(path+'/D_time.txt'):
        T=ip.read_data1('D_time',path)
        finalvts=len(T)
    return finalvts       
    
def all_magmaP(finalvts):
    all_magmaP=[]
    time=[]
    for kk in range(1,finalvts,20):
        print('frame:',kk)
        magmaP,ttime=get_magmaP(kk)
        all_magmaP.append(magmaP)
        time.append(ttime)
    return all_magmaP, time
        
def get_magmaP(frame):   
    
    frame=frame+1      
    import flac 
    fl=flac. Flac() 
    
    time=fl.time[frame]
    
    if frame > 10:
        production=0
        
        for framek in range(frame-5,frame+5):   
            x,z=fl.read_mesh(framek)
            countmarker=fl.read_countmarker(framek)
            meltingmarker=fl.read_meltingmarker(framek)

            mi=ip.read_data('D_melt',path,5)
            mj=ip.read_data('D_melt',path,6)
            mt=ip.read_data('D_melt',path,4)
                
            for tkk in range(len(mt)-1):
                if mt[tkk]>fl.time[framek] and mt[tkk] < fl.time[framek+1]: 
                    meltingmarker[mi[tkk],mj[tkk]]=meltingmarker[mi[tkk],mj[tkk]]+1  

            for xk in range(1,fl.nx-1):
                for zk in range(1,fl.nz-1):
                    production=production+(0.25*(meltingmarker[xk,zk]/countmarker[xk,zk])*read_area(x,z,xk,zk))
        deltaT=fl.time[frame+5]-fl.time[frame-5] #in Myrs
        magmaP = production/deltaT
    else:
        magmaP = 0

    return magmaP,time

#================================================

def time2vts(time,path):
    vts=1
    if os.path.isfile(path+'/D_time.txt'):
        T=ip.read_data1('D_time',path)
              
        for kk in range(len(T)):
            if time == 0:
                vts=1
            else:
                if time <= T[kk]:
                    vts = kk
                    break
    return vts    
    
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
        

def get_BASdata():
    BAST=[]
    BASL=[]

    for folderk in range(len(foldername)):
        path = inputpath+foldername[folderk]
        #os.chdir(path)
        #print(path)
        if os.path.isfile(path+'/D_rifting.txt'):
            kk=0
            #print('exist')
            
            rt=ip.read_data('D_rifting',path,3)
            time=ip.read_data1('D_time',path)
            Ltime=ip.read_data1('D_Ltime',path)
            
            BAST.append(round(rt[-1],1))
            BASL.append(1000) 
            #print(foldername[folderk],BAST[folderk],BASL[folderk]) 

   
            for kk in range(len(time)):
                if time[kk] >= BAST[folderk]:
                    BASL[folderk]=round(Ltime[kk],1)
                    break
        else:
            print('no exist')
            BAST.append(1000)
            BASL.append(5000)
     
    #print(foldername[folderk],BAST[folderk],BASL[folderk]) 

    BAST=np.reshape(BAST,arraysize)
    BASL=np.reshape(BASL,arraysize)
    return BAST, BASL
    
def BAST2L(foldername,BAST,arraysize):
    BASL=[]

    for folderk in range(len(foldername)):
        path = inputpath+foldername[folderk]
        #os.chdir(path)
        #print(path)
        if os.path.isfile(path+'/D_rifting.txt'):
            kk=0
            #print('exist')
            
            time=ip.read_data1('D_time',path)
            Ltime=ip.read_data1('D_Ltime',path)
            
            BASL.append(5000) 
   
            for kk in range(len(time)):
                if time[kk] >= BAST[folderk]:
                    BASL[folderk]=round(Ltime[kk],1)
                    break
        else:
            BASL.append(5000)
     
    #print(foldername[folderk],BAST[folderk],BASL[folderk]) 

    BAST=np.reshape(BAST,arraysize)
    BASL=np.reshape(BASL,arraysize)
    return BAST, BASL   
    
def getdip(depth1,depth2,time):
 
    dip=[]
    time=np.reshape(time,(-1,1))
    #print(time,len(time)) 
    for folderk in range(len(foldername)):
        
        path = inputpath+foldername[folderk]
        os.chdir(path)
        
        if os.path.isfile(path+'/D_time.txt'):
            T=ip.read_data1('D_time',path)
            dip.append(0)        
        
            for kk in range(len(T)):
                    if time[folderk] ==0:
                         dip[folderk]=0
                    else:
                        if time[folderk] <= T[kk]:
                            dip[folderk]=round(read_slab_dip(kk,depth1,depth2),1)
                            #print (foldername[folderk],kk,dip[folderk])
                            break
        else:
            dip.append(0)
            
    dip=np.reshape(dip,arraysize)

    return dip   
    
def read_slab_dip(frame,depth1,depth2):
    
    import flac 
    fl=flac. Flac()   
    import math
    import function_ReadData as rd

    # read the dip of dip between depth1 and depth2(as the input parameters)
    xmesh,zmesh=fl.read_mesh(frame)
    x_len,z_len=xmesh.shape
    phase=fl.read_phase(frame)        

    temp=0 # when here's no slab between depth1 and depth2, both two depth will be shallower 
    depth2_temp=depth2+5
    while temp<=0:
        depth2_temp=depth2_temp-5
        for kk in range(0,z_len-1):
            # find z-index in depth2 -> j2
            if (rd.read_depth(zmesh,0,kk)>depth2_temp):
                j2=kk
                break
        for kk in range(0,x_len-1):
            if phase[kk,j2] in rd.slab_phase:
                i2=kk          
                temp=5
                break
    if (depth2_temp-20)<=depth1:
        depth1_temp=depth2_temp-20
    else:
        depth1_temp=depth1       
    for kk in range(0,z_len-1):
        # find z-index in depth2 -> j2
        if (rd.read_depth(zmesh,0,kk)<depth1_temp):
            j1=kk
        else:
            break
        # find x-index of surface of slab in depth2 -> i2
        for kk in range(0,x_len-1):
            if phase[kk,j1] in rd.slab_phase:
                i1=kk
                break  
    detla_x=abs(xmesh[i1,j1]-xmesh[i2,j2])
    detla_z=abs(zmesh[i1,j1]-zmesh[i2,j2])
    di=math.degrees(math.atan(detla_z/detla_x))

    return di

    
def get_maxarcT(time):
    
    arc_phase=[14]
    
    arcT=[]
    time=np.reshape(time,(-1,1))
    for folderk in range(len(foldername)):
        path = inputpath+foldername[folderk]
        os.chdir(path)
        
        import flac 
        fl=flac. Flac() 

        arcthickness=[0]
        frame=time2vts(time[folderk],path)
        if frame != 1:
            phase=fl.read_phase(frame)          
            x,z=fl.read_mesh(frame)
            #zz=z[:,0]
            #imax = zz.argmax() #the highest point = arc peak
            
            for kk1 in range(0,fl.nx-1):
                if phase[kk1,0] in arc_phase:
                    for kk2 in range(fl.nz):
                        if phase[kk1,kk2] not in arc_phase:
                            break
                    arcthickness.append(z[kk1,0]-z[kk1,kk2])
                
            arcT.append(round(max(arcthickness),2))
        else:
            arcT.append(0.0)
    arcT=np.reshape(arcT,arraysize)
    return arcT
    '''
def get_magmaP(time):      
    magmaP=[]
    time=np.reshape(time,(-1,1))
    for folderk in range(len(foldername)):
        path = inputpath+foldername[folderk]
        os.chdir(path)
        
        import flac 
        fl=flac. Flac() 

        frame=time2vts(time[folderk],path)        
        if frame != 1:
            production=0
            for framekk in range(frame-10,frame+10):
                countmarker=fl.read_countmarker(framek)
                meltingmarker=fl.read_meltingmarker(framek)
                x,z=fl.read_mesh(framek)

                for xk in range(1,fl.nx):
                    for zk in range(1,fl.nz):
                        production=production+(0.25*(meltingmarker[xk,zk]/countmarker[xk,zk])*read_area(x,z,xk,zk))
            deltaT=fl.time[frame+10]-fl.time[frame-10] #in Myrs
            magmaP.append(production/deltaT)
        else:
            magmaP.append(0.)
    magmaP=np.reshape(magmaP,arraysize)
    return magmaP

'''




