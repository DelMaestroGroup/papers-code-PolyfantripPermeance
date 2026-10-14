#this will be a simple plot to be used as an inset.

import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import rc, rcdefaults
from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.collections
import matplotlib as mpl

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
fig=plt.figure(figsize=(3,2))
ax1=fig.add_subplot(111)


ApsCOM = np.array([0.09100968698017403, 0.1695743375091883, 0.17463148472049275, 0.20609699077304394, 0.22454860981890962 ])

ApsNON = np.array([0.2380612328632507, 0.20411717646724367, 0.17463148472049275, 0.20609699077304394, 0.22454860981890962])

masses = np.array([(6*18.998+32.06), (2*15.9994+12.0107), (2*14.0067), 4.002602, 2*1.00794])

massHe = np.array([4.002602])
areaHe = np.array([0.20609699077304394])
massSF6 = np.array([(6*18.998+32.06)])
areaSF6 = np.array([0.09100968698017403])

ax1.plot(1/np.sqrt(masses),ApsCOM,marker='o',ms=6.0,color='k',linestyle='None',zorder=1)
#ax1.plot(1/masses,ApsNON,marker='o',ms=10.0,color='blue',linestyle='None',zorder=0)

#plot He and SF6 in different colors
ax1.plot(1/np.sqrt(massHe),areaHe,marker='o',ms=6.0,color='red',linestyle='None',zorder=1)
ax1.plot(1/np.sqrt(massSF6),areaSF6,marker='o',ms=6.0,color='blue',linestyle='None',zorder=1)


ax1.set_xlim([0.0,0.76])
ax1.set_ylim([0.0,0.25])

# make tick labels larger
ax1.tick_params(axis='x', labelsize=12)  # x-axis tick labels
ax1.tick_params(axis='y', labelsize=12)  # y-axis tick labels

ax1.set_xlabel(r"$1/ \sqrt{M_W}$",fontsize=20,usetex=True)
ax1.set_ylabel(r"$A_p/A$",fontsize=20,usetex=True)
ax1.set_axisbelow(True)
ax1.grid(True, which='major', linestyle='--', linewidth=1.0, alpha=1.0,zorder=0)

plt.savefig('../figures/Ap.png', dpi=900, bbox_inches='tight')
plt.tight_layout()
plt.show()


