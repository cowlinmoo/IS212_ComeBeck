import React, { useEffect, useState } from 'react';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";
import { EmployeeLocation, getMyEmployee, getMyTeam } from '@/app/schedule/api';
import { Team } from '@/app/schedule/api';
import useAuth from '@/lib/auth';
import { PersonIcon } from '@radix-ui/react-icons';
import { Briefcase, Home, AlertTriangle } from 'lucide-react';
import { Badge } from "@/components/ui/badge"
import { Skeleton } from '@/components/ui/skeleton';


interface IStaffSchedule {
    employeeLocations: EmployeeLocation[];
}

export interface flName {
    staff_id: number;
    staff_fname: string;
    staff_lname: string;
    position: string;
}

interface defName extends flName {
    role: number;
}

const StaffAccordion: React.FC<IStaffSchedule> = ({ employeeLocations }) => {
    const { token, userId, user } = useAuth();
    const [myTeam, setMyTeam] = useState<Team | undefined>(undefined);
    const [defWio, setDefWio] = useState<defName[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    const [WIOPercent, setWIOPercent] = useState<number>(0)
    useEffect(() => {
        if (token && userId) {
            const getTeam = async () => {
                try {
                    setLoading(true);
                    const response: Team = await getMyTeam(token as string, Number(user?.team_id));
                    setMyTeam(response); // Set myTeam with fetched response

                    // Filter members not included in the provided employeeLocations
                    const filteredTeam: flName[] = response.members.filter((team) => {
                        const names = employeeLocations.map((item) => `${item.employee_fname}:${item.employee_lname}`);
                        return !names.includes(`${team.staff_fname}:${team.staff_lname}`);
                    });

                    // Fetch detailed info for each filtered member
                    const defNames: defName[] = [];
                    for (const item of filteredTeam) {
                        const response = await getMyEmployee(token as string, item.staff_id);
                        defNames.push({ ...item, role: response.role });
                    }
                    setMyTeam(response)
                    setDefWio(defNames)
                    setLoading(false)

                    if (response.members.length > 0) {
                        const percent = (100 - ((defNames.length / response.members.length) * 100))
                        setWIOPercent(percent)
                    }
                }
                catch (error) {
                    console.error(error)
                    setLoading(false)
                }

                
            }
            getTeam()
        }
    }, [employeeLocations, token, user?.team_id, userId])

    const getPercentageColor = (percent: number) => {
        if (myTeam?.members.length == 3) {
            if (percent >= 33) return 'text-yellow-500'
            if (percent >= 50) return 'text-red-500'
        } else {
            if (percent >= 40) return 'text-yellow-500'
            if (percent >= 50) return 'text-red-500'
        }
        return 'text-green-500'
    }
    return (
        <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
            <div className="flex items-center space-x-2">
                <span className={`font-bold ${getPercentageColor(WIOPercent)}`}>
                        ({WIOPercent.toFixed(2)}% Working from Home)
                    </span>
                    {WIOPercent >= 40 && WIOPercent <= 50 && (
                        <span className="text-yellow-500 flex items-center">
                            <AlertTriangle className="h-4 w-4 mr-1" />
                            Warning: Close to 50%
                        </span>
                    )}
                </div>
                <AccordionTrigger>My Team</AccordionTrigger>
                <AccordionContent className='overflow-y-scroll h-64 flex flex-col gap-2'>
                    {loading ? (
                        <div className="flex justify-center items-center h-16">
                            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-900"></div>
                        </div>
                    ) : (
                        <>
                            {myTeam ? (
                                <h3 className="font-semibold mb-2">
                                    {myTeam.name} - {myTeam.description}
                                </h3>
                            ) : (
                                <p>No team information available.</p>
                            )}
                            <ul className="space-y-2">
                                {employeeLocations?.map((member: EmployeeLocation) => {
                                    if ((user?.role === 3 || user?.role === 1) || (user?.role === 2 && member.role !== 3)) {
                                        if (member.employee_id !== myTeam?.manager.staff_id && member.team_id === user?.team_id) {
                                            return (
                                                <li key={`${member.employee_fname}-${member.employee_lname}`}
                                                    className="flex items-center space-x-2">
                                                    <PersonIcon />
                                                    <span>{`${member.employee_fname} ${member.employee_lname} (${member.position})`}</span>
                                                    <Badge variant={member.location === 'wfo' ? 'default' : 'secondary'}>
                                                        {member.location === 'wfo' ? <Briefcase className="h-4 w-4 mr-1" /> :
                                                            <Home className="h-4 w-4 mr-1" />}
                                                        {member.location === 'wfo' ? 'Office' : `Home (${member.application_hour.toUpperCase()})`}
                                                    </Badge>
                                                </li>
                                            );
                                        }
                                    }
                                })}
                            </ul>
                            <hr className='my-2' />
                            <ul className="space-y-2">
                                {defWio.map((member: defName) => {
                                    if ((user?.role === 3 || user?.role === 1) || (user?.role === 2 && member.role !== 3)) {
                                        return (
                                            <li key={`${member.staff_fname}-${member.staff_lname}`}
                                                className="flex items-center space-x-2">
                                                <PersonIcon />
                                                <span>{`${member.staff_fname} ${member.staff_lname} (${member.position})`}</span>
                                                <Badge>
                                                    <Briefcase className="h-4 w-4 mr-1" />
                                                    Office
                                                </Badge>
                                            </li>
                                        );
                                    }
                                })}
                            </ul>
                        </>
                    )}
                </AccordionContent>
            </AccordionItem>
        </Accordion>
    );
};

export default StaffAccordion;
