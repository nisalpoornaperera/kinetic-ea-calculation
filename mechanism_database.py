import yaml

class MechanismDatabase:
    def __init__(self, filepath='mechanisms.yaml'):
        self.filepath = filepath
        self.mechanisms = self.load_database()

    def load_database(self):
        try:
            with open(self.filepath, 'r') as file:
                return yaml.safe_load(file).get('mechanisms', [])
        except FileNotFoundError:
            return []

    def get_all(self):
        return self.mechanisms
