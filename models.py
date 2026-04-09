class Patient:
    def __init__(self, name, age, disease):
        self.name = name
        self.age = age
        self.disease = disease

    def get_info(self):
        return f"{self.name} ({self.age}) - {self.disease}"