class EaValidator:
    def validate_ts(self, imaginary_freqs):
        """
        Validates TS structural properties.
        Exactly one imaginary frequency required.
        """
        if len(imaginary_freqs) == 1:
            return True, "Valid TS (1 imaginary frequency)"
        elif len(imaginary_freqs) == 0:
            return False, "Invalid TS (0 imaginary frequencies - likely a minimum)"
        else:
            return False, f"Invalid TS ({len(imaginary_freqs)} imaginary frequencies - higher order saddle point)"

    def check_negative_ea(self, ea_hartree):
        """
        Checks if Ea is negative and issues warnings.
        """
        if ea_hartree < 0:
            return ("Warning: Negative Ea detected. This may indicate an invalid TS, "
                    "incorrect energy reference, or barrierless association. "
                    "Please inspect TS validation, imaginary frequency, IRC/path connection, "
                    "charge, spin, and reactant complex energy.")
        return ""
