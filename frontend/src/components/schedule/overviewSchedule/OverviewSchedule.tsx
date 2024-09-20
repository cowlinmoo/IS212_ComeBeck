"use client";
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Calendar } from "@/components/ui/calendar"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'
import { Home, Briefcase, CalendarIcon } from "lucide-react"
import { format } from "date-fns"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

// Mock data for departments and staff
const departments = [
  { id: 1, name: "Engineering" },
  { id: 2, name: "Marketing" },
  { id: 3, name: "Sales" },
  { id: 4, name: "Human Resources" },
]

const generateStaffSchedule = (date: Date) => {
  // This is a mock function that generates random staff schedules for demonstration
  // In a real application, this would fetch data from an API based on the selected date
  console.log(date)
  return [
    { id: 1, name: "Alice Johnson", avatar: "/placeholder.svg?height=40&width=40", department: 1, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 2, name: "Bob Smith", avatar: "/placeholder.svg?height=40&width=40", department: 1, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 3, name: "Charlie Brown", avatar: "/placeholder.svg?height=40&width=40", department: 2, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 4, name: "Diana Prince", avatar: "/placeholder.svg?height=40&width=40", department: 2, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 5, name: "Ethan Hunt", avatar: "/placeholder.svg?height=40&width=40", department: 3, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 6, name: "Fiona Apple", avatar: "/placeholder.svg?height=40&width=40", department: 3, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 7, name: "George Clooney", avatar: "/placeholder.svg?height=40&width=40", department: 4, location: Math.random() > 0.5 ? "office" : "home" },
    { id: 8, name: "Hannah Montana", avatar: "/placeholder.svg?height=40&width=40", department: 4, location: Math.random() > 0.5 ? "office" : "home" },
  ]
}

export default function ScheduleOverview() {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date())
  const [selectedDepartment, setSelectedDepartment] = useState<string | undefined>(undefined)

  const staffMembers = generateStaffSchedule(selectedDate || new Date())

  const filteredStaff = selectedDepartment
    ? staffMembers.filter(staff => staff.department.toString() === selectedDepartment)
    : staffMembers

  const departmentSummary = departments.map(dept => {
    const deptStaff = staffMembers.filter(staff => staff.department === dept.id)
    const inOffice = deptStaff.filter(staff => staff.location === "office").length
    const atHome = deptStaff.filter(staff => staff.location === "home").length
    return { ...dept, inOffice, atHome, total: deptStaff.length }
  })

  const overallSummary = departmentSummary.reduce(
    (acc, dept) => ({
      inOffice: acc.inOffice + dept.inOffice,
      atHome: acc.atHome + dept.atHome,
      total: acc.total + dept.total,
    }),
    { inOffice: 0, atHome: 0, total: 0 }
  )

  const pieChartData = [
    { name: 'In Office', value: overallSummary.inOffice, color: '#3b82f6' },
    { name: 'At Home', value: overallSummary.atHome, color: '#10b981' },
  ]

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Schedule Overview</CardTitle>
          <CardDescription>View overall and team schedules for all departments.</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="overall">
            <TabsList>
              <TabsTrigger value="overall">Overall View</TabsTrigger>
              <TabsTrigger value="department">Department View</TabsTrigger>
            </TabsList>
            <TabsContent value="overall">
              <div className="mb-4">
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant={"outline"}
                      className={`w-[280px] justify-start text-left font-normal ${
                        !selectedDate && "text-muted-foreground"
                      }`}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {selectedDate ? format(selectedDate, "PPP") : <span>Pick a date</span>}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={selectedDate}
                      onSelect={setSelectedDate}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              </div>
              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Overall Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-[300px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={pieChartData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {pieChartData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Legend />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="mt-4 text-center">
                      <p>Total Staff: {overallSummary.total}</p>
                      <p>In Office: {overallSummary.inOffice}</p>
                      <p>At Home: {overallSummary.atHome}</p>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Department Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Department</TableHead>
                          <TableHead>In Office</TableHead>
                          <TableHead>At Home</TableHead>
                          <TableHead>Total</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {departmentSummary.map((dept) => (
                          <TableRow key={dept.id}>
                            <TableCell>{dept.name}</TableCell>
                            <TableCell>{dept.inOffice}</TableCell>
                            <TableCell>{dept.atHome}</TableCell>
                            <TableCell>{dept.total}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
            <TabsContent value="department">
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <Select onValueChange={setSelectedDepartment}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder="Select Department" />
                    </SelectTrigger>
                    <SelectContent>
                      {departments.map((dept) => (
                        <SelectItem key={dept.id} value={dept.id.toString()}>
                          {dept.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant={"outline"}
                        className={`w-[280px] justify-start text-left font-normal ${
                          !selectedDate && "text-muted-foreground"
                        }`}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {selectedDate ? format(selectedDate, "PPP") : <span>Pick a date</span>}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar
                        mode="single"
                        selected={selectedDate}
                        onSelect={setSelectedDate}
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                </div>
                <Card>
                  <CardHeader>
                    <CardTitle>Staff Schedule</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Name</TableHead>
                          <TableHead>Department</TableHead>
                          <TableHead>Location</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {filteredStaff.map((staff) => (
                          <TableRow key={staff.id}>
                            <TableCell className="flex items-center space-x-2">
                              <Avatar>
                                <AvatarImage src={staff.avatar} alt={staff.name} />
                                <AvatarFallback>{staff.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                              </Avatar>
                              <span>{staff.name}</span>
                            </TableCell>
                            <TableCell>{departments.find(d => d.id === staff.department)?.name}</TableCell>
                            <TableCell>
                              <Badge variant={staff.location === 'office' ? 'default' : 'secondary'}>
                                {staff.location === 'office' ? <Briefcase className="h-4 w-4 mr-1" /> : <Home className="h-4 w-4 mr-1" />}
                                {staff.location === 'office' ? 'Office' : 'Home'}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}