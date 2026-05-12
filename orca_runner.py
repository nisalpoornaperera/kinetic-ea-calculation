import numpy as np

class OrcaRunner:
    def __init__(self, method="B3LYP", basis="6-31G(d)"):
        self.method = method
        self.basis = basis

    def run_optimization(self, geometry, is_ts=False):
        """
        Mocks ORCA DFT Optimization and Frequencies
        """
        # Provide physically constrained mocked values to test EA validator
        energy = -950.0  # Base energy
        
        if is_ts:
            energy = -949.9  # TS is higher in energy than reactant complex
            freqs = [-500.5, 300.1, 1500.2] # 1 Imaginary frequency
        elif geometry == "Reactant_Complex_Geometry":
            energy = -950.05
            freqs = [200.1, 1400.2, 2900.5]
        else:
            energy = -950.0 # Separated reactants sum 
            freqs = [300.1, 1500.2, 3000.5]

        return {
            "electronic_energy": energy,
            "frequencies": freqs,
            "imaginary_freqs": [f for f in freqs if f < 0],
            "geometry": "Optimized_" + geometry
        }
