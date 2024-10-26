'use client';

import useAuth from "@/lib/auth";
import StaffSchedule from "@/components/schedule/staffSchedule/StaffSchedule";
import SideBar from "@/components/core/sidebar/SideBar";
import { Header } from "@/components/core/header/Header";
import { useEffect, useState } from "react";
import { EmployeeLocation, getApprovedStaffLocation } from "./api";


export default function Component() {
  const { token, userId, pageLoading, } = useAuth();
  const [staffLocation, setStaffLocation] = useState<EmployeeLocation[]>([])
  useEffect(() => {
    if (token && userId) {
      const getLocation = async () => {

        const response: EmployeeLocation[] = await getApprovedStaffLocation(token as string, Number(userId))
        setStaffLocation(response)

      }
      getLocation()
    }
  }, [token, userId])


  return (
    <div className="flex h-screen text-black bg-gray-100 ">
      {/* Left Navbar */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-y-scroll">
        {/* Header */}
        <Header />

        {/* Page Content */}
        <>
          {
            (!pageLoading) ?
              (<StaffSchedule teamMembers={staffLocation} />) :
              (<div className='flex items-center justify-center h-screen w-screen'>Loading...</div>)}
        </>
      </div>
    </div>
  )
}

