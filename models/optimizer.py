from scipy.optimize import minimize_scalar
from models.lethality import required_time

def find_optimal_time(D_ref, T_ref, Z, T, target_log):
    t = required_time(D_ref, T_ref, Z, T, target_log)
    return round(t, 2)

def find_optimal_temperature(D_ref, T_ref, Z, target_log, T_min=60, T_max=100):
    def objective(T):
        return required_time(D_ref, T_ref, Z, T, target_log)
    
    result = minimize_scalar(objective, bounds=(T_min, T_max), method='bounded')
    return round(result.x, 2), round(result.fun, 2)