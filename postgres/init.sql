INSERT INTO departments (department_id, name, description, director_id)
VALUES
    (1, 'Technology', 'Oversees all technology-related operations', NULL),
    (2, 'Marketing', 'Handles all marketing and branding activities', NULL),
    (3, 'Human Resources', 'Manages employee relations and recruitment', NULL),
    (4, 'Finance', 'Oversees financial planning and accounting', NULL),
    (5, 'Customer Support', 'Provides assistance and support to customers', NULL)
ON CONFLICT (department_id) DO NOTHING;

INSERT INTO teams (team_id, name, description, manager_id, department_id, parent_team_id)
VALUES
    (1, 'Engineering', 'Handles product development and software engineering', NULL, 1, NULL),
    (2, 'Marketing Team', 'Responsible for branding and communications',  NULL, 2, NULL),
    (3, 'HR Team', 'Manages employee relations and recruitment',  NULL, 3, NULL),
    (4, 'Finance Team', 'Oversees financial planning and accounting', NULL, 4, NULL),
    (5, 'Support Team', 'Provides assistance and support to customers',  NULL, 5, NULL),
    (6, 'Frontend Team', 'Develops user interfaces and client-side applications',  NULL, 1, 1),
    (7, 'Backend Team', 'Develops server-side applications and APIs',  NULL, 1, 1),
    (8, 'DevOps Team', 'Manages infrastructure and deployment processes',  NULL, 1, 1),
    (9, 'Digital Marketing', 'Focuses on online marketing strategies',  NULL, 2, 2),
    (10, 'Content Creation', 'Produces marketing content across various media',  NULL, 2, 2)
ON CONFLICT (team_id) DO NOTHING;


INSERT INTO employees (staff_id, staff_fname, staff_lname, position, department_id, team_id, country, email, reporting_manager, role, password)
VALUES
    (100, 'John', 'Doe', 'CTO', 1, 1, 'Singapore', 'etainez88@gmail.com', NULL, 3, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (101, 'Alice', 'Smith', 'Software Engineer', 1, 1, 'USA', 'khaosdiscord@gmail.com', 100, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (102, 'Bob', 'Johnson', 'Tech Lead', 1, 1, 'Canada', 'test1@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (103, 'Charlie', 'Brown', 'Marketing Manager', 2, 2, 'UK', 'test2@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (104, 'David', 'Williams', 'Senior Engineer', 1, 1, 'Australia', 'test3@gmail.com', 102, 1, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (105, 'Emma', 'Jones', 'HR Manager', 3, 3, 'New Zealand', 'test4@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (106, 'Frank', 'Miller', 'Finance Manager', 4, 4, 'Germany', 'test5@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO'),
    (107, 'Grace', 'Lee', 'Support Manager', 5, 5, 'South Korea', 'test6@gmail.com', 100, 2, '$2b$12$agWjFGi0AaStERzrWIncZe7B7Rc3DaBmSNo7QZ7/wa6HAyxyymMyO')
ON CONFLICT (staff_id) DO NOTHING;

-- Update department directors and team managers
UPDATE departments SET director_id = 100 WHERE department_id = 1;
UPDATE departments SET director_id = 103 WHERE department_id = 2;
UPDATE departments SET director_id = 105 WHERE department_id = 3;
UPDATE departments SET director_id = 106 WHERE department_id = 4;
UPDATE departments SET director_id = 107 WHERE department_id = 5;

-- Update team managers
UPDATE teams SET manager_id = 100 WHERE team_id = 1;
UPDATE teams SET manager_id = 103 WHERE team_id = 2;
UPDATE teams SET manager_id = 105 WHERE team_id = 3;
UPDATE teams SET manager_id = 106 WHERE team_id = 4;
UPDATE teams SET manager_id = 107 WHERE team_id = 5;
UPDATE teams SET manager_id = 102 WHERE team_id IN (6, 7);  -- Bob manages Frontend and Backend teams
UPDATE teams SET manager_id = 104 WHERE team_id = 8;        -- David manages DevOps team
UPDATE teams SET manager_id = 103 WHERE team_id IN (9, 10); -- Charlie manages Digital Marketing and Content Creation teams

INSERT INTO application (application_id, reason, description, created_on, last_updated_on, status, staff_id, approver_id, recurring, recurrence_type, end_date)
VALUES
    (201, 'WFH Request', 'Requesting to work from home for two weeks due to home renovation.', '2023-07-01 08:00:00', '2023-07-02 10:00:00', 'pending', 101, 100, FALSE, NULL, NULL),
    (202, 'Relocation', 'Requesting to relocate to the New York office for 3 months.', '2023-07-05 09:00:00', '2023-07-06 11:00:00', 'pending', 101, 102, FALSE, NULL, NULL),
    (203, 'Flexible Hours', 'Requesting flexible working hours for childcare reasons.', '2023-07-10 14:00:00', '2023-07-11 09:00:00', 'pending', 103, 100, TRUE, 'DAILY', '2023-08-10'),
    (204, 'Remote Work', 'Requesting to work remotely from Bali for 1 month.', '2023-07-15 11:00:00', '2023-07-16 13:00:00', 'rejected', 106, 100, FALSE, NULL, NULL),
    (205, 'Office Change', 'Requesting to move to a quieter area in the office.', '2023-07-20 10:00:00', '2023-07-20 15:00:00', 'pending', 100, 103, FALSE, NULL, NULL)
ON CONFLICT (application_id) DO NOTHING;

INSERT INTO event (event_id, requested_date, location, application_id)
VALUES
    (401, '2023-07-10', 'wfh', 201),  -- Alice working from home
    (402, '2023-07-12', 'wfh', 201),  -- Alice working from home
    (403, '2023-08-01', 'wfo', 202),  -- Alice's relocation pending
    (404, '2023-07-15', 'wfo', 203),  -- Charlie's flexible hours
    (405, '2023-07-16', 'wfo', 203),  -- Charlie's flexible hours
    (406, '2023-08-05', 'wfh', 204),  -- Frank's rejected remote work
    (407, '2023-07-25', 'wfo', 205)   -- John's office change pending
ON CONFLICT (event_id) DO NOTHING;