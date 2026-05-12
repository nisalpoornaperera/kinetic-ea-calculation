import numpy as np
from conversions import CM_TO_HARTREE

DEFAULT_SCALE_FACTOR = 0.9613

def calculate_zpe(frequencies, is_ts=False):
    """
    Calculates Zero Point Energy (ZPE) in Hartrees.
    For Reactants: filters out negative frequencies (should be none).
    For TS: ignores exactly one negative frequency.
    """
    freqs = np.array(frequencies, dtype=float)
    freqs = freqs[freqs != 0]

    if is_ts:
        # Ignore negative imaginary frequency for TS
        freqs = freqs[freqs > 0]
    else:
        freqs = freqs[freqs > 0]

    if len(freqs) == 0:
        return 0.0

    scaled_freqs = freqs * DEFAULT_SCALE_FACTOR
    zpe_hartree = 0.5 * np.sum(scaled_freqs * CM_TO_HARTREE)
    return zpe_hartree

def get_corrected_energy(electronic_energy, frequencies, is_ts=False):
    zpe = calculate_zpe(frequencies, is_ts)
    return electronic_energy + zpe, zpe

def calc_activation_energy(corr_r1, corr_r2, corr_ts):
    return corr_ts - (corr_r1 + corr_r2)
