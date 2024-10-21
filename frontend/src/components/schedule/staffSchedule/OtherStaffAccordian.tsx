import { EmployeeLocation, getTeamsUnderMe, Team } from '@/app/schedule/api';
import React, { useEffect, useState } from 'react';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"
import useAuth from '@/lib/auth';
import { PersonIcon } from '@radix-ui/react-icons';
import { Badge } from '@/components/ui/badge';
import { Briefcase, Building2Icon, HomeIcon } from 'lucide-react';

interface OtherStaffAccordionProps {
    employeeLocations: EmployeeLocation[];
}

const OtherStaffAccordion: React.FC<OtherStaffAccordionProps> = ({ employeeLocations }) => {
    const { token, user } = useAuth()
    const [otherTeams, setOtherTeams] = useState<Team[]>([])
    useEffect(() => {
        const getOtherTeams = async () => {
            const response = await getTeamsUnderMe(token as string, user?.team_id as number)
            setOtherTeams(response)
        }
        getOtherTeams()
    }, [token, user])
    return (
        <Accordion type="single" collapsible className={`${user?.role === 3 ? "block" : "none"}`}>
            <AccordionItem value='item-1' >
                <AccordionTrigger>
                    Other Teams Under Me
                </AccordionTrigger>
                <AccordionContent>
                    {otherTeams.map((team) => {
                        return (
                            <Accordion type="single" collapsible className={`${user?.role === 3 ? "block" : "none"}`}>
                                <AccordionItem value='item-1' >
                                    <AccordionTrigger>
                                        {team.name}
                                    </AccordionTrigger>
                                    <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                                        {
                                            team.members.map((member) => {
                                                return (<div className='flex flex-row gap-4'>
                                                    <PersonIcon />
                                                    {member.staff_fname} {member.staff_lname}

                                                    {
                                                        employeeLocations.map((item) => item.employee_id).includes(member.staff_id) ? (
                                                            <Badge variant='secondary'><HomeIcon className="h-4 w-4 mr-1" />HOME</Badge>
                                                        ) : (
                                                            <Badge variant="default"><Briefcase className="h-4 w-4 mr-1" />OFFICE</Badge>
                                                        )
                                                    }

                                                </div>)
                                            })
                                        }
                                    </AccordionContent>
                                </AccordionItem>
                            </Accordion>
                        )
                    })}
                </AccordionContent>
            </AccordionItem>
        </Accordion >
    );
};

export default OtherStaffAccordion;
