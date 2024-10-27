"use client";

import { useEffect, useState } from "react";
import { getAllDepartments, getApprovedStaffLocation, DepartmentSchema, EmployeeLocation } from "@/app/overview/api";
import OverviewScheduleComponent from "./OverviewScheduleComponent";

interface OverviewScheduleProps {
  token: string;
  userId: number;
}

export default function OverviewSchedule({ token, userId }: OverviewScheduleProps) {
  const [departments, setDepartments] = useState<DepartmentSchema[]>([]);
  const [staffMembers, setStaffMembers] = useState<EmployeeLocation[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const [selectedDepartment, setSelectedDepartment] = useState<string | undefined>(undefined);
  const [selectedPieChartDepartment, setSelectedPieChartDepartment] = useState<string | undefined>(undefined); // Separate pie chart filter
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        setLoading(true);
        const data = await getAllDepartments(token);
        setDepartments(data);
      } catch (error) {
        console.error("Failed to fetch departments:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDepartments();
  }, [token]);

  useEffect(() => {
    const fetchStaffSchedule = async () => {
      try {
        setLoading(true);
        const staff = await getApprovedStaffLocation(token, userId);
        const formattedDate = selectedDate
          ? selectedDate.toLocaleDateString("en-CA", { timeZone: "Asia/Singapore" })
          : new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Singapore" });
        console.log("Selected date:", formattedDate);
        const homeStaff = staff.filter(
          (member) => member.date === formattedDate && (member.location === "wfh" || member.location === "Home")
        );

        const allEmployees = departments.flatMap((dept) => dept.teams.flatMap((team) => team.members));

        const completeStaffList: EmployeeLocation[] = allEmployees.map((employee) => {
          const isHome = homeStaff.some((home) => home.employee_id === employee.staff_id);
          return {
            employee_fname: employee.staff_fname,
            employee_lname: employee.staff_lname,
            employee_id: employee.staff_id,
            team_id: employee.team_id,
            position: employee.position,
            location: isHome ? "wfh" : "wfo",
            application_hour: isHome ? "FULLDAY" : "N/A",
            date: formattedDate,
            role: employee.role || 1,
          };
        });

        setStaffMembers(completeStaffList);
      } catch (error) {
        console.error("Failed to fetch staff schedule:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStaffSchedule();
  }, [selectedDate, token, userId, departments]);

  return loading ? (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
    </div>
  ) : (
    <OverviewScheduleComponent
      departments={departments}
      staffMembers={staffMembers}
      selectedDate={selectedDate}
      setSelectedDate={setSelectedDate}
      selectedDepartment={selectedDepartment}
      setSelectedDepartment={setSelectedDepartment}
      selectedPieChartDepartment={selectedPieChartDepartment} // Passing pie chart filter
      setSelectedPieChartDepartment={setSelectedPieChartDepartment} // Passing pie chart filter setter
    />
  );
}
