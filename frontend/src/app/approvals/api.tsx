const URL = 'http://localhost:8080/api/application';
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb2xpbm1vazEwMDBAZ21haWwuY29tIiwicm9sZSI6MywiaWQiOjEwMCwiZXhwIjoxNzI4MTE5OTQxfQ.JNLJHD7DOm6d9pZ2JKcmRj45hIQfV0dgAG5qa2Vfavw';

export const GetApplicationOfStaff = async (staff_id: number) => {
    
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
