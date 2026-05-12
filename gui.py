import tkinter as tk
from tkinter import messagebox, ttk
from mechanism_engine import MechanismEngine
from quantum_engine import QuantumEngine
from energy import get_corrected_energy, calc_activation_energy
from conversions import convert_ea

class KineticsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Reaction Kinetics Generator (ORCA/Psi4)")
        
        self.mech_engine = MechanismEngine()
        self.quantum_engine = QuantumEngine()
        
        self.mechanisms = []
        self.r1_data = {}
        self.r2_data = {}
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # User Inputs
        ttk.Label(frame, text="Reactant 1 (Formula/SMILES):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.r1_var = tk.StringVar(value="C6H10O5")
        ttk.Entry(frame, textvariable=self.r1_var, width=30).grid(row=0, column=1)
        
        ttk.Label(frame, text="Reactant 2 (Formula/SMILES):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.r2_var = tk.StringVar(value="O3")
        ttk.Entry(frame, textvariable=self.r2_var, width=30).grid(row=1, column=1)
        
        # Generate Mechanisms Button
        ttk.Button(frame, text="Generate Mechanisms", command=self.generate_mechanisms).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Mechanisms List
        ttk.Label(frame, text="Select Mechanism:").grid(row=3, column=0, sticky=tk.W)
        self.mech_var = tk.StringVar()
        self.mech_dropdown = ttk.Combobox(frame, textvariable=self.mech_var, width=40, state="readonly")
        self.mech_dropdown.grid(row=3, column=1, sticky=tk.W)
        
        # Compute Button
        ttk.Button(frame, text="Compute Transition State & Kinetics", command=self.compute_kinetics).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Output text area
        self.text_area = tk.Text(frame, height=25, width=70, font=("Courier", 10))
        self.text_area.grid(row=5, column=0, columnspan=2)
        
    def append_output(self, text):
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        
    def generate_mechanisms(self):
        self.text_area.delete('1.0', tk.END)
        r1 = self.r1_var.get().strip()
        r2 = self.r2_var.get().strip()
        
        if not r1 or not r2:
            messagebox.showerror("Error", "Provide both reactants.")
            return
            
        self.append_output("Parsing molecules and generating mechanisms using RDKit/ASE...")
        
        self.mechanisms = self.mech_engine.generate_mechanisms(r1, r2)
        
        # Compute Reactant energies first
        self.append_output(f"Optimizing {r1}...")
        self.r1_data = self.quantum_engine.optimize_and_freq("R1", is_ts=False)
        self.append_output(f"Optimizing {r2}...")
        self.r2_data = self.quantum_engine.optimize_and_freq("R2", is_ts=False)
        
        self.append_output("\nPossible Mechanisms Found:")
        mech_names = []
        for i, mech in enumerate(self.mechanisms):
            self.append_output(f"{i+1}. {mech['name']} - {mech['description']}")
            mech_names.append(mech['name'])
            
        self.mech_dropdown['values'] = mech_names
        if mech_names:
            self.mech_dropdown.current(0)
            
    def compute_kinetics(self):
        selected_name = self.mech_var.get()
        if not selected_name:
            messagebox.showerror("Error", "Select a mechanism first.")
            return
            
        mech = next((m for m in self.mechanisms if m['name'] == selected_name), None)
        
        self.append_output(f"\n--- Processing Mechanism: {mech['name']} ---")
        self.append_output("Generating TS guess using NEB/QST2...")
        self.append_output("Submitting DFT optimization to ORCA/Psi4...")
        
        ts_data = self.quantum_engine.optimize_and_freq(mech['ts_guess_geometry'], is_ts=True)
        
        # Validating TS
        is_valid, msg = self.quantum_engine.validate_ts(ts_data['frequencies'])
        self.append_output(f"TS Validation: {msg}")
        if not is_valid:
            self.append_output("ABORTING: Structure is not a valid Transition State.")
            return
            
        r1_corr, r1_zpe = get_corrected_energy(self.r1_data['electronic_energy'], self.r1_data['frequencies'], is_ts=False)
        r2_corr, r2_zpe = get_corrected_energy(self.r2_data['electronic_energy'], self.r2_data['frequencies'], is_ts=False)
        ts_corr, ts_zpe = get_corrected_energy(ts_data['electronic_energy'], ts_data['frequencies'], is_ts=True)
        
        ea_ha = calc_activation_energy(r1_corr, r2_corr, ts_corr)
        ea_conv = convert_ea(ea_ha)
        
        report = f'''
------------------------------------------------
Reactant 1 ({self.r1_var.get()})
Electronic Energy: {self.r1_data['electronic_energy']:.6f} Ha
ZPE: {r1_zpe:.6f} Ha
Corrected Energy (A): {r1_corr:.6f} Ha

Reactant 2 ({self.r2_var.get()})
Electronic Energy: {self.r2_data['electronic_energy']:.6f} Ha
ZPE: {r2_zpe:.6f} Ha
Corrected Energy (B): {r2_corr:.6f} Ha

Transition State [{mech['name']}]
Optimized Geometry: {ts_data['optimized_geometry']}
Electronic Energy: {ts_data['electronic_energy']:.6f} Ha
ZPE: {ts_zpe:.6f} Ha
Imaginary Frequencies: {[f for f in ts_data['frequencies'] if f < 0]}
Corrected Energy (C): {ts_corr:.6f} Ha

Activation Energy
Ea (Hartree): {ea_conv['hartree']:.6f}
Ea (kcal/mol): {ea_conv['kcal_mol']:.6f}
Ea (kJ/mol): {ea_conv['kj_mol']:.6f}
Ea (eV): {ea_conv['ev']:.6f}
------------------------------------------------'''
        self.append_output(report)
