import json
import pyodbc
from modules.finance import Finance
import modules.database as database

class Pharmacy:
    def __init__(self):
      
        self.conn = self.connect_to_db()
        self.inventory = self.load_inventory()
        self.finance = Finance()

    def connect_to_db(self):
        try: 
            conn = database
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def load_inventory(self):
       
        if not self.conn:
            return {}

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT MedicationName, Stock, Price FROM PharmacyInventory")
            inventory = {}
            for row in cursor:
                inventory[row.MedicationName] = {
                    'stock': row.Stock,
                    'price': row.Price
                }
            return inventory
        except Exception as e:
            print(f"Error loading inventory: {e}")
            return {}
        finally:
            cursor.close()

    def update_inventory(self, medication, stock):
      
        if not self.conn:
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM PharmacyInventory WHERE MedicationName = ?", (medication,))
            row = cursor.fetchone()

            if row:
                cursor.execute("""
                    UPDATE PharmacyInventory
                    SET Stock = Stock + ?
                    WHERE MedicationName = ?
                """, (stock, medication))
            else:
                cursor.execute("""
                    INSERT INTO PharmacyInventory (MedicationName, Stock, Price)
                    VALUES (?, ?, ?)
                """, (medication, stock, 0))  

            self.conn.commit()
            self.inventory = self.load_inventory()
            print(f"Inventory updated for {medication}.")
        except Exception as e:
            print(f"Error updating inventory: {e}")
        finally:
            cursor.close()

    def check_expired_medications(self):
     
        if not self.conn:
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT MedicationName, ExpiryDate 
                FROM PharmacyInventory 
                WHERE ExpiryDate < GETDATE()
            """)
            expired_medications = cursor.fetchall()
            
            if expired_medications:
                print("Expired Medications:")
                for row in expired_medications:
                    print(f"{row.MedicationName} expired on {row.ExpiryDate}.")
            else:
                print("No expired medications found.")
        except Exception as e:
            print(f"Error checking expired medications: {e}")
        finally:
            cursor.close()

    def view_inventory(self):
     
        print("Pharmacy Inventory:")
        for medication, details in self.inventory.items():
            print(f"{medication}: {details['stock']} units, Price: ${details['price']}")

    def dispense_medication(self, patient, medication, quantity):
       
        if not self.conn:
            return

        if medication in self.inventory and self.inventory[medication]['stock'] >= quantity:
            cursor = self.conn.cursor()
            try:
                cursor.execute("""
                    UPDATE PharmacyInventory
                    SET Stock = Stock - ?
                    WHERE MedicationName = ?
                """, (quantity, medication))

                self.conn.commit()
                self.inventory = self.load_inventory()

                self.finance.pay_for_medication(patient, medication, quantity, self.inventory[medication]['price'])
                print(f"Dispensed {quantity} units of {medication} to {patient}.")
            except Exception as e:
                print(f"Error dispensing medication: {e}")
            finally:
                cursor.close()
        else:
            print(f"Insufficient stock for {medication}.")

    def close_connection(self):
      
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")

    def analyze_prescription_trends(self):
      
        if not self.conn:
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT MedicationName, SUM(PrescriptionCount) AS TotalPrescriptions
                FROM PrescriptionTrends
                GROUP BY MedicationName
            """)
            prescription_trends = cursor.fetchall()
            
            if prescription_trends:
                print("Prescription Trends:")
                for row in prescription_trends:
                    print(f"{row.MedicationName}: {row.TotalPrescriptions} prescriptions")
            else:
                print("No prescription trends found.")
        except Exception as e:
            print(f"Error analyzing prescription trends: {e}")
        finally:
            cursor.close()

    def check_compliance(self):
    
        if not self.conn:
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT Patient, MedicationName, ComplianceStatus
                FROM COMPLIANCE
                WHERE ComplianceStatus = 'non-compliant'
            """)
            non_compliant_patients = cursor.fetchall()
            
            if non_compliant_patients:
                print("Non-Compliant Patients:")
                for row in non_compliant_patients:
                    print(f"Patient: {row.Patient}, Medication: {row.MedicationName}, Status: {row.ComplianceStatus}")
            else:
                print("All patients are compliant.")
        except Exception as e:
            print(f"Error checking compliance: {e}")
        finally:
            cursor.close()

    def analyze_supplier_performance(self):
    
        if not self.conn:
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT SupplierName, AVG(PerformanceRating) AS AvgRating
                FROM Supplier
                GROUP BY SupplierName
            """)
            supplier_performance = cursor.fetchall()
            
            if supplier_performance:
                print("Supplier Performance:")
                for row in supplier_performance:
                    print(f"{row.SupplierName}: Average Rating {row.AvgRating}")
            else:
                print("No supplier performance data found.")
        except Exception as e:
            print(f"Error analyzing supplier performance: {e}")
        finally:
            cursor.close()