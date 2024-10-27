'use client';

import useAuth from "@/lib/auth";
import StaffSchedule from "@/components/schedule/staffSchedule/StaffSchedule";
import SideBar from "@/components/core/sidebar/SideBar";
import { Header } from "@/components/core/header/Header";
import { useEffect, useState } from "react";
import { EmployeeLocation, getApprovedStaffLocation } from "./api";

export default function Component() {
  const { token, userId, pageLoading } = useAuth();
  const [staffLocation, setStaffLocation] = useState<EmployeeLocation[]>([]);

  useEffect(() => {
    if (token && userId) {
      const getLocation = async () => {
        const response: EmployeeLocation[] = await getApprovedStaffLocation(token as string, Number(userId));
        setStaffLocation(response);
      };
      getLocation();
    }
  }, [token, userId]);

  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Sidebar always visible */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-y-scroll">
        {/* Header always visible */}
        <Header />

        {/* Conditionally render Page Content based on loading state */}
        <div className="flex-1 overflow-y-auto">
          {pageLoading ? (
            <div className="flex flex-col items-center justify-center h-full w-full">
              {/* Spinner */}
              <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
              <p className="text-gray-600">Loading Schedule Page...</p>
            </div>
          ) : (
            <StaffSchedule teamMembers={staffLocation} />
          )}
        </div>
      </div>
    </div>
  );
}
