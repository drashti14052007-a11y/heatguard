def pasteurization_units(T, t, T_ref, Z):
    return t * 10 ** ((T - T_ref) / Z)

def f0_value(T, t):
    return t * 10 ** ((T - 121.1) / 10)

def required_time(D_ref, T_ref, Z, T, target_log):
    D = D_ref * 10 ** ((T_ref - T) / Z)
    return target_log * D