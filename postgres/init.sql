-- Insert seed data into the Employee table if not exists
-- All passwords are "password123"
INSERT INTO employees (staff_id, staff_fname, staff_lname, dept, position, country, email, reporting_manager, role, password)
VALUES
    (100, 'John', 'Doe', 'Engineering', 'CTO', 'Singapore', 'etainez88@gmail.com', 100, 3, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (101, 'Alice', 'Smith', 'Engineering', 'Software Engineer', 'USA', 'etainez88@gmail.com', 100, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (102, 'Bob', 'Johnson', 'Engineering', 'Tech Lead', 'Canada', 'etainez88@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (103, 'Charlie', 'Brown', 'Marketing', 'Marketing Manager', 'UK', 'etainez88@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (104, 'David', 'Williams', 'Engineering', 'Senior Engineer', 'Australia', 'etainez88@gmail.com', 102, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (105, 'Emma', 'Jones', 'Human Resources', 'HR Manager', 'New Zealand', 'etainez88@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (106, 'Frank', 'Miller', 'Finance', 'Finance Manager', 'Germany', 'etainez88@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (107, 'Grace', 'Lee', 'Customer Support', 'Support Manager', 'South Korea', 'etainez88@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO')
ON CONFLICT (staff_id) DO NOTHING;
-- Insert seed data into the Team table if not exists
INSERT INTO team (team_id, name, description, created_on, manager_id)
VALUES
    (1, 'Engineering', 'Handles product development and software engineering.', '2023-01-01 09:00:00', 100),
    (2, 'Marketing', 'Responsible for branding and communications.', '2023-02-15 10:00:00', 103),
    (3, 'Human Resources', 'Manages employee relations and recruitment.', '2023-03-01 11:00:00', 105),
    (4, 'Finance', 'Oversees financial planning and accounting.', '2023-04-01 09:30:00', 106),
    (5, 'Customer Support', 'Provides assistance and support to customers.', '2023-05-01 08:45:00', 107)
ON CONFLICT (team_id) DO NOTHING;
-- Insert seed data into the team_employee junction table if not exists
INSERT INTO team_employee (team_id, staff_id)
VALUES
    (1, 100),  -- John in Engineering
    (1, 101),  -- Alice in Engineering
    (1, 102),  -- Bob in Engineering
    (1, 104),  -- David in Engineering
    (2, 103),  -- Charlie in Marketing
    (3, 105),  -- Emma in Human Resources
    (4, 106),  -- Frank in Finance
    (5, 107)   -- Grace in Customer Support
ON CONFLICT (team_id, staff_id) DO NOTHING;

-- Insert seed data into the Application table if not exists
INSERT INTO application (application_id, reason, description, created_on, last_updated_on, status, staff_id, approver_id, recurring)
VALUES
    (201, 'WFH Request', 'Requesting to work from home for two weeks due to home renovation.', '2023-07-01 08:00:00', '2023-07-02 10:00:00', 'pending', 101, 102, TRUE),
    (202, 'Relocation', 'Requesting to relocate to the New York office for 3 months.', '2023-07-05 09:00:00', '2023-07-06 11:00:00', 'pending', 104, 100, FALSE),
    (203, 'Flexible Hours', 'Requesting flexible working hours for childcare reasons.', '2023-07-10 14:00:00', '2023-07-11 09:00:00', 'pending', 103, 100, TRUE),
    (204, 'Remote Work', 'Requesting to work remotely from Bali for 1 month.', '2023-07-15 11:00:00', '2023-07-16 13:00:00', 'pending', 106, 100, FALSE),
    (205, 'Office Change', 'Requesting to move to a quieter area in the office.', '2023-07-20 10:00:00', '2023-07-20 15:00:00', 'pending', 107, 103, FALSE)
ON CONFLICT (application_id) DO NOTHING;

-- Insert seed data into the Event table if not exists
INSERT INTO event (event_id, requested_date, location, application_id)
VALUES
    (401, '2023-07-10', 'wfh', 201),  -- Alice working from home
    (402, '2023-07-12', 'wfh', 201),  -- Alice working from home
    (403, '2023-08-01', 'wfo', 202),  -- David's relocation pending
    (404, '2023-07-15', 'wfo', 203),  -- Charlie's flexible hours
    (405, '2023-07-16', 'wfo', 203),  -- Charlie's flexible hours
    (406, '2023-08-05', 'wfh', 204),  -- Frank's rejected remote work
    (407, '2023-07-25', 'wfo', 205)   -- Grace's office change pending
ON CONFLICT (event_id) DO NOTHING;