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
import { EmployeeLocation, getAllDepartments, DepartmentSchema } from '@/app/schedule/api';

interface AllDepartmentsAccordionProps {
    employeeLocations: EmployeeLocation[];
}

const AllDepartmentsAccordion: React.FC<AllDepartmentsAccordionProps> = ({ employeeLocations }) => {
    const { token } = useAuth();
    const [departments, setDepartments] = useState<DepartmentSchema[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        const fetchAllDepartments = async () => {
            try {
                setLoading(true);
                const departmentData = await getAllDepartments(token as string);
                setDepartments(departmentData);
                setLoading(false);
            } catch (error) {
                console.error(error);
                setLoading(false);
            }
        };
        fetchAllDepartments();
    }, [token]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-gray-900"></div>
            </div>
        );
    }

    return (
        <Accordion type="single" collapsible>
            {departments.map((department) => (
                <Accordion key={department.department_id} type="single" collapsible className="mb-4">
                    <AccordionItem value={`dept-${department.department_id}`}>
                        <AccordionTrigger>{department.name} Department</AccordionTrigger>
                        <AccordionContent>
                            {department.teams.map((team) => (
                                <Accordion type="single" collapsible key={team.team_id} className="mb-4">
                                    <AccordionItem value={`team-${team.team_id}`}>
                                        <AccordionTrigger>{team.name}</AccordionTrigger>
                                        <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                                            <h3 className="font-semibold mb-2">{team.description}</h3>
                                            {team.members.map((member) => (
                                                <div className='flex flex-row gap-4' key={member.staff_id}>
                                                    <PersonIcon/>
                                                    {member.staff_fname} {member.staff_lname} ({member.position})
                                                    {employeeLocations.some((item) => item.employee_id === member.staff_id) ? (
                                                        <Badge variant='secondary'>
                                                            <HomeIcon className="h-4 w-4 mr-1"/>HOME
                                                            ({employeeLocations.find((location) => location.employee_id === member.staff_id)?.application_hour.toUpperCase()})
                                                        </Badge>
                                                    ) : (
                                                        <Badge variant="default">
                                                            <Briefcase className="h-4 w-4 mr-1"/>OFFICE
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

export default AllDepartmentsAccordion;
