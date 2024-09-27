"use client";

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bell } from "lucide-react"
import { useRouter } from "next/navigation";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { clearToken } from '@/lib/cookie';


export const Header = () => {
  const router = useRouter();

  const handleProfileClick = () => {
    // Navigate to the profile page or perform any profile-related actions
    clearToken();
    router.push('/logout');

  };

  const handleLogoutClick = () => {
    // Perform logout logic here
    // For example, clearing user session or token
    // Then redirecting to login page or home page
    clearToken();
    router.push('/login');
  };

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
              <DropdownMenu>
                <DropdownMenuTrigger><AvatarImage src="https://github.com/shadcn.png" /></DropdownMenuTrigger>
                <DropdownMenuContent>
                  {/* {label && (
                    <>
                      <DropdownMenuLabel>{label}</DropdownMenuLabel>
                      <DropdownMenuSeparator />
                    </>
                  )} */}
                  {/* {tabs.map((tab, index) => (
                    <DropdownMenuItem key={index} onClick={handlers[index]}>
                      {tab}
                    </DropdownMenuItem>
                  ))} */}
                  <DropdownMenuItem onClick={handleProfileClick}>
                      Profile
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleLogoutClick}>
                      Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
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
