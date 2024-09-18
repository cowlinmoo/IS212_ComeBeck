'use client';

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Search, Bell, Camera, Home, FileText, Settings } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Textarea } from "@/components/ui/textarea"

const tabs = [
  { name: "Home", icon: Home },
  { name: "Schedule", icon: FileText },
  { name: "Arrangement Management", icon: Settings },
]

export default function Component() {
    const [activeTab, setActiveTab] = useState("Settings")
    const [notifications, setNotifications] = useState(true)

  return (
    <div className="flex h-screen bg-gray-100 text-black">
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
      <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
          <h3 className="text-gray-700 text-3xl font-medium mb-4">Profile</h3>
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>Update your photo and personal details here.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-4">
                  <Avatar className="w-20 h-20">
                    <AvatarImage src="/placeholder.svg?height=80&width=80" alt="User" />
                    <AvatarFallback>JP</AvatarFallback>
                  </Avatar>
                  <Button variant="outline" size="sm">
                    <Camera className="mr-2 h-4 w-4" />
                    Change Photo
                  </Button>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="name">Name</Label>
                  <Input id="name" defaultValue="John Doe" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" defaultValue="john.doe@example.com" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea id="bio" defaultValue="I'm a software developer with a passion for creating intuitive user interfaces." />
                </div>
              </CardContent>
              <CardFooter>
                <Button>Save Changes</Button>
              </CardFooter>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Account Settings</CardTitle>
                <CardDescription>Manage your account settings and set email preferences.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <Label htmlFor="notifications" className="flex items-center space-x-2">
                    <span>Email Notifications</span>
                  </Label>
                  <Switch
                    id="notifications"
                    checked={notifications}
                    onCheckedChange={setNotifications}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="language">Language</Label>
                  <select id="language" className="w-full p-2 border rounded">
                    <option>English</option>
                    <option>Spanish</option>
                    <option>French</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="timezone">Timezone</Label>
                  <select id="timezone" className="w-full p-2 border rounded">
                    <option>Pacific Time (PT)</option>
                    <option>Eastern Time (ET)</option>
                    <option>Coordinated Universal Time (UTC)</option>
                  </select>
                </div>
              </CardContent>
              <CardFooter>
                <Button>Update Settings</Button>
              </CardFooter>
            </Card>
          </div>
        </main>
    </div>
  </div>
  )
}