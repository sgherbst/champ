import numpy as np
from scipy.interpolate import interp1d
from scipy.fftpack import ifft
from math import floor

def is_mostly_real(v, ratio=1e-6):
    return np.all(np.abs(np.imag(v)/np.real(v)) < ratio)

def is_almost_int(v, thresh=1e-6):
    return np.modf(v)[0] < thresh

def tf_to_imp(freq, resp):
    """ Calculates the impulse response, given a single-sided transfer function.
    f should be non-negative and increasing.  See https://www.overleaf.com/read/mxxtgdvkmkvt
    """

    # compute frequency spacing
    df = np.median(np.diff(freq))

    # sanity checks
    assert all(np.isclose(df, val) for val in np.diff(freq)), 'Frequencies must be sampled linearly.'
    assert is_almost_int(np.max(freq) / df), 'df parameter is not aligned to the max frequency.'

    # compute number of points needed in frequency response vector (must be an even number)
    n = 2 * ((np.max(freq) / df) + 1)
    n = int(floor(n))
    n = (n // 2)*2

    # sanity checks
    assert n % 2 == 0, 'n must be even'
    assert ((n//2) - 1) * df <= np.max(freq), 'the highest requested frequency must not exceed np.max(f)'

    # copy f and tf vectors so they can be modified
    freq = freq.copy()
    resp = resp.copy()

    # make sure that the DC component is real if present
    if freq[0] == 0:
        assert is_mostly_real(resp[0]), 'The frequency response at DC must be essentially real.'
        resp[0] = np.abs(resp[0])
    else:
        dc = np.abs(resp[0])
        print(f'Adding estimated DC value to frequency response: {dc}.')

        freq = np.concatenate(([0], freq))
        resp = np.concatenate(([dc], resp))

    # calculate magnitude and phase
    ma = np.abs(resp)
    ph = np.unwrap(np.angle(resp))

    # interpolate magnitude and phase
    f_interp = [k*df for k in range(n//2)]
    ma_interp = interp1d(freq, ma)(f_interp)
    ph_interp = interp1d(freq, ph)(f_interp)

    # create frequency response vector needed for IFFT
    # note that Gtilde[n//2] is left at zero
    Gtilde = np.zeros(n, dtype=np.complex128)
    Gtilde[:(n//2)] = ma_interp * np.exp(1j*ph_interp)
    Gtilde[((n//2)+1):] = np.conjugate(Gtilde[((n//2)-1):0:-1])

    # compute impulse response
    y_imp = n*df*ifft(Gtilde)

    # check that the impulse response is real to within numerical precision
    assert is_mostly_real(y_imp), 'IFFT contains unacceptable imaginary component.'

    # having checked that, make the impulse response completely real
    y_imp = np.abs(y_imp)

    # compute the time vector
    t_imp = np.array([k for k in range(n)])*(1/(n*df))

    return t_imp, y_imp