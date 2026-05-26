import numpy as np

def d_value(D_ref, T_ref, Z, T):
    return D_ref * 10 ** ((T_ref - T) / Z)

def log_reduction(D_ref, T_ref, Z, T, time):
    D = d_value(D_ref, T_ref, Z, T)
    return time / D

def kill_curve(D_ref, T_ref, Z, T, max_time=60):
    times = np.linspace(0, max_time, 300)
    log_reductions = [log_reduction(D_ref, T_ref, Z, T, t) for t in times]
    return times, log_reductions