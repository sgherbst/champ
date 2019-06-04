from scipy.interpolate import interp1d

def step_to_pulse(t_step, y_step, t_width):
    delayed = interp1d(t_step, y_step, bounds_error=False, fill_value=(y_step[0], y_step[-1]))(t_step - t_width)
    return t_step, y_step - delayed