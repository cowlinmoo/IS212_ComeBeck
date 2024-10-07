const URL = 'http://localhost:8080/api/application';


export const GetPendingApplications = async (token:string,userId:number) => {
    try {
        const response = await fetch(`${URL}/approver/${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
    });
        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.log(error);
    }
}