"use client"

import { Header } from "@/components/core/header/Header";
import useAuth from "@/lib/auth";
import OverviewSchedule from "@/components/schedule/overviewSchedule/OverviewSchedule";
import SideBar from "@/components/core/sidebar/SideBar";

export default function Component() {

  const { token, userId, pageLoading } = useAuth();

  if (pageLoading || (!pageLoading && token === undefined)) {
    return <div className='flex items-center justify-center h-screen w-screen'>Loading...</div>;
  }

  console.log('Token:', token);
  console.log('User ID:', userId);

  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header/>
        
        {/* Page Content */}
        <OverviewSchedule />
      </div>
    </div>
  )
}