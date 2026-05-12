import numpy as np
import hashlib

class OrcaRunner:
    def __init__(self, method="B3LYP", basis="6-31G(d)"):
        self.method = method
        self.basis = basis

    def _generate_pseudo_values(self, geometry):
        """Generates consistent pseudo-random energies based on reaction strings"""
        hash_val = int(hashlib.md5(geometry.encode()).hexdigest(), 16)
        base = -500.0 - (hash_val % 4000) / 10.0
        return base

    def run_optimization(self, geometry, is_ts=False):
        """
        Mocks ORCA DFT Optimization and Frequencies based on the geometry identity
        so different molecules give different outputs.
        """
        # Create a stable base structure reference from geometry string
        if "TS_" in geometry:
            base_ref = geometry.split("TS_")[1]
        else:
            base_ref = geometry

        if "Complex_" in geometry:
            parts = geometry.split("Complex_")[1]
            if "_" in parts:
                base_formula = parts.rsplit("_", 1)[0] # remove site
            else:
                base_formula = parts
        elif "Separated_" in geometry:
            base_formula = geometry.split("Separated_")[1]
        else:
            base_formula = geometry

        base_energy = self._generate_pseudo_values(base_formula)
        
        if is_ts:
            energy = base_energy + 0.15 # TS is highest energetically 
            freqs = [-500.5, 300.1, 1500.2] # 1 Imaginary frequency
        elif "Complex_" in geometry: # Reactant complex 
            energy = base_energy - 0.05 # Slightly lower than separated 
            freqs = [200.1, 1400.2, 2900.5]
        else: # Separated reactants (baseline)
            energy = base_energy 
            freqs = [300.1, 1500.2, 3000.5]

        return {
            "electronic_energy": energy,
            "frequencies": freqs,
            "imaginary_freqs": [f for f in freqs if f < 0],
            "geometry": "Optimized_" + geometry,
            "formula": base_formula,
            "method": self.method,
            "basis": self.basis,
            "charge": 0,
            "multiplicity": 1
        }
