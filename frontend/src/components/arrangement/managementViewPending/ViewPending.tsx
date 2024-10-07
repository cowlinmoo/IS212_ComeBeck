"use client";


import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar as CalendarIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Application } from "@/app/managementViewPending/page";



export default function ViewPending({ data }: { data: Application[] | undefined }) {
    const pendingRequests = Array.isArray(data) 
    ? data.filter((request) => request.status === "pending")
    : [];
    console.log(pendingRequests,"hello");
    return (
        <div className="container mx-auto p-4">
            <Card>
                <CardHeader>
                    <CardTitle>Pending Arrangements </CardTitle>
                    <CardDescription>Review and manage pending arrangement requests.</CardDescription>
                </CardHeader>
                <ScrollArea className="h-[600px] w-full rounded-md border p-4">
                        {pendingRequests.length === 0 ? (
                            <p>No pending requests.</p>
                        ): (
                        pendingRequests.map((request) => (
                            <Card key={request.application_id} className="mb-4">
                                <CardHeader>
                                    <CardTitle>Requested By: {request.staff.staff_fname} {request.staff.staff_lname}</CardTitle>
                                    <CardDescription>Request ID: {request.application_id}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <p>Reason: {request.reason}</p>                                  
                                    <p>Date of WFH arrangement:</p>
                                    {request.events.map((event) => (
                                        <div key={event.event_id} className="flex items-center space-x-2">
                                            <CalendarIcon className="h-4 w-4" />
                                            <span> {new Date(event.requested_date).toDateString()}</span>
                                        </div>
                                    ))}
                                    <div className="flex justify-end space-x-2">
                                        <Button>Approve</Button>
                                        <Button>Reject</Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </ScrollArea>
            </Card>
        </div>
    )
}