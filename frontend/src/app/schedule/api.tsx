const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;
const TEAM_URL = `${BASE_URL}/team`
const EMPLOYEE_URL = `${BASE_URL}/employee`

export type EmployeeLocation = {
    employee_fname: string;
    employee_lname: string;
    application_hour: string;
    location: "wfo" | "wfh";
    position: string;
    date: string
};


export const getApprovedStaffLocation = async (token: string, id: number): Promise<EmployeeLocation[]> => {
    try {
        const response = await fetch(`${URL}/location/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        const data = await response.json();
        return data as EmployeeLocation[];
    } catch (error) {
        if (error instanceof Error) {
            throw new Error(error.message);
        } else {
            throw new Error('An unknown error occurred');
        }
    }
}

export interface Team {
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
    };
    parent_team: {
        team_id: number;
        name: string;
        description: string;
    };
    child_teams: Array<{
        team_id: number;
        name: string;
        description: string;
    }>;
    members: Array<{
        staff_id: number;
        staff_fname: string;
        staff_lname: string;
    }>;
}



export const getMyTeam = async (token: string, teamId: number): Promise<Team> => {
    try {
        const response = await fetch(`${TEAM_URL}/${teamId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        const data = await response.json();
        return data as Team
    } catch (error) {

        if (error instanceof Error) {
            throw new Error(error.message);
        } else {
            throw new Error('An unknown error occurred');
        }
    }
}

export type Employee = {
    staff_id: number;
    staff_fname: string;
    staff_lname: string;
    position: string;
    department_id: number;
    team_id: number;
    country: string;
    email: string;
    reporting_manager: number;
    role: number;
    department: {
        department_id: number;
        name: string;
    };
    team: {
        team_id: number;
        name: string;
        description: string;
    };
    directed_department: {
        department_id: number;
        name: string;
    };
    managed_team: {
        team_id: number;
        name: string;
        description: string;
    };
    direct_reports: Array<{
        staff_id: number;
        staff_fname: string;
        staff_lname: string;
        position: string;
        department_id: number;
        team_id: number;
        country: string;
        email: string;
        reporting_manager: number;
        role: number;
    }>;
};



export const getMyEmployee = async (token: string, staffId: number): Promise<Employee> => {
    try {
        const response = await fetch(`${EMPLOYEE_URL}/${staffId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        const data = await response.json();
        return data as Employee;
    } catch (error) {
        if (error instanceof Error) {
            throw new Error(error.message);
        } else {
            throw new Error('An unknown error occurred');
        }
    }
}