CREATE DATABASE HospitalManagement;

USE HospitalManagement;

CREATE TABLE Users (
    Username NVARCHAR(50) PRIMARY KEY,
    Password NVARCHAR(50) NOT NULL,
    Role NVARCHAR(50) NOT NULL,
    PhoneNumber NVARCHAR(15),
    Age INT,
    Gender NVARCHAR(10),
    Salary DECIMAL(15, 2),
    Profession NVARCHAR(50),
    Department NVARCHAR(50),
    ChronicDisease NVARCHAR(MAX),
    Nationality NVARCHAR(50)
);

CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY IDENTITY(1,1),
    Doctor NVARCHAR(50) NOT NULL,
    Patient NVARCHAR(50) NOT NULL,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Room NVARCHAR(50) NOT NULL,
    Department NVARCHAR(50) NOT NULL
);

CREATE TABLE Prescriptions (
    PrescriptionID INT PRIMARY KEY IDENTITY(1,1),
    Patient NVARCHAR(50) NOT NULL,
    Prescription NVARCHAR(MAX) NOT NULL
);

CREATE TABLE PatientRecords (
    RecordID INT PRIMARY KEY IDENTITY(1,1),
    Patient NVARCHAR(50) NOT NULL,
    Record NVARCHAR(MAX) NOT NULL
);

CREATE TABLE FinancialTransactions (
    TransactionID INT PRIMARY KEY IDENTITY(1,1),  
    Patient NVARCHAR(50) NOT NULL,
    TransactionType NVARCHAR(50) NOT NULL,
    Amount DECIMAL(18, 2) NOT NULL,
    Balance DECIMAL(18, 2) NOT NULL,
    TransactionDate DATETIME DEFAULT GETDATE()  
);

CREATE TABLE Departments (
    DepartmentID INT PRIMARY KEY IDENTITY(1,1), 
    DepartmentName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(MAX)
);
CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY IDENTITY(1,1),  
    RoomNumber NVARCHAR(50) NOT NULL,
    RoomType NVARCHAR(50) NOT NULL,
);
CREATE TABLE PharmacyInventory (
    MedicationID INT PRIMARY KEY IDENTITY(1,1),  
    MedicationName NVARCHAR(100) NOT NULL,
    Stock INT NOT NULL,
    Price DECIMAL(18, 2) NOT NULL

);


CREATE TABLE Staff (
    StaffID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(50) NOT NULL,
    Role VARCHAR(50) NOT NULL CHECK (Role IN ('doctor', 'nurse', 'admin')),
    Specialization VARCHAR(100),
    Shift VARCHAR(50) CHECK (Shift IN ('morning', 'afternoon', 'night')),
    OvertimeHours INT DEFAULT 0,
    Certifications TEXT,
    TrainingPrograms TEXT
);

CREATE TABLE PerformanceEvaluation (
    EvaluationID INT PRIMARY KEY IDENTITY(1,1),
    StaffID INT,
    PatientFeedback TEXT,
    PatientsTreatedPerDay INT,
    TreatmentSuccessRate FLOAT,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);
CREATE TABLE Turnover (
    TurnoverID INT PRIMARY KEY identity(1,1),
    StaffID INT,
    ResignationReason TEXT,
    HiringDate DATE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
);

CREATE TABLE Patient (
    PatientID INT PRIMARY KEY IDENTITY (1,1),
    Username VARCHAR(50) UNIQUE,
    Age INT,
    Gender NVARCHAR(50),
    GeographicLocation VARCHAR(100)
);

CREATE TABLE Treatment (
    TreatmentID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT,
    Condition VARCHAR(100),
    LengthOfStay INT,
    Readmission BIT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE PatientFeedback (
    FeedbackID INT PRIMARY KEY  IDENTITY(1,1),
    PatientID INT,
    Feedback TEXT,
    NPSScore INT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE MedicalHistory (
    HistoryID INT PRIMARY KEY  IDENTITY(1,1),
    PatientID INT,
    EHRUsage TEXT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);


CREATE TABLE PrescriptionTrends (
    PrescriptionID INT PRIMARY KEY IDENTITY(1,1),
    MedicationID INT,
    Department VARCHAR(100),
    PrescriptionCount INT,
    FOREIGN KEY (MedicationID) REFERENCES PharmacyInventory(MedicationID)
);

CREATE TABLE COMPLIANCE (
    ComplianceID INT PRIMARY KEY IDENTITY(1,1),
    MedicationID INT,
    ComplianceStatus VARCHAR(50) NOT NULL CHECK (ComplianceStatus IN ('compliant', 'non-compliant')),
    FOREIGN KEY (MedicationID) REFERENCES PharmacyInventory(MedicationID)
);

CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY IDENTITY(1,1),
    MedicationID INT,
    SupplierName VARCHAR(100),
    PerformanceRating INT,
    FOREIGN KEY (MedicationID) REFERENCES PharmacyInventory(MedicationID)
);




CREATE TABLE Revenue (
    RevenueID INT PRIMARY KEY IDENTITY(1,1),
    Source VARCHAR(50) NOT NULL CHECK (Source IN ('insurance', 'out-of-pocket', 'government')),
    Amount DECIMAL(18, 2),
    Date DATE
);

CREATE TABLE Costs (
    CostID INT PRIMARY KEY IDENTITY(1,1),
    Category VARCHAR(50) NOT NULL CHECK (Category IN ('salaries', 'utilities', 'maintenance', 'equipment')),
    Amount DECIMAL(18, 2),
    Date DATE
);

CREATE TABLE Billing (
    BillingID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT,
    Amount DECIMAL(10, 2),
    Pending bit,
    BillingCycleTime INT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

CREATE TABLE Profitability (
    ProfitabilityID INT PRIMARY KEY IDENTITY(1,1),
    Department VARCHAR(100),
    Revenue DECIMAL(10, 2),
    Cost DECIMAL(10, 2),
    Profit DECIMAL(10, 2)
);

CREATE TABLE FinancialAid (
    AidID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT,
    Amount DECIMAL(10, 2),
    Date DATE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);


CREATE TABLE PatientCarePathways (
    PathwayID INT PRIMARY KEY IDENTITY(1,1),
    PatientID INT,
    StaffID INT,
    MedicationID INT,
    FinancialID INT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (MedicationID) REFERENCES PharmacyInventory(MedicationID),
    FOREIGN KEY (FinancialID) REFERENCES Revenue(RevenueID)
);

CREATE TABLE SystemEfficiency (
    EfficiencyID INT PRIMARY KEY IDENTITY(1,1),
    RegistrationToDischargeTime INT,
    InterDepartmentalDelays TEXT
);

CREATE TABLE TechnologyUsage (
    TechnologyID INT PRIMARY KEY IDENTITY(1,1),
    EHRIntegration bit,
    AutomationUsage bit,
    AIUsage bit
);


CREATE TABLE Dashboards (
    DashboardID INT PRIMARY KEY IDENTITY(1,1),
    MetricType VARCHAR(50) NOT NULL CHECK (MetricType IN ('staff', 'patient', 'pharmacy', 'financial', 'system')),
    Data NVARCHAR(MAX)
);

CREATE TABLE Reports (
    ReportID INT PRIMARY KEY IDENTITY(1,1),
    ReportType VARCHAR(50) NOT NULL CHECK (ReportType IN ('staff', 'patient', 'pharmacy', 'financial', 'system')),
    ReportData NVARCHAR(MAX),
    DateGenerated DATE
);


