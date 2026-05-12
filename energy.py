import numpy as np

def get_corrected_energy(mol_data, is_ts=False):
    """
    Calculates zero-point energy and corrects the electronic energy.
    TS molecules have one imaginary frequency that is ignored.
    """
    freqs = np.array(mol_data.get('frequencies', []))
    
    if is_ts:
        freqs = freqs[freqs > 0]
        
    zpe = np.sum(freqs) * 0.5 / 219474.63137
    
    elec_energy = mol_data.get('electronic_energy', 0.0)
    return elec_energy + zpe, zpe

def calc_activation_energy(r_corr, ts_corr):
    """
    Activation Energy is the difference between Transition State and Reactants
    """
    return ts_corr - r_corr
