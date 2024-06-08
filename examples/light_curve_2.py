#!/usr/bin/env python
import matplotlib.pyplot
import numpy as np
import pylab
import os
import matplotlib.pyplot as plt
import GeePea
import MyFuncs as MF
import Infer
from scipy.stats.distributions import chi2
from scipy.stats.distributions import gamma

# define transit parameters
# mfp = [0., 2.5, 9.2, .1, 0.2, 0.5, 0.3, 1., 0.]
# hp = [0.0003,0.1,0.0003]
# ep = [0.0001, 0, 0.1, 0.001, 0.01, 0, 0, 0.0001, 0, 0.0001, 0.001, 0.00001]
#
# mfp = [246.15 ,5.2,11.2,.1,0.4, 0.1519 , 0.3383,1,0]
# hp = [0.0005,100,100,100,100,100,100,0.0005]
# ep = [0.0001 ,0 ,0.1 ,0.001 ,0.01 ,0 ,0 ,0.0001 , 0.0, 0.0005, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.0001]


# mfp = [246.15, 2.218581, 8.92,.1,0.671, 0.0920,0.2656,1,0]
# hp = [0.091,0.98,1.99,1.99,1.99,1.99,1.99,1.99,0.0003]
# ep = [0.0001 ,0 ,0.0001 ,0.0001 ,0.0001 ,0 ,0 ,0.0001 , 0.0001, 0.0005, 0.001, 0.001,0.001, 0.001,0.001, 0.001, 0.001, 0.0001]


mfp = [246.15, 2.218581, 8.92, .1, 0.671, 0.0905,	0.2818, 1, 0]
hp = [0.0005, 30, 30, 30, 30, 30, 30, 0.0005]
#    [ #1    #2  #3     #4      #5    #6 #7   #8    #9       #10     #11    #12    #13    #14    #15     #16    #17]
ep = [0.000, 0, 0.000, 0.0001, 0.000, 0, 0, 0.0001, 0.0001, 0.0005, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.0001]

# create the data set (ie training data) with some simulated systematics
# time = np.linspace(-0.1,0.1,200)
# flux = MF.Transit_aRs(mfp,time) + np.random.normal(0,0.001,time.size)
# pylab.plot(time,flux,'.')
# pylab.savefig('sample.png')

fluxread = np.loadtxt('/Users/poojaalgikar/PycharmProjects/RGPECPYTHON/GeePea/examples/Nicmos1.dat')
# fluxread = np.delete(fluxread, slice(119), axis=0)
IS = np.loadtxt('/Users/poojaalgikar/PycharmProjects/RGPECPYTHON/GeePea/examples/Nicmos2.dat')
# IS = np.delete(IS, slice(119), axis=0)
time_n = IS[:, 0] - 2454000
IS = np.delete(IS, [0, 1, 8], axis=1)
fluxreadN = np.delete(fluxread, [0, 1], axis=1)
orbit1 = fluxread[:, 1] == 1
orbit2 = fluxread[:, 1] == 2
orbit3 = fluxread[:, 1] == 3
orbit4 = fluxread[:, 1] == 4
orbit5 = fluxread[:, 1] == 5
# for i in range(18):

# IStrain= IS[~orbit3]
# A = np.append(IStrain, np.ones([len(IStrain),1]),1)
# beta = np.linalg.lstsq(A, fluxtrain, rcond=None)[0]
# B = np.append(IS, np.ones([len(IS),1]),1)
# flux0=np.dot(B,beta)
# for i in range(18):
i = 1  # wavelength channel
flux = fluxreadN[:, i]
fluxtrain = flux[~orbit3]
fluxD = flux / fluxtrain.mean()
# matplotlib.pyplot.plot(time_n, fluxD, 'b.')
# matplotlib.pyplot.xlabel('time')
# matplotlib.pyplot.ylabel('flux')
# pylab.savefig('flux.png')
IS = (IS - IS.mean(axis=0)) / IS.std(axis=0)
IS[:, 0] = time_n
IS1 = IS[orbit1, :]
IS2 = IS[orbit2, :]
IS3 = IS[orbit3, :]
# IS3[1,1]=10000
IS4 = IS[orbit4, :]
IS5 = IS[orbit5, :]


# define the GP
# gp = GeePea.GP(time,flux,p=mfp+hp,mf=MF.Transit_aRs_ctypes,ep=ep) #using normal SqExponential kernel
# gp = GeePea.GP(time_n,flux_n,p=mfp+hp,kf=GeePea.ToeplitzSqExponential,mf=MF.Transit_aRs,ep=ep)
# gp = GeePea.GP(IS,flux_n,p=mfp+hp,xmf=time_n,kf=GeePea.SqExponential,mf=MF.Transit_aRs,ep=ep)

