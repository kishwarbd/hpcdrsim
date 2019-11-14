# optimization.py :- perform the optimization 
from scipy.optimize import minimize
import numpy as np

class Optimizer(object):
    def __init__(self):
        # intialize the optimizer
        pass 

    def obj_func(self, x, a, b, c, d, e, f, g):
        # objective function
        opt_value = a*e*x[0]**5 + a*f*x[0]**4 + a*g*x[0]**3 +\
                    b*e*x[0]**4 + b*f*x[0]**3 + b*g*x[0]**2 +\
                    c*e*x[0]**3 + c*f*x[0]**2 + c*g*x[0] +\
                    d*e*x[0]**2 + d*f*x[0] + d*g
        return opt_value

    def deriv_func(self, x, a, b, c, d, e, f, g):
        # derivatve of objective function
        derivative = 5*a*e*x[0]**4 + 4*a*f*x[0]**3 + 3*a*g*x[0]**2 +\
                    4*b*e*x[0]**3 + 3*b*f*x[0]**2 + 2*b*g*x[0] +\
                    3*c*e*x[0]**2 + 2*c*f*x[0] + c*g + 2*d*e*x[0] + d*f
        return np.array([derivative])
                         
    def find_opt_freq(self, reg_runtime, reg_power, min_freq, max_freq):
        # determine the optimal values
        a = reg_power[0]; b = reg_power[1]; c = reg_power[2]; d = reg_power[3]
        e = reg_runtime[0]; f = reg_runtime[1]; g = reg_runtime[2]
        
        initial_guess = (min_freq+max_freq)/2.0
        res = minimize(self.obj_func, (initial_guess,),
    args=(a,b,c,d,e,f,g,), jac=self.deriv_func, bounds=((min_freq,
    max_freq),), method='SLSQP', options={'disp': False})
        return res.x 

