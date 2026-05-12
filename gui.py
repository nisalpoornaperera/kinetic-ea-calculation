import tkinter as tk
from tkinter import ttk, messagebox
from molecule_parser import MoleculeParser
from mechanism_selector import MechanismSelector
from reactive_site_identifier import ReactiveSiteIdentifier
from geometry_builder import GeometryBuilder
from ts_guess_builder import TSGuessBuilder
from orca_runner import OrcaRunner
from energy import get_corrected_energy, calc_activation_energy
from conversions import convert_ea
from report_generator import ReportGenerator

class MechanismGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Reaction Mechanism & TS Generator")
        
        # Modules
        self.parser = MoleculeParser()
        self.selector = MechanismSelector()
        self.site_identifier = ReactiveSiteIdentifier()
        self.geo_builder = GeometryBuilder()
        self.ts_builder = TSGuessBuilder()
        self.runner = OrcaRunner()
        self.reporter = ReportGenerator()
        
        self.available_mechanisms = []
        
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Reactant 1 (Formula/SMILES):").grid(row=0, column=0, sticky=tk.W)
        self.r1_var = tk.StringVar(value="C6H10O5")
        ttk.Entry(frame, textvariable=self.r1_var, width=30).grid(row=0, column=1)

        ttk.Label(frame, text="Reactant 2 (Formula/SMILES):").grid(row=1, column=0, sticky=tk.W)
        self.r2_var = tk.StringVar(value="O")
        ttk.Entry(frame, textvariable=self.r2_var, width=30).grid(row=1, column=1)
        
        ttk.Button(frame, text="Identify Mechanisms", command=self.find_mechanisms).grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Label(frame, text="Select Mechanism:").grid(row=3, column=0, sticky=tk.W)
        self.mech_var = tk.StringVar()
        self.mech_dropdown = ttk.Combobox(frame, textvariable=self.mech_var, width=40, state="readonly")
        self.mech_dropdown.grid(row=3, column=1)
        self.mech_dropdown.bind('<<ComboboxSelected>>', self.update_sites)

        ttk.Label(frame, text="Select Attacked Site:").grid(row=4, column=0, sticky=tk.W)
        self.site_var = tk.StringVar()
        self.site_dropdown = ttk.Combobox(frame, textvariable=self.site_var, width=40, state="readonly")
        self.site_dropdown.grid(row=4, column=1)
        
        ttk.Button(frame, text="Compute Activation Energy", command=self.compute).grid(row=5, column=0, columnspan=2, pady=10)
        
        self.text_area = tk.Text(frame, height=20, width=70)
        self.text_area.grid(row=6, column=0, columnspan=2)

    def write_output(self, text):
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)

    def find_mechanisms(self):
        r1 = self.r1_var.get().strip()
        r2 = self.r2_var.get().strip()
        
        self.parser.parse(r1) # Will print warning if purely formula
        self.write_output(f"Loaded Reactants: {r1} + {r2}")
        
        self.available_mechanisms = self.selector.find_matches(r1, r2)
        mech_names = [m["name"] for m in self.available_mechanisms]
        self.mech_dropdown['values'] = mech_names
        
        if mech_names:
            self.mech_dropdown.current(0)
            self.update_sites(None)

    def update_sites(self, event):
        selected_name = self.mech_var.get()
        mech = next((m for m in self.available_mechanisms if m["name"] == selected_name), None)
        if mech:
            sites = self.site_identifier.identify_sites(mech, None, None)
            self.site_dropdown['values'] = sites
            if sites:
                self.site_dropdown.current(0)

    def compute(self):
        selected_name = self.mech_var.get()
        selected_site = self.site_var.get()
        mech = next((m for m in self.available_mechanisms if m["name"] == selected_name), None)
        
        if not mech:
            messagebox.showerror("Error", "Select a valid mechanism.")
            return

        self.text_area.delete('1.0', tk.END)
        self.write_output("Generating geometries and TS guesses...")

        # 1. Build Geometries
        r_complex_geo = self.geo_builder.build_reactant_complex("R1", "R2", selected_site)
        ts_guess_geo = self.ts_builder.build_guess(r_complex_geo, mech, selected_site)
        
        # 2. Run ORCA
        self.write_output("Running DFT Optimizations in ORCA...")
        r_sep_data = self.runner.run_optimization("Separated_Reactants", is_ts=False)
        r_complex_data = self.runner.run_optimization(r_complex_geo, is_ts=False)
        ts_data = self.runner.run_optimization(ts_guess_geo, is_ts=True)
        
        # 3. Energy Calculations
        r_sep_corr, _ = get_corrected_energy(r_sep_data['electronic_energy'], r_sep_data['frequencies'], False)
        r_complex_corr, _ = get_corrected_energy(r_complex_data['electronic_energy'], r_complex_data['frequencies'], False)
        ts_corr, _ = get_corrected_energy(ts_data['electronic_energy'], ts_data['frequencies'], True)

        ea_sep = convert_ea(calc_activation_energy(r_sep_corr, 0, ts_corr)) # Assuming A+B simplified into sep logic
        ea_complex = convert_ea(calc_activation_energy(r_complex_corr, 0, ts_corr))

        # 4. Generate Report
        report = self.reporter.generate(mech["name"], r_complex_data, r_sep_data, ts_data, ea_sep, ea_complex)
        self.write_output(report)

if __name__ == "__main__":
    root = tk.Tk()
    app = MechanismGUI(root)
    root.mainloop()
