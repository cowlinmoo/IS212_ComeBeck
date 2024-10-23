const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;

// Get all accepted applications
export async function GetAcceptedApplications(token: string){
  try {
    const response = await fetch(`${URL}/status/approved`, {
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

// Withdraw an application event
export async function WithdrawApplicationEvent(token: string, applicationId: number, eventId: number, userId: number){
  try {
    const content = {
      "status": "withdrawn",
      "editor_id": userId,
      "withdraw_reason": "Personal reasons"
    };
    const response = await fetch(`${URL}/withdraw/${applicationId}/${eventId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(content),
    });
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.log(error);
  }
}