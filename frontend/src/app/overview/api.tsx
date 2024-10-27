const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;
const DEPARTMENT_URL = `${BASE_URL}/department`;

export type EmployeeLocation = {
  employee_fname: string;
  employee_lname: string;
  application_hour: string;
  location: "wfo" | "wfh" | "Home";
  position: string;
  date: string;
  role: number;
  team_id: number;
  employee_id: number;
};

export interface DepartmentSchema {
  department_id: number;
  name: string;
  description: string;
  director_id: number;
  director: {
    staff_id: number;
    staff_fname: string;
    staff_lname: string;
    position: string;
    role: number;
    team_id: number;
    country: string;
    email: string;
  };
  teams: Array<{
    team_id: number;
    name: string;
    description: string;
    department: {
      department_id: number;
      name: string;
    };
    manager: {
      staff_id: number;
      staff_fname: string;
      staff_lname: string;
      position: string;
      role: number;
      team_id: number;
      country: string;
      email: string;
    };
    parent_team: {
      team_id: number;
      name: string;
      description: string;
    } | null;
    child_teams: Array<{
      team_id: number;
      name: string;
      description: string;
    }> | null;
    members: Array<{
      staff_id: number;
      staff_fname: string;
      staff_lname: string;
      position: string;
      role: number;
      team_id: number;
      country: string;
      email: string;
    }>;
  }>;
}

// Fetch all departments
export const getAllDepartments = async (token: string): Promise<DepartmentSchema[]> => {
  try {
    console.log("Fetching all departments");
    const response = await fetch(`${DEPARTMENT_URL}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Failed to fetch departments');
    console.log("Departments fetched successfully");
    return await response.json() as DepartmentSchema[];
  } catch (error) {
    console.error("Error fetching departments:", error);
    throw new Error(error instanceof Error ? error.message : 'An unknown error occurred');
  }
};

// Fetch approved staff location and directly set all entries to "wfh"
export const getApprovedStaffLocation = async (
  token: string,
  userId: number
): Promise<EmployeeLocation[]> => {
  try {
    console.log("Fetching approved staff location for user:", userId);
    const response = await fetch(`${URL}/location/${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Failed to fetch staff location');

    const data = await response.json() as EmployeeLocation[];
    console.log("Data received for WFH staff:", data);

    // Set all entries as WFH without checking the `location` field
    return data.map((employee) => ({
      ...employee,
      location: "wfh", // Directly set as "wfh" for all entries
      application_hour: employee.application_hour || "fullday"
    }));
  } catch (error) {
    console.error("Error fetching staff location:", error);
    throw new Error(error instanceof Error ? error.message : 'An unknown error occurred');
  }
};
