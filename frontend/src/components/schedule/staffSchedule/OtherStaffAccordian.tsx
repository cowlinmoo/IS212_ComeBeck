import React, { useEffect, useState } from 'react';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";
import { PersonIcon } from '@radix-ui/react-icons';
import { Badge } from '@/components/ui/badge';
import { Briefcase, HomeIcon } from 'lucide-react';
import useAuth from '@/lib/auth';
import { EmployeeLocation, getAllTeamsUnderMe, Team } from '@/app/schedule/api';

interface OtherStaffAccordionProps {
    employeeLocations: EmployeeLocation[];
}

const OtherStaffAccordion: React.FC<OtherStaffAccordionProps> = ({ employeeLocations }) => {
    const { token, user } = useAuth();
    const [departmentTeams, setDepartmentTeams] = useState<{ [departmentName: string]: Team[] }>({});
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        const getOtherTeams = async () => {
            try {
                setLoading(true);
                let response = await getAllTeamsUnderMe(token as string, user?.team_id as number);
                response = response.filter((team) => team.team_id !== user?.team_id);

                // Group teams by department name
                const groupedByDepartment = response.reduce((acc, team) => {
                    const deptName = team.department.name;
                    if (!acc[deptName]) acc[deptName] = [];
                    acc[deptName].push(team);
                    return acc;
                }, {} as { [departmentName: string]: Team[] });

                setDepartmentTeams(groupedByDepartment);
                setLoading(false);
            } catch (error) {
                console.error(error);
                setLoading(false);
            }
        };
        getOtherTeams();
    }, [token, user]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
            </div>
        );
    }

    return (
        <Accordion type="single" collapsible>
            {Object.entries(departmentTeams)
                .sort(([a], [b]) => a.localeCompare(b)) // Sorting departments alphabetically by name
                .map(([departmentName, teams]) => (
                    <Accordion key={departmentName} type="single" collapsible className="mb-4">
                        <AccordionItem value={`dept-${departmentName}`}>
                            <AccordionTrigger>{departmentName} Department</AccordionTrigger>
                            <AccordionContent>
                                {teams.map((team) => (
                                    <Accordion type="single" collapsible key={team.team_id} className="mb-4">
                                        <AccordionItem value={`team-${team.team_id}`}>
                                            <AccordionTrigger>{team.name}</AccordionTrigger>
                                            <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                                                {team.members.map((member) => (
                                                    <div className='flex flex-row gap-4' key={member.staff_id}>
                                                        <PersonIcon />
                                                        {member.staff_fname} {member.staff_lname} ({member.position})
                                                        {employeeLocations.some((item) => item.employee_id === member.staff_id) ? (
                                                            <Badge variant='secondary'>
                                                                <HomeIcon className="h-4 w-4 mr-1" />HOME
                                                                ({employeeLocations.find((location) => location.employee_id === member.staff_id)?.application_hour.toUpperCase()})
                                                            </Badge>
                                                        ) : (
                                                            <Badge variant="default">
                                                                <Briefcase className="h-4 w-4 mr-1" />OFFICE
                                                            </Badge>
                                                        )}
                                                    </div>
                                                ))}
                                            </AccordionContent>
                                        </AccordionItem>
                                    </Accordion>
                                ))}
                            </AccordionContent>
                        </AccordionItem>
                    </Accordion>
                ))}
        </Accordion>
    );
};

export default OtherStaffAccordion;
