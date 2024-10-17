'use client';

import useAuth from "@/lib/auth";
import { Header } from "@/components/core/header/Header";
import Approvals from "@/components/arrangement/approvals/Approvals";
import SideBar from "@/components/core/sidebar/SideBar";
import { GetApplicationOfStaff } from "./api";
import { useEffect, useState } from "react";

export interface Application {
  application_id: number;
  reason: string;
  description: string;
  created_on: string;
  last_updated_on: string;
  status: string;
  staff_id: number;
  approver_id: number;
  recurring: boolean;
  events: Event[];
}

export interface Event {
  event_id: number;
  requested_date: string;
  location: string;
}

export default function Component() {

  const { token, userId, pageLoading } = useAuth();

  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    if (userId) {
      try {
        console.log("Fetching staff application...");
        const fetchData = async () => {
          const data = await GetApplicationOfStaff(Number(userId), String(token));
          setApplications(data);
        };
        fetchData();
      } catch (error) {
        console.error("Failed to fetch staff application:", error);
      }
    }
  }, [userId, token]);

  if (pageLoading || (!pageLoading && token === undefined)) {
    return <div className='flex items-center justify-center h-screen w-screen'>Loading...</div>;
  }

  console.log(applications);


  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header/>
        {/* Page Content */}
        <Approvals data={applications} />
      </div>
    </div>
  )
}