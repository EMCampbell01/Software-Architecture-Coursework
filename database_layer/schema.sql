CREATE TABLE Ambulances (
    ambulance_id TEXT PRIMARY KEY,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    available BOOLEAN NOT NULL
);

CREATE TABLE Hospitals (
    hospital_name TEXT PRIMARY KEY,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE EmergencyCallReports (
    call_id TEXT PRIMARY KEY,
    call_number INTEGER NOT NULL,
    call_time TEXT NOT NULL,
    call_date TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    incident_type  TEXT NOT NULL,
    call_details TEXT NOT NULL
);

CREATE TABLE DispatchRequests (
    dispatch_id TEXT PRIMARY KEY,
    ambulance_id TEXT NOT NULL,
    hospital_name TEXT NOT NULL,
    call_id INTEGER,
    FOREIGN KEY (call_id) REFERENCES EmergencyCallReports(call_id)
    FOREIGN KEY (hospital_name) REFERENCES EmergencyCallReports(hospital_name)
);

-- Patients Table
CREATE TABLE Patients (
    nhs_patient_id TEXT PRIMARY KEY, -- Assuming NHS ID is unique and serves as the primary key
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    sex TEXT CHECK (sex IN ('M', 'F')), -- Constraint for valid values
    dob DATE NOT NULL,
    address TEXT
);

