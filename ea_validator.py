import os

class EaValidator:
    def is_dummy_data(self, data):
        """ Reject values such as known dummy energies or sources listed as mock/test """
        if not data:
            return True
            
        energy = data.get("electronic_energy", 0)
        freqs = data.get("frequencies", [])
        source = str(data.get("source", "")).lower()

        # Check source string explicitly
        if any(bad in source for bad in ["mock", "test", "demo", "placeholder", "none", ""]):
            return True

        if abs(energy - -501.100000) < 0.0001:
            return True
        if abs(energy - -549.950000) < 0.0001:
            return True
        if abs(energy - -897.550000) < 0.0001:
            return True
        if len(freqs) == 1 and abs(freqs[0] - -500.5) < 0.0001:
            return True

        return False

    def validate_energy_reference(self, reactants_data, r_complex_data, ts_data):
        errors = []

        if self.is_dummy_data(reactants_data) or self.is_dummy_data(r_complex_data) or self.is_dummy_data(ts_data):
            errors.append("Invalid energy computation: dummy, test, or missing input data detected.")

        rc_form = reactants_data.get('formula')
        ts_form = ts_data.get('formula')
        
        if rc_form and ts_form and rc_form != ts_form:
            errors.append(f"Stoichiometry mismatch: Reactants ({rc_form}) vs TS ({ts_form})")

        for key in ["method", "basis", "charge", "multiplicity"]:
            r_val = reactants_data.get(key)
            ts_val = ts_data.get(key)
            if r_val != ts_val:
                errors.append(f"Inconsistent {key} between reactants ({r_val}) and TS ({ts_val}).")

        if len(reactants_data.get("imaginary_freqs", [])) > 0:
            errors.append("Reactants have imaginary frequencies (not a minimum).")
        if len(r_complex_data.get("imaginary_freqs", [])) > 0:
            errors.append("Reactant complex has imaginary frequencies.")
        if len(ts_data.get("imaginary_freqs", [])) != 1:
            errors.append(f"TS must have exactly 1 imaginary frequency, found {len(ts_data.get('imaginary_freqs', []))}.")

        e_diff = abs(ts_data.get("electronic_energy", 0) - reactants_data.get("electronic_energy", 0))
        if e_diff > 2.0:
            errors.append(f"Invalid energy comparison: TS and reactants differ by more than 2 Hartree ({e_diff:.2f} Ha). This usually means different atom counts, wrong molecule, wrong charge/spin, or wrong output file.")

        return len(errors) == 0, errors

    def validate_ts(self, imaginary_freqs):
        if len(imaginary_freqs) == 1:
            return True, "Valid TS (1 imaginary frequency)"
        elif len(imaginary_freqs) == 0:
            return False, "Invalid TS (0 imaginary frequencies - likely a minimum)"
        else:
            return False, f"Invalid TS ({len(imaginary_freqs)} imaginary frequencies - higher order saddle point)"

    def check_negative_ea(self, ea_hartree):
        if ea_hartree < 0:
            return False, "Negative Ea detected after validation. This may indicate a submerged barrier or barrierless association, but it must be confirmed by IRC/path analysis."
        return True, ""
