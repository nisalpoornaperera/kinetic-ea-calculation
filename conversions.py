HARTREE_TO_KCAL_MOL = 627.509
HARTREE_TO_KJ_MOL = 2625.50
HARTREE_TO_EV = 27.2114
CM_TO_HARTREE = 1.0 / 219474.63137

def convert_ea(ea_hartree):
    """Convert Activation Energy to other units."""
    return {
        "hartree": ea_hartree,
        "kcal_mol": ea_hartree * HARTREE_TO_KCAL_MOL,
        "kj_mol": ea_hartree * HARTREE_TO_KJ_MOL,
        "ev": ea_hartree * HARTREE_TO_EV
    }
