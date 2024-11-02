const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const EMPLOYEE_URL = `${BASE_URL}/employee`;

// Function to fetch a specific employee's data
export const getMyEmployee = async (token: string, staffId: number): Promise<Employee> => {
  try {
    const response = await fetch(`${EMPLOYEE_URL}/${staffId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch employee data.");
    }

    const data = await response.json();
    return data as Employee;
  } catch (error) {
    console.error("Error fetching employee data:", error);
    throw error instanceof Error ? error : new Error("Unknown error occurred.");
  }
};

export interface BaseDepartmentInfo {
  department_id: number;
  name: string;
}

export interface BaseTeamInfo {
  team_id: number;
  name: string;
  description: string;
}

export interface Employee {
  staff_id: number;
  staff_fname: string;
  staff_lname: string;
  position: string;
  role: number;
  team_id: number;
  country: string;
  email: string;
  department_id: number;
  reporting_manager?: number;
  department: BaseDepartmentInfo;
  team: BaseTeamInfo;
  directed_department?: BaseDepartmentInfo;
  managed_team?: BaseTeamInfo;
  direct_reports?: Employee[];
}
