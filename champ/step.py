import numpy as np
from scipy.integrate import cumtrapz

def imp_to_step(t_imp, y_imp):
    dt = np.median(np.diff(t_imp))
    assert all(np.isclose(val, dt) for val in np.diff(t_imp))

    y_step = cumtrapz(y_imp, initial=0)*dt

    return t_imp, y_step
