# Homework Set 4 [Due by 10/10 Tues 11 PM, Group]:

In this HW, write codes for pricing options under SABR stochastic volatility model

* Hagan's volatility approximation formula is already provided for beta=0 (normal vol) and 0<beta<=1 (bsm vol). Using the codes, complete the smile calibration method: When 3 options prices (or volatilities) are given, find the roots of (sigma0, alpha, rho).
* Write MC simulation pricing. (Simulate both price and volatility)
* Write conditional MC simulation pricing. (Simulate only volatility, compute integrated variance, then use normal or bsm formula)
* Complete the test code and make sure it runs without error.

## Suggestions for final projects
* Arbitrage-free pricing method by [Kennedy et al, 2011](http://www.tandfonline.com/doi/abs/10.1080/1350486X.2011.646523) ([Download](http://ssrn.com/abstract_id=2043504)): simpler approach introduced in class is enough. Implement the method, create a new class ModelKennedy in sabr.py, and write a thorough test code. In python notebook, summarize the method, write a quick help and report strength and weakness. 
* Efficient first guess for SABR calibrations to 3 option prices by [Le Floc’h and Kennedy, 2014](https://ssrn.com/abstract_id=2467231) (see also [here](https://www.clarusft.com/sabr-calibration-a-simple-explicit-initial-guess/)): Implement the method, add to sabr.py, and write a code comparing the efficient against the dumb initial guess. In python notebook, summarize the method, write a quick help and report strength and weakness. 

* [Heston Model](https://en.wikipedia.org/wiki/Heston_model): pricing by conditional Monte-Carlo + Fast Fourier Transform (FFT) method. Contact me.
