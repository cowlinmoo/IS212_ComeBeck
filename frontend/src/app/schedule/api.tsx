const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;

export type EmployeeLocation = {
    employee_fname: string;
    employee_lname: string;
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