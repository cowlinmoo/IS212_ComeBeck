import React, { useEffect, useState } from 'react';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"
import { EmployeeLocation, getMyEmployee, getMyTeam } from '@/app/schedule/api';
import { Team } from '@/app/schedule/api'
import useAuth from '@/lib/auth';
import { PersonIcon } from '@radix-ui/react-icons';
import { Briefcase, Home } from 'lucide-react';
import { Badge } from "@/components/ui/badge"
import { Skeleton } from '@/components/ui/skeleton';


interface IStaffSchedule {
    // all approved events, if none, defaults to work in office
    employeeLocations: EmployeeLocation[]

}

export interface flName {
    staff_id: number,
    staff_fname: string,
    staff_lname: string,

}

interface defName extends flName {
    role: number
}

const role: string[] = ["", "HR", "STAFF", "MANAGER"]

const StaffAccordion: React.FC<IStaffSchedule> = ({ employeeLocations }) => {
    const { token, userId, user } = useAuth()
    const [myTeam, setMyTeam] = useState<Team | undefined>(undefined)
    const [defWio, setDefWio] = useState<defName[]>([])
    const [loading, setLoading] = useState<boolean>(false)

    useEffect(() => {
        if (token && userId) {
            const getTeam = async () => {
                try {
                    setLoading(true)
                    const response: Team = await getMyTeam(token as string, Number(user?.team_id))

                    const filteredTeam: flName[] = response.members.filter((team) => {
                        const names = employeeLocations.map((item) => `${item.employee_fname}:${item.employee_lname}`)
                        return !names.includes(`${team.staff_fname}:${team.staff_lname}`)
                    })
                    const defNames: defName[] = [];
                    for (const item of filteredTeam) {
                        const response = await getMyEmployee(token as string, item.staff_id);
                        defNames.push({ ...item, role: response.role });
                    }
                    setMyTeam(response)
                    setDefWio(defNames)
                    setLoading(false)
                }
                catch (error) {
                    console.error(error)
                    setLoading(false)
                }
            }
            getTeam()
        }
    }, [token, userId, employeeLocations])
    return (
        <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
                <AccordionTrigger>My Team</AccordionTrigger>
                <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                    {loading ? (<>
                        <Skeleton className="w-full h-[50px] rounded-md" />
                    </>) : (<> <ul className="space-y-2">
                        {employeeLocations?.map((member: EmployeeLocation) => {
                            if ((user?.role === 3 || user?.role === 1) || (user?.role === 2 && member.role !== 3)) {
                                if (member.employee_id !== myTeam?.manager.staff_id && member.team_id === user?.team_id) {
                                    return (
                                        <li key={`${member.employee_fname}-${member.employee_lname}`} className="flex items-center space-x-2">
                                            <PersonIcon />
                                            <span>{`${member.employee_fname} ${member.employee_lname} (${member.position})`}</span>
                                            <Badge variant={member.location === 'wfo' ? 'default' : 'secondary'}>
                                                {member.location === 'wfo' ? <Briefcase className="h-4 w-4 mr-1" /> : <Home className="h-4 w-4 mr-1" />}
                                                {member.location === 'wfo' ? 'Office' : `Home (${member.application_hour.toUpperCase()})`}
                                            </Badge>
                                        </li>
                                    )
                                }

                            }
                        })}
                    </ul>
                        <hr className='my-2' />
                        <ul className="space-y-2">
                            {
                                defWio.map((member: defName) => {
                                    if ((user?.role === 3 || user?.role === 1) || (user?.role === 2 && member.role !== 3)) {
                                        return (
                                            <li key={`${member.staff_fname}-${member.staff_lname}`} className="flex items-center space-x-2">
                                                <PersonIcon />
                                                <span>{`${member.staff_fname} ${member.staff_lname} (${role[member.role]})`}</span>
                                                <Badge>
                                                    <Briefcase className="h-4 w-4 mr-1" />
                                                    Office
                                                </Badge>
                                            </li>
                                        )
                                    }
                                })
                            }
                        </ul></>)}
                </AccordionContent>
            </AccordionItem>
        </Accordion>

    );
};

export default StaffAccordion;
