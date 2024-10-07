'use client';

import useAuth from "@/lib/auth";
import { Header } from "@/components/core/header/Header";
import Applications from "@/components/arrangement/applications/Applications";
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
      <div className="flex-1 flex flex-col overflow-scroll">
        {/* Header */}
        <Header />
        {/* Page Content */}
        <Applications staffId = {userId} token= {token}/>
      </div>
      </div>
  );
}
