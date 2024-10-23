const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;

const temp = [
  {
    "staff": {
      "staff_id": 500000,
      "staff_fname": "Molin",
      "staff_lname": "Cok",
      "position": "Developer",
      "role": 1,
      "team_id": 19,
      "country": "Singapore",
      "email": "colinmok3@gmail.com"
    },
    "application_id": 5,
    "application_state": "new_application",
    "reason": "Work From Home",
    "description": "I want to work from home",
    "created_on": "2024-10-22T07:00:00",
    "last_updated_on": "2024-10-22T08:00:00",
    "staff_id": 500000,
    "status": "approved",
    "approver_id": 300000,
    "recurring": false,
    "events": [
      {
        "event_id": 10,
        "requested_date": "2024-10-23",
        "location": "Home",
        "application_hour": "fullday"
      },
      {
        "event_id": 11,
        "requested_date": "2024-10-24",
        "location": "Home",
        "application_hour": "fullday"
      }
    ]
  },
  {
    "staff": {
      "staff_id": 400000,
      "staff_fname": "Fatti",
      "staff_lname": "Bom Bom",
      "position": "Developer",
      "role": 2,
      "team_id": 19,
      "country": "Singapore",
      "email": "colinmok3@gmail.com"
    },
    "application_id": 3,
    "application_state": "new_application",
    "reason": "Work From Home",
    "description": "I want to work from home",
    "created_on": "2024-10-20T08:00:00",
    "last_updated_on": "2024-10-20T08:00:00",
    "staff_id": 400000,
    "status": "approved",
    "approver_id": 300000,
    "recurring": true,
    "events": [
      {
        "event_id": 5,
        "requested_date": "2024-10-21",
        "location": "Home",
        "application_hour": "am"
      },
      {
        "event_id": 6,
        "requested_date": "2024-10-28",
        "location": "Home",
        "application_hour": "am"
      },
      {
        "event_id": 7,
        "requested_date": "2024-11-04",
        "location": "Home",
        "application_hour": "am"
      }
    ]
  },
  {
    "staff": {
      "staff_id": 400000,
      "staff_fname": "Fatti",
      "staff_lname": "Bom Bom",
      "position": "Developer",
      "role": 2,
      "team_id": 19,
      "country": "Singapore",
      "email": "colinmok3@gmail.com"
    },
    "application_id": 2,
    "application_state": "new_application",
    "reason": "Work From Home",
    "description": "I want to work from home",
    "created_on": "2024-10-19T10:30:00",
    "last_updated_on": "2024-10-19T11:00:00",
    "staff_id": 400000,
    "status": "approved",
    "approver_id": 300000,
    "recurring": false,
    "events": [
      {
        "event_id": 4,
        "requested_date": "2024-10-20",
        "location": "Home",
        "application_hour": "fullday"
      }
    ]
  },
  {
    "staff": {
      "staff_id": 400000,
      "staff_fname": "Fatti",
      "staff_lname": "Bom Bom",
      "position": "Developer",
      "role": 2,
      "team_id": 19,
      "country": "Singapore",
      "email": "colinmok3@gmail.com"
    },
    "application_id": 1,
    "application_state": "new_application",
    "reason": "Work From Home",
    "description": "I want to work from home",
    "created_on": "2024-10-18T09:00:00",
    "last_updated_on": "2024-10-18T09:00:00",
    "staff_id": 400000,
    "status": "approved",
    "approver_id": 300000,
    "recurring": false,
    "events": [
      {
        "event_id": 1,
        "requested_date": "2024-11-01",
        "location": "Home",
        "application_hour": "fullday"
      },
      {
        "event_id": 2,
        "requested_date": "2024-11-02",
        "location": "Home",
        "application_hour": "fullday"
      },
      {
        "event_id": 3,
        "requested_date": "2024-11-03",
        "location": "Home",
        "application_hour": "fullday"
      }
    ]
  }
]

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