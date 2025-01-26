import json
import readline
import pyodbc
from datetime import datetime
from modules.finance import Finance
from modules.user import Admin, Doctor, Patient, Receptionist, Nurse
from modules.hospital import Hospital
from modules.appointment import Appointment
from modules.pharmacy import Pharmacy
from modules.user import load_nationalities, complete
import modules.database as Database


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def signup(self, username, password, role, phone_number, age, gender, salary, profession, department, chronic_disease, nationality):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Users (Username, Password, Role, PhoneNumber, Age, Gender, Salary, Profession, Department, ChronicDisease, Nationality)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, username, password, role, phone_number, age, gender, salary, profession, department, chronic_disease, nationality)
        conn.commit()
        conn.close()

    def login(self, username, password):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", username, password)
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def add_user(self, username, password, role, phone_number, age, gender, salary, profession, department):
        self.signup(username, password, role, phone_number, age, gender, salary, profession, department, None, None)

    def remove_user(self, username):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE Username = ?", username)
        conn.commit()
        conn.close()

    def view_financial_insights(self):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM FinancialTransactions")
        transactions = cursor.fetchall()
        for transaction in transactions:
            print(transaction)
        conn.close()

    def update_pharmacy_inventory(self, medication, stock):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("UPDATE PharmacyInventory SET Stock = ? WHERE MedicationName = ?", stock, medication)
        conn.commit()
        conn.close()

    def view_pharmacy_inventory(self):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PharmacyInventory")
        inventory = cursor.fetchall()
        for item in inventory:
            print(item)
        conn.close()

    def add_department(self, hospital, department_name, description):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Departments (DepartmentName, Description) VALUES (?, ?)", department_name, description)
        conn.commit()
        conn.close()

    def remove_department(self, hospital, department_name):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Departments WHERE DepartmentName = ?", department_name)
        conn.commit()
        conn.close()

    def add_room(self, hospital, room_number, room_type):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Rooms (RoomNumber, RoomType) VALUES (?, ?)", room_number, room_type)
        conn.commit()
        conn.close()

    def view_all_users(self):
        conn = Database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        for user in users:
            print(user)
        conn.close()


def main():
    hospital = Hospital('Al-Shifa Hospital')
    hospital.add_room(101, 'Single')
    hospital.add_room(102, 'Double')

    admin = Admin('admin', 'admin123')
    username = interactive_input(admin)

    users = admin.load_users()
    role = users[username]['role'].lower()

    match role:
        case 'admin':
            print(f"Welcome, Admin {username}!")
            admin_menu(admin, hospital)
        case 'doctor':
            doctor = Doctor(username, users[username]['password'])
            print(f"Welcome, Dr. {username}!")
            while True:
                print("\n1. View Appointments\n2. Write Prescription\n3. View Patient Records\n4. Add Patient Record\n5. Exit")
                choice = input("Enter your choice: ")
                match choice:
                    case '1':
                        doctor.view_appointments()
                    case '2':
                        patient = input("Enter patient username: ")
                        prescription = input("Enter prescription: ")
                        doctor.write_prescriptions(patient, prescription)
                    case '3':
                        patient = input("Enter patient username: ")
                        doctor.view_patient_records(patient)
                    case '4':
                        patient = input("Enter patient username: ")
                        record = input("Enter record details: ")
                        doctor.add_patient_record(patient, record)
                    case '5':
                        print("Thank you for using our HMS. Have a nice day!")
                        break
                    case _:
                        print("Invalid choice. Please try again.")
        case 'patient':
            patient = Patient(username, users[username]['password'])
            print(f"Welcome, {username}!")
            while True:
                print("\n1. View Appointments\n2. Request Appointment\n3. Exit")
                choice = input("Enter your choice: ")
                match choice:
                    case '1':
                        patient.view_appointments()
                    case '2':
                        doctor = input("Enter doctor username: ")
                        date = input("Enter date (YYYY-MM-DD): ")
                        time = input("Enter time (HH:MM): ")
                        room = int(input("Enter room number: "))
                        print("Available departments:")
                        hospital.view_departments()
                        department = input("Enter department: ")
                        patient.request_appointments(doctor, date, time, room, department)
                    case '3':
                        print("Thank you for using our HMS. Have a nice day!")
                        break
                    case _:
                        print("Invalid choice. Please try again.")
        case 'receptionist':
            receptionist = Receptionist(username, users[username]['password'])
            print(f"Welcome, {username}!")
            while True:
                print("\n1. Book Appointment\n2. Cancel Appointment\n3. Allocate Room\n4. Release Room\n5. View Rooms\n6. Exit")
                choice = input("Enter your choice: ")
                match choice:
                    case '1':
                        doctor = input("Enter doctor username: ")
                        patient = input("Enter patient username: ")
                        date = input("Enter date (YYYY-MM-DD): ")
                        time = input("Enter time (HH:MM): ")
                        room = int(input("Enter room number: "))
                        print("Available departments:")
                        hospital.view_departments()
                        department = input("Enter department: ")
                        receptionist.book_appointments(doctor, patient, date, time, room, department)
                    case '2':
                        appointment_id = int(input("Enter appointment ID to cancel: "))
                        receptionist.cancel_appointments(appointment_id)
                    case '3':
                        room_type = input("Enter room type: ")
                        receptionist.allocate_room(hospital, room_type)
                    case '4':
                        room_number = int(input("Enter room number to release: "))
                        receptionist.release_room(hospital, room_number)
                    case '5':
                        receptionist.view_rooms(hospital)
                    case '6':
                        print("Thank you for using our HMS. Have a nice day!")
                        break
                    case _:
                        print("Invalid choice. Please try again.")
        case 'nurse':
            nurse = Nurse(username, users[username]['password'])
            print(f"Welcome, Nurse {username}!")
            while True:
                print("\n1. View Patient Records\n2. View Prescriptions\n3. Exit")
                choice = input("Enter your choice: ")
                match choice:
                    case '1':
                        nurse.view_patient_records()
                    case '2':
                        nurse.view_prescriptions()
                    case '3':
                        print("Thank you for using our HMS. Have a nice day!")
                        break
                    case _:
                        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()