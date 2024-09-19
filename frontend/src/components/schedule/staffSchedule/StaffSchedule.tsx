import { useState } from "react"
// import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Calendar } from "@/components/ui/calendar"
import { Badge } from "@/components/ui/badge"
import { Home, Briefcase } from "lucide-react"

// Mock data for team members and schedules
const teamMembers = [
  { id: 1, name: "Alice Johnson", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 2, name: "Bob Smith", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 3, name: "Charlie Brown", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 4, name: "Diana Prince", avatar: "/placeholder.svg?height=40&width=40" },
]

const generateSchedule = (startDate: Date, days: number) => {
  const schedule = {}
  for (let i = 0; i < days; i++) {
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    const dateString = date.toISOString().split('T')[0]
    schedule[dateString] = teamMembers.map(member => ({
      ...member,
      location: Math.random() > 0.5 ? 'office' : 'home'
    }))
  }
  return schedule
}

const today = new Date()
const teamSchedule = generateSchedule(today, 30)

export default function StaffSchedule() {
  const [activeTab, setActiveTab] = useState("team")
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(today)

  const formatDate = (date: Date) => {
    return date.toISOString().split('T')[0]
  }

  const getScheduleForDate = (date: Date) => {
    return teamSchedule[formatDate(date)] || []
  }

  return (
    <div className="container mx-auto p-4">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-2 bg-white text-black">
          <TabsTrigger value="team">Team Schedule</TabsTrigger>
          <TabsTrigger value="own">My Schedule</TabsTrigger>
        </TabsList>
        <TabsContent value="team">
          <Card>
            <CardHeader>
              <CardTitle>Team Schedule</CardTitle>
              <CardDescription>View who is in the office and who is working from home in your department.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={setSelectedDate}
                    className="rounded-md border"
                  />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">
                    {selectedDate ? selectedDate.toDateString() : 'Select a date'}
                  </h3>
                  <ul className="space-y-2">
                    {selectedDate && getScheduleForDate(selectedDate).map((member) => (
                      <li key={member.id} className="flex items-center space-x-2">
                        <Avatar>
                          <AvatarImage src={member.avatar} alt={member.name} />
                          <AvatarFallback>{member.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <span>{member.name}</span>
                        <Badge variant={member.location === 'office' ? 'default' : 'secondary'}>
                          {member.location === 'office' ? <Briefcase className="h-4 w-4 mr-1" /> : <Home className="h-4 w-4 mr-1" />}
                          {member.location === 'office' ? 'Office' : 'Home'}
                        </Badge>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="own">
          <Card>
            <CardHeader>
              <CardTitle>My Schedule</CardTitle>
              <CardDescription>View your personal work schedule.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={setSelectedDate}
                    className="rounded-md border"
                  />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">
                    {selectedDate ? selectedDate.toDateString() : 'Select a date'}
                  </h3>
                  {selectedDate && (
                    <div className="space-y-2">
                      <p>Your schedule for this date:</p>
                      <Badge variant={getScheduleForDate(selectedDate)[0]?.location === 'office' ? 'default' : 'secondary'}>
                        {getScheduleForDate(selectedDate)[0]?.location === 'office' ? (
                          <><Briefcase className="h-4 w-4 mr-1" /> Working from Office</>
                        ) : (
                          <><Home className="h-4 w-4 mr-1" /> Working from Home</>
                        )}
                      </Badge>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}