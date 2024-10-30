'use client';

import React, { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Checkbox } from "@/components/ui/checkbox";

export interface ApprovedApplication {
    staff: {
        staff_id: number;
        staff_fname: string;
        staff_lname: string;
        email: string; // Email is part of staff
    };
    application_id: number;
    application_state: string;
    reason: string;
    description: string;
    created_on: string;
    last_updated_on: string;
    staff_id: number;
    status: string;
    approver_id: number;
    recurring: boolean;
    events: Event[];
}

export interface Event {
    event_id: number;
    requested_date: string;
    location: string;
    application_hour: number; // Application hours are part of each event
}

interface ViewWithdrawProps {
    data: ApprovedApplication[] | undefined;
    onWithdraw: (selectedEvents: { applicationId: number; eventId: number }[]) => void;
}

export default function ViewWithdraw({ data, onWithdraw }: ViewWithdrawProps) {
    const [selectedEvents, setSelectedEvents] = useState<{ [eventId: number]: { applicationId: number; eventId: number } }>({});

    const handleEventSelection = (applicationId: number, eventId: number) => {
        setSelectedEvents(prev => {
            if (prev[eventId]) {
                // eslint-disable-next-line @typescript-eslint/no-unused-vars
                const { [eventId]: _, ...rest } = prev; // Deselect the event
                return rest;
            }
            return {
                ...prev,
                [eventId]: { applicationId, eventId } // Select the event
            };
        });
    };

    const handleWithdraw = () => {
        const eventsToWithdraw = Object.values(selectedEvents); // Get all selected application-event pairs
        onWithdraw(eventsToWithdraw); // Pass the selected events (with applicationId and eventId) to the parent
    };

    return (
        <div className="container mx-auto p-4">
            <Card>
                <CardHeader>
                    <CardTitle>Approved Arrangements</CardTitle>
                    <CardDescription>Review and manage approved arrangement requests.</CardDescription>
                </CardHeader>
                <CardContent>
                    <ScrollArea className="h-96">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Select</TableHead>
                                    <TableHead>Event ID</TableHead>
                                    <TableHead>Date</TableHead>
                                    <TableHead>Location</TableHead>
                                    <TableHead>Staff Full Name</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead>Application ID</TableHead>
                                    <TableHead>Application Hours</TableHead> {/* Updated to reflect event-specific application hours */}
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {data && data.map(application =>
                                    application.events.map(event => (
                                        <TableRow key={event.event_id}>
                                            <TableCell>
                                                <Checkbox
                                                    checked={!!selectedEvents[event.event_id]}
                                                    onCheckedChange={() => handleEventSelection(application.application_id, event.event_id)}
                                                />
                                            </TableCell>
                                            <TableCell>{event.event_id}</TableCell>
                                            <TableCell>{event.requested_date}</TableCell>
                                            <TableCell>{event.location}</TableCell>
                                            <TableCell>{`${application.staff.staff_fname} ${application.staff.staff_lname}`}</TableCell>
                                            <TableCell>{application.staff.email}</TableCell>
                                            <TableCell>{application.application_id}</TableCell>
                                            <TableCell>{event.application_hour}</TableCell> {/* Updated to reflect event's application hours */}
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </ScrollArea>
                    <Button className="mt-4" onClick={handleWithdraw}>
                        Withdraw Selected Events
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
