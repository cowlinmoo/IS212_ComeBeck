"use client";

import Schedule from "@/components/schedule/page";
import SideBar from "@/components/core/sidebar/SideBar";
import { Header } from "@/components/core/header/Header";

export default function Component() {

  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar/>
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header/>

        {/* Page Content */}
        <Schedule />
      </div>
    </div>
  )
}