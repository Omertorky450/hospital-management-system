# HMS - Hospital Management System

## Overview

The Hospital Management System (HMS) is a comprehensive application designed to streamline the operations of a hospital. It provides role-based access for different users, including administrators, doctors, patients, receptionists, and nurses. The system manages appointments, financial transactions, pharmacy inventory, and patient records efficiently.

## Features

### Role-Based Access

- **Admin**:
  - Manage users (add/remove users with roles: Nurse, Receptionist, Doctor).
  - Access business insights, financial reports, and pharmacy data.
  - View and analyze data using visualizations.

- **Doctor**:
  - View appointments.
  - Write prescriptions with auto-complete for medications.
  - Update and manage patient medical records.

- **Patient**:
  - Request appointments.
  - View personal appointment history.

- **Receptionist**:
  - Book and cancel appointments.
  - Manage room allocations.

- **Nurse**:
  - View patient records and prescriptions.

### Appointment Management

- Book, view, and manage appointments for patients and doctors.
- Include department information in appointment details.

### Financial Management

- Track financial transactions related to patient deposits and payments.
- Generate financial analytics and visual reports.

### Pharmacy Integration

- Manage medication inventory, including viewing, updating, and dispensing medications.
- Notify pharmacy about prescribed medications and generate receipts for patients.

### Data Analysis and Visualization

- Provide real-time insights using data visualization tools for:
  - Business performance.
  - Pharmacy inventory trends.
  - Financial metrics.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Ziadelshazly22/Hospital-Management-System
   ```

2. Navigate to the project directory:

   ```bash
   cd HMS
   ```

3. Set up a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage Instructions

- Run the application:

  ```bash
  python main.py
  ```

- Interact with the system based on your role:
  - **Admin**: Manage users, view analytics, and access financial and pharmacy data.
  - **Doctor**: Write prescriptions and manage patient records.
  - **Patient**: Request appointments and view history.

## Data Files

- **appointments.json**: Stores appointment data in JSON format.
- **medications_New_prices_up_to_03-08-2024.json**: Contains medication details for pharmacy operations.
- **nationalities-common.json**:Contains all of the Nationalities for auto complete or select while data entry.
- **patient_records.txt**: Stores patient medical records in JSON format.
- **prescriptions.txt**: Stores prescription data in JSON format.
- **users.json**: Stores user data in JSON format.
- **financial_data.csv**: Stores financial transactions in CSV format.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
