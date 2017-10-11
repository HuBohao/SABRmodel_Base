    # -*- coding: utf-8 -*-
"""
Created on Tue Oct 10

@author: jaehyuk
"""

import numpy as np
import scipy.stats as ss
import scipy.optimize as sopt
from . import normal

def sabr_normvol(strike, forward, sigma, texp, alpha=0, rho=0, beta=0):
    # forward, spot, sigma may be either scalar or np.array. 
    # texp, alpha, rho, beta should be scholar values

    if(texp<=0.0):
        return( sigma )
    
    zeta = (forward - strike)*alpha/np.fmax(sigma, 1e-32)
    # explicitly make np.array even if args are all scalar or list
    if isinstance(zeta, float):
        zeta = np.array([zeta])
        
    yy = np.sqrt(1 + zeta*(zeta - 2*rho))
    chi_zeta = np.zeros(zeta.size)
    
    rho2 = rho*rho
    ind = np.where(abs(zeta) < 1e-5)
    chi_zeta[ind] = 1 + 0.5*rho*zeta[ind] + (0.5*rho2 - 1/6)*zeta[ind]**2 + 1/8*(5*rho2-3)*rho*zeta[ind]**3

    ind = np.where(zeta >= 1e-5)
    chi_zeta[ind] = np.log( (yy[ind] + (zeta[ind] - rho))/(1-rho) ) / zeta[ind]

    ind = np.where(zeta <= -1e-5)
    chi_zeta[ind] = np.log( (1+rho)/(yy[ind] - (zeta[ind] - rho)) ) / zeta[ind]

    nvol = sigma * (1 + (2-3*rho2)/24*alpha**2*texp) / chi_zeta
 
    return(nvol[0] if nvol.size==1 else nvol)

def sabr_price(strike, forward, sigma, texp, cp_sign=1, alpha=0, rho=0, beta=0):
    nvol = sabr_normvol(strike, forward, sigma, texp, alpha=alpha, rho=rho, beta=beta)
    price = normal.normal_price(strike, forward, nvol, texp, cp_sign=cp_sign)
    return price


class SabrModel_Hagan:
    alpha, beta, rho = 0, 0.0, 0.0
    sigma, intr, divr = None, None, None
    
    def __init__(self, sigma, alpha=0, rho=0.0, beta=0.0, intr=0, divr=0):
        self.sigma = sigma
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.intr = intr
        self.divr = divr

    def normvol(self, strike, spot, texp):
        div_fac = np.exp(-texp*self.divr)
        disc_fac = np.exp(-texp*self.intr)
        forward = spot / disc_fac * div_fac
        return sabr_normvol(strike, forward, self.sigma, texp, alpha=self.alpha, rho=self.rho, beta=self.beta)
        
    def price(self, strike, spot, texp, cp_sign=1):
        n_vol = self.normvol(strike, spot, texp) 
        return normal.normal_price(strike, spot, n_vol, texp, cp_sign=cp_sign, intr=self.intr, divr=self.divr)
    
    def impvol(self, price, strike, spot, texp, cp_sign=1):
        iv_func = lambda _sigma: \
            sabr_price(strike, forward, self.sigma, texp, cp_sign, alpha=self.alpha, rho=self.rho, beta=self.beta) - price
        sigma = sopt.brentq(iv_func, 0, 10)
        return sigma
