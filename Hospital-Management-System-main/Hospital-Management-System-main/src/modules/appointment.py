import pyodbc
import modules.database as database

class Appointment:
    def __init__(self, doctor, patient, date, time, room, department, is_emergency=False):
        self.doctor = doctor
        self.patient = patient
        self.date = date
        self.time = time
        self.room = room
        self.department = department
        self.is_emergency = is_emergency

    @staticmethod
    def database():
        """
        Establish a connection to the database.
        """
        try:
            conn = database
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def book_appointment(self):
        """
        Book an appointment and save it to the database.
        """
        conn = self.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Appointments (Doctor, Patient, Date, Time, Room, Department, IsEmergency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.doctor, self.patient, self.date, self.time, self.room, self.department, self.is_emergency))
            
            conn.commit()
            print("Appointment booked successfully.")
        except Exception as e:
            print(f"Error booking appointment: {e}")
        finally:
            conn.close()

    @staticmethod
    def load_appointments():
        """
        Load all appointments from the database.
        """
        conn = Appointment.database()
        if conn is None:
            return {}

        cursor = conn.cursor()
        appointments = {}
        try:
            cursor.execute("SELECT * FROM Appointments")
            for row in cursor:
                appointments[row.AppointmentID] = {
                    'doctor': row.Doctor,
                    'patient': row.Patient,
                    'date': row.Date,
                    'time': row.Time,
                    'room': row.Room,
                    'department': row.Department,
                    'is_emergency': row.IsEmergency
                }
        except Exception as e:
            print(f"Error loading appointments: {e}")
        finally:
            conn.close()
        return appointments

    @staticmethod
    def save_appointments(appointments):
        """
        Save all appointments to the database.
        """
        conn = Appointment.database()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            # Clear  appointments
            cursor.execute("DELETE FROM Appointments")
            
            # Insert updated appointments
            for appointment_id, details in appointments.items():
                cursor.execute("""
                    INSERT INTO Appointments (Doctor, Patient, Date, Time, Room, Department, IsEmergency)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (details['doctor'], details['patient'], details['date'], details['time'], details['room'], details['department'], details['is_emergency']))
            
            conn.commit()
            print("Appointments saved successfully.")
        except Exception as e:
            print(f"Error saving appointments: {e}")
        finally:
            conn.close()