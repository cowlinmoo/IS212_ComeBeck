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
  application_state: string;
  events: Event[];
}

export interface Event {
  event_id: number;
  requested_date: string;
  location: string;
  application_hour: string;
}

export default function Component() {
  const { token, userId, pageLoading } = useAuth();
  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    if (userId) {
      const fetchData = async () => {
        try {
          console.log("Fetching staff application...");
          const data = await GetApplicationOfStaff(Number(userId), String(token));
          setApplications(data);
        } catch (error) {
          console.error("Failed to fetch staff application:", error);
        }
      };
      fetchData();
    }
  }, [userId, token]);

  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header />

        {/* Page Content */}
        {pageLoading || (!pageLoading && token === undefined) ? (
          <div className='flex flex-col items-center justify-center h-full w-full'>
            {/* Spinner */}
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
            <p className="text-gray-600">Loading approvals page...</p>
          </div>
        ) : (
          <Approvals data={applications} />
        )}
      </div>
    </div>
  );
}