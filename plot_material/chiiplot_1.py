#!/usr/bin/env python

import sys, os
import numpy as np

import flac
import flac_interpolate as fi
import flac_gravity3 as fg


# domain bounds
left = -500
right = 100
up = 25
down = -275

left2 = -200 
right2 = 0
up2 = 25
down2 = -75 

left3 = -1000 
right3 = 650 
up3 = 25
down3 = -800 

dx = 2
dz = 1.5

def find_trench_index(z):
    '''Returns the i index of trench location.'''
    zz = z[:-50,0]
    # the highest point defines the forearc
    imax = zz.argmax()
    # the trench is the lowest point west of forearc
    #i = zz[:imax].argmin()
    # the trench is the lowest point east of forearc
    i = zz[imax:imax+100].argmin()+imax
    #ii = zz[100:140].argmin()+100
    print('arc=',imax)
    return i


def interpolate_phase(frame, xtrench, kinds):
    if (kinds == 1):
        # domain bounds in km
        fi.xmin = xtrench + left
        fi.xmax = xtrench + right
        fi.zmin = down
        fi.zmax = up
        # resolution in km
        fi.dx = dx
        fi.dz = dz

    xx, zz, ph = fi.interpolate(frame, 'phase')
    return xx, zz, ph

def interpolate_visc(frame, xtrench):
    # domain bounds in km
    fi.xmin = xtrench + left
    fi.xmax = xtrench + right
    fi.zmin = down
    fi.zmax = up

    # resolution in km
    fi.dx = dx
    fi.dz = dz

    xx, zz, visc = fi.interpolate(frame, 'visc')
    return xx, zz, visc

def interpolate_chamber(frame, xtrench):
    # domain bounds in km
    fi.xmin = xtrench + left
    fi.xmax = xtrench + right
    fi.zmin = down
    fi.zmax = up

    # resolution in km
    fi.dx = dx
    fi.dz = dz

    xx, zz, C = fi.interpolate(frame, 'chamber')
    return xx, zz, C

def interpolate_edot(frame, xtrench):
    # domain bounds in km
    fi.xmin = xtrench + left3
    fi.xmax = xtrench + right3
    fi.zmin = down3
    fi.zmax = up3

    # resolution in km
    fi.dx = dx
    fi.dz = dz

    xx, zz, edot = fi.interpolate(frame, 'srII')
    return xx, zz, edot

def interpolate_dens(frame, xtrench):
    # domain bounds in km
    fi.xmin = xtrench + left3
    fi.xmax = xtrench + right3
    fi.zmin = down3
    fi.zmax = up3

    # resolution in km
    fi.dx = dx
    fi.dz = dz

    xx, zz, dens = fi.interpolate(frame, 'density')
    return xx, zz, dens


###############################################

frame = int(sys.argv[1])
left2 = int(sys.argv[2])
rigth2 = left2 + 200

fl = flac.Flac()
x, z = fl.read_mesh(frame)
itrench = find_trench_index(z)
xtrench = x[itrench,0]
print('trench =', itrench)
print('trench location =', xtrench)

