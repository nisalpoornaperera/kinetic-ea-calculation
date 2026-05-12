class GeometryBuilder:
    def build_reactant_complex(self, r1, r2, site):
        # Embed the reactants into the geometry string so ORCA mock can differentiate them
        return f"Complex_{r1}_{r2}_{site}"
