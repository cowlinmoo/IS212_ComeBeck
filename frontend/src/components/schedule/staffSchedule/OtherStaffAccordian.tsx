import { EmployeeLocation, getTeamsUnderMe } from '@/app/schedule/api';
import React, { useEffect } from 'react';
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion"
import useAuth from '@/lib/auth';

interface OtherStaffAccordionProps {
    employeeLocations: EmployeeLocation[];
}

const OtherStaffAccordion: React.FC<OtherStaffAccordionProps> = ({ employeeLocations }) => {
    const { token, user } = useAuth()
    useEffect(() => {
        const getOtherTeams = async () => {
            const response = await getTeamsUnderMe(token as string, user?.team_id as number)
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
                    
                </AccordionContent>
            </AccordionItem>
        </Accordion >
    );
};

export default OtherStaffAccordion;
