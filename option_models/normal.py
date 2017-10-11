# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 22:56:58 2017

@author: jaehyuk
"""
import numpy as np
import scipy.stats as ss
import scipy.optimize as sopt

def normal_price(strike, spot, vol, texp, intr=0.0, divr=0.0, cp_sign=1):
    div_fac = np.exp(-texp*divr)
    disc_fac = np.exp(-texp*intr)
    forward = spot / disc_fac * div_fac
    
    if( texp<=0 ):
        return disc_fac * np.fmax( cp_sign*(forward-strike), 0 )
    
    # floor vol_std above a very small number
    vol_std = np.fmax(vol*np.sqrt(texp), 1e-32)
    d = (forward-strike)/vol_std
    
    price = disc_fac*(cp_sign*(forward-strike)*ss.norm.cdf(cp_sign*d)+vol_std*ss.norm.pdf(d))
    return price

class NormalModel:
    
    vol, intr, divr = None, None, None
    
    def __init__(self, vol, intr=0, divr=0):
        self.vol = vol
        self.intr = intr
        self.divr = divr
    
    def price(self, strike, spot, vol, texp, intr=0.0, divr=0.0, cp_sign=1):
        return normal_price(strike, spot, self.vol, texp, intr=self.intr, divr=self.divr, cp_sign=cp_sign)
    
    def delta(self, strike, spot, vol, texp, intr=0.0, divr=0.0, cp_sign=1):
        ''' 
        <-- PUT your implementation here
        '''
        return 0

    def vega(self, strike, spot, vol, texp, intr=0.0, divr=0.0, cp_sign=1):
        ''' 
        <-- PUT your implementation here
        '''
        return 0

    def gamma(self, strike, spot, vol, texp, intr=0.0, divr=0.0, cp_sign=1):
        ''' 
        <-- PUT your implementation here
        '''
        return 0

    def impvol(self, price, strike, spot, texp, cp_sign=1):
        div_fac = np.exp(-texp*self.divr)
        disc_fac = np.exp(-texp*self.intr)
        forward = spot/disc_fac*div_fac
        price_fwd = price/disc_fac
        price_straddle = 2*price_fwd - cp_sign*(forward-strike)# forward straddle price
        
        int_val = np.fmax(cp_sign*(forward-strike), 0)
        if(int_val > price_fwd):
            raise ValueError('Option value is lower than intrinsic value', price_fwd, int_val) 
        
        iv_func = lambda _vol: \
            normal_price(strike, forward, _vol, texp, cp_sign=cp_sign) - price_fwd
        vol = sopt.brentq(iv_func, 0, price_straddle*np.sqrt(np.pi/2/texp))
        return vol