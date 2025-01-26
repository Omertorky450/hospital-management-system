     
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc
import json
import os
import readline
import plotly.express as px
from modules.appointment import Appointment
from modules.finance import Finance
from modules.pharmacy import Pharmacy
from modules.hospital import Hospital
import modules.database as Database
import csv

# Load nationalities for autocompletion
def load_nationalities():
    with open('data/nationalities-common.json', 'r') as file:
        data = json.load(file)
    return data['Nationalities']

# Autocompletion setup
def complete(text, state):
    options = [i for i in nationalities if i.lower().startswith(text.lower())]
    if state < len(options):
        return options[state]
    else:
        return None

nationalities = load_nationalities()
readline.set_completer(complete)
readline.parse_and_bind('tab: complete')

#  User class
class User:
    def __init__(self, username, password, role, phone_number=None, age=None, gender=None, specialization=None, shift=None, overtime_hours=0, certifications=None, training_programs=None):
        self.username = username
        self.password = password
        self.role = role
        self.phone_number = phone_number
        self.age = age
        self.gender = gender
        self.specialization = specialization
        self.shift = shift
        self.overtime_hours = overtime_hours
        self.certifications = certifications if certifications else []
        self.training_programs = training_programs if training_programs else []

    @staticmethod
    def load_users():
        """
        Load all users from the SQL Server database.
        """
        connection = Database()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users")
            rows = cursor.fetchall()
            users = {}
            for row in rows:
                users[row.Username] = {
                    'password': row.Password,
                    'role': row.Role,
                    'phone_number': row.PhoneNumber,
                    'age': row.Age,
                    'gender': row.Gender,
                    'salary': row.Salary,
                    'profession': row.Profession,
                    'department': row.Department,
                    'chronic_disease': row.ChronicDisease,
                    'nationality': row.Nationality
                }
            connection.close()
            return users
        return {}

    @staticmethod
    def save_users(users):
        """
        Save users to the SQL Server database.
        """
        connection = Database()
        if connection:
            cursor = connection.cursor()
            for username, details in users.items():
                cursor.execute("""
                    MERGE INTO Users AS target
                    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (Username, Password, Role, PhoneNumber, Age, Gender, Salary, Profession, Department, ChronicDisease, Nationality)
                    ON target.Username = source.Username
                    WHEN MATCHED THEN
                        UPDATE SET Password = source.Password, Role = source.Role, PhoneNumber = source.PhoneNumber, Age = source.Age, Gender = source.Gender,
                        Salary = source.Salary, Profession = source.Profession, Department = source.Department, ChronicDisease = source.ChronicDisease, Nationality = source.Nationality
                    WHEN NOT MATCHED THEN
                        INSERT (Username, Password, Role, PhoneNumber, Age, Gender, Salary, Profession, Department, ChronicDisease, Nationality)
                        VALUES (source.Username, source.Password, source.Role, source.PhoneNumber, source.Age, source.Gender, source.Salary, source.Profession, source.Department, source.ChronicDisease, source.Nationality);
                """, (username, details['password'], details['role'], details['phone_number'], details['age'], details['gender'],
                      details.get('salary'), details.get('profession'), details.get('department'), details.get('chronic_disease'), details.get('nationality')))
            connection.commit()
            connection.close()

    def login(self, username, password):
        """
        Authenticate a user by checking their username and password in the database.
        """
        connection = Database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
                row = cursor.fetchone()
                if row:
                    print(f"Login successful. Welcome {username}!")
                    return True
                else:
                    print("Login failed. Invalid username or password.")
                    return False
            except Exception as e:
                print(f"Error during login: {e}")
                return False
            finally:
                connection.close()
        return False

    def signup(self, username, password, role, phone_number=None, age=None, gender=None, salary=None, profession=None, department=None, chronic_disease=None, nationality=None):
        """
        Register a new user in the database.
        """
        connection = Database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
                if cursor.fetchone():
                    print("Username already exists.")
                    return False

                if phone_number:
                    phone_number = ''.join(filter(str.isdigit, phone_number))
                    if len(phone_number) != 11:
                        print("Phone number must be 11 digits long.")
                        return False

                cursor.execute("""
                    INSERT INTO Users (Username, Password, Role, PhoneNumber, Age, Gender, Salary, Profession, Department, ChronicDisease, Nationality)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password, role, phone_number, age, gender, salary, profession, department, chronic_disease, nationality))
                connection.commit()
                print("Signup successful.")
                return True
            except Exception as e:
                print(f"Error during signup: {e}")
                return False
            finally:
                connection.close()
        return False

    def update_certifications(self, certification):
        self.certifications.append(certification)

    def add_training_program(self, program):
        self.training_programs.append(program)
  
  
  
# Admin class
class Admin(User):
    def connect_to_db(self):
        try:
            conn = Database()
            print("Connected to the database successfully!")
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def fetch_data(self, query, conn):
        try:
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def perform_analysis(self, choice):
        analysis_functions = {
            1: {
                "name": "Patient Analysis",
                "query": """
                    SELECT Age, Gender, GeographicLocation, ChronicDisease, Readmission 
                    FROM Patient
                    LEFT JOIN Treatment ON Patient.PatientID = Treatment.PatientID
                """,
                "process": lambda df: (
                    print("\nPatient Demographics:"),
                    print(df[["Age", "Gender", "GeographicLocation", "ChronicDisease"]].describe()),
                    print("\nReadmission Rates:"),
                    print(df["Readmission"].value_counts(normalize=True) * 100),
                    sns.countplot(x="Gender", hue="Readmission", data=df),
                    plt.title("Readmission Rates by Gender"),
                    plt.show()
                )
            },
            2: {
                "name": "Department Analysis",
                "query": """
                    SELECT DepartmentName, COUNT(AppointmentID) AS PatientCount 
                    FROM Appointments
                    JOIN Departments ON Appointments.Department = Departments.DepartmentName
                    GROUP BY DepartmentName
                """,
                "process": lambda df: (
                    print("\nDepartment Workload:"),
                    print(df),
                    sns.barplot(x="DepartmentName", y="PatientCount", data=df),
                    plt.title("Patient Distribution by Department"),
                    plt.show()
                )
            },
            3: {
                "name": "Staff Analysis",
                "query": """
                    SELECT Role, COUNT(StaffID) AS StaffCount 
                    FROM Staff
                    GROUP BY Role
                """,
                "process": lambda df: (
                    print("\nStaff Workload:"),
                    print(df),
                    sns.barplot(x="Role", y="StaffCount", data=df),
                    plt.title("Staff Distribution by Role"),
                    plt.show()
                )
            },
            4: {
                "name": "Pharmacy Analysis",
                "query": """
                    SELECT MedicationName, SUM(PrescriptionCount) AS TotalPrescriptions 
                    FROM PrescriptionTrends
                    JOIN PharmacyInventory ON PrescriptionTrends.MedicationID = PharmacyInventory.MedicationID
                    GROUP BY MedicationName
                """,
                "process": lambda df: (
                    print("\nMedication Usage:"),
                    print(df),
                    sns.barplot(x="MedicationName", y="TotalPrescriptions", data=df),
                    plt.title("Medication Usage"),
                    plt.show()
                )
            },
            5: {
                "name": "Financial Analysis",
                "query": """
                    SELECT Source, SUM(Amount) AS TotalAmount 
                    FROM Revenue
                    GROUP BY Source
                """,
                "process": lambda df: (
                    print("\nRevenue by Source:"),
                    print(df),
                    sns.barplot(x="Source", y="TotalAmount", data=df),
                    plt.title("Revenue by Source"),
                    plt.show()
                )
            }
        }

        conn = self.connect_to_db()
        if conn is None:
            return

        if choice in analysis_functions:
            analysis = analysis_functions[choice]
            print(f"\n--- {analysis['name']} ---")
            df = self.fetch_data(analysis["query"], conn)
            if df is not None:
                analysis["process"](df)
        else:
            print("Invalid choice. Please try again.")

        conn.close()

    # Other methods in the Admin class
    def add_user(self, username, password, role, phone_number=None, age=None, gender=None, salary=None, profession=None, department=None, chronic_disease=None):
        return self.signup(username, password, role, phone_number, age, gender, salary, profession, department, chronic_disease)

    def remove_user(self, username):
        connection = Database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Users WHERE Username = ?", (username,))
                connection.commit()
                print(f"User {username} removed successfully.")
                return True
            except Exception as e:
                print(f"Error removing user: {e}")
                return False
            finally:
                connection.close()
        return False

    def update_pharmacy_inventory(self, medication, stock):
        pharmacy = Pharmacy()
        pharmacy.update_inventory(medication, stock)
        print(f"Updated inventory for {medication} with {stock} units.")

    def view_pharmacy_inventory(self):
        pharmacy = Pharmacy()
        pharmacy.view_inventory()

    def view_financial_insights(self):
        finance = Finance()
        transactions = finance.load_transactions()
        
        if not transactions:
            print("No financial transactions available.")
            return

        df = pd.DataFrame(transactions)
        print(df)

        if 'Transaction Type' not in df.columns or 'Amount' not in df.columns:
            print("Required columns are missing in the financial data.")
            return

        try:
            fig = px.bar(df, x='Transaction Type', y='Amount', title='Financial Transactions', color='Transaction Type', barmode='group')
            fig.update_layout(xaxis_title='Transaction Type', yaxis_title='Total Amount', title_x=0.5)
            fig.show()
        except Exception as e:
            print(f"An error occurred while generating financial insights: {e}")

    def add_department(self, hospital, department_name, description=""):
        hospital.add_department(department_name, description)

    def remove_department(self, hospital, department_name):
        hospital.remove_department(department_name)

    def add_room(self, hospital, room_number, room_type):
        hospital.add_room(room_number, room_type)

    def view_all_users(self):
        connection = Database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM Users")
                rows = cursor.fetchall()
                for row in rows:
                    print(f"Username: {row.Username}")
                    print(f"  Role: {row.Role}")
                    print(f"  Phone Number: {row.PhoneNumber}")
                    print(f"  Age: {row.Age}")
                    print(f"  Gender: {row.Gender}")
                    print(f"  Salary: {row.Salary}")
                    print(f"  Profession: {row.Profession}")
                    print(f"  Department: {row.Department}")
                    print(f"  Chronic Disease: {row.ChronicDisease}")
                    print(f"  Nationality: {row.Nationality}")
                    print()
            except Exception as e:
                print(f"Error viewing users: {e}")
            finally:
                connection.close()

    def view_users_as_dataframe(self):
        connection = Database()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM Users")
                rows = cursor.fetchall()
                users_df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
                users_df.index.name = 'Username'
                users_df.reset_index(inplace=True)
                
                print(users_df.to_string(index=False))

                fig = px.bar(users_df, x='Username', y='age', color='role', title='User Details by Age and Role', barmode='group')
                fig.update_layout(xaxis_title='Username', yaxis_title='Age', title_x=0.5)
                fig.show()

                return users_df
            except Exception as e:
                print(f"Error viewing users: {e}")
            finally:
                connection.close()
        return pd.DataFrame()

    def analyze_workforce_distribution(self):
        users = self.load_users()
        distribution = {
            'doctors': {'specialization': {}, 'shift': {}},
            'nurses': {'shift': {}}, 
            'admin': {'shift': {}}
        }
        for username, details in users.items():
            if details['role'] == 'doctor':
                distribution['doctors']['specialization'][details.get('specialization')] = distribution['doctors']['specialization'].get(details.get('specialization'), 0) + 1
                distribution['doctors']['shift'][details.get('shift')] = distribution['doctors']['shift'].get(details.get('shift'), 0) + 1
            elif details['role'] == 'nurse':
                distribution['nurses']['shift'][details.get('shift')] = distribution['nurses']['shift'].get(details.get('shift'), 0) + 1
            elif details['role'] == 'admin':
                distribution['admin']['shift'][details.get('shift')] = distribution['admin']['shift'].get(details.get('shift'), 0) + 1
        return distribution

    def visualize_workforce_distribution(self):
        distribution = self.analyze_workforce_distribution()
        plt.bar(distribution['doctors']['specialization'].keys(), distribution['doctors']['specialization'].values())
        plt.show()

    def search(self):
        query = input("Enter your search query: ")
        conn = Database()  
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Username, Role, Specialization, PhoneNumber 
            FROM Staff 
            WHERE Username LIKE ? OR Role LIKE ? OR Specialization LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        staff = cursor.fetchall()
        for staff_member in staff:
            print("Staff member found:")
            print("Username:", staff_member[0])
            print("Role:", staff_member[1])
            print("Specialization:", staff_member[2])
            print("Contact:", staff_member[3])
            print("------")

        cursor.execute("""
            SELECT Username, Age, Gender, GeographicLocation 
            FROM Patient 
            WHERE Username LIKE ? OR Gender LIKE ? OR GeographicLocation LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        patients = cursor.fetchall()
        for patient in patients:
            print("Patient found:")
            print("Username:", patient[0])
            print("Age:", patient[1])
            print("Gender:", patient[2])
            print("Geographic Location:", patient[3])
            print("------")

        cursor.execute("""
            SELECT MedicationName, Stock, Price 
            FROM PharmacyInventory 
            WHERE MedicationName LIKE ? OR Stock LIKE ? OR Price LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        pharmacy = cursor.fetchall()
        for item in pharmacy:
            print("Pharmacy item found:")
            print("Medication Name:", item[0])
            print("Stock:", item[1])
            print("Price:", item[2])
            print("------")

        cursor.execute("""
            SELECT DepartmentName, Description 
            FROM Departments 
            WHERE DepartmentName LIKE ? OR Description LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        departments = cursor.fetchall()
        for department in departments:
            print("Department found:")
            print("Department Name:", department[0])
            print("Description:", department[1])
            print("------")

        cursor.execute("""
            SELECT TransactionType, Amount, Balance, TransactionDate 
            FROM FinancialTransactions 
            WHERE TransactionType LIKE ? OR Amount LIKE ? OR Balance LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        transactions = cursor.fetchall()
        for transaction in transactions:
            print("Financial Transaction found:")
            print("Transaction Type:", transaction[0])
            print("Amount:", transaction[1])
            print("Balance:", transaction[2])
            print("Transaction Date:", transaction[3])
            print("------")

        conn.close()





# Doctor class
class Doctor(User):
    def __init__(self, username, password):
        super().__init__(username, password, 'doctor')

    def view_appointments(self):
        appointments = Appointment.load_appointments()
        for appointment_id, details in appointments.items():
            if details['doctor'] == self.username:
                print(f"Appointment {appointment_id}: {details}")

    def write_prescriptions(self, patient, prescription):
        prescriptions = self.load_prescriptions()
        if patient not in prescriptions:
            prescriptions[patient] = []
        prescriptions[patient].append(prescription)
        self.save_prescriptions(prescriptions)
        print(f"Prescription for {patient} added.")

    def load_prescriptions(self):
        try:
            if os.path.exists('data/prescriptions.txt') and os.path.getsize('data/prescriptions.txt') > 0:
                with open('data/prescriptions.txt', 'r') as file:
                    return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading prescriptions: {e}")
        return {}

    def save_prescriptions(self, prescriptions):
        try:
            with open('data/prescriptions.txt', 'w') as file:
                json.dump(prescriptions, file)
        except IOError as e:
            print(f"Error saving prescriptions: {e}")

    def view_patient_records(self, patient):
        records = self.load_patient_records()
        if patient in records:
            print(f"Patient Records for {patient}: {records[patient]}")
        else:
            print(f"No records found for patient {patient}.")

    def add_patient_record(self, patient, record):
        records = self.load_patient_records()
        if patient not in records:
            records[patient] = []
        records[patient].append(record)
        self.save_patient_records(records)
        print(f"Record added for patient {patient}.")

    def load_patient_records(self):
        try:
            if os.path.exists('data/patient_records.txt') and os.path.getsize('data/patient_records.txt') > 0:
                with open('data/patient_records.txt', 'r') as file:
                    return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading patient records: {e}")
        return {}

    def save_patient_records(self, records):
        try:
            with open('data/patient_records.txt', 'w') as file:
                json.dump(records, file)
        except IOError as e:
            print(f"Error saving patient records: {e}")

    def record_treatment_data(self, patient, condition, length_of_stay, readmission):
        treatment_data = self.load_treatment_data()
        treatment_data[patient] = {
            'condition': condition,
            'length_of_stay': length_of_stay,
            'readmission': readmission
        }
        self.save_treatment_data(treatment_data)
        
    def record_patient_feedback(self, patient, feedback):
        feedback_data = self.load_feedback()
        feedback_data[patient] = feedback
        self.save_feedback(feedback_data)

    def record_treatment_outcome(self, patient, success):
        treatment_data = self.load_treatment_data()
        treatment_data[patient] = success
        self.save_treatment_data(treatment_data)




# Patient class



class Patient(User):
    def __init__(self, username, password, age=None, gender=None, geographic_location=None):
        super().__init__(username, password, 'patient')
        self.age = age
        self.gender = gender
        self.geographic_location = geographic_location
        self.finance = Finance()

    def view_appointments(self):
        appointments = Appointment.load_appointments()
        for appointment_id, details in appointments.items():
            if details['patient'] == self.username:
                print(f"Appointment {appointment_id}: {details}")

    def request_appointments(self, doctor, date, time, room, department):
        appointment = Appointment(doctor, self.username, date, time, room, department)
        appointment.book_appointment()
        self.finance.pay_for_appointment(self.username)

    def provide_feedback(self, feedback):
        feedback_data = self.load_feedback()
        feedback_data[self.username] = feedback
        self.save_feedback(feedback_data)



# Receptionist class


class Receptionist(User):
    def __init__(self, username, password):
        super().__init__(username, password, 'receptionist')

    def book_appointments(self, doctor, patient, date, time, room, department):
        appointment = Appointment(doctor, patient, date, time, room, department)
        appointment.book_appointment()

    def cancel_appointments(self, appointment_id):
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-MA8DP5U;DATABASE=HospitalManagement;UID=your_username;PWD=your_password')
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM Appointments
            WHERE AppointmentID = ?
        """, appointment_id)
        conn.commit()
        print(f"Appointment {appointment_id} cancelled.")
        
        conn.close()

    def allocate_room(self, hospital, room_type):
        hospital.allocate_room(room_type)

    def release_room(self, hospital, room_number):
        hospital.release_room(room_number)

    def view_rooms(self, hospital):
        hospital.view_rooms()





# Nurse class
class Nurse(User):
    def __init__(self, username, password):
        super().__init__(username, password, 'nurse')

    def view_patient_records(self):
        records = self.load_patient_records()
        if records:
            print("Patient Records:")
            for record in records:
                print(f"Record ID: {record['RecordID']}, Patient: {record['Patient']}, Record: {record['Record']}")
        else:
            print("No patient records found.")
        return records

    def load_patient_records(self):
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server_name;DATABASE=HospitalManagement;UID=your_username;PWD=your_password')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM PatientRecords")
        records = []
        for row in cursor:
            records.append({
                'RecordID': row.RecordID,
                'Patient': row.Patient,
                'Record': row.Record
            })
        
        conn.close()
        return records