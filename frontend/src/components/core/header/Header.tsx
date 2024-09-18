"use client";

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bell } from "lucide-react"
// import { useRouter } from "next/navigation";

export const Header = () => {
//   const router = useRouter();

//   const handleProfileClick = () => {
//     // Navigate to the profile page or perform any profile-related actions
//     router.push('/profile');
//   };

//   const handleLogoutClick = () => {
//     // Perform logout logic here
//     // For example, clearing user session or token
//     // Then redirecting to login page or home page
//     router.push('/login');
//   };

  return (
    <div className='flex flex-row px-6 py-3 gap-8 bg-white items-center text-sm w-full grow-0'>
      {/* Search bar */}
      <div className='flex-grow'>
        <input type="text" placeholder="Search..." className='w-full p-3 rounded bg-gray-100' />
      </div>
      
      {/* Notification Bell */}
      <div>
        <button>
          <Bell size={18}/>
        </button>
      </div>

      {/* Profile Section with Menu */}
      <div className='flex flex-row gap-4 items-center'>
        {/* <Menu
          trigger={
            <Avatar>
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
          }
          tabs={["Profile", "Logout"]}
          handlers={[
            handleProfileClick,
            handleLogoutClick
          ]}
        /> */}
        <Avatar>
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <div className='flex flex-col gap-0.5'>
          <div className='font-medium'>
            Daryl Yoon Kaile
          </div>
          <div className='text-sm text-gray-500 text-xs'>
            Employee
          </div>
        </div>
      </div>
    </div>
  );
};
