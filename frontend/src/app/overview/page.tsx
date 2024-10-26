"use client"

import { Header } from "@/components/core/header/Header";
import useAuth from "@/lib/auth";
import OverviewSchedule from "@/components/schedule/overviewSchedule/OverviewSchedule";
import SideBar from "@/components/core/sidebar/SideBar";
import { useEffect, useState } from "react";
import { GetTeam, GetTeamID } from "./api";

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
  child_teams: Array<ChildTeam>;
  members: Array<{
      staff_id: number;
      staff_fname: string;
      staff_lname: string;
  }>;
}
export interface ChildTeam {
  team_id: number;
  name: string;
  description: string;
}

export default function Component() {

  const { token, userId, pageLoading } = useAuth();

  const [team, setTeam] = useState<Team>();

  useEffect(() => {
    if (userId) {
      try {
        console.log('Fetching team...');
        const fetchData = async () => {
          const TeamID = await GetTeamID(String(token), Number(userId));
          const data = await GetTeam(String(token), TeamID);
          setTeam(data);
          console.log(data);
        };
        fetchData();
      } catch (error) {
        console.error('Failed to fetch team:', error);
      }
    }
  }, [userId, token]);

  if (pageLoading || (!pageLoading && token === undefined)) {
    return <div className='flex items-center justify-center h-screen w-screen'>Loading...</div>;
  }



  
  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header/>
        
        {/* Page Content */}
        <OverviewSchedule teamData={team}/>
      </div>
    </div>
  )
}