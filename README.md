# Homework Set 4 [Due by 10/10 Tues 11 PM, Group]:

In this HW, write codes for pricing options under SABR stochastic volatility model

* Hagan's volatility approximation formula is already provided for beta=0 (normal vol) and 0<beta<=1 (bsm vol). Using the codes, complete the smile calibration method: When 3 options prices (or volatilities) are given, find the roots of (sigma0, alpha, rho).
* Write MC simulation pricing. (Simulate both price and volatility)
* Write conditional MC simulation pricing. (Simulate only volatility, compute integrated variance, then use normal or bsm formula)
* Complete the test code and make sure it runs without error.

## For advanced works (e.g., final project)
You may consider implementing and improving [Kennedy's method](http://www.tandfonline.com/doi/abs/10.1080/1350486X.2011.646523) ([Download](http://ssrn.com/abstract_id=2043504))
