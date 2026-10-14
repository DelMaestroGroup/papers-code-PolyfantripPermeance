import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import rc, rcdefaults
from scipy.optimize import curve_fit
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


### make the main plot
fig=plt.figure(figsize=(6,6))
ax1=fig.add_subplot(111)


def Lin(x, A, B):
    y = A*x + B
    return y

def getfit(xvals,yvals,yerrs):
    guess = [1.0,0.0]
    lbnds = [-10000.0,-1e-10]
    ubnds = [10000.0,1e-10]
    parameters, covariance = curve_fit(Lin,xvals,yvals,sigma=yerrs,p0=guess,bounds=(lbnds,ubnds))
    fit_A = parameters[0]
    fit_B = parameters[1]
    err_A = np.sqrt(covariance[0, 0])
    err_B = np.sqrt(covariance[1, 1])
    return fit_A,fit_B,err_A,err_B

LAMPSperms=np.array([0.03975797861747728,0.02605853989226564,0.012628561728222368,0.01056635702212578,0.004817498295934323])
err_LAMPSperms=np.array([0.0005622371195251953,0.00042558480465777635,0.00028880358643962106,0.0002624450653026476,0.00026114540389121437])
masses = np.array([2*1.00794,4.002602,(2*14.0067),(2*15.9994+12.0107),(6*18.998+32.06)])#this is g/mol, mult by 1e-3 for kg/mol
ax1.errorbar(
    1.0/np.sqrt(masses),
    LAMPSperms,
    yerr=err_LAMPSperms,
    marker='o',
    ms=12,
    linestyle='None',
    label=r'$\mathrm{Simulation}$',
    markerfacecolor=(1, 0, 0, 0.3),  # red with alpha=0.3
    markeredgecolor='red',          # solid red edge
    markeredgewidth=1.5,
    ecolor='red',                    # <-- error bars
    color='red'                      # (optional, keeps everything consistent)
)


#EXPERIMENTAL DATA
exp1perms = np.array([0.0443,0.0303,0.0121,0.0104,0.0053]) #original numbers, why was He different?
exp2perms = np.array([0.051,0.0262,0.0125,0.0101,0.0053])
exp2errs = np.array([0.00396, 0.00032, 0.0001716, 0.000528, 6.6208e-05])
exp1errs = np.array([np.max([abs(exp1perms[i]-exp2perms[i]),exp2errs[i]]) for i in range(len(exp1perms))])


'''
#from python script output
[0.012248291250460825, 0.012003278003532847, 0.011983945317661934, 0.012164985888480057, 0.0123327454233739, 0.01246497347857325]
N2 error
0.00017164350937311825 X
[0.02620664965071126, 0.02599787550255046, 0.026317883307972346]
He error
0.00032000780542188606
[0.050976924971430124, 0.0470090470610939]
H2 error
0.003967877910336225
[0.005281810415717774, 0.00534801906793021]
SF6 error
6.620865221243586e-05 X
[0.010089211868565848, 0.010472037337203656, 0.01061728306054501]
CO2 error
0.0005280711919791615 X
'''

print(((LAMPSperms-exp1perms)/exp1perms)*100.0)
exp1masss = np.array([2*1.00794,4.002602,(2*14.0067),(2*15.9994+12.0107),(6*18.998+32.06)])
#exp2perms = np.array([0.034,0.012,0.010])
#exp2perms = np.array([0.036,0.014,0.011])
#exp2masss = np.array([4.002602,(2*14.0067),(2*15.9994+12.0107)])
ax1.errorbar(
    1.0/np.sqrt(exp1masss),
    exp1perms,
    yerr=exp1errs,
    marker='o',
    ms=12,
    linestyle='None',
    label='$\\mathrm{Experiment}$',#'$\\mathrm{Experiment}^\\mathrm{a}$',
    markerfacecolor=(0, 0, 1, 0.3),  # blue with alpha=0.3
    markeredgecolor='blue',          # solid blue edge
    markeredgewidth=1.5,
    ecolor='blue',                    # <-- error bars
    color='blue',                      # (optional, keeps everything consistent)
    zorder=0
)


#ax1.errorbar(
#    1.0/np.sqrt(exp1masss),
#    exp2perms,
#    yerr=exp1errs,
#    marker='s',
#    ms=10,
#    linestyle='None',
#    label='$\\mathrm{Experiment}^\\mathrm{b}$',
#    markerfacecolor=(0, 0, 1, 0.3),  # blue with alpha=0.3
#    markeredgecolor='blue',          # solid blue edge
#    markeredgewidth=1.5,
#    zorder=0
#)



