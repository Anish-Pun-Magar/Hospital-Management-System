from datetime import datetime

class Patient:
    def __init__(self, name, age, gender, disease, condition):
        self.name = name.lower().strip()
        self.age = age
        self.gender = gender
        self.disease = disease
        self.condition = condition

    def __str__(self):
        return (
            f"Name: {self.name.title()}\n"
            f"Age: {self.age}\n"
            f"Gender: {self.gender}\n"
            f"Disease: {self.disease}\n"
            f"Condition: {self.condition}"
        )

class Doctor:
    def __init__(self, name, specialization, availability):
        self.name = name.lower().strip()
        self.specialization = specialization
        self.availability = availability  # Just a display string, not used for logic

    def __str__(self):
        return (
            f"Name: {self.name.title()}\n"
            f"Specialization: {self.specialization}\n"
            f"Availability: {self.availability}"
        )

class Hospital:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []  # Each item: (doctor_name, patient_name, time_slot)

    def admit_patient(self, name, age, gender, disease, condition):
        name_key = name.lower().strip()
        if any(p.name == name_key for p in self.patients):
            return f"{name_key} already exists."
        patient = Patient(name, age, gender, disease, condition)
        self.patients.append(patient)
        with open("Admitted_Log.txt", 'a') as f:
            time_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            f.write(f"{name_key} was admitted on {time_now}\n")
        return f"'{name_key}' has been admitted"

    def discharge_patient(self, name):
        name_key = name.lower().strip()
        for patient in self.patients:
            if patient.name == name_key:
                self.patients.remove(patient)
                with open("Discharge_Log.txt", 'a') as f:
                    time_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    f.write(f"{name_key} was discharged on {time_now}\n")
                return f"'{name_key}' has been discharged"
        return f"No patient named '{name_key}' found."

    def view_patients(self):
        if not self.patients:
            return "No patients available."
        return "\n\n".join(f"{idx}. {p}" for idx, p in enumerate(self.patients, start=1))

    def search_patient(self, search_term):
        search_term = search_term.lower().strip()
        matches = list(filter(lambda p: search_term in p.name, self.patients))
        if matches:
            return "\n\n".join(str(p) for p in matches)
        return "No match found."

    def add_doctor(self, name, specialization, availability):
        doc = Doctor(name, specialization, availability)
        self.doctors.append(doc)
        return f"{name.title()} added to doctor list."

    def available_doctors(self, time_slot=None):
        if time_slot:
            booked_doctors = {doc for doc, _, slot in self.appointments if slot == time_slot}
            return [doc for doc in self.doctors if doc.name not in booked_doctors]
        return self.doctors

    def appoint_doctor(self, patient_name, time_slot):
        patient_name_key = patient_name.lower().strip()
        patient = next((p for p in self.patients if p.name == patient_name_key), None)
        if not patient:
            return f"No patient named '{patient_name_key}' found."

        available_docs = self.available_doctors(time_slot)
        if not available_docs:
            return f"No doctors available at {time_slot}."

        print(f"Available Doctors at {time_slot}:")
        for idx, doc in enumerate(available_docs, start=1):
            print(f"{idx}. {doc.name.title()} ({doc.specialization})")

        try:
            choice = int(input("Choose doctor number: ")) - 1
            if choice < 0 or choice >= len(available_docs):
                return "Invalid choice."
        except ValueError:
            return "Invalid input."

        chosen_doc = available_docs[choice]
        self.appointments.append((chosen_doc.name, patient.name, time_slot))
        return f"✅ Appointment booked: Dr. {chosen_doc.name.title()} with {patient.name.title()} at {time_slot}."

    def view_appointments(self):
        if not self.appointments:
            return "No appointments scheduled."
        return "\n".join(
            f"🗓️ Dr. {doc.title()} is booked with {pat.title()} at {slot}"
            for doc, pat, slot in self.appointments
        )

    def view_available_doctor(self):
        if not self.doctors:
            return "No doctors available."
        return "\n".join(f"{idx}. {d}" for idx, d in enumerate(self.doctors, start=1))

def main():
    hospital = Hospital()

    patients = [
        {"name": "ronaldo", "age": 1, "gender": "male", "disease": "Fever", "condition": "good"},
        {"name": "messi", "age": 2, "gender": "male", "disease": "Cough", "condition": "bad"},
        {"name": "neymar", "age": 3, "gender": "male", "disease": "Fracture", "condition": "good"},
        {"name": "mbappe", "age": 4, "gender": "male", "disease": "Flu", "condition": "bad"}
    ]
    for p in patients:
        hospital.admit_patient(p['name'], p['age'], p['gender'], p['disease'], p['condition'])

    doctors = [
        {"name": "Dr. House", "specialization": "Diagnostics", "availability": "9am-5pm"},
        {"name": "Dr. Strange", "specialization": "Surgery", "availability": "10am-6pm"},
        {"name": "Dr. Grey", "specialization": "General", "availability": "8am-4pm"}
    ]
    for d in doctors:
        hospital.add_doctor(d['name'], d['specialization'], d['availability'])

    while True:
        print("\n== Hospital Menu ==")
        print("1. Admit Patient")
        print("2. Discharge Patient")
        print("3. View Patients")
        print("4. Search Patient")
        print("5. View Doctors")
        print("6. Book Appointment")
        print("7. View Appointments")
        print("8. Add Doctor")        
        print("0. Exit")


        choice = input("Enter choice: ").strip()
        if choice == '1':
            name = input("Name: ")
            age = int(input("Age: "))
            gender = input("Gender (M/F): ").strip().upper()
            if gender not in ['M', 'F']:
                print("Invalid gender. Please enter M or F.")
                continue
            disease = input("Disease: ")
            condition = input("Condition (Good/Bad): ")
            print(hospital.admit_patient(name, age, gender, disease, condition))

        elif choice == '2':
            name = input("Enter patient name to discharge: ")
            print(hospital.discharge_patient(name))

        elif choice == '3':
            print(hospital.view_patients())

        elif choice == '4':
            name = input("Search patient name: ")
            print(hospital.search_patient(name))

        elif choice == '5':
            print(hospital.view_available_doctor())

        elif choice == '6':
            patient_name = input("Enter patient name for appointment: ")
            time_slot = input("Enter time slot (e.g., 2pm-3pm): ")
            print(hospital.appoint_doctor(patient_name, time_slot))

        elif choice == '7':
            print(hospital.view_appointments())

        elif choice == '8':
            name = input("Doctor Name: ")
            specialization = input("Specialization: ")
            availability = input("Availability (e.g., 9am-5pm): ")
            print(hospital.add_doctor(name, specialization, availability))

        elif choice == '0':
            print("👋 Exiting system. Stay healthy!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
