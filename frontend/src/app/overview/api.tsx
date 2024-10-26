const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const EMPLOYEE_URl = `${BASE_URL}/employee`;
const TEAM_URL = `${BASE_URL}/team`;

export const GetTeamID = async (token:string,userId:number) => {
    try {
        const response = await fetch(`${EMPLOYEE_URl}/${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        const data = await response.json();
        console.log(data.team.team_id);
        return data.team.team_id;
    } catch (error) {
        console.log(error);
    }
}

export const GetTeam = async (token:string,team_id:number) => {
    try {
        const response = await fetch(`${TEAM_URL}/${team_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });
        const data = await response.json();
        // console.log(data);
        return data;
    } catch (error) {
        console.log(error);
    }
}
        
