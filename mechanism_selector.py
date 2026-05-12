from mechanism_database import MechanismDatabase

class MechanismSelector:
    def __init__(self):
        self.db = MechanismDatabase()

    def find_matches(self, r1_formula, r2_formula):
        """
        Matches reactants to mechanism database.
        Mock implementation prioritizing known formulas for demonstration.
        """
        matches = []
        all_mechs = self.db.get_all()
        for m in all_mechs:
            # Simplified matching logic
            if "O" in r2_formula or "O3" in r2_formula:
                matches.append(m)
        return matches
