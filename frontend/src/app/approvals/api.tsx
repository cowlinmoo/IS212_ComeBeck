
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;

export const GetApplicationOfStaff = async (staff_id: number, token: string) => {
    
    try {
      const response = await fetch(`${URL}/staff/${staff_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
      });
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.log(error);
    }
}