#FIT to all of the experimental data and simulation data
xvals = np.append(1/np.sqrt(exp1masss),1/np.sqrt(masses))
yvals = np.append(exp1perms,LAMPSperms)
errs = np.append(exp1errs,err_LAMPSperms)
#xvals = 1/np.sqrt(exp1masss)
#yvals = exp1perms
#errs = np.ones(len(yvals))
slope,intercept,slope_err,intercept_err = getfit(xvals,yvals,errs)
fitxvals = np.linspace(0.0,0.9,100)
fityvals = Lin(fitxvals,slope,intercept)
#ax1.plot(fitxvals,fityvals,marker=None,linestyle='--',color='blue',alpha=0.5,label=r'$\mathrm{Fit}$')
R=8.31441
Temp = 298.0
afrac_exp = slope*np.sqrt(2*np.pi*(1e-3)*R*Temp)
print("Ap/A val = ",afrac_exp)
print("Ap/A err = ", slope_err*np.sqrt(2*np.pi*(1e-3)*R*Temp))

R=8.31441
Temp = 298.0
fitxvals = np.linspace(0.0,0.9,100)
fityvals = Lin(fitxvals,slope,0.0)
fityvals_minus = Lin(fitxvals,slope-slope_err,0.0)
fityvals_plus = Lin(fitxvals,slope+slope_err,0.0)

ax1.fill_between(fitxvals, fityvals_minus, fityvals_plus,color='k',alpha=0.1)
ax1.plot(fitxvals,fityvals,marker=None,linestyle='--',color='k',alpha=1.0,zorder=-1,label='$A_p/A=0.23(1)$')#'$\\mathrm{Fit}$')
ax1.legend(loc='lower right',fontsize=16,handlelength=1.0,handletextpad=0.3)



#FIT to the simulation values
'''
xvals = 1/np.sqrt(masses)
yvals = LAMPSperms
errs = err_LAMPSperms
slope,intercept = getfit(xvals,yvals,errs)
fitxvals = np.linspace(0.0,0.9,100)
fityvals = Lin(fitxvals,slope,intercept)
ax1.plot(fitxvals,fityvals,marker=None,linestyle='--',color='red',alpha=0.5,label=None)#'$\\mathrm{Fit}$')
afrac_sim = slope*np.sqrt(2*np.pi*(1e-3)*R*Temp)
print("Ap/A sims = ",afrac_sim)
'''

#JUST PLOT LINE WITH AP/A=0.22 from sims

R=8.31441
Temp = 298.0
fitxvals = np.linspace(0.0,0.9,100)
fityvals = Lin(fitxvals,0.22/np.sqrt(2*np.pi*(1e-3)*R*Temp),0.0)
fityvals_minus = Lin(fitxvals,0.20/np.sqrt(2*np.pi*(1e-3)*R*Temp),0.0)
fityvals_plus = Lin(fitxvals,0.24/np.sqrt(2*np.pi*(1e-3)*R*Temp),0.0)

#ax1.fill_between(fitxvals, fityvals_minus, fityvals_plus,color='k',alpha=0.1)
#ax1.plot(fitxvals,fityvals,marker=None,linestyle='--',color='k',alpha=1.0,zorder=-1,label='$A_p/A=0.22(2)$')#'$\\mathrm{Fit}$')
#ax1.legend(loc='lower right',fontsize=16,handlelength=1.0,handletextpad=0.3)
# 2. Extract the current handles and labels
handles, labels = ax1.get_legend_handles_labels()
# 3. Specify your exact desired order by index
# Example: Swapping index 0 and 1 so the trend line shows first
desired_order = [2, 1, 0] #[0, 1, 3 ,2]
ordered_handles = [handles[i] for i in desired_order]
ordered_labels = [labels[i] for i in desired_order]
# 4. Pass the custom-sorted lists to the legend
ax1.legend(ordered_handles, ordered_labels,loc='lower right',fontsize=16,handlelength=1.0,handletextpad=0.3)


ax1.set_ylabel('$Q \\, \\, (\\mathrm{mol} / \\mathrm{s} \\cdot \\mathrm{Pa} \\cdot \\mathrm{m}^{2})$',fontsize=18,usetex=True)
ax1.set_xlabel('$1/\\sqrt{M_W} \\, \\, (1/\\sqrt{\\mathrm{g/mol}})$',fontsize=18,usetex=True)

# make tick labels larger
ax1.tick_params(axis='x', labelsize=12)  # x-axis tick labels
ax1.tick_params(axis='y', labelsize=12)  # y-axis tick labels



ax1.set_xlim([0.0,0.8])
ax1.set_ylim([0.0,0.055])



ax1.grid(True, which='major', linestyle='--', linewidth=0.6, alpha=0.5)
plt.savefig('../figures/grahamslaw.png', dpi=900, bbox_inches='tight')
plt.tight_layout()
plt.show()
