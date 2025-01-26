import pyodbc

def create_connection():
    """
    Create a connection to the SQL Server database.
    
    Returns:
        pyodbc.Connection: A connection object if successful, otherwise None.
    """
    try:
        connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-MA8DP5U;" 
            "DATABASE=HospitalManagement;"  
            "Trusted_Connection=yes;"  
            )

        connection = pyodbc.connect(connection_string)
        print("Connection to SQL Server successful.")
        return connection
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None