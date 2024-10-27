/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { DepartmentSchema, EmployeeLocation } from "@/app/overview/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { Home, Briefcase, CalendarIcon } from "lucide-react";
import { format } from "date-fns";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";

interface OverviewScheduleComponentProps {
  departments: DepartmentSchema[];
  staffMembers: EmployeeLocation[];
  selectedDate: Date | undefined;
  setSelectedDate: React.Dispatch<React.SetStateAction<Date | undefined>>;
  selectedDepartment: string | undefined;
  setSelectedDepartment: React.Dispatch<React.SetStateAction<string | undefined>>;
  selectedPieChartDepartment: string | undefined;
  setSelectedPieChartDepartment: React.Dispatch<React.SetStateAction<string | undefined>>;
}

export default function OverviewScheduleComponent({
  departments,
  staffMembers,
  selectedDate,
  setSelectedDate,
  selectedDepartment,
  setSelectedDepartment,
  selectedPieChartDepartment,
  setSelectedPieChartDepartment,
}: OverviewScheduleComponentProps) {
  // Mapping teams to departments
  const teamDepartmentMap: { [teamId: number]: string } = {};
  departments.forEach(department => {
    department.teams.forEach(team => {
      teamDepartmentMap[team.team_id] = department.name;
    });
  });

  // Filtered staff for Staff Schedule based on selectedDepartment
  const filteredStaff = selectedDepartment && selectedDepartment !== "all"
    ? staffMembers.filter(staff =>
        departments
          .find(dept => dept.department_id.toString() === selectedDepartment)
          ?.teams.some(team => team.team_id === staff.team_id)
      )
    : staffMembers;

  // Filtered staff for Pie Chart based on selectedPieChartDepartment
  const pieChartStaff = selectedPieChartDepartment && selectedPieChartDepartment !== "all"
    ? staffMembers.filter(staff =>
        departments
          .find(dept => dept.department_id.toString() === selectedPieChartDepartment)
          ?.teams.some(team => team.team_id === staff.team_id)
      )
    : staffMembers;

  // Calculate pie chart data
  const inOfficeCount = pieChartStaff.filter(staff => staff.location === "wfo").length;
  const atHomeCount = pieChartStaff.filter(staff => staff.location === "wfh").length;
  const totalStaff = inOfficeCount + atHomeCount;
  const pieChartData = [
    { name: "In Office", value: inOfficeCount, color: "#3b82f6" },
    { name: "At Home", value: atHomeCount, color: "#10b981" },
  ];

  const departmentSummary = departments.map(dept => {
    const deptStaff = staffMembers.filter(staff =>
      dept.teams.some(team => team.team_id === staff.team_id)
    );
    const inOffice = deptStaff.filter(staff => staff.location === "wfo").length;
    const atHome = deptStaff.filter(staff => staff.location === "wfh").length;
    const total = deptStaff.length;
    return {
      name: dept.name,
      inOffice,
      atHome,
      total,
      atHomePercentage: total > 0 ? ((atHome / total) * 100).toFixed(2) : "0.00"
    };
  });

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Department Schedule Overview</CardTitle>
          <CardDescription>View overall schedules for all departments.</CardDescription>
        </CardHeader>
        <CardContent>
          {/* Date Selector */}
          <div className="mb-4">
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className={`w-[280px] justify-start ${!selectedDate && "text-muted-foreground"}`}>
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {selectedDate ? format(selectedDate, "PPP") : "Pick a date"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0">
                <Calendar
                  mode="single"
                  selected={selectedDate}
                  onSelect={(date) => setSelectedDate(date ? new Date(date) : new Date())}
                />
              </PopoverContent>
            </Popover>
          </div>

          <div className="grid gap-4 md:grid-cols-2 mt-6">
            {/* Pie Chart with Filter */}
            <Card>
              <CardHeader>
                <div className="flex items-center space-x-4">
                  <CardTitle>
                    {selectedPieChartDepartment && selectedPieChartDepartment !== "all" ? "Filtered Department Summary" : "Overall Summary"}
                  </CardTitle>

                  <Select onValueChange={(value) => setSelectedPieChartDepartment(value || "all")}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder="Filter By Dept" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Departments</SelectItem>
                      {departments.map(dept => (
                        <SelectItem key={dept.department_id} value={dept.department_id.toString()}>
                          {dept.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieChartData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value: any) => `${((Number(value) / totalStaff) * 100).toFixed(2)}%`} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
                <div className="text-center mt-4">
                  <p>Total Staff: {totalStaff}</p>
                  <p>In Office: {inOfficeCount}</p>
                  <p>At Home: {atHomeCount}</p>
                </div>
              </CardContent>
            </Card>

            {/* Department Summary Table */}
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
                      <TableHead>% At Home</TableHead> {/* New Column */}
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {departmentSummary.map(dept => (
                      <TableRow key={dept.name}>
                        <TableCell>{dept.name}</TableCell>
                        <TableCell>{dept.inOffice}</TableCell>
                        <TableCell>{dept.atHome}</TableCell>
                        <TableCell>{dept.total}</TableCell>
                        <TableCell>{dept.atHomePercentage}%</TableCell> {/* Calculated percentage */}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>

          {/* Staff Schedule with Filter */}
          <div className="space-y-4 mt-6">
            <Card>
              <CardHeader>
                <div className="flex items-center space-x-4">
                  <CardTitle>Staff Schedule</CardTitle>

                  <Select onValueChange={(value) => setSelectedDepartment(value || "all")}>
                    <SelectTrigger className="w-[180px]">
                      <SelectValue placeholder="Filter By Dept" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Departments</SelectItem>
                      {departments.map(dept => (
                        <SelectItem key={dept.department_id} value={dept.department_id.toString()}>
                          {dept.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardHeader>
              <CardContent>
                <div className="overflow-y-auto max-h-96">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Department</TableHead>
                        <TableHead>Location</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredStaff.map(staff => (
                        <TableRow key={staff.employee_id}>
                          <TableCell className="flex items-center space-x-2">
                            <Avatar>
                              <AvatarImage src="/placeholder.svg" alt={`${staff.employee_fname} ${staff.employee_lname}`} />
                              <AvatarFallback>{staff.employee_fname[0]}{staff.employee_lname[0]}</AvatarFallback>
                            </Avatar>
                            <span>{staff.employee_fname} {staff.employee_lname}</span>
                          </TableCell>
                          <TableCell>{teamDepartmentMap[staff.team_id] || "N/A"}</TableCell>
                          <TableCell>
                            <Badge variant={staff.location === "wfo" ? "default" : "secondary"}>
                              {staff.location === "wfo" ? <Briefcase className="h-4 w-4 mr-1" /> : <Home className="h-4 w-4 mr-1" />}
                              {staff.location === "wfo" ? "Office" : `Home (${staff.application_hour.toUpperCase()})`}
                            </Badge>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
