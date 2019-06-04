import numpy as np
from scipy.integrate import cumtrapz

from skrf import Network

def s2sdd(s_params, option=1):
    """ Converts a 4-port single-ended S-parameter matrix to a 2-port differential mode representation.
    References:
    (1) https://www.aesa-cortaillod.com/fileadmin/documents/knowledge/AN_150421_E_Single_ended_S_Parameters.pdf
    (2) https://www.mathworks.com/help/rf/ug/s2sdd.html
    """

    # determine the port order from the given option

    if option == 1:
        ap = 0
        bp = 1
        an = 2
        bn = 3
    elif option == 2:
        ap = 0
        an = 1
        bp = 2
        bn = 3
    else:
        raise ValueError(f'Invalid option: {option}.')

    # fill entries of S-parameter matrix

    sdd = np.zeros((2, 2), dtype=np.complex128)

    a = 0
    b = 1

    sdd[a, a] = 0.5*(s_params[ap, ap] - s_params[ap, an] - s_params[an, ap] + s_params[an, an])
    sdd[a, b] = 0.5*(s_params[ap, bp] - s_params[ap, bn] - s_params[an, bp] + s_params[an, bn])
    sdd[b, a] = 0.5*(s_params[bp, ap] - s_params[bp, an] - s_params[bn, ap] + s_params[bn, an])
    sdd[b, b] = 0.5*(s_params[bp, bp] - s_params[bp, bn] - s_params[bn, bp] + s_params[bn, bn])

    # return new S-parameter matrix

    return sdd

def s2tf(s, zo, zs, zl):
    """ Converts a two-port S-parameter matrix to a transfer function,
    given characteristic impedance, input impedance, and output impedance.
    Reference: https://www.mathworks.com/help/rf/ug/s2tf.html
    """

    gamma_l = (zl-zo)/(zl+zo)
    gamma_s = (zs-zo)/(zs+zo)
    gamma_in = s[0,0]+(s[0,1]*s[1,0]*gamma_l/(1-s[1,1]*gamma_l))

    tf = ((zs + np.conj(zs))/np.conj(zs))*(s[1,0]*(1+gamma_l)*(1-gamma_s))/(2*(1-s[1,1]*gamma_l)*(1-gamma_in*gamma_s))

    return tf

def s4p_to_tf(s4p, zs=50, zl=50):
    # read S-parameter file
    ntwk = Network(s4p)

    # extract characteristic impedance
    # assumed to be the same for all 16 measurements
    z0 = ntwk.z0[0, 0]

    # extract frequency list
    freq = ntwk.frequency.f

    # extract transfer function
    resp = np.array([s2tf(s2sdd(s), 2 * z0, 2 * zs, 2 * zl) for s in ntwk.s])

    return freq, resp
