'use client';

import { useEffect, useState } from "react"
import { getToken, getUserId } from "@/lib/cookie"
import StaffSchedule from "@/components/schedule/staffSchedule/StaffSchedule";
import SideBar from "@/components/core/sidebar/SideBar";
import { Header } from "@/components/core/header/Header";

export default function Component() {
  const [token, setToken] = useState<string | undefined>(undefined);
  const [userId, setUserId] = useState<string | undefined>(undefined);

  useEffect(() => {
    const fetchToken = async () => {
      const token = await getToken();
      const userId = await getUserId();
      setToken(token);
      setUserId(userId);
    };

    fetchToken();
  }, []);

  console.log("Token: ", token);
  console.log("User ID: ", userId);

  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar/>
      
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header/>

        {/* Page Content */}
        <StaffSchedule />
      </div>
    </div>
  )
}