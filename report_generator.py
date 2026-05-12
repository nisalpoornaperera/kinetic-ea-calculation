from ea_validator import EaValidator

class ReportGenerator:
    def __init__(self):
        self.validator = EaValidator()

    def generate(self, mech_name, r_complex_data, r_sep_data, ts_data, ea_sep, ea_complex):
        report = []
        report.append("-" * 60)
        report.append(f"Mechanism: {mech_name}")
        report.append("-" * 60)
        
        # Sources
        report.append("Data Sources:")
        report.append(f"Separated Reactants:")
        report.append(f"Source = {r_sep_data.get('source', 'Unknown')}")
        report.append(f"Method = {r_sep_data.get('method', 'Unknown')}")
        report.append(f"Basis = {r_sep_data.get('basis', 'Unknown')}")
        report.append(f"Electronic Energy = {r_sep_data.get('electronic_energy', 'None')}")
        
        report.append(f"\nReactant Complex:")
        report.append(f"Source = {r_complex_data.get('source', 'Unknown')}")
        report.append(f"Method = {r_complex_data.get('method', 'Unknown')}")
        report.append(f"Basis = {r_complex_data.get('basis', 'Unknown')}")
        report.append(f"Electronic Energy = {r_complex_data.get('electronic_energy', 'None')}")

        report.append(f"\nTransition State:")
        report.append(f"Source = {ts_data.get('source', 'Unknown')}")
        report.append(f"Method = {ts_data.get('method', 'Unknown')}")
        report.append(f"Basis = {ts_data.get('basis', 'Unknown')}")
        report.append(f"Electronic Energy = {ts_data.get('electronic_energy', 'None')}")
        report.append(f"Imaginary Frequencies = {ts_data.get('imaginary_freqs', 'None')}")
        
        # TS Validation
        valid_ts, ts_msg = self.validator.validate_ts(ts_data.get("imaginary_freqs", []))
        report.append(f"\nTS Validation: {ts_msg}")

        if ea_sep is not None:
            report.append("\nActivation Energy (from separated reactants):")
            report.append(f"Ea (Ha) = {ea_sep['hartree']:.6f}")
            report.append(f"Ea (kJ/mol) = {ea_sep['kj_mol']:.6f}")

        if ea_complex is not None:
            report.append("\nActivation Energy (from pre-reactive complex):")
            report.append(f"Ea (Ha) = {ea_complex['hartree']:.6f}")
            report.append(f"Ea (kJ/mol) = {ea_complex['kj_mol']:.6f}")

        if ea_sep and ea_complex:
            val_valid, val_msg_sep = self.validator.check_negative_ea(ea_sep['hartree'])
            if not val_valid:
                report.append(f"\n{val_msg_sep}")

        report.append("-" * 60)
        return "\n".join(report)
