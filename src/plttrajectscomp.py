import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import rc, rcdefaults
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.collections
import matplotlib as mpl

#mpl.rcParams.update({
#    "text.usetex": True,
#    "font.family": "sans-serif",
#    "font.serif": ["Computer Modern Roman"],  # standard LaTeX font
#})
mpl.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"],
    "text.latex.preamble": r"""
        \usepackage{helvet}
        \usepackage{sansmath}
        \sansmath
    """
})

#main plot
fig=plt.figure(figsize=(6,6))
ax1=fig.add_subplot(111)



##########################################################
############### GEOMETRIC HOLE PLOT ######################
##########################################################

holecolor='blue'
pfancolor='orange'
alphahole=0.2
alphapfan=0.2

#atom types and kinetic radii
# 1    12.010700000 # C_3
# 2    12.010700000 # C_R
# 3     1.007940000 # H_
# 4    18.998403200 # F_
# 5    12.010700000 # C_2
# 6    15.999400000 # O_2

radii = [1.7,1.7,1.2,1.47,1.7,1.52]
pclrs = ['darkgray','darkgray','orange','green','darkgray','red']
pclrs = ['#303030','#303030','#E8E8E8','#32CD32','#303030','#E53935']

def get_area(x, y):
    area = 0.5*(x[0]*(y[1] - y[2]) + x[1]*(y[2] - y[0]) + x[2]*(y[0] - y[1]))
    return area

def get_area2(x, y):
    l1 = np.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2)
    l2 = np.sqrt((x[1] - x[2])**2 + (y[1] - y[2])**2)
    l3 = np.sqrt((x[2] - x[0])**2 + (y[2] - y[0])**2)
    p = (l1 + l2 + l3)/2
    area = np.sqrt(p * (p - l1) * (p - l2) * (p - l3))
    return area

def xy(x,y,r,phi):
    return x+r*np.cos(phi), y+r*np.sin(phi)
phis=np.arange(0,6.28,0.01)

dat = np.loadtxt('../data/pfan_coords_type') #files: pfan_coords    pfantri_xvals  pfantri_yvals
#ax1.plot(dat[:,1],dat[:,2],marker='.',ms=4.0,color='k',linestyle='None')

for c in range(len(dat[:,0])):
    atype = int(dat[c,0])
    rad=radii[atype-1]
    #ax1.plot(*xy(dat[c,1],dat[c,2],rad,phis), c='#962929',ls='-',lw=1,zorder=0)


# Note that the patches won't be added to the axes, instead a collection will
patches = [plt.Circle(center, size) for center, size in zip(dat[:,1:3], [radii[int(atype)-1] for atype in dat[:,0]])]

patch_colors = [
    pclrs[int(atype)-1]
    for atype in dat[:, 0]
]

#coll = matplotlib.collections.PatchCollection(
#    patches,
#    facecolors=patch_colors,
#    alpha=alphapfan
#)
coll = matplotlib.collections.PatchCollection(
    patches,
    facecolors=patch_colors,
    edgecolors='black',
    linewidths=0.5,
    alpha=alphapfan
)

#coll = matplotlib.collections.PatchCollection(patches, facecolors=pfancolor,alpha=alphapfan)
ax1.add_collection(coll)

hdat = np.loadtxt('../data/pfanholepoints1.txt')
#ax1.plot(hdat[:,0],hdat[:,1],marker='.',ms=2.0,color='g',linestyle='None')

#plot the actual triangles to shade in...
xdat = np.loadtxt('../data/tri_xvals1')
ydat = np.loadtxt('../data/tri_yvals1')
areas = np.zeros(len(xdat[:,0]))
for t in range(len(xdat[:,0])):
    trianglex=[xdat[t,0],xdat[t,1],xdat[t,2],xdat[t,0]]
    triangley=[ydat[t,0],ydat[t,1],ydat[t,2],ydat[t,0]]
    #ax1.plot(trianglex,triangley,color='k',linestyle='-',lw=0.5)
    ax1.fill(trianglex, triangley, color=holecolor, edgecolor=None, alpha=alphahole)
    areas[t] = get_area2(trianglex, triangley)

#print(areas)
print(6*np.sum(areas))
print((6*np.sum(areas))/(51.315800*35.324000))
print('open area ratio = '+str(round((6*np.sum(areas))/(51.315800*35.324000),3)))
kinarea = (6*np.sum(areas))/(51.315800*35.324000)


xcenter=19.11
ycenter=16.38
dx=18.75
dy=18.75
xmin,xmax = xcenter-dx/2,xcenter+dx/2
ymin,ymax = ycenter-dy/2,ycenter+dy/2
ax1.set_xlim([xmin,xmax])
ax1.set_ylim([ymin,ymax])

print("xmin,xmax")
print(xmin,xmax)
print("ymin,ymax")
print(ymin,ymax)


ax1.set_xlabel('x',fontsize=20,usetex=True)
ax1.set_ylabel('y',fontsize=20,usetex=True)
#ax1.set_title('open area ratio = '+str(round((6*np.sum(areas))/(51.315800*35.324000),3)))



##########################################################
############### NEXT PLOT TAJECTORS ######################
##########################################################


#jobname = str(sys.argv[1])
jobname = '../data/jobsNp200'
dat = np.loadtxt(jobname+'/gasposxyz')

xdat = np.loadtxt(jobname+'/tri_xvals')
ydat = np.loadtxt(jobname+'/tri_yvals')
areas = np.zeros(len(xdat[:,0]))
for t in range(len(xdat[:,0])):

    trianglex=[xdat[t,0],xdat[t,1],xdat[t,2],xdat[t,0]]
    triangley=[ydat[t,0],ydat[t,1],ydat[t,2],ydat[t,0]]
    if xmin<xdat[t,0]<xmax and ymin<ydat[t,0]<ymax:
        ax1.plot(trianglex,triangley,color='red',linestyle='-',lw=0.5)
        #ax1.fill(trianglex, triangley, color='g', alpha=0.5)
    areas[t] = get_area2(trianglex, triangley)
    
#ax1.plot(dat[:,0],dat[:,1],marker='.',ms=1.0,color='red',linestyle='None')


jobname = '../data/jobsSF6Np50FINALbetterLJ'
dat = np.loadtxt(jobname+'/gasposxyz')

xdat = np.loadtxt(jobname+'/tri_xvals')
ydat = np.loadtxt(jobname+'/tri_yvals')
areas = np.zeros(len(xdat[:,0]))
for t in range(len(xdat[:,0])):

    trianglex=[xdat[t,0],xdat[t,1],xdat[t,2],xdat[t,0]]
    triangley=[ydat[t,0],ydat[t,1],ydat[t,2],ydat[t,0]]
    if xmin<xdat[t,0]<xmax and ymin<ydat[t,0]<ymax:
        ax1.plot(trianglex,triangley,color='blue',linestyle='-',lw=0.5)
        #ax1.fill(trianglex, triangley, color='g', alpha=0.5)
    areas[t] = get_area2(trianglex, triangley)

#ax1.plot(dat[:,0],dat[:,1],marker='.',ms=1.0,color='blue',linestyle='None')


#print(areas)
print(np.sum(areas)/(51.315800*35.324000))
trajarea = np.sum(areas)/(51.315800*35.324000)



##########################  CHATGPT for legend!!!!!!!


from matplotlib.patches import Polygon
from matplotlib.legend_handler import HandlerBase

