import os
import re

class OrcaRunner:
    def __init__(self, method="B3LYP", basis="6-31G(d)"):
        self.method = method
        self.basis = basis

    def run_optimization(self, geometry, is_ts=False):
        """
        Reads REAL completed ORCA output files instantly.
        Extracts final electronic energy and vibrational frequencies.
        """
        filename = f"{geometry.replace(' ', '_')}.out"
        
        if not os.path.exists(filename):
            print(f"Warning: ORCA output file {filename} not found.")
            return {
                "source": "None",
            }
            
        energy = None
        freqs = []
        
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            # Parse final electronic energy
            if "FINAL SINGLE POINT ENERGY" in line:
                try:
                    energy = float(line.split()[-1])
                except:
                    continue
            # Parse vibrational frequencies
            elif re.match(r"^\s*\d+:\s+-?\d+\.\d+\s+cm\*\*-1", line):
                try:
                    parts = line.split()
                    freq = float(parts[1])
                    freqs.append(freq)
                except:
                    continue

        if energy is None:
            return {"source": "None"} # File exists but failed to read valid quantum data

        return {
            "source": f"ORCA output file ({filename})",
            "electronic_energy": energy,
            "frequencies": freqs,
            "imaginary_freqs": [f for f in freqs if f < 0],
            "geometry": geometry,
            "formula": geometry.split("_")[1] if "_" in geometry else geometry,
            "method": self.method,
            "basis": self.basis,
            "charge": 0,
            "multiplicity": 1
        }
