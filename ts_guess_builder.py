class TSGuessBuilder:
    def build_guess(self, complex_geo, mechanism, site):
        """
        Uses constrained scan, NEB or QST2 based on mechanism rules
        """
        method = mechanism.get("ts_generation", {}).get("method", "interpolation")
        return f"TS_Guess_Geometry_via_{method}_at_{site}"
