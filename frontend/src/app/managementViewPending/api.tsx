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

export const processApplicationStatus = async (token: string,userId: number, applicationId: number, status: 'approved' | 'rejected', reason: string) => {
    try {
        const content = { 
                        status: status,
                        approver_id: String(userId),
                        application_id: String(applicationId),
                        outcome_reason: reason
                    };
        console.log(content);
      const response = await fetch(`${URL}/process/${applicationId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(content)
      });
      if (!response.ok) {
        throw new Error('Failed to update application status');
      }
      return await response.json();
    } catch (error) {
      console.error('Error updating application status:', error);
      throw error;
    }
  }