import csv
import os
import pyodbc
import modules.database as database

class Finance:
    def __init__(self):
      
        self.database = self.connect_to_db()
        if self.database:
            self.cursor = self.database.cursor()
        else:
            self.cursor = None

    def connect_to_db(self):
       
        try:
            conn = database
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def save_transaction(self, patient, transaction_type, amount):
     
        if self.database is None:
            print("Database connection is not available.")
            return

        balance = self.get_balance(patient) + amount
        
        try:
            self.cursor.execute("""
                INSERT INTO FinancialTransactions (Patient, TransactionType, Amount, Balance)
                VALUES (?, ?, ?, ?)
            """, (patient, transaction_type, amount, balance))
            
            self.database.commit()
            print(f"Transaction saved: {transaction_type} of {amount} EGP for {patient}.")
        except Exception as e:
            print(f"Error saving transaction: {e}")

    def get_balance(self, patient):
      
        if self.database is None:
            print("Database connection is not available.")
            return 0

        try:
            self.cursor.execute("""
                SELECT TOP 1 Balance FROM FinancialTransactions
                WHERE Patient = ?
                ORDER BY TransactionDate DESC
            """, (patient,))
            row = self.cursor.fetchone()
            
            return row.Balance if row else 0
        except Exception as e:
            print(f"Error retrieving balance: {e}")
            return 0

    def deposit(self, patient, amount):
      
        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return

        self.save_transaction(patient, 'Deposit', amount)
        print(f"Deposited {amount} EGP to {patient}'s account.")

    def pay_for_appointment(self, patient):
    
        appointment_cost = -200
        self.save_transaction(patient, 'Appointment Payment', appointment_cost)
        print(f"Paid {abs(appointment_cost)} EGP for appointment from {patient}'s account.")

    def pay_for_medication(self, patient, medication, quantity, price):
      
        if quantity <= 0 or price <= 0:
            print("Quantity and price must be greater than 0.")
            return

        total_cost = -quantity * price
        self.save_transaction(patient, f'Medication Payment ({medication})', total_cost)
        print(f"Paid {abs(total_cost)} EGP for {quantity} units of {medication} from {patient}'s account.")

    def track_revenue(self, source, amount):
       
        if self.database is None:
            print("Database connection is not available.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO Revenue (Source, Amount, Date)
                VALUES (?, ?, GETDATE())
            """, (source, amount))
            
            self.database.commit()
            print(f"Revenue tracked: {amount} EGP from {source}.")
        except Exception as e:
            print(f"Error tracking revenue: {e}")

    def track_costs(self, category, amount):
       
        if self.database is None:
            print("Database connection is not available.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO Costs (Category, Amount, Date)
                VALUES (?, ?, GETDATE())
            """, (category, amount))
            
            self.database.commit()
            print(f"Cost tracked: {amount} EGP for {category}.")
        except Exception as e:
            print(f"Error tracking costs: {e}")

    def track_pending_payments(self):
     
        if self.database is None:
            print("Database connection is not available.")
            return

        try:
            self.cursor.execute("""
                SELECT Patient, SUM(Amount) AS PendingAmount
                FROM FinancialTransactions
                WHERE TransactionType = 'Appointment Payment' OR TransactionType LIKE 'Medication Payment%'
                GROUP BY Patient
                HAVING SUM(Amount) < 0
            """)
            pending_payments = self.cursor.fetchall()
            
            if pending_payments:
                print("Pending Payments:")
                for row in pending_payments:
                    print(f"Patient: {row.Patient}, Pending Amount: {abs(row.PendingAmount)} EGP")
            else:
                print("No pending payments found.")
        except Exception as e:
            print(f"Error tracking pending payments: {e}")

    def analyze_profitability(self):
    
        if self.database is None:
            print("Database connection is not available.")
            return

        try:
            self.cursor.execute("""
                SELECT SUM(Amount) AS TotalRevenue FROM Revenue
            """)
            total_revenue = self.cursor.fetchone().TotalRevenue or 0

            self.cursor.execute("""
                SELECT SUM(Amount) AS TotalCost FROM Costs
            """)
            total_cost = self.cursor.fetchone().TotalCost or 0

            profit = total_revenue - total_cost
            print(f"Profitability Analysis:")
            print(f"Total Revenue: {total_revenue} EGP")
            print(f"Total Cost: {total_cost} EGP")
            print(f"Profit: {profit} EGP")
        except Exception as e:
            print(f"Error analyzing profitability: {e}")

    def close_connection(self):
     
        if self.database:
            self.database.close()
            print("Database connection closed.")