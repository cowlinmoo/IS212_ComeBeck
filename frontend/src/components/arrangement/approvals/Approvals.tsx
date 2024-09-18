"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Check, X, Calendar as CalendarIcon } from "lucide-react";

// Define types for requests
interface RequestType {
  id: number;
  employeeName: string;
  avatar: string;
  type: string;
  startDate: Date;
  endDate: Date;
  reason: string;
}

// Mock data for pending requests
const pendingRequests: RequestType[] = [
  {
    id: 1,
    employeeName: "Alice Johnson",
    avatar: "/placeholder.svg?height=40&width=40",
    type: "Work from Home",
    startDate: new Date(2023, 5, 15),
    endDate: new Date(2023, 5, 19),
    reason: "Family commitments",
  },
  {
    id: 2,
    employeeName: "Bob Smith",
    avatar: "/placeholder.svg?height=40&width=40",
    type: "Flexible Hours",
    startDate: new Date(2023, 5, 20),
    endDate: new Date(2023, 5, 24),
    reason: "Personal development course",
  },
  {
    id: 3,
    employeeName: "Charlie Brown",
    avatar: "/placeholder.svg?height=40&width=40",
    type: "Work from Home",
    startDate: new Date(2023, 5, 22),
    endDate: new Date(2023, 5, 26),
    reason: "Home repairs",
  },
];

export default function Approvals() {
  const [requests, setRequests] = useState<RequestType[]>(pendingRequests);
  const [selectedRequest, setSelectedRequest] = useState<RequestType | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [approvalComment, setApprovalComment] = useState("");

  const handleApprove = (id: number) => {
    setRequests(requests.filter((request) => request.id !== id));
    setIsDialogOpen(false);
    setApprovalComment("");
    // API request can be added here
  };

  const handleReject = (id: number) => {
    setRequests(requests.filter((request) => request.id !== id));
    setIsDialogOpen(false);
    setApprovalComment("");
    // API request can be added here
  };

  const openDialogForRequest = (request: RequestType) => {
    setSelectedRequest(request);
    setIsDialogOpen(true);
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Flexible Working Arrangements Approval</CardTitle>
          <CardDescription>Review and manage pending flexible working arrangement requests.</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="pending">
            <TabsList>
              <TabsTrigger value="pending">Pending Requests</TabsTrigger>
              <TabsTrigger value="approved">Approved</TabsTrigger>
              <TabsTrigger value="rejected">Rejected</TabsTrigger>
            </TabsList>
            <TabsContent value="pending">
              <ScrollArea className="h-[400px] w-full rounded-md border p-4">
                {requests.map((request) => (
                  <Card key={request.id} className="mb-4">
                    <CardHeader>
                      <div className="flex items-center space-x-4">
                        <Avatar>
                          <AvatarImage src={request.avatar} alt={request.employeeName} />
                          <AvatarFallback>{request.employeeName.split(" ").map((n) => n[0]).join("")}</AvatarFallback>
                        </Avatar>
                        <div>
                          <CardTitle>{request.employeeName}</CardTitle>
                          <CardDescription>{request.type}</CardDescription>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center space-x-2 mb-2">
                        <CalendarIcon className="h-4 w-4" />
                        <span>
                          {request.startDate.toDateString()} - {request.endDate.toDateString()}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">{request.reason}</p>
                    </CardContent>
                    <CardFooter className="flex justify-end space-x-2">
                      <Dialog open={isDialogOpen && selectedRequest?.id === request.id} onOpenChange={setIsDialogOpen}>
                        <DialogTrigger asChild>
                          <Button variant="outline" onClick={() => openDialogForRequest(request)}>Review</Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Review Request</DialogTitle>
                            <DialogDescription>Review and approve or reject the flexible working arrangement request.</DialogDescription>
                          </DialogHeader>
                          <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-4 items-center gap-4">
                              <Label htmlFor="name" className="text-right">
                                Name
                              </Label>
                              <div className="col-span-3">{selectedRequest?.employeeName}</div>
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                              <Label htmlFor="type" className="text-right">
                                Type
                              </Label>
                              <div className="col-span-3">{selectedRequest?.type}</div>
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                              <Label htmlFor="dates" className="text-right">
                                Dates
                              </Label>
                              <div className="col-span-3">
                                {selectedRequest?.startDate.toDateString()} - {selectedRequest?.endDate.toDateString()}
                              </div>
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                              <Label htmlFor="reason" className="text-right">
                                Reason
                              </Label>
                              <div className="col-span-3">{selectedRequest?.reason}</div>
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                              <Label htmlFor="comment" className="text-right">
                                Comment
                              </Label>
                              <Textarea
                                id="comment"
                                className="col-span-3"
                                value={approvalComment}
                                onChange={(e) => setApprovalComment(e.target.value)}
                              />
                            </div>
                          </div>
                          <DialogFooter>
                            <Button variant="outline" onClick={() => handleReject(selectedRequest!.id)}>
                              <X className="mr-2 h-4 w-4" /> Reject
                            </Button>
                            <Button onClick={() => handleApprove(selectedRequest!.id)}>
                              <Check className="mr-2 h-4 w-4" /> Approve
                            </Button>
                          </DialogFooter>
                        </DialogContent>
                      </Dialog>
                    </CardFooter>
                  </Card>
                ))}
              </ScrollArea>
            </TabsContent>
            <TabsContent value="approved">
              <p>Approved requests will be shown here.</p>
            </TabsContent>
            <TabsContent value="rejected">
              <p>Rejected requests will be shown here.</p>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
