import numpy as np

class QuantumEngine:
    def __init__(self, engine="ORCA", level_of_theory="B3LYP/6-31G(d)"):
        self.engine = engine
        self.level_of_theory = level_of_theory

    def optimize_and_freq(self, geometry, is_ts=False):
        """
        Mock Quantum Engine Interface.
        In a real implementation, this would use ASE to call ORCA or Psi4.
        """
        # Simulate an optimization and frequency calculation
        if geometry == "geometry_guess_1":
            energy = -910.1234
            freqs = [-500.5, 300.1, 1500.2, 3000.5] if is_ts else [300.1, 1500.2, 3000.5]
        elif geometry == "geometry_guess_2":
            energy = -910.1001
            freqs = [-200.2, 400.1, 1600.2, 3100.2] if is_ts else [400.1, 1600.2, 3100.2]
        elif geometry == "geometry_guess_3":
            energy = -910.1500
            freqs = [-800.8, 500.1, 1400.2, 2900.2] if is_ts else [500.1, 1400.2, 2900.2]
        else:
            energy = -100.0
            freqs = [1000.0, 2000.0]

        return {
            "electronic_energy": energy - (np.random.random() * 0.05), # randomized slight variation
            "frequencies": freqs,
            "optimized_geometry": "optimized_coords"
        }

    def validate_ts(self, frequencies):
        neg_freqs = [f for f in frequencies if f < 0]
        if len(neg_freqs) == 1:
            return True, "Valid TS (1 imaginary frequency)"
        elif len(neg_freqs) == 0:
            return False, "Invalid TS (0 imaginary frequencies - minimum)"
        else:
            return False, f"Invalid TS ({len(neg_freqs)} imaginary frequencies)"