def projectionstatistics(IS):
    # H = np.append(np.ones([len(IS), 1]), IS, 1)
    H = IS
    m, n = np.shape(H)
    M = np.median(H, axis=0)
    u = np.zeros((m, n))
    v = np.zeros((m, n))
    z = np.zeros((m, 1))
    P = np.zeros((m, m))
    for kk in range(m):
        u[kk, :] = H[kk, :] - M
        v[kk, :] = u[kk, :] / np.linalg.norm(u[kk, :])
        for ii in range(m):
            z[ii, :] = np.dot(H[ii, :], v[kk, :])
        zmed = np.median(z, axis=0)
        mad = 1.4826 * (1 + 15 / m) * np.median(np.abs(z - zmed))
        for ii in range(m):
            P[kk, ii] = np.abs(z[ii] - zmed) / mad
    ps = np.max(P, axis=0)
    return ps


# ISany=IS[~orbit3,:]
# ps_3=projectionstatistics(IS3)
# # ps_3=np.ones((130))
# ps_any =projectionstatistics(ISany)
#
# ps_any=projectionstatistics(ISany)
# ps2=ps_any[0:len(IS2)]
# ps4=ps_any[len(IS2):len(IS2)+len(IS4)]


IS12=np.vstack((IS1,IS2))
IS45=np.vstack((IS4,IS5))

ps12 = projectionstatistics(IS12)
ps3 = projectionstatistics(IS3)
ps45 = projectionstatistics(IS45)

ps=np.hstack((ps12,ps3,ps45))
wi = np.zeros((ps.size, 1))
cutoff = chi2.ppf(0.975, df=IS.shape[1])
for i in range(ps.size):
    wi[i] = np.minimum(1, cutoff / np.square(ps[i]))


def logPrior(p, nhp):
    # return -np.inf if restricted prior space
    # this way the full posterior won't be evaluated, which is costly
    # transit parameters
    # if np.array(p[:8]<0).any(): return -np.inf
    # hyperparameters
    # if np.array(p[-nhp:]<0).any(): return -np.inf
    # limb darkening parameters
    # if (p[5] + p[6]) > 1.: return -np.inf #ensure positive surface brightness

    # else calculate the log prior
    log_prior = 0.
    # eg of gamma prior
    log_prior += np.log(gamma.pdf(p[-nhp + 1], 1., 0., 1.e2)).sum()
    # eg or normal prior
    # log_prior += np.log(norm_dist.pdf(p[4],b,b_err)).sum()
    return log_prior


gp1 = GeePea.GP(IS, fluxD, n_hp=9, n_mfp=9, xmf=time_n, xmf_pred=time_n, x_pred=IS, p=mfp + hp,
               kf=GeePea.SqExponentialARD, mf=MF.Transit_aRs_ctypes, ep=ep,mode=1,wi=wi)    #RGPE

gp1.logPrior = logPrior

# optimise the free parameters
gp1.optimise()
t_pred, t_pred_err = gp1.predict(wn=True)

pylab.figure(1)
gp1.plot()





gp2=GeePea.GP(IS, fluxD, n_hp=9, n_mfp=9, xmf=time_n, xmf_pred=time_n, x_pred=IS, p=mfp + hp,
               kf=GeePea.SqExponentialARD, mf=MF.Transit_aRs_ctypes, ep=ep,mode=2,wi=wi)     #MLE
gp2.logPrior = logPrior
gp2.optimise()
t_predL, t_pred_errL = gp2.predict(wn=True)
# and plot
pylab.figure(2)
gp2.plot()
pylab.savefig('lightcurve.png')


pylab.figure(3)
fig, ax = plt.subplots()
ax.plot(time_n, fluxD, '.', label='Data points')
ax.plot(time_n, t_predL, 'r', label='MLE')
ax.plot(time_n, t_pred, 'k:', label='R-GMPE')
plt.xlabel('time ([HJD-2454000])')
plt.ylabel('relative flux')
legend = ax.legend(loc='upper center', shadow=True, fontsize='x-small')
legend.get_frame().set_facecolor('tab:gray')
plt.show()


# can also run an MCMC by using GP.logPosterior()
# gp.ep[-9:] = 0
# gp.p[0], gp.ep[0] = 246.15, 0.00
# gp.p[1], gp.ep[1] = 2.218581, 0.00
# gp.ep[2] = 0.00
# gp.p[2] = 8.92
# gp.p[4], gp.ep[4] = 0.671, 0.00

lims = (0, 10000, 1)
Infer.MCMC_N(gp1.loglikelihoodUN, gp1.p, (), 20000, gp1.ep, N=4, adapt_limits=lims, glob_limits=lims)

# get the parameters and uncertainties from the MCMC
gp1.p, gp1.ep = Infer.AnalyseChains(10000, n_chains=4)

# and plot the correlations
pylab.figure(4)
Infer.PlotCorrelations(10000, n_chains=4, p=np.where(np.array(gp1.ep) > 0)[0])
pylab.savefig('Correlations.png')
# #delete the MCMC chains
if os.path.exists('MCMC_chain_1.npy'): os.remove('MCMC_chain_1.npy')
if os.path.exists('MCMC_chain_2.npy'): os.remove('MCMC_chain_2.npy')
if os.path.exists('MCMC_chain_3.npy'): os.remove('MCMC_chain_3.npy')
if os.path.exists('MCMC_chain_4.npy'): os.remove('MCMC_chain_4.npy')
# raw_input()
