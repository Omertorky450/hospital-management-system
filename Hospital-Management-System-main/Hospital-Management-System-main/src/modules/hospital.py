import pyodbc
import modules.database as database

class Hospital:
    def __init__(self, name):
       
        self.name = name
        self.initialize_departments()

    def database(self):
       
        try:
            conn = database
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def initialize_departments(self):
        
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            # Fetch existing departments
            cursor.execute("SELECT DepartmentName, Description FROM Departments")
            self.departments = {row.DepartmentName: row.Description for row in cursor}
        except Exception as e:
            print(f"Error initializing departments: {e}")
        finally:
            conn.close()

    def add_department(self, department_name, description=""):
       
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DepartmentName FROM Departments WHERE DepartmentName = ?", (department_name,))
            if cursor.fetchone():
                print(f"Department {department_name} already exists.")
            else:
                cursor.execute("""
                    INSERT INTO Departments (DepartmentName, Description)
                    VALUES (?, ?)
                """, (department_name, description))
                conn.commit()
                print(f"Department {department_name} added successfully.")
        except Exception as e:
            print(f"Error adding department: {e}")
        finally:
            conn.close()

    def remove_department(self, department_name):
     
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DepartmentName FROM Departments WHERE DepartmentName = ?", (department_name,))
            if cursor.fetchone():
                cursor.execute("DELETE FROM Departments WHERE DepartmentName = ?", (department_name,))
                conn.commit()
                print(f"Department {department_name} removed successfully.")
            else:
                print(f"Department {department_name} does not exist.")
        except Exception as e:
            print(f"Error removing department: {e}")
        finally:
            conn.close()

    def add_room(self, room_number, room_type):
     
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT RoomNumber FROM Rooms WHERE RoomNumber = ?", (room_number,))
            if cursor.fetchone():
                print(f"Room {room_number} already exists.")
            else:
                cursor.execute("""
                    INSERT INTO Rooms (RoomNumber, RoomType, IsAvailable)
                    VALUES (?, ?, 1)
                """, (room_number, room_type))
                conn.commit()
                print(f"Room {room_number} of type {room_type} added successfully.")
        except Exception as e:
            print(f"Error adding room: {e}")
        finally:
            conn.close()

    def allocate_room(self, room_type):
    
        conn = self.database()
        if conn is None:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT TOP 1 RoomNumber FROM Rooms
                WHERE RoomType = ? AND IsAvailable = 1
            """, (room_type,))
            row = cursor.fetchone()
            
            if row:
                room_number = row.RoomNumber
                cursor.execute("""
                    UPDATE Rooms SET IsAvailable = 0
                    WHERE RoomNumber = ?
                """, (room_number,))
                conn.commit()
                print(f"Allocated room number: {room_number}")
            else:
                print(f"No available rooms of type {room_type}.")
            
            return room_number if row else None
        except Exception as e:
            print(f"Error allocating room: {e}")
            return None
        finally:
            conn.close()

    def release_room(self, room_number):
     
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT RoomNumber FROM Rooms WHERE RoomNumber = ?", (room_number,))
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE Rooms SET IsAvailable = 1
                    WHERE RoomNumber = ?
                """, (room_number,))
                conn.commit()
                print(f"Room {room_number} is now available.")
            else:
                print(f"Room {room_number} does not exist.")
        except Exception as e:
            print(f"Error releasing room: {e}")
        finally:
            conn.close()

    def view_departments(self):
       
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DepartmentName, Description FROM Departments")
            print("Departments in the hospital:")
            for row in cursor:
                print(f"- {row.DepartmentName}: {row.Description}")
        except Exception as e:
            print(f"Error viewing departments: {e}")
        finally:
            conn.close()

    def view_rooms(self):
       
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT RoomNumber, RoomType, IsAvailable FROM Rooms")
            print("Rooms in the hospital:")
            for row in cursor:
                status = "Available" if row.IsAvailable else "Occupied"
                print(f"Room {row.RoomNumber}: Type: {row.RoomType}, Status: {status}")
        except Exception as e:
            print(f"Error viewing rooms: {e}")
        finally:
            conn.close()

    def add_user(self, username, password, role, phone_number=None, age=None, gender=None, salary=None, profession=None, department=None, chronic_disease=None, nationality=None):
     
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Username FROM Users WHERE Username = ?", (username,))
            if cursor.fetchone():
                print(f"User {username} already exists.")
            else:
                cursor.execute("""
                    INSERT INTO Users (Username, Password, Role, PhoneNumber, Age, Gender, Salary, Profession, Department, ChronicDisease, Nationality)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password, role, phone_number, age, gender, salary, profession, department, chronic_disease, nationality))
                conn.commit()
                print(f"User {username} added successfully.")
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            conn.close()

    def schedule_appointment(self, doctor, patient, date, time, room, department):
    
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Appointments (Doctor, Patient, Date, Time, Room, Department)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (doctor, patient, date, time, room, department))
            conn.commit()
            print(f"Appointment scheduled for {patient} with {doctor} on {date} at {time} in {room}.")
        except Exception as e:
            print(f"Error scheduling appointment: {e}")
        finally:
            conn.close()

    def add_prescription(self, patient, prescription):
    
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Prescriptions (Patient, Prescription)
                VALUES (?, ?)
            """, (patient, prescription))
            conn.commit()
            print(f"Prescription added for {patient}.")
        except Exception as e:
            print(f"Error adding prescription: {e}")
        finally:
            conn.close()

    def add_patient_record(self, patient, record):
        """
        Add a record for a patient.
        """
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO PatientRecords (Patient, Record)
                VALUES (?, ?)
            """, (patient, record))
            conn.commit()
            print(f"Record added for {patient}.")
        except Exception as e:
            print(f"Error adding patient record: {e}")
        finally:
            conn.close()

    def add_financial_transaction(self, patient, transaction_type, amount, balance):
       
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO FinancialTransactions (Patient, TransactionType, Amount, Balance)
                VALUES (?, ?, ?, ?)
            """, (patient, transaction_type, amount, balance))
            conn.commit()
            print(f"Financial transaction added for {patient}.")
        except Exception as e:
            print(f"Error adding financial transaction: {e}")
        finally:
            conn.close()

    def add_medication(self, medication_name, stock, price):
      
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MedicationName FROM PharmacyInventory WHERE MedicationName = ?", (medication_name,))
            if cursor.fetchone():
                print(f"Medication {medication_name} already exists.")
            else:
                cursor.execute("""
                    INSERT INTO PharmacyInventory (MedicationName, Stock, Price)
                    VALUES (?, ?, ?)
                """, (medication_name, stock, price))
                conn.commit()
                print(f"Medication {medication_name} added successfully.")
        except Exception as e:
            print(f"Error adding medication: {e}")
        finally:
            conn.close()