# get interpolated phase either from previous run or from original data
phasefile = 'intp3-phase.%d' % frame
if not os.path.exists(phasefile):
    xx, zz, ph = interpolate_phase(frame, xtrench,1)
    f = open(phasefile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(xx, zz, ph, stream=f)
    f.close()
else:
    f = open(phasefile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    nx = int(nx)
    nz = int(nz)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    xx = tmp[:,:,0]
    zz = tmp[:,:,1]
    ph = tmp[:,:,2]
    f.close()

# get interpolated T either from previous run or from original data
tfile = 'intp3-T.%d' % frame
if not os.path.exists(tfile):
    T = fl.read_temperature(frame)
    f = open(tfile, 'w')
    f.write('%d %d\n' % x.shape)
    flac.printing(x, z, T, stream=f)
    f.close()
else:
    f = open(tfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    nx = int(nx)
    nz = int(nz)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    T = tmp[:,:,2]
    f.close()

# get interpolated viscosity either from previous run or from original data
viscfile = 'intp3-visc.%d' % frame
if not os.path.exists(viscfile):
    xx, zz, visc = interpolate_visc(frame, xtrench)
    f = open(viscfile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(xx, zz, visc, stream=f)
    f.close()
else:
    f = open(viscfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    nx = int(nx)
    nz = int(nz)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    xx = tmp[:,:,0]
    zz = tmp[:,:,1]
    visc = tmp[:,:,2]
    f.close()

# get interpolated chamber(C) either from previous run or from original data
Cfile = 'intp3-chamber.%d' % frame
if not os.path.exists(Cfile):
    xx, zz, C = interpolate_chamber(frame, xtrench)
    f = open(Cfile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(xx, zz, C, stream=f)
    f.close()
else:
    f = open(Cfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    nx = int(nx)
    nz = int(nz)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    xx = tmp[:,:,0]
    zz = tmp[:,:,1]
    C = tmp[:,:,2]
    f.close()

# get interpolated strain rate either from previous run or from original data
edotfile = 'intp3-edot.%d' % frame
if not os.path.exists(edotfile):
    xx, zz, edot = interpolate_edot(frame, xtrench)
    f = open(edotfile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(xx, zz, edot, stream=f)
    f.close()
else:
    f = open(edotfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    nx = int(nx)
    nz = int(nz)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    xx = tmp[:,:,0]
    zz = tmp[:,:,1]
    edot = tmp[:,:,2]
    f.close()

# get interpolated density either from previous run or from original data
densfile = 'intp3-dens.%d' % frame
if not os.path.exists(densfile):
    xx, zz, dens = interpolate_dens(frame, xtrench)
    f = open(densfile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(xx, zz, dens, stream=f)
    f.close()
else:
    f = open(densfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    nx = int(nx)
    nz = int(nz)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    xx = tmp[:,:,0]
    zz = tmp[:,:,1]
    dens = tmp[:,:,2]
    f.close()

# velocity
vfile = 'intp-vel.%d' % frame
vspacing = 20
vscale = 7e-2
vx, vz = fl.read_vel(frame)
theta = np.rad2deg(np.arctan2(vz, vx))
h = np.hypot(vx, vz) * vscale
f = open(vfile, 'w')
#f.write('%d %d\n' % vx.shape)
flac.printing(x[::vspacing,::vspacing], z[::vspacing,::vspacing], theta[::vspacing,::vspacing], h[::vspacing,::vspacing], stream=f)
f.close()

###############
model = os.path.split(os.getcwd())[-1]
psfile = 'result1.%d.ps' % frame
pngfile = 'result1.%d.png' % frame
phgrd = 'phase.%d.grd' % frame
phcpt = '/home/chiilee/code/git-code/plot_material/phase18.cpt'
tgrd = 'temperature3.%d.grd' % frame
viscgrd = 'visc3.%d.grd' % frame
visccpt = '/home/chiilee/code/git-code/plot_material/visc.cpt'
visccpt2 = '/home/chiilee/code/git-code/plot_material/visc2.cpt'
tgrd = 'temperature3.%d.grd' % frame
Cgrd = 'chamber3.%d.grd' % frame
Ccpt = '/home/chiilee/code/git-code/plot_material/chamber.cpt'
Ccpt2 = '/home/chiilee/code/git-code/plot_material/chamber2.cpt'
edotgrd = 'edot3.%d.grd' % frame
edotcpt = '/home/chiilee/code/git-code/plot_material/strain_rate.cpt'
densgrd = 'dens3.%d.grd' % frame
denscpt = '/home/chiilee/code/git-code/plot_material/strain_rate.cpt'

xmin = xtrench + left
xmax = xtrench + right
zmin = down
zmax = up
xmin2 = xtrench + left2
xmax2 = xtrench + right2
zmin2 = down2
zmax2 = up2
xmin3 = xtrench + left3
xmax3 = xtrench + right3
zmin3 = down3
zmax3 = up3

aspect_ratio = float(up - down) / (right - left)
width = 3.3
height = width * aspect_ratio

shiftz = height + 0.4
shiftx = width + 0.3
shiftx2 = -1 * shiftx 
shiftz2 = (-1 * shiftz) - 0.35 

# interval of temperature contours
cint = 200
# interval of chamber(%) contours
cint2 = 0.05
# velocity vector color
vcolor = 'white'


if not os.path.exists(phgrd):
    cmd = 'tail -n +2 %(phasefile)s | xyz2grd -G%(phgrd)s -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)

'''
if not os.path.exists(phgrd2):
    cmd = 'tail -n +2 %(phasefile2)s | xyz2grd -G%(phgrd2)s -I%(dx)f/%(dz)f -R%(xmin2)f/%(xmax2)f/%(zmin2)f/%(zmax2)f' % locals()
    #print cmd
    os.system(cmd)

if not os.path.exists(phgrd3):
    cmd = 'tail -n +2 %(phasefile3)s | xyz2grd -G%(phgrd3)s -I%(dx)f/%(dz)f -R%(xmin3)f/%(xmax3)f/%(zmin3)f/%(zmax3)f' % locals()
    #print cmd
    os.system(cmd)
'''

if not os.path.exists(tgrd):
    cmd = 'tail -n +2 %(tfile)s | surface -G%(tgrd)s -Ll0 -I%(dx)f/%(dz)f -R%(xmin3)f/%(xmax3)f/%(zmin3)f/20' % locals()
    #print cmd
    os.system(cmd)

if not os.path.exists(viscgrd):
    cmd = 'tail -n +2 %(viscfile)s | xyz2grd -G%(viscgrd)s -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)

if not os.path.exists(Cgrd):
    cmd = 'tail -n +2 %(Cfile)s | surface -G%(Cgrd)s -Ll0 -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)

if not os.path.exists(edotgrd):
    cmd = 'tail -n +2 %(edotfile)s | xyz2grd -G%(edotgrd)s -I%(dx)f/%(dz)f -R%(xmin3)f/%(xmax3)f/%(zmin3)f/%(zmax3)f' % locals()
    #print cmd
    os.system(cmd)

if not os.path.exists(densgrd):
    cmd = 'tail -n +2 %(densfile)s | xyz2grd -G%(densgrd)s -I%(dx)f/%(dz)f -R%(xmin3)f/%(xmax3)f/%(zmin3)f/%(zmax3)f' % locals()
    #print cmd
    os.system(cmd)


cmd = '''
rm -f .gmtcommands* .gmtdefaults*

gmtset MEASURE_UNIT = inch
gmtset LABEL_FONT_SIZE=14 ANNOT_FONT_SIZE_PRIMARY=10

##########
# PLOT 1 # (left down)
##########

# axis annotation
psbasemap -JX%(width)f/%(height)f -Ba100f10/a50f10::WSne -R%(left)f/%(right)f/%(zmin)f/%(zmax)f -X0.9 -Y4 -P -K > %(psfile)s

# viscosity plot
grdimage %(viscgrd)s -C%(visccpt)s -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f -J -P -O -K >> %(psfile)s

# velocity vectors
psxy %(vfile)s -J -R -A -Sv0.005c/0.04c/0.04c -G%(vcolor)s -W1p,%(vcolor)s -P -O -K >> %(psfile)s

# chamber plot
grdcontour %(Cgrd)s -C%(Ccpt)s -A- -W+1p -J -R -P -K -O >> %(psfile)s

#########
# PLOT 2 # (right down) 
##########

# axis annotation
psbasemap -JX%(width)f/%(height)f -Ba200f20/a150f50::wSnE -R%(left3)f/%(right3)f/%(zmin3)f/%(zmax3)f -X%(shiftx)f -P -O -K >> %(psfile)s

# phase plot
grdimage %(edotgrd)s -C%(edotcpt)s -R%(xmin3)f/%(xmax3)f/%(zmin3)f/%(zmax3)f -J -P -O -K >> %(psfile)s

# temperature contours
grdcontour %(tgrd)s -C+600/1200 -W1p,red -J -P -R -K -O >> %(psfile)s

##########
# PLOT 3 # (right up)
##########

# axis annotation
psbasemap -JX%(width)f/%(height)f -Ba50f5/a25f5::wSnE -R%(left2)f/%(right2)f/%(zmin2)f/%(zmax2)f -Y%(shiftz)f -P -O -K >> %(psfile)s

# phase plot
grdimage %(phgrd)s -C%(phcpt)s -R%(xmin2)f/%(xmax2)f/%(zmin2)f/%(zmax2)f -J -P -O -K >> %(psfile)s

# temperature contours
#grdcontour %(tgrd)s -C%(cint)f -L10/1600 -W1p -J -P -R -K -O >> %(psfile)s
grdcontour %(tgrd)s -C%(cint)f -W1p -J -P -R -K -O >> %(psfile)s


##########
# PLOT 4 # (left up)
##########

# axis annotation
psbasemap -JX%(width)f/%(height)f -Ba100f10/a50f10::WSne -R%(left)f/%(right)f/%(zmin)f/%(zmax)f -X%(shiftx2)f -P -O -K >> %(psfile)s

# phase plot
grdimage %(phgrd)s -C%(phcpt)s -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f -J -P -O -K >> %(psfile)s

# temperature contours
grdcontour %(tgrd)s -C%(cint)f -L10/1600 -W1p -J -P -R -K -O >> %(psfile)s

###########
# colorbar #
############

#makecpt -Ccyclic -Ic -T0/1500/100 >T.cpt

psscale -C%(visccpt2)s -D0.75/%(shiftz2)f/1.5/0.15h -B1:"log@-10@-(Viscosity)(Pa.s)":  -P -O -K >>%(psfile)s
psscale -C%(Ccpt2)s -D2.75/%(shiftz2)f/1.5/0.15h -B0.02:"Melt Vol":  -P -O -K >>%(psfile)s
psscale -C%(edotcpt)s -D4.75/%(shiftz2)f/1.5/0.15h -B1:"Starin rate(log.s@+-1@+)":  -P -O -K >>%(psfile)s

##########
# title  #
##########
echo %(xmin)f %(shiftz)d 14 0 1 LB "Model=%(model)s   Frame=%(frame)d   Trench location=%(xtrench).3f km" | \
pstext -D0/1 -X%(shiftx2)f -Y-0.6 -N -J -R -P -O >> %(psfile)s

convert -density 150 %(psfile)s %(pngfile)s

''' % locals()
#print cmd
os.system(cmd)

