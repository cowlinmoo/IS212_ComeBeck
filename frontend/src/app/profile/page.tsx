'use client';

import useAuth from "@/lib/auth";
import SideBar from "@/components/core/sidebar/SideBar";
import { Header } from "@/components/core/header/Header";
import ProfileClient from "@/components/profile/ProfileClient";

export default function ProfilePage() {
  const { pageLoading } = useAuth();

  return (
    <div className="flex h-screen bg-gray-100 text-black">
      {/* Sidebar */}
      <SideBar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />

        {/* Conditionally render Profile Content based on loading state */}
        <div className="flex-1 overflow-y-auto">
          {pageLoading ? (
            <div className="flex flex-col items-center justify-center h-full w-full">
              {/* Spinner */}
              <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
              <p className="text-gray-600">Loading Profile Page...</p>
            </div>
          ) : (
            <ProfileClient />
          )}
        </div>
      </div>
    </div>
  );
}
