class ReactiveSiteIdentifier:
    def identify_sites(self, mechanism, r1_parsed, r2_parsed):
        """
        Identifies reactive sites based on selected mechanism.
        """
        return mechanism.get("attacked_atom_options", ["Default active site"])
