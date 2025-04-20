import numpy as np

def linear_curve(q, base_price, slope):
    return base_price + slope * q

def logarithmic_curve(q, base_price, scale):
    return base_price * (1 + scale * np.log1p(q))

def exponential_curve(q, base_price, growth):
    return base_price * np.exp(growth * q)