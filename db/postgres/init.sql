-- Team table
CREATE TABLE IF NOT EXISTS team (
    team_id BIGINT PRIMARY KEY, 
    name VARCHAR(100) NOT NULL, 
    description TEXT, 
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employee table
CREATE TABLE IF NOT EXISTS employees (
    staff_id BIGINT PRIMARY KEY, 
    staff_fname VARCHAR(50) NOT NULL, 
    staff_lname VARCHAR(50) NOT NULL, 
    dept VARCHAR(50) NOT NULL, 
    position VARCHAR(50) NOT NULL, 
    country VARCHAR(50) NOT NULL, 
    email VARCHAR(50) NOT NULL UNIQUE, 
    reporting_manager BIGINT, 
    role INT NOT NULL, 
    password VARCHAR(128) NOT NULL, 
    CONSTRAINT fk_reporting_manager FOREIGN KEY (reporting_manager) REFERENCES employees(staff_id)
);

-- Junction table for the many-to-many relationship between Employees and Team
CREATE TABLE IF NOT EXISTS team_employee (
    team_id BIGINT NOT NULL, 
    staff_id BIGINT NOT NULL, 
    PRIMARY KEY (team_id, staff_id), 
    CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES team(team_id), 
    CONSTRAINT fk_employee FOREIGN KEY (staff_id) REFERENCES employees(staff_id)
);

-- Application table
CREATE TABLE IF NOT EXISTS application (
    application_id BIGINT PRIMARY KEY, 
    reason TEXT NOT NULL, 
    description TEXT, 
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    last_updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    status VARCHAR(20) CHECK (status IN ('approved', 'pending', 'rejected', 'withdrawn')), 
    staff_id BIGINT NOT NULL, 
    CONSTRAINT fk_employee_application FOREIGN KEY (staff_id) REFERENCES employees(staff_id)
);

-- Arrangement table
CREATE TABLE IF NOT EXISTS arrangement (
    arrangement_id BIGINT PRIMARY KEY, 
    reason TEXT NOT NULL, 
    description TEXT, 
    recurring BOOLEAN, 
    application_id BIGINT NOT NULL, 
    CONSTRAINT fk_application FOREIGN KEY (application_id) REFERENCES application(application_id)
);

-- Event table
CREATE TABLE IF NOT EXISTS event (
    event_id BIGINT PRIMARY KEY, 
    datetime TIMESTAMP NOT NULL, 
    location VARCHAR(10) CHECK (location IN ('wfh', 'wio', 'wfo')), 
    arrangement_id BIGINT NOT NULL, 
    CONSTRAINT fk_arrangement FOREIGN KEY (arrangement_id) REFERENCES arrangement(arrangement_id)
);

-- Insert seed data into the Team table if not exists
INSERT INTO team (team_id, name, description, created_on)
VALUES 
    (1, 'Engineering', 'Handles product development and software engineering.', '2023-01-01 09:00:00'),
    (2, 'Marketing', 'Responsible for branding and communications.', '2023-02-15 10:00:00')
ON CONFLICT (team_id) DO NOTHING;

-- Insert seed data into the Employee table if not exists
INSERT INTO employees (staff_id, staff_fname, staff_lname, dept, position, country, email, reporting_manager, role, password)
VALUES 
    (101, 'Alice', 'Smith', 'Engineering', 'Software Engineer', 'USA', 'alice.smith@example.com', NULL, 1, 'password123'),
    (102, 'Bob', 'Johnson', 'Engineering', 'Tech Lead', 'Canada', 'bob.johnson@example.com', NULL, 2, 'password456'),
    (103, 'Charlie', 'Brown', 'Marketing', 'Marketing Manager', 'UK', 'charlie.brown@example.com', NULL, 2, 'password789'),
    (104, 'David', 'Williams', 'Engineering', 'Senior Engineer', 'Australia', 'david.williams@example.com', 102, 1, 'passwordabc')
ON CONFLICT (staff_id) DO NOTHING;

-- Insert seed data into the team_employee junction table if not exists
INSERT INTO team_employee (team_id, staff_id)
VALUES
    (1, 101),  -- Alice in Engineering
    (1, 102),  -- Bob in Engineering
    (1, 104),  -- David in Engineering
    (2, 103)   -- Charlie in Marketing
ON CONFLICT (team_id, staff_id) DO NOTHING;

-- Insert seed data into the Application table if not exists
INSERT INTO application (application_id, reason, description, created_on, last_updated_on, status, staff_id)
VALUES 
    (201, 'WFH Request', 'Requesting to work from home for two weeks.', '2023-07-01 08:00:00', '2023-07-01 08:00:00', 'approved', 101),
    (202, 'Relocation', 'Requesting to relocate to a different city.', '2023-07-05 09:00:00', '2023-07-06 10:00:00', 'pending', 104)
ON CONFLICT (application_id) DO NOTHING;

-- Insert seed data into the Arrangement table if not exists
INSERT INTO arrangement (arrangement_id, reason, description, recurring, application_id)
VALUES
    (301,"'WFH Arrangement', 'Approved WFH arrangement for Alice.", TRUE, 201),
    (302, "Relocation Arrangement', 'Pending approval for David\'s relocation.", FALSE, 202)
ON CONFLICT (arrangement_id) DO NOTHING;

-- Insert seed data into the Event table if not exists
INSERT INTO event (event_id, datetime, location, arrangement_id)
VALUES
    (401, '2023-07-10 09:00:00', 'wfh', 301),  -- Alice working from home
    (402, '2023-07-12 09:00:00', 'wfh', 301),  -- Alice working from home
    (403, '2023-08-01 09:00:00', 'wfo', 302)   -- David's relocation pending
ON CONFLICT (event_id) DO NOTHING;