class FilledTriMarkerHandler(HandlerBase):
    def __init__(self, scale=1.0):
        """
        scale: relative size of the triangle inside the legend handle box
        """
        super().__init__()
        self.scale = scale

    def create_artists(self, legend, orig_handle,
                       x0, y0, width, height, fontsize, trans):
        """
        Draw a filled blue triangle inside the legend handle box.
        """
        # triangle vertices in normalized 0–1 box
        base_verts = np.array([
            [0.2, 0.2],
            [0.8, 0.2],
            [0.5, 0.8]
        ])

        # compute center of handle box
        cx, cy = x0 + width/2, y0 + height/2

        # scale vertices around center
        verts = (base_verts - 0.5) * self.scale * min(width, height) + np.array([cx, cy])

        tri = Polygon(
            verts,
            facecolor='blue',
            edgecolor='none',
            alpha=0.2
        )
        tri.set_transform(trans)
        return [tri]




from matplotlib.lines import Line2D
from matplotlib.patches import Circle

class LineTriMarkerHandler(HandlerBase):
    def __init__(self, scale=1.0, dot_radius=0.04, line_width=0.8, tricolor = 'black'):
        """
        scale: size multiplier for the triangle inside the legend handle box
        dot_radius: relative size of the black dots (0–1, fraction of box height)
        line_width: width of the connecting red lines
        """
        super().__init__()
        self.scale = scale
        self.dot_radius = dot_radius
        self.line_width = line_width
        self.tricolor = tricolor

    def create_artists(self, legend, orig_handle,
                       x0, y0, width, height, fontsize, trans):
        # base triangle vertices in normalized box [0–1]
        base_verts = np.array([
            [0.2, 0.2],
            [0.8, 0.2],
            [0.5, 0.8]
        ])

        # center of handle box
        cx, cy = x0 + width/2, y0 + height/2

        # scale vertices around center
        verts = (base_verts - 0.5) * self.scale * min(width, height) + np.array([cx, cy])

        artists = []

        # --- Draw red edges ---
        for i, j in [(0, 1), (1, 2), (2, 0)]:
            l = Line2D(
                [verts[i,0], verts[j,0]],
                [verts[i,1], verts[j,1]],
                color=self.tricolor,
                lw=self.line_width
            )
            l.set_transform(trans)
            artists.append(l)

        return artists



#LEGEND
dummy1 = object()
dummy2 = object()

rounded_kinarea = round(kinarea,2)
formatted_kinarea = f"{rounded_kinarea:.2f}"
rounded_trajarea = round(trajarea,2)
formatted_trajarea = f"{rounded_trajarea:.2f}"


# UCOMMMENT FOR LEGEND!!!!!!!!!!!!!!!!!!!1
# scaled & centered legend marker
ax1.legend([dummy1,dummy2], [r"He", r"SF$_6$"],
          handler_map={dummy1: LineTriMarkerHandler(scale=1.5, dot_radius=0.06, line_width=0.8, tricolor='red'), dummy2: LineTriMarkerHandler(scale=1.5, dot_radius=0.06, line_width=0.8, tricolor='blue')},
          fontsize=16)

################### END CHATGPT


################### chat for axis conversion..

from matplotlib.ticker import FuncFormatter
#ax1.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val*0.1:.2f}"))
#ax1.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val*0.1:.2f}"))

# scaling factor (Å → nm)
scale = 0.1
# shifts in nm
x_shift = 1.0
y_shift = 0.75

# apply both scaling and shift in tick labels
ax1.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val*scale - x_shift:.2f}"))
ax1.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val*scale - y_shift:.2f}"))
##################


# make tick labels larger
ax1.tick_params(axis='x', labelsize=12)  # x-axis tick labels
ax1.tick_params(axis='y', labelsize=12)  # y-axis tick labels

# optional: axis labels
ax1.set_xlabel(r"$x \, \, (\mathrm{nm})$", fontsize=18)
ax1.set_ylabel(r"$y \, \, (\mathrm{nm})$", fontsize=18)

plt.savefig('../figures/HeSF6trajcomp.png', dpi=900, bbox_inches='tight')
plt.tight_layout()
plt.show()
