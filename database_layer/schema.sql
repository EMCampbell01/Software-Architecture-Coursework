CREATE TABLE EmergencyCallReports (
    call_id TEXT PRIMARY KEY,
    call_number INTEGER NOT NULL,
    call_time TEXT NOT NULL,
    call_date TEXT NOT NULL,
    call_location TEXT NOT NULL,
    incident_type  TEXT NOT NULL,
    call_details TEXT NOT NULL
);

CREATE TABLE DispatchRequests (
    dispatch_id TEXT PRIMARY KEY,
    ambulance_id TEXT NOT NULL,
    hospital_id, TEXT NOT NULL,
    call_id INTEGER,
    FOREIGN KEY (call_id) REFERENCES EmergencyCallReports(call_id)
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

