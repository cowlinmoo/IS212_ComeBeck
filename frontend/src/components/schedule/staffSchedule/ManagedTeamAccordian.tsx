import React, { useEffect, useState } from 'react';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"
import { PersonIcon } from '@radix-ui/react-icons';
import { Badge } from '@/components/ui/badge';
import { Briefcase, HomeIcon } from 'lucide-react';
import useAuth from '@/lib/auth';
import { EmployeeLocation, getTeamByManagerId, Team } from '@/app/schedule/api';

interface ManagedTeamAccordionProps {
    employeeLocations: EmployeeLocation[];
}

const ManagedTeamAccordion: React.FC<ManagedTeamAccordionProps> = ({ employeeLocations }) => {
    const { token, userId } = useAuth();
    const [managedTeam, setManagedTeam] = useState<Team | null>(null);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        if (token && userId) {
            const fetchManagedTeam = async () => {
                try {
                    setLoading(true);
                    const teamData = await getTeamByManagerId(token, Number(userId));
                    setManagedTeam(teamData);
                    setLoading(false);
                } catch (error) {
                    console.error(error);
                    setLoading(false);
                }
            };
            fetchManagedTeam();
        }
    }, [token, userId]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-16">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-900"></div>
            </div>
        );
    }

    // Conditionally render the Accordion only if a managed team with members is found
    return managedTeam && managedTeam.members ? (
        <Accordion type="single" collapsible>
            <AccordionItem value="managed-team">
                <AccordionTrigger>Team Members I Manage</AccordionTrigger>
                <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                    <h3 className="font-semibold mb-2">{managedTeam.name} - {managedTeam.description}</h3>
                    <hr className='my-2'/>
                    <ul className="space-y-2">
                        {managedTeam.members.length > 0 ? (
                            managedTeam.members.map((member) => (
                                <li key={member.staff_id} className="flex items-center space-x-2">
                                    <PersonIcon />
                                    <span>{`${member.staff_fname} ${member.staff_lname} (${member.position})`}</span>
                                    {employeeLocations.some((loc) => loc.employee_id === member.staff_id) ? (
                                        <Badge variant="secondary">
                                            <HomeIcon className="h-4 w-4 mr-1" />
                                            Home ({employeeLocations.find((loc) => loc.employee_id === member.staff_id)?.application_hour.toUpperCase()})
                                        </Badge>
                                    ) : (
                                        <Badge variant="default">
                                            <Briefcase className="h-4 w-4 mr-1" /> Office
                                        </Badge>
                                    )}
                                </li>
                            ))
                        ) : (
                            <li className="text-gray-500 italic">No team members to manage.</li>
                        )}
                    </ul>
                </AccordionContent>
            </AccordionItem>
        </Accordion>
    ) : null; // Return null if no managed team is found or if there are no members
};

export default ManagedTeamAccordion;
