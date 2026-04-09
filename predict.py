def predict_disease(symptoms):
    if "fever" in symptoms and "cough" in symptoms:
        return "Flu"
    elif "headache" in symptoms:
        return "Migraine"
    elif "itching" in symptoms:
        return "Allergy"
    else:
        return "General Checkup"

def assign_doctor(disease):
    doctors = {
        "Flu": "Dr. Sharma (General)",
        "Migraine": "Dr. Mehta (Neuro)",
        "Allergy": "Dr. Khan (Skin)",
        "General Checkup": "Dr. Verma"
    }
    return doctors.get(disease, "Dr. Default")