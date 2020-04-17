# -*- coding: utf-8 -*-
"""
Created on Wed May  8 20:59:09 2019

@author: chiilee
"""
import sys
sys.path.append("/home/chiilee/git-flac/flac/util")
sys.path.append("/home/chiilee/code")
sys.path.append("/home/chiilee/code/git-code")
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#----------------------------
#          SETTING
#----------------------------
inputpath='/home/chiilee/data/'+sys.argv[1]
outputpath='/home/chiilee/Pic/'+sys.argv[2]
foldername=sys.argv[3]

vts=int(sys.argv[4])  #len(time-1)
time_length=30

axis_tick=1
legend=1
folderplot=0



path = inputpath+'/'+foldername
os.chdir(path)
results_dir = os.path.abspath(outputpath+'/'+foldername)
if not os.path.isdir(results_dir):
       os.makedirs(results_dir) 
import function_DevelopmentOfSystem as subf
import function_DataInOut as ip

#-------------------------------------------
print ('>>>>> read data in <<<<<')    
#-------------------------------------------
time=ip.read_data1('D_time',path)
trench_index=ip.read_data1('D_trench_index',path)
trench_location=ip.read_data1('D_trench_location',path)




#-----------------------------------------
print ('>>>>> ploting <<<<<')
#-----------------------------------------
 
# =========================
#     strenght proflie
# =========================
strenght,strenght_D,strenght_T=subf.read_strenght(vts,trench_index,1)
 
fig=plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)
 
dot=ax.scatter(strenght_D,strenght_T,c=strenght,s=25,cmap='spectral',vmax=5,vmin=2,linewidths=0)
plt.grid(True)
plt.xlim((500,0))
plt.ylim((0,time_length))
 
if (axis_tick<1):
   plt.setp(ax.get_xticklabels(), visible=False)
   plt.setp(ax.get_yticklabels(), visible=False)
else:
   plt.title('Strength of plate ', fontsize=15, color='black')
   plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
   plt.ylabel('Time (Myr)', fontsize=12, color='black')
if (legend >= 1):
   colorbar=plt.colorbar(dot,ax=ax)
   colorbar.set_label('strength (GPa.m)', fontsize=10, color='black')
   colorbar.ax.tick_params(labelsize=8)
if (folderplot >=1):
    plt.text(490,1.5,foldername)

plt.savefig(results_dir+'/pic_AccumulatedStrenght'+'.png') 

 
# ==================================
#     strain rate profile
# ==================================
strainrate,strainrate_D,strainrate_T=subf.read_srII(vts,trench_index,3) 
 
fig=plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)
dot=ax.scatter(strainrate_D,strainrate_T,c=strainrate,s=30,cmap='jet',vmax=-12.5,vmin=-16,linewidths=0)
 
plt.grid(True)
plt.xlim((500,0))
plt.ylim((0,time_length))
 
if (axis_tick<1):
   plt.setp(ax.get_xticklabels(), visible=False)
   plt.setp(ax.get_yticklabels(), visible=False)
else:
   plt.title('Strain rate ', fontsize=15, color='black')
   plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
   plt.ylabel('Time (Myr)', fontsize=12, color='black')
if (legend >= 1):
   colorbar=plt.colorbar(dot,ax=ax)
   colorbar.set_label('log10 (strain rate) (s-1)', fontsize=10, color='black')
   colorbar.ax.tick_params(labelsize=8)
if (folderplot >=1):
    plt.text(490,1.5,foldername)

plt.savefig(results_dir+'/pic_StrainRate'+'.png')

 
# ============================
#       phase on surface
# ============================
phase,phase_D,phase_T=subf.read_phase(vts,trench_index)
 
fig=plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)
 
colors = ["#93CCB1","#8BFF8B","#7158FF","#FF966F","#9F0042",
          "#660000","#524B52","#D14309","#5AB245","#004B00",
          "#008B00","#455E45","#B89FCE","#C97BEA","#525252",
          "#FF0000","#00FF00","#FFFF00","#7158FF"]
phase15= matplotlib.colors.ListedColormap(colors)
dot=ax.scatter(phase_D,phase_T,c=phase,s=25,cmap=phase15,vmax=19.5,vmin=0.5,linewidths=0)

plt.grid(True)
plt.xlim((500,0))
plt.ylim((0,time_length))
 
if (axis_tick<1):
   plt.setp(ax.get_xticklabels(), visible=False)
   plt.setp(ax.get_yticklabels(), visible=False)
else:
   plt.title('Phase of plate ', fontsize=15, color='black')
   plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
   plt.ylabel('Time (Myr)', fontsize=12, color='black')
if (legend >= 1):
   colorbar=plt.colorbar(dot,ax=ax)
   colorbar.set_label('strength (GPa.m)', fontsize=10, color='black')
   colorbar.ax.tick_params(labelsize=8)
if (folderplot >=1):
    plt.text(490,1.5,foldername)

plt.savefig(results_dir+'/pic_Phase'+'.png') 
 
'''
# =================
#      topo
# ================= 
topo,topo_D,topo_T=subf.read_topo(vts,trench_index)

fig=plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)

colors = ["#0000AA","#0044BB","#0066FF","#33CCFF","#FFFF33",
          "#C63300","#DDAA00","#AA7700","#FFFFFF"]
topo15= matplotlib.colors.ListedColormap(colors)
dot=ax.scatter(topo_D,topo_T,c=topo,s=25,cmap='gist_ncar',vmax=8,vmin=-4,linewidths=0)
 
plt.grid(True)
plt.xlim(500,0)
plt.ylim((0,time_length))
 
if (axis_tick<1):
   plt.setp(ax.get_xticklabels(), visible=False)
   plt.setp(ax.get_yticklabels(), visible=False)
else:
   plt.title('Topography ', fontsize=15, color='black')
   plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
   plt.ylabel('Time (Myr)', fontsize=12, color='black')
if (legend >= 1):
   colorbar=plt.colorbar(dot,ax=ax)
   colorbar.set_label('topography (km)', fontsize=10, color='black')
   colorbar.ax.tick_params(labelsize=8)
if (folderplot >=1):
    plt.text(490,1.5,foldername)

plt.savefig(results_dir+'/pic_Topo'+'.png') 
  
 
# ============================
#       melt vol. profile 
# ============================

meltvol,meltvol_D,meltvol_T=subf.read_meltvol(vts,trench_index,50)

fig=plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)
dot = ax.scatter(meltvol_D,meltvol_T,c=meltvol,s=25,cmap='YlOrBr',vmax=0.6,vmin=0,linewidths=0)
 
plt.grid(True)
plt.xlim((500,0))
plt.ylim((0,time_length))

if (axis_tick<1):
   plt.setp(ax.get_xticklabels(), visible=False)
   plt.setp(ax.get_yticklabels(), visible=False)
else:
   plt.title('Partial melting volume ratio in 50 km', fontsize=15, color='black')
   plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
   plt.ylabel('Time (Myr)', fontsize=12, color='black')
if (legend >= 1):
   colorbar=plt.colorbar(dot,ax=ax)
   colorbar.set_label('M (%)', fontsize=10, color='black')
   colorbar.ax.tick_params(labelsize=8)
if (folderplot >=1):
    plt.text(490,1.5,foldername)

plt.savefig(results_dir+'/pic_MeltVol'+'.png') 
'''
# ===================================================
#      location of rifting and partial melting 
# =================================================== 
fig=plt.figure(figsize=(6,5))
ax = fig.add_subplot(111)
 
mx=ip.read_data('D_melt',path,2)
mt=ip.read_data('D_melt',path,4)
mz=ip.read_data('D_melt',path,8)

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
 
for kk in range (len(mx)):
   mx[kk]=mx[kk]*1e-3
   mz[kk]=-mz[kk]*1e-3
trench_mx=[0]*len(mx)
for kk in range(0,len(time)-1):
   for kk1 in range(0,len(mt)):
       if time[kk] < mt[kk1] and time[kk+1]> mt[kk1]:
           trench_mx[kk1]=mx[kk1]-trench_location[kk]
 
trench_rx=[0]*len(rx)
for kk in range(0,len(time)-1):
   for kk1 in range(0,len(rt)):
       if time[kk] < rt[kk1] and time[kk+1]>= rt[kk1]:
           trench_rx[kk1]=rx[kk1]-trench_location[kk]
 
line1=ax.scatter(trench_mx,mt,c='#aaaaaa',linewidths=0)
line2=ax.scatter(trench_rx,rt,c='#000000',linewidths=0)

plt.grid(True)
plt.xlim((-550,-50))
plt.ylim((0,30))
 
if (axis_tick<1):
   plt.setp(ax.get_xticklabels(), visible=False)
   plt.setp(ax.get_yticklabels(), visible=False)
else:
   plt.title('Location of Rifting and Partial melting', fontsize=15, color='black')
   plt.xlabel('Distance to trench (km)', fontsize=12, color='black')
   plt.ylabel('Time (Myr)', fontsize=12, color='black')

if (folderplot >=1):
   plt.text(-530,2,foldername)

plt.savefig(results_dir+'/pic_LocationOfMeltandRift-'+'.png')
