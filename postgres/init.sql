-- Insert data into departments table
INSERT INTO "departments" (department_id, name, description, director_id)
VALUES
    (100, 'John', 'Doe', 'Engineering', 'CTO', 'Singapore', 'colinmok1000@gmail.com', 100, 3, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (101, 'Alice', 'Smith', 'Engineering', 'Software Engineer', 'USA', 'colinmok3@gmail.com', 100, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (102, 'Bob', 'Johnson', 'Engineering', 'Tech Lead', 'Canada', 'test@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (103, 'Charlie', 'Brown', 'Marketing', 'Marketing Manager', 'UK', 'test@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (104, 'David', 'Williams', 'Engineering', 'Senior Engineer', 'Australia', 'test@gmail.com', 102, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (105, 'Emma', 'Jones', 'Human Resources', 'HR Manager', 'New Zealand', 'test@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (106, 'Frank', 'Miller', 'Finance', 'Finance Manager', 'Germany', 'test@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (107, 'Grace', 'Lee', 'Customer Support', 'Support Manager', 'South Korea', 'test@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO')
ON CONFLICT (staff_id) DO NOTHING;
-- Insert seed data into the Team table if not exists
INSERT INTO team (team_id, name, description, created_on, manager_id)
VALUES
    (1, 'Executives', 'Team for the executive leadership including the CEO.', NULL, 1, NULL),
    (2, 'Consultants - Ernst Sim''s Team', 'Team that advises clients on business strategies.', NULL, 7, 1),
    (3, 'Engineers - Philip Lee''s Team', 'Team responsible for product development and software engineering.', NULL, 4, 1),
    (4, 'Finance Managers - David Yap''s Team', 'Team that oversees financial planning and accounting.', NULL, 6, 1),
    (5, 'Finance Executives - Seng Kesavan''s Team', 'Team that handles day-to-day financial operations.', NULL, 6, 4),
    (6, 'Finance Executives - Narong Pillai''s Team', 'Team that handles day-to-day financial sales.', NULL, 6, 4),
    (7, 'Finance Executives - Ji Truong''s Team', 'Team that handles day-to-day financial trading.', NULL, 6,4),
    (8, 'Finance Executives - Chandra Kong''s Team', 'Team that handles all company assets.', NULL, 6,4),
    (9, 'Finance Executives - Rithy Luong''s Team', 'Team that handles manages company cashflow and balance sheet.', NULL, 6,4),
    (10, 'HR Team - Sally Loh''s Team', 'Team that manages employee relations and recruitment.', NULL, 5,1),
    (11, 'IT Team- Peter Yap''s Team', 'Team that manages technology infrastructure and support.', NULL, 8,1),
    (12, 'Sales Managers - Derek Tan''s Team', 'Team that manages sales and customer acquisition activities.', NULL,2, 1),
    (13, 'Account Managers - Jaclyn Lee''s Team', 'Team that manages all the <$5k accounts for the company.', NULL, 2,12),
    (14, 'Account Managers - Sophia Toh''s Team', 'Team that manages all the <$10k accounts for the company.', NULL, 2,12),
    (15, 'Account Managers - Siti Abdullah''s Team', 'Team that manages all the <$20k accounts for the company.', NULL, 2,12),
    (16, 'Account Managers - Rahim Khalid''s Team', 'Team that manages all the <$30k accounts for the company.', NULL, 2,12),
    (17, 'Account Managers - Yee Lim''s Team', 'Team that manages all the <$40k accounts for the company.', NULL, 2,12),
    (18, 'Solutioning Managers - Eric Loh''s Team', 'Team that creates tailored solutions for clients.', NULL, 3, 1)
ON CONFLICT (team_id) DO NOTHING;  -- Adjust this as necessary for your team's uniqueness criteria

-- Insert employees into the employees table
INSERT INTO "employees" (staff_id, staff_fname, staff_lname, position, department_id, team_id, country, email, reporting_manager, role, password)
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
    (201, 'WFH Request', 'Requesting to work from home for two weeks due to home renovation.', '2023-07-01 08:00:00', '2023-07-02 10:00:00', 'approved', 101, 100, FALSE),
    (202, 'Relocation', 'Requesting to relocate to the New York office for 3 months.', '2023-07-05 09:00:00', '2023-07-06 11:00:00', 'pending', 101, 102, FALSE),
    (203, 'Flexible Hours', 'Requesting flexible working hours for childcare reasons.', '2023-07-10 14:00:00', '2023-07-11 09:00:00', 'approved', 103, 100, FALSE),
    (204, 'Remote Work', 'Requesting to work remotely from Bali for 1 month.', '2023-07-15 11:00:00', '2023-07-16 13:00:00', 'rejected', 106, 100, FALSE),
    (205, 'Office Change', 'Requesting to move to a quieter area in the office.', '2023-07-20 10:00:00', '2023-07-20 15:00:00', 'pending', 100, 103, FALSE)
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