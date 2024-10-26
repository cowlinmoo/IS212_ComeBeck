import { EmployeeLocation, getAllTeamsUnderMe, getApprovedStaffLocation, Team } from '@/app/schedule/api';
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
import { Briefcase, HomeIcon } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';

interface OtherStaffAccordionProps {
    employeeLocations: EmployeeLocation[];
}

const OtherStaffAccordion: React.FC<OtherStaffAccordionProps> = ({ employeeLocations }) => {
    const { token, user } = useAuth()
    const [otherTeams, setOtherTeams] = useState<Team[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [staffLocation, setStaffLocation] = useState<EmployeeLocation[]>([])
    
    useEffect(() => {
        const getOtherTeams = async () => {
            try {
                setLoading(true)
                let response = await getAllTeamsUnderMe(token as string, user?.team_id as number)
                response = response.filter((team) => team.team_id !== user?.team_id)
                setOtherTeams(response)
                setLoading(false)
            }
            catch (error) {
                console.error(error)
                setLoading(false)
            }
        }
        getOtherTeams()
    }, [token, user])
    return (
        <Accordion type="single" collapsible className={`${user?.role === 3 ? "block" : "none"}`}>
            <AccordionItem value='item-1' >
                <AccordionTrigger>
                    Other Teams
                </AccordionTrigger>
                <AccordionContent>
                    {otherTeams.map((team) => {
                        return (
                            <Accordion type="single" collapsible className={`${user?.role === 3 ? "block" : "none"}`} key={`${team.name}-key`}>
                                <AccordionItem value='item-1' >
                                    <AccordionTrigger>
                                        {team.name}
                                    </AccordionTrigger>
                                    <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                                        {loading ? (<>
                                            <Skeleton className="w-full h-[50px] rounded-md" />
                                        </>) : (<> {
                                            team.members.map((member) => {
                                                return (<div className='flex flex-row gap-4' key={`${member.staff_id}-key`}>
                                                    <PersonIcon />
                                                    {member.staff_fname} {member.staff_lname} ({member.position})

                                                    {
                                                        employeeLocations.map((item) => item.employee_id).includes(member.staff_id) ? (
                                                            <Badge variant='secondary'><HomeIcon className="h-4 w-4 mr-1" />HOME
                                                                ({employeeLocations.filter((location) => location.employee_id === member.staff_id)[0].application_hour.toUpperCase()})
                                                            </Badge>
                                                        ) : (
                                                            <Badge variant="default"><Briefcase className="h-4 w-4 mr-1" />OFFICE</Badge>
                                                        )
                                                    }

                                                </div>)
                                            })
                                        }</>)}
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
