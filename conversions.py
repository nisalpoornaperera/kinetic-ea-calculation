def convert_ea(ea_hartree):
    """
    Converts activation energy from Hartrees to other common units.
    """
    return {
        'hartree': ea_hartree,
        'kcal_mol': ea_hartree * 627.509,
        'kj_mol': ea_hartree * 2625.5,
        'ev': ea_hartree * 27.2114
    }
