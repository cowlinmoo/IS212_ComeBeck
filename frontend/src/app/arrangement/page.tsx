'use client';

import useAuth from "@/lib/auth";
import { Header } from "@/components/core/header/Header";
import Applications from "@/components/arrangement/applications/Applications";
import Apply_Withdrawal from "@/components/arrangement/applications/Apply_Withdrawal";
import Apply_Change from "@/components/arrangement/applications/Apply_Change";
import SideBar from "@/components/core/sidebar/SideBar";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState} from "react";


export default function Component() {
  const [activeTab, setActiveTab] = useState("apply");
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
        <div className="container mx-auto p-4">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full h-full grid-cols-3 bg-white text-black ">
          <TabsTrigger value="apply">Apply for arrangement</TabsTrigger>
          <TabsTrigger value="change">Change arrangement</TabsTrigger>
          <TabsTrigger value="withdraw">Withdraw arrangement</TabsTrigger>
        </TabsList>
        <Applications staffId = {userId} token= {token}/>
        <Apply_Change staffId = {userId} token= {token}/>
        <Apply_Withdrawal staffId = {userId} token= {token}/>
        </Tabs>
        </div>
      </div>
      </div>
  );
}
