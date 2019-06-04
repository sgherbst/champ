import numpy as np
from scipy.interpolate import interp1d

def step_to_pulse(t_step, y_step, t_width):
    delayed = interp1d(t_step, y_step, bounds_error=False, fill_value=(y_step[0], y_step[-1]))(t_step - t_width)
    return t_step, y_step - delayed

def center_pulse(t_pulse, y_pulse):
    i_max = np.argmax(y_pulse)
    t_max = t_pulse[i_max]

    return t_pulse-t_max, y_pulse

def get_pulse_coeffs(t_pulse, y_pulse, t_samp, n_pre, n_post):
    t_pulse, y_pulse = center_pulse(t_pulse=t_pulse, y_pulse=y_pulse)

    t_interp = np.linspace(-n_pre*t_samp, n_post*t_samp, n_pre+n_post+1)

    return interp1d(t_pulse, y_pulse)(t_interp)