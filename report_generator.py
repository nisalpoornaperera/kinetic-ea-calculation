from ea_validator import EaValidator

class ReportGenerator:
    def __init__(self):
        self.validator = EaValidator()

    def generate(self, mech_name, r_complex_data, r_sep_data, ts_data, ea_sep, ea_complex):
        report = []
        report.append("-" * 60)
        report.append(f"Mechanism: {mech_name}")
        report.append("-" * 60)
        
        # TS Validation
        valid_ts, ts_msg = self.validator.validate_ts(ts_data["imaginary_freqs"])
        report.append(f"TS Validation: {ts_msg}")
        
        # Energies
        report.append(f"\nSeparated Reactants E (A+B): {r_sep_data['electronic_energy']:.6f} Ha")
        report.append(f"Reactant Complex E (A+B): {r_complex_data['electronic_energy']:.6f} Ha")
        report.append(f"Transition State E (C): {ts_data['electronic_energy']:.6f} Ha")
        
        report.append("\nImaginary Frequencies (TS): " + str(ts_data["imaginary_freqs"]))

        report.append("\nActivation Energy (from separated reactants):")
        report.append(f"Ea (Ha) = {ea_sep['hartree']:.6f}")
        report.append(f"Ea (kJ/mol) = {ea_sep['kj_mol']:.6f}")

        report.append("\nActivation Energy (from pre-reactive complex):")
        report.append(f"Ea (Ha) = {ea_complex['hartree']:.6f}")
        report.append(f"Ea (kJ/mol) = {ea_complex['kj_mol']:.6f}")

        # Warn on negative Ea
        val_msg_sep = self.validator.check_negative_ea(ea_sep['hartree'])
        if val_msg_sep:
            report.append(f"\n{val_msg_sep}")

        report.append("-" * 60)
        return "\n".join(report)
