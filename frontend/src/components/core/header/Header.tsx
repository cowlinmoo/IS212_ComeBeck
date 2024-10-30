"use client";

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useRouter } from "next/navigation";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { clearToken } from '@/lib/cookie';
import useAuth from '@/lib/auth';


export const Header = () => {
  const router = useRouter();
  const { user } = useAuth()

  const handleLogoutClick = () => {
    // Perform logout logic here
    // For example, clearing user session or token
    // Then redirecting to login page or home page
    clearToken();
    router.push('/login');
  };

  return (
    <div className='flex flex-row px-6 py-3 gap-8 bg-white items-center text-sm w-full grow-0 justify-end'>

      {/* Profile Section with Menu */}
      <div className='flex flex-row gap-4 items-center'>
        <Avatar>
          <DropdownMenu>
            <DropdownMenuTrigger><AvatarImage src="https://github.com/shadcn.png" /></DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={handleLogoutClick}>
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <div className='flex flex-col gap-0.5'>
          <div className='font-medium'>
            {user?.staff_fname} {user?.staff_lname}
          </div>
          <div className='text-sm text-gray-500 text-xs'>
            {user?.position}
          </div>
        </div>
      </div>
    </div>
  );
};
