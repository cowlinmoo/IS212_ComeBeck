const URL = 'http://localhost:8080/api/application';
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGdtYWlsLmNvbSIsInJvbGUiOjIsImlkIjoxMDIsImV4cCI6MTcyODIzNDYzNH0.Rcjkj4oEkJjN5LvfGgpYUn_fXkZn1IJ8Rs04h6o4w5A';

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
