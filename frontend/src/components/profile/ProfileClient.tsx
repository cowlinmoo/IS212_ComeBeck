"use client"

import { useEffect, useState } from "react"
import useAuth from "@/lib/auth"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { getMyEmployee } from "@/app/profile/api"
import { Employee } from "@/app/profile/api"
import { Briefcase, Users, Building, Mail, MapPin, UserCircle } from "lucide-react"

export default function ProfileClient() {
  const { token, userId } = useAuth()
  const [employee, setEmployee] = useState<Employee | null>(null)

  useEffect(() => {
    const fetchEmployeeData = async () => {
      if (token && userId) {
        const employeeData = await getMyEmployee(token, Number(userId))
        setEmployee(employeeData)
      }
    }
    fetchEmployeeData()
  }, [token, userId])

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Profile</h1>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-2">
          {/* Personal Information Card */}
          <Card>
            <CardHeader>
              <CardTitle>Personal Information</CardTitle>
              <CardDescription>Your photo and personal details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center space-x-4">
                <Avatar className="w-20 h-20">
                  <AvatarFallback>{employee ? employee.staff_fname.charAt(0) + employee.staff_lname.charAt(0) : "JD"}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-semibold text-lg">{`${employee?.staff_fname} ${employee?.staff_lname}`}</p>
                  <p className="text-sm text-gray-500">{employee?.position}</p>
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email" className="flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <span>Email</span>
                </Label>
                <Input id="email" type="email" value={employee?.email} readOnly />
              </div>
              <div className="space-y-2">
                <Label htmlFor="position" className="flex items-center space-x-2">
                  <Briefcase className="h-4 w-4" />
                  <span>Position</span>
                </Label>
                <Input id="position" value={employee?.position} readOnly />
              </div>
              <div className="space-y-2">
                <Label htmlFor="country" className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4" />
                  <span>Country</span>
                </Label>
                <Input id="country" value={employee?.country} readOnly />
              </div>
            </CardContent>
          </Card>

          {/* Organizational Information Card */}
          <Card>
            <CardHeader>
              <CardTitle>Organizational Information</CardTitle>
              <CardDescription>Details about departments and teams</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="department" className="flex items-center space-x-2">
                  <Building className="h-4 w-4" />
                  <span>Department</span>
                </Label>
                <Input id="department" value={employee?.department?.name || "N/A"} readOnly />
              </div>
              <div className="space-y-2">
                <Label htmlFor="team" className="flex items-center space-x-2">
                  <Users className="h-4 w-4" />
                  <span>Team</span>
                </Label>
                <Input id="team" value={employee?.team?.name || "N/A"} readOnly />
              </div>
              <div className="space-y-2">
                <Label htmlFor="managed_team" className="flex items-center space-x-2">
                  <UserCircle className="h-4 w-4" />
                  <span>Managed Team</span>
                </Label>
                <Input id="managed_team" value={employee?.managed_team?.name || "N/A"} readOnly />
              </div>
              <div className="space-y-2">
                <Label htmlFor="directed_department" className="flex items-center space-x-2">
                  <Building className="h-4 w-4" />
                  <span>Directed Department</span>
                </Label>
                <Input id="directed_department" value={employee?.directed_department?.name || "N/A"} readOnly />
              </div>
            </CardContent>
          </Card>

          {/* Direct Reports Card - spans two columns */}
          <Card className="md:col-span-2 lg:col-span-2">
            <CardHeader>
              <CardTitle>Direct Reports</CardTitle>
              <CardDescription>List of employees reporting to you</CardDescription>
            </CardHeader>
            <CardContent className="max-h-[400px] overflow-y-auto space-y-4">
              {employee?.direct_reports && employee.direct_reports.length > 0 ? (
                employee.direct_reports.map((report) => (
                  <div key={report.staff_id} className="border p-4 rounded-lg shadow-sm">
                    <div className="flex items-center space-x-4 mb-2">
                      <Avatar>
                        <AvatarFallback>{report.staff_fname.charAt(0) + report.staff_lname.charAt(0)}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-semibold">{report.staff_fname} {report.staff_lname}</p>
                        <p className="text-sm text-gray-500">{report.position}</p>
                      </div>
                    </div>
                    <div className="text-sm space-y-1">
                      <p className="flex items-center space-x-2">
                        <Mail className="h-4 w-4 text-gray-400" />
                        <span>{report.email}</span>
                      </p>
                      <p className="flex items-center space-x-2">
                        <Building className="h-4 w-4 text-gray-400" />
                        <span>Department ID: {report.department_id}</span>
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 italic">No direct reports</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
