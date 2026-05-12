class MoleculeParser:
    def parse(self, input_string):
        """
        Mocks RDKit/ASE parsing.
        """
        is_smiles = "=" in input_string or "c1" in input_string.lower()
        if not is_smiles and "C6H10O5" in input_string:
            print(f"Warning: {input_string} is only a molecular formula. A default cellulose model geometry is being used.")
        
        return {
            "input": input_string,
            "type": "SMILES" if is_smiles else "Formula",
            "geometry": "3D_coordinates_mock"
        }
