from datetime import datetime

class Patient:
    def __init__(self, id, name, age, gender, disease):
        self.id = id
        self.name = name.lower().strip()
        self.age = age
        self.gender = gender.upper()
        self.disease = disease

    def __str__(self):
        return (
            f"Patient ID: {self.id}\n"
            f"Name: {self.name.title()}\n"
            f"Age: {self.age}\n"
            f"Gender: {self.gender}\n"
            f"Disease: {self.disease}\n"
        )

class Doctor:
    def __init__(self, id, name, specialization, availability):
        self.id = id
        self.name = name.lower().strip()
        self.specialization = specialization
        self.availability = availability

    def __str__(self):
        avail = self.availability if self.availability else "Not available"
        return (
            f"Doctor ID: {self.id}\n"
            f"Name: {self.name.title()}\n"
            f"Specialization: {self.specialization}\n"
            f"Availability: {avail}\n"
        )

class Appointment:
    def __init__(self, doctor_name, patient_name, time_slot):
        self.doctor_name = doctor_name
        self.patient_name = patient_name
        self.time_slot = time_slot

    def __str__(self):
        return f"Dr. {self.doctor_name.title()} is booked with {self.patient_name.title()} at {self.time_slot}"

class Hospital:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []

    def admit_patient(self, patient_id, name, age, gender, disease):
        if any(p.id == patient_id for p in self.patients):
            return f"Patient with ID {patient_id} already exists."
        new_patient = Patient(patient_id, name, age, gender, disease)
        self.patients.append(new_patient)
        # Log admission
        with open("Admitted_Log.txt", "a") as f:
            time_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            f.write(f"{name.title()} (ID: {patient_id}) admitted on {time_now}\n")
        return f"Patient '{name.title()}' admitted successfully with ID {patient_id}."

    def discharge_patient(self, patient_id):
        for patient in self.patients:
            if patient.id == patient_id:
                self.patients.remove(patient)
                with open("Discharge_Log.txt", "a") as f:
                    time_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    f.write(f"{patient.name.title()} (ID: {patient_id}) discharged on {time_now}\n")
                return f"Patient with ID {patient_id} discharged successfully."
        return f"No patient found with ID {patient_id}."

    def view_patients(self):
        if not self.patients:
            return "No patients available currently."
        return "\n".join(f"{idx}. {p}" for idx, p in enumerate(self.patients, start=1))

    def search_patient(self, search_term):
        search_term = search_term.lower().strip()
        matches = list(filter(lambda p: search_term in p.name or str(p.id) == search_term, self.patients))
        if matches:
            return "\n".join(str(p) for p in matches)
        return "No patient match found."

    def add_doctor(self, doc_id, name, specialization, availability):
        if any(d.id == doc_id for d in self.doctors):
            return f"Doctor with ID {doc_id} already exists."
        doctor = Doctor(doc_id, name, specialization, availability)
        self.doctors.append(doctor)
        return f"Dr. {name.title()} added successfully with ID {doc_id}."

    def available_doctors(self, time_slot=None):
        if time_slot:
            booked_doctors = {doc for doc, _, slot in self.appointments if slot == time_slot}
            return [d for d in self.doctors if d.name not in booked_doctors]
        return self.doctors

    def appoint_doctor(self, patient_id, time_slot):
        patient = next((p for p in self.patients if p.id == patient_id), None)
        if not patient:
            return f"No patient found with ID {patient_id}."

        available_docs = self.available_doctors(time_slot)
        if not available_docs:
            return f"No doctors available at {time_slot}."

        print(f"\nAvailable Doctors at {time_slot}:")
        for idx, doc in enumerate(available_docs, start=1):
            print(f"{idx}. Dr. {doc.name.title()} ({doc.specialization})")

        try:
            choice = int(input("Choose doctor number: ")) - 1
            if choice < 0 or choice >= len(available_docs):
                return "Invalid choice."
        except ValueError:
            return "Invalid input."

        chosen_doc = available_docs[choice]
        appointment = Appointment(chosen_doc.name, patient.name, time_slot)
        self.appointments.append(appointment)
        return f"✅ Appointment booked: Dr. {chosen_doc.name.title()} with {patient.name.title()} at {time_slot}."

    def view_appointments(self):
        if not self.appointments:
            return "No appointments scheduled."
        return "\n".join(str(a) for a in self.appointments)

    def view_doctors(self):
        if not self.doctors:
            return "No doctors available."
        return "\n".join(f"{idx}. {d}" for idx, d in enumerate(self.doctors, start=1))


def main():
    hospital = Hospital()

    # Preload patients
    patients = [
        {"patient_id": 1, "name": "luffy", "age": 1, "gender": "M", "disease": "Fever"},
        {"patient_id": 2, "name": "Zoro", "age": 2, "gender": "M", "disease": "Cough"},
        {"patient_id": 3, "name": "Jimbe", "age": 3, "gender": "M", "disease": "Fracture"},
        {"patient_id": 4, "name": "Brook", "age": 4, "gender": "M", "disease": "Flu"},
    ]
    for p in patients:
        hospital.admit_patient(p['patient_id'], p['name'], p['age'], p['gender'], p['disease'])

    # Preload doctors
    doctors = [
        {"doc_id": 1, "name": "Dr. Chopper", "specialization": "Diagnostics", "availability": "9am-5pm"},
        {"doc_id": 2, "name": "Dr. Strange", "specialization": "Surgery", "availability": "10am-6pm"},
        {"doc_id": 3, "name": "Dr. Grey", "specialization": "General", "availability": "8am-4pm"},
    ]
    for d in doctors:
        hospital.add_doctor(d['doc_id'], d['name'], d['specialization'], d['availability'])

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

        match choice:
            case '1':
                try:
                    patient_id = int(input("Enter Patient ID (number): "))
                    name = input("Name: ")
                    age = int(input("Age: "))
                    gender = input("Gender (M/F): ").strip().upper()
                    if gender not in ['M', 'F']:
                        print("Invalid gender. Please enter M or F.")
                    else:
                        disease = input("Disease: ")
                        print(hospital.admit_patient(patient_id, name, age, gender, disease))
                except ValueError:
                    print("Invalid input. Please enter correct data.")

            case '2':
                try:
                    patient_id = int(input("Enter Patient ID to discharge: "))
                    print(hospital.discharge_patient(patient_id))
                except ValueError:
                    print("Invalid ID. Must be a number.")

            case '3':
                print(hospital.view_patients())

            case '4':
                term = input("Search patient by name or ID: ")
                print(hospital.search_patient(term))

            case '5':
                print(hospital.view_doctors())

            case '6':
                try:
                    patient_id = int(input("Enter Patient ID for appointment: "))
                    time_slot = input("Enter time slot (e.g., 2pm-3pm): ").strip()
                    print(hospital.appoint_doctor(patient_id, time_slot))
                except ValueError:
                    print("Invalid input for patient ID.")

            case '7':
                print(hospital.view_appointments())

            case '8':
                try:
                    doc_id = int(input("Doctor ID: "))
                    name = input("Doctor Name: ")
                    specialization = input("Specialization: ")
                    availability = input("Availability (e.g., 9am-5pm): ")
                    print(hospital.add_doctor(doc_id, name, specialization, availability))
                except ValueError:
                    print("Invalid input for Doctor ID.")

            case '0':
                print("👋 Exiting system. Stay healthy!")
                exit()

            case _:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
