-- Insert seed data into the Team table if not exists
INSERT INTO team (team_id, name, description, created_on)
VALUES
    (1, 'Engineering', 'Handles product development and software engineering.', '2023-01-01 09:00:00'),
    (2, 'Marketing', 'Responsible for branding and communications.', '2023-02-15 10:00:00')
ON CONFLICT (team_id) DO NOTHING;

-- Insert seed data into the Employee table if not exists
-- All the password is "password123"
INSERT INTO employees (staff_id, staff_fname, staff_lname, dept, position, country, email, reporting_manager, role, password)
VALUES
    (101, 'Alice', 'Smith', 'Engineering', 'Software Engineer', 'USA', 'alice.smith@example.com', 101, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (102, 'Bob', 'Johnson', 'Engineering', 'Tech Lead', 'Canada', 'bob.johnson@example.com', 101, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (103, 'Charlie', 'Brown', 'Marketing', 'Marketing Manager', 'UK', 'charlie.brown@example.com', 102, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (104, 'David', 'Williams', 'Engineering', 'Senior Engineer', 'Australia', 'david.williams@example.com', 103, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO')
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
    (301,'WFH Arrangement', 'Approved WFH arrangement for Alice.', TRUE, 201),
    (302, 'Relocation Arrangement', 'Pending approval for David relocation.', FALSE, 202)
ON CONFLICT (arrangement_id) DO NOTHING;

-- Insert seed data into the Event table if not exists
INSERT INTO event (event_id, datetime, location, arrangement_id)
VALUES
    (401, '2023-07-10 09:00:00', 'wfh', 301),  -- Alice working from home
    (402, '2023-07-12 09:00:00', 'wfh', 301),  -- Alice working from home
    (403, '2023-08-01 09:00:00', 'wfo', 302)   -- David's relocation pending
ON CONFLICT (event_id) DO NOTHING;
