"use client";


import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Calendar as CalendarIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Application } from "@/app/managementViewPending/page";
import { useToast } from "@/components/hooks/use-toast";
import { processApplicationStatus } from '@/app/managementViewPending/api';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import React, { useState, useEffect } from "react";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";


export default function ViewPending({ data, token, userId }: { data: Application[] | undefined, token: string, userId: number }) {
    const [pendingRequests, setPendingRequests] = useState<Application[]>([]);
    const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);
    const [reviewReason, setReviewReason] = useState('');
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const {toast} = useToast();
    useEffect(() => {
        if (Array.isArray(data)) {
            const filteredRequests = data.filter((request) => request.status === "pending");
            setPendingRequests(filteredRequests);
        }
    }, [data]);
    console.log(pendingRequests);
    const handleStatusUpdate = async (status: "approved" | "rejected") => {
        if (!selectedApplication) return;

        try {
            await processApplicationStatus(token, userId, selectedApplication.application_id, status, reviewReason);
            setPendingRequests(prevRequests => prevRequests.filter(request => request.application_id !== selectedApplication.application_id));
            setSelectedApplication(null);
            setIsDialogOpen(false);
            setReviewReason('');
            toast({
                title: `Request ${status}`,
                description: `The request has been ${status}.`,
                variant: "default",
            })
    }   catch (error) {
            console.error("Failed to approve/reject application", error);
            toast({
                title: "Failed to approve/reject application",
                description: "An error occurred while approving/rejecting the application.",
                variant: "destructive",
            })
        }
    }

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
                                    <div className="flex justify-end mt-4">
                                        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                                            <DialogTrigger asChild>
                                                <Button onClick={() => setSelectedApplication(request)}>
                                                    Review
                                                </Button>
                                            </DialogTrigger>
                                            <DialogContent className="sm:max-w-[425px]">
                                                <DialogHeader>
                                                    <DialogTitle>Review Application</DialogTitle>
                                                    <DialogDescription>
                                                        Provide a reason for your decision and either approve or reject the application.
                                                    </DialogDescription>
                                                </DialogHeader>
                                                <div className="grid gap-4 py-4">
                                                    <div className="grid grid-cols-4 items-center gap-4">
                                                        <Label htmlFor="reason" className="text-right">
                                                            Reason
                                                        </Label>
                                                        <Textarea
                                                            id="reason"
                                                            className="col-span-3"
                                                            value={reviewReason}
                                                            onChange={(e) => setReviewReason(e.target.value)}
                                                        />
                                                    </div>
                                                </div>
                                                <DialogFooter>
                                                    <Button onClick={() => handleStatusUpdate('approved')} variant="default">
                                                        Approve
                                                    </Button>
                                                    <Button onClick={() => handleStatusUpdate('rejected')} variant="destructive">
                                                        Reject
                                                    </Button>   
                                                </DialogFooter>
                                            </DialogContent>
                                        </Dialog>
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