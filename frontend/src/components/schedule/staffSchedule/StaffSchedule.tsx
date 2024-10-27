import React, { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar } from "@/components/ui/calendar";
import { Badge } from "@/components/ui/badge";
import { Home, Briefcase } from "lucide-react";
import { EmployeeLocation } from "@/app/schedule/api";
import StaffAccordion from "./StaffAccordian";
import ManagedTeamAccordion from "./ManagedTeamAccordian";
// import OtherStaffAccordion from "./OtherStaffAccordian";
import { addMonths, subMonths } from "date-fns";
import useAuth from "@/lib/auth";
import AllDepartmentsAccordion from "./AllDepartmentsAccordian";

const today = new Date();

interface IStaffSchedule {
  teamMembers: EmployeeLocation[];
}

const StaffSchedule: React.FC<IStaffSchedule> = ({ teamMembers }) => {
  const { userId, user } = useAuth();
  const [activeTab, setActiveTab] = useState("team");
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(today);
  const [currTeamMembers, setCurrTeamMembers] = useState<EmployeeLocation[]>(teamMembers);

  const formatDate = (date: Date) => date.toISOString().split('T')[0];

  useEffect(() => {
    if (selectedDate) {
      const adjustedDate = new Date(selectedDate);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      const formattedDate = formatDate(adjustedDate);
      const filteredMembers = teamMembers?.filter(member => member.date === formattedDate);
      setCurrTeamMembers(filteredMembers);
    }
  }, [selectedDate, teamMembers]);

  const arrangement = currTeamMembers.some((member) => member.employee_id === Number(userId));
  const userCurrArrangement = currTeamMembers.find((member) => member.employee_id === Number(userId));

  return (
    <div className="container mx-auto p-4">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList
          className={`grid w-full ${user?.role === 1 ? 'grid-cols-3' : 'grid-cols-2'} bg-white text-black`}
        >
          {user?.role === 1 && (
            <TabsTrigger value="department">Department Schedule</TabsTrigger>
          )}
          <TabsTrigger value="team">Team Schedule</TabsTrigger>
          <TabsTrigger value="own">My Schedule</TabsTrigger>
        </TabsList>
        <TabsContent value="department">
          <Card>
            <CardHeader>
              <CardTitle>Team Schedule</CardTitle>
              <CardDescription>View who is in the office and who is working from home in the organisation.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={setSelectedDate}
                    className="rounded-md border"
                    fromDate={subMonths(new Date(), 2)}
                    toDate={addMonths(new Date(), 3)}
                  />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">
                    {selectedDate ? selectedDate.toDateString() : 'Select a date'}
                  </h3>
                  <AllDepartmentsAccordion employeeLocations={currTeamMembers} />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="team">
          <Card>
            <CardHeader>
              <CardTitle>Team Schedule</CardTitle>
              <CardDescription>View who is in the office and who is working from home in your team.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={setSelectedDate}
                    className="rounded-md border"
                    fromDate={subMonths(new Date(), 2)}
                    toDate={addMonths(new Date(), 3)}
                  />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">
                    {selectedDate ? selectedDate.toDateString() : 'Select a date'}
                  </h3>
                  <StaffAccordion employeeLocations={currTeamMembers} />
                  <ManagedTeamAccordion employeeLocations={currTeamMembers} />
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
                      <Badge variant={arrangement ? 'secondary' : 'default'}>
                        {arrangement ? (
                          <>
                            <Home className="h-4 w-4 mr-1" />HOME ({userCurrArrangement?.application_hour.toUpperCase()})
                          </>
                        ) : (
                          <>
                            <Briefcase className="h-4 w-4 mr-1" /> Working from Office
                          </>
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
  );
};

export default StaffSchedule;
