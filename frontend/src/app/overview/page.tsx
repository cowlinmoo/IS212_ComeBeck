'use client';

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

export default function Page() {
  const { token, userId, pageLoading } = useAuth();

  return (
    <div className="flex h-screen text-black bg-gray-100 animate-fadeIn">
      {/* Sidebar always visible */}
      <SideBar />
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header always visible */}
        <Header />
        
        {/* Conditionally render Page Content based on loading state */}
        <div className="flex-1 overflow-y-auto">
          {pageLoading || !token || userId === undefined ? (
            <div className="flex flex-col items-center justify-center h-full w-full">
              {/* Spinner */}
              <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
              <p className="text-gray-600">Loading department schedule page...</p>
            </div>
          ) : (
            <OverviewSchedule token={token} userId={Number(userId)} />
          )}
        </div>
      </div>
    </div>
  );
}
