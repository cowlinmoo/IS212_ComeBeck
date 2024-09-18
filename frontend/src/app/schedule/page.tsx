'use client';

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Bell, Search, Home, FileText, Settings } from "lucide-react"
import Schedule from "@/components/schedule/page";

const tabs = [
  { name: "Home", icon: Home },
  { name: "Schedule", icon: FileText },
  { name: "Arrangement Management", icon: Settings },
]

export default function Component() {
  const [activeTab, setActiveTab] = useState("Schedule")

  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <nav className="bg-white w-64 h-screen flex flex-col border-r">
        <div className="flex items-center justify-center h-16 border-b">
          <h2 className="text-xl font-bold">ComeBeck</h2>
        </div>
        <div className="flex-1 overflow-y-auto">
          {tabs.map((tab) => (
            <Button
              key={tab.name}
              variant={activeTab === tab.name ? "default" : "ghost"}
              className="w-full justify-start rounded-none h-12"
              onClick={() => setActiveTab(tab.name)}
            >
              <tab.icon className="mr-2 h-5 w-5" />
              {tab.name}
            </Button>
          ))}
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm z-10 h-16 flex items-center px-6">
          <div className="flex-1 flex items-center">
            <Input
              type="search"
              placeholder="Search..."
              className="w-64 mr-4"
            />
            <Button variant="ghost" size="icon">
              <Search className="h-5 w-5" />
            </Button>
          </div>
          <div className="flex items-center">
            <Button variant="ghost" size="icon" className="mr-2">
              <Bell className="h-5 w-5" />
            </Button>
            <Avatar>
              <AvatarImage src="/placeholder.svg?height=32&width=32" alt="User" />
              <AvatarFallback>U</AvatarFallback>
            </Avatar>
          </div>
        </header>

        {/* Page Content */}
        <Schedule />
      </div>
    </div>
  )
}