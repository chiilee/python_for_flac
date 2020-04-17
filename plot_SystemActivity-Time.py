# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:08:24 2019

@author: chiilee
"""
import sys
sys.path.append("/home/chiilee/flac-git/flac/util")
sys.path.append("/home/chiilee/code")
sys.path.append("/home/chiilee/code/git-code")
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import function_DataInOut as ip
import function_DataProcess as cd

#----------------------------
#          SETTING
#----------------------------
inputpath='/home/chiilee/data/feb2020=/DG80/'
outputpath='/home/chiilee/Pic/feb_DG80/'
foldername=['DG80_0.1-','DG80_0.01-','DG80_0.5-']
'''
inputpath='/home/chiilee/data/feb2020/DG80/'
outputpath='/home/chiilee/Pic/DG80/'       
foldername=['DG0.01-']
'''

stop_timing=0
time_length=30
Ltime_length=1200

axis_tick=1
legend=0
folderplot=1



for folderk in range(len(foldername)):
 path = inputpath+foldername[folderk]
 os.chdir(path)
 results_dir = os.path.abspath(outputpath+foldername[folderk])
 if not os.path.isdir(results_dir):
        os.makedirs(results_dir)


 #-------------------------------------------
 print ('>>>>> read data in <<<<<')
 #-------------------------------------------
 time=ip.read_data1('D_time',path)
 Ltime=ip.read_data1('D_Ltime',path)

 trench_index=ip.read_data1('D_trench_index',path)
 trench_location=ip.read_data1('D_trench_location',path)
 #trench_retreat_rate=ip.read_data1('D_retreat',path)
 trench_retreat_rate=cd.rate_calculating2(trench_location,time)
 trench_retreat_rate=cd.moving_window_smooth(trench_retreat_rate,15)
 trench_retreat_rate=cd.moving_window_smooth(trench_retreat_rate,15)
 subductingV=ip.read_data1('D_subductingV',path)
 dip=ip.read_data1('D_dip100_200',path)

 rx=ip.read_data('D_rifting',path,1)
 rz=ip.read_data('D_rifting',path,2)
 rt=ip.read_data('D_rifting',path,3)
 rift_count=ip.read_data1('D_rift_count',path)

 mx=ip.read_data('D_melt',path,2)
 mt=ip.read_data('D_melt',path,4)
 mlabel=ip.read_data('D_melt',path,7)
 mz=ip.read_data('D_melt',path,8)
 for kk in range (len(mx)):
    mx[kk]=mx[kk]*1e-3
    mz[kk]=-mz[kk]*1e-3
 
 all_meltcount=ip.read_data('D_melt_count',path,1)
 basalt_meltcount=ip.read_data('D_melt_count',path,2)
 peri_meltcount=ip.read_data('D_melt_count',path,3)


 
 #-----------------------------------------
 print ('>>>>> plotting <<<<<')
 #-----------------------------------------

 a=[0,10000]
 b=[0,0]
 a2=[Ltime[int(float(stop_timing)/0.05)],Ltime[int(float(stop_timing)/0.05)]]
 b2=[-100,100]
 a3=[stop_timing,stop_timing]
 b3=[-100,100]

 #==========================================================
 #    subducting rate / trench retreat rate / dip   
 #========================================================== 
 '''    
 fig1_1=plt.figure(figsize=(6,3))
 ax = fig1_1.add_subplot(111)
 ax2 = ax.twinx()
 ax3 = ax.twiny()
 
 zero = ax.plot(a,b,"black")
 timing = ax.plot(a2,b2,"--",color='black',  lw=1)
 line1 = ax.plot(Ltime, trench_retreat_rate, '-g', label = 'trench retreat rate',  lw=2)
 line2 = ax.plot(Ltime, subductingV, '-',color='#FF3333', label = 'subducting rate',  lw=2)
 line3 = ax2.plot(Ltime, dip, '--',color='#0044bb', label = 'dip(100-200km)',  lw=2)
 
 tick_value,tick_location=cd.tick_function(Ltime,time,Ltime_length,2)
 ax.grid()
 ax.set_xlim(0,Ltime_length)
 ax.set_ylim(-5,10)
 ax2.set_ylim(20,75)
 ax3.set_xlim(0,Ltime_length)
 ax3.set_xticks(tick_location)
 ax3.set_xticklabels("%.0f" % z for z in tick_value)
 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)   
 else:
    ax.set_xlabel("Subducting length (km)")
    ax.set_ylabel(r"velcoity ($cm/yr$)")
    ax2.set_ylabel(r"dip ($^\circ$)")
    ax3.set_xlabel(r"Time (Myrs)") 
 if (legend >= 1): 
    lines = line1+line2+line3
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=4)   
 if (folderplot >=1):
    plt.text(20,-4,foldername[folderk])  
 
 plt.savefig(results_dir+'/Lpic1-'+'.png')
 '''
 #-------------------
 fig1_2 = plt.figure(figsize=(6,3))
 ax1 = fig1_2.add_subplot(111)
 ax2 = ax1.twinx()
 #ax3 = ax1.twiny()
 
 zero = ax1.plot(a,b,"black")
 timing = ax1.plot(a3,b3,"--",color='black',  lw=1)
 line1 = ax1.plot(time, trench_retreat_rate, '-g', label = 'trench retreat rate',  lw=2)
 line2 = ax1.plot(time, subductingV, '-',color='#FF3333', label = 'subducting rate',  lw=2)
 line3 = ax2.plot(time, dip, '--',color='#0044bb', label = 'dip(100-200km)',  lw=2)

 tick_value,tick_location=cd.tick_function(time,Ltime,time_length,100)
 tick_value=tick_value/100.
 ax1.grid()
 
 ax1.set_xlim(1,time_length)
 ax1.set_ylim(-5,10)
 ax2.set_ylim(20,75)
 #ax3.set_xlim(0,time_length)
 #ax3.set_xticks(tick_location)
 #ax3.set_xticklabels("%.0f" % z for z in tick_value)
 
 if (axis_tick<1):
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax1.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    #plt.setp(ax3.get_xticklabels(), visible=False)   
 else:
    ax1.set_xlabel("Time (Myrs)")
    ax1.set_ylabel(r"velcoity ($cm/yr$)")
    ax2.set_ylabel(r"dip ($^\circ$)")
    #ax3.set_xlabel(r"Subducting length (100 km)")
 if (legend >= 1): 
    lines = line1+line2+line3
    labs = [l.get_label() for l in lines]
    ax1.legend(lines, labs, loc=4) 
 if (folderplot >=1):
    plt.text(1,-4,foldername[folderk])
 
 plt.savefig(results_dir+'/pic1-'+'.png')

 #===================================================
 #        melting & MOR produce rate
 #===================================================
 '''
 fig2_1=plt.figure(figsize=(6,3))
 ax = fig2_1.add_subplot(111)
 ax2 = ax.twinx()
 ax3 = ax.twiny()
 
 zero = ax.plot(a,b,"black")
 timing = ax.plot(a2,b2,"--",color='black',  lw=1)
 line0 = ax.plot(Ltime, all_meltcount, '-', label = 'All',color="black",  lw=2)
 line1 = ax.plot(Ltime, basalt_meltcount, ':', label = 'basaltic',color="green",  lw=3)
 line3 = ax.plot(Ltime, peri_meltcount, ':', label = 'peridoitie',color='orange',lw=3)
 line4 = ax2.plot(Ltime, rift_count, '-', label = 'OC',color="red",  lw=2)

 tick_value,tick_location=cd.tick_function(Ltime,time,Ltime_length,2)
 ax.grid()
 ax.set_xlim(0,Ltime_length)
 ax.set_ylim(0,30)
 ax2.set_ylim(0,45)
 ax3.set_xlim(0,Ltime_length)
 ax3.set_xticks(tick_location)
 ax3.set_xticklabels("%.0f" % z for z in tick_value)
 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)   
 else:
    ax.set_xlabel("Subducting length (km)")
    ax.set_ylabel(r"Magma produce rate (km$^2$/yr)")
    ax2.set_ylabel(r"OC produce rate (km$^2$/yr)")
    ax3.set_xlabel(r"time (Myrs)")
 if (legend >= 1): 
    lines = line0+line1+line3+line4
    labs = [l.get_label() for l in lines]
    ax.legend(lines, labs, loc=1)
 if (folderplot >=1):
    plt.text(20,3,foldername[folderk])
 
 plt.savefig(results_dir+'/Lpic2-'+'.png')
 '''
 #-----------------------------------
 fig2_2=plt.figure(figsize=(6,3))
 ax1 = fig2_2.add_subplot(111)
 ax2 = ax1.twinx()
 #ax3 = ax1.twiny()
  
 zero = ax1.plot(a,b,"black")
 timing = ax1.plot(a3,b3,"--",color='black',  lw=1)
 line0 = ax1.plot(time, all_meltcount, '-', label = 'All',color="black",  lw=2)
 line1 = ax1.plot(time, basalt_meltcount, ':', label = 'basaltic',color="green",  lw=3)
 line3 = ax1.plot(time, peri_meltcount, ':', label = 'peridoitie',color='orange',lw=3)
 line4 = ax2.plot(time, rift_count, '-', label = 'OC',color="red",  lw=2)
 
 tick_value,tick_location=cd.tick_function(time,Ltime,time_length,100)
 tick_value=tick_value/100.
 ax1.grid()
 ax1.set_xlim(1,time_length)
 ax1.set_ylim(0,30)
 ax2.set_ylim(0,45)
 #ax3.set_xlim(0,time_length)
 #ax3.set_xticks(tick_location)
 #ax3.set_xticklabels("%.0f" % z for z in tick_value)

 if (axis_tick<1):
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax1.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
    #plt.setp(ax3.get_xticklabels(), visible=False)   
 else:
    ax1.set_xlabel("Time (Myrs)")
    ax1.set_ylabel(r"Magma roduce rate (km$^2$/yr)")
    ax2.set_ylabel(r"OC produce rate (km$^2$/yr)")
    #ax3.set_xlabel(r"Subducting length (100 km)")
 if (legend >= 1): 
    lines = line0+line1+line3+line4#+line4
    labs = [l.get_label() for l in lines]
    ax1.legend(lines, labs, loc=1)
 if (folderplot >=1):
    plt.text(1,3,foldername[folderk])
 
 plt.savefig(results_dir+'/pic2'+'.png')

 #=============================================================
 #   location of melting markers (distance to the trench)
 #=============================================================

 fig4=plt.figure(figsize=(5,4))
 ax = fig4.add_subplot(111)
 
 trench_mx=[0]*len(mx)
 for kk in range(0,len(time)-1):
    for kk1 in range(0,len(mt)):
        if time[kk] < mt[kk1] and time[kk+1]> mt[kk1]:
            trench_mx[kk1]=mx[kk1]-trench_location[kk]
            
 line1=ax.scatter(trench_mx,mz,c=mt,s=7,cmap='spectral',vmax=time_length,vmin=0,linewidths=0)

 plt.grid(True)
 plt.ylim((-240,-20))
 plt.xlim((-400,20))
 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
 else:
    plt.title('Location of markers ', fontsize=15, color='black')
    plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
    plt.ylabel('Depth (km)', fontsize=12, color='black')
 if (legend >= 1): 
    colorbar=plt.colorbar(line1,ax=ax)
    colorbar.set_label('time (Myr)', fontsize=10, color='black')
    colorbar.ax.tick_params(labelsize=8)
 if (folderplot >=1):
    plt.text(-390,-235,foldername[folderk])

 plt.savefig(results_dir+'/pic4-'+'.png')
 
 #=================================================================
 #     location of rifting marker (distance to the trench)
 #=================================================================
 '''
 fig6=plt.figure(figsize=(5,2.5))
 ax = fig6.add_subplot(111)
 
 trench_rx=[0]*len(rx)
 for kk in range(0,len(time)-1):
    for kk1 in range(0,len(rt)):
        if time[kk] < rt[kk1] and time[kk+1]>= rt[kk1]:
            trench_rx[kk1]=rx[kk1]-trench_location[kk]

 line1=ax.scatter(trench_rx,rt,c=rt,s=7,cmap='spectral',vmax=time_length+2,vmin=5,linewidths=0)
 
 plt.grid(True)
 plt.xlim((-600,-50))
 plt.ylim((0,time_length))
 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
 else:
    plt.title('Location of Rifting ', fontsize=15, color='black')
    plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
    plt.ylabel('Time (Myr)', fontsize=12, color='black')
 if (legend >= 1):
    colorbar=plt.colorbar(line1,ax=ax)
    colorbar.set_label('time (Myr)', fontsize=10, color='black')
    colorbar.ax.tick_params(labelsize=8)
 if (folderplot >=1):
     plt.text(-590,6,foldername[folderk])

 plt.savefig(results_dir+'/pic6-'+'.png')
 '''
 #------------------------------------------------------
 #fig6-1:location of rifting (absoult location)
 fig6_1=plt.figure(figsize=(5,2.5))
 ax = fig6_1.add_subplot(111)
 
 line1=ax.scatter(rx,rt,c=rt,s=7,cmap='spectral',vmax=time_length+2,vmin=5,linewidths=0)
  
 plt.grid(True)
 plt.xlim((600,1200))
 plt.ylim((0,time_length))
 
 if (axis_tick<1):
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
 else:
    plt.title('Location of Rifting ', fontsize=15, color='black')
    plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
    plt.ylabel('Time (Myr)', fontsize=12, color='black')
 if (legend >= 1):
    colorbar=plt.colorbar(line1,ax=ax)
    colorbar.set_label('time (Myr)', fontsize=10, color='black')
    colorbar.ax.tick_params(labelsize=8)
 if (folderplot >=1):
     plt.text(610,2,foldername[folderk])

 plt.savefig(results_dir+'/pic6_1-'+'.png')
 
 #===================================================
 #   subducted lenght & new OC producted rate
 #=================================================== 
 
 fig9 = plt.figure(figsize=(6,3))
 ax1 = fig9.add_subplot(111)
 ax2 = ax1.twinx()

 zero = ax1.plot(a,b,"black")
 timing = ax1.plot(a3,b3,"--",color='black',  lw=1)
 line1 = ax1.plot(time,Ltime, '-',color="green", label = 'subduction length',  lw=2)
 line5 = ax2.plot(time, rift_count, '-r',label = 'OC',  lw=2)

 tick_value,tick_location=cd.tick_function(time,Ltime,time_length,100)
 tick_value=tick_value/100.
 ax1.grid()
 ax1.set_xlim(1,time_length)
 ax1.set_ylim(0,1200)
 ax2.set_ylim(0,50)

 if (axis_tick<1):
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax1.get_yticklabels(), visible=False)
    plt.setp(ax2.get_yticklabels(), visible=False)
 else:
    ax1.set_xlabel("Time (Myrs)")
    ax1.set_ylabel(r"Length (km)")
    ax2.set_ylabel(r"OC produce rate (km$^2$/yr)")
 if (legend >= 1):
    lines = line1+line5
    labs = [l.get_label() for l in lines]
    ax1.legend(lines, labs, loc=2)
 if (folderplot >=1):
    plt.text(1,-8,foldername[folderk])

 plt.savefig(results_dir+'/pic9-'+'.png')
