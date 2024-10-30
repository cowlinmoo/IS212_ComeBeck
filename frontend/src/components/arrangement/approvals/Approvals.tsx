"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar as CalendarIcon } from "lucide-react";
import { Application } from "@/app/approvals/page";

let requestType = '';
const setRequestType = (request: string) => {
  if (request === 'new_application') {
      requestType = 'New Application';
  } else if (request === 'change_request') {
      requestType = 'Change Request';
  } else {
      requestType = 'Withdraw Request';
  }
};

export default function Approvals({ data }: { data: Application[] }) {
  return (
    <div className="container mx-auto p-4">
      <Card>
        <ScrollArea className="h-[600px] w-full rounded-md border p-4">
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
              <ScrollArea className="h-[600px] w-full rounded-md border p-4">
                {data.filter((request) => request.status === "pending").length === 0 ? (
                  <p>No pending requests.</p>
                ) : (
                  data
                    .filter((request) => request.status === "pending")
                    .map((request) => (
                      setRequestType(request.application_state),
                      <Card key={request.application_id} className="mb-4">
                        <CardHeader>
                          <div className="flex items-center space-x-4">
                            <div>
                              <CardTitle>{`Application ID: ${request.application_id}`}</CardTitle>
                              <CardDescription>{`Application Type: ${requestType}`}</CardDescription>
                              <CardDescription>{`Reason: ${request.reason}`}</CardDescription>
                              <CardDescription>{`Approved by: -`}</CardDescription>
                              <CardDescription>{`Recurring: ${request.recurring ? "Yes" : "No"}`}</CardDescription>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          {request.events.map((event) => (
                            <div key={event.event_id} className="flex items-center space-x-2">
                              <CalendarIcon className="h-4 w-4" />
                              <span>{new Date(event.requested_date).toDateString()}</span>
                              <span>({event.application_hour[0].toUpperCase()+event.application_hour.slice(1)})</span>
                            </div>
                          ))}
                        </CardContent>
                      </Card>
                    ))
                )}
              </ScrollArea>
            </TabsContent>

            <TabsContent value="approved">
              <ScrollArea className="h-[600px] w-full rounded-md border p-4">
                {data.filter((request) => request.status === "approved").length === 0 ? (
                  <p>No approved requests.</p>
                ) : (
                  data
                    .filter((request) => request.status === "approved")
                    .map((request) => (
                      setRequestType(request.application_state),
                      <Card key={request.application_id} className="mb-4">
                        <CardHeader>
                          <div className="flex items-center space-x-4">
                            <div>
                              <CardTitle>{`Application ID: ${request.application_id}`}</CardTitle>
                              <CardDescription>{`Application Type: ${requestType}`}</CardDescription>
                              <CardDescription>{`Reason: ${request.reason}`}</CardDescription>
                              <CardDescription>{`Approved by: ${request.approver_id}`}</CardDescription>
                              <CardDescription>{`Recurring: ${request.recurring ? "Yes" : "No"}`}</CardDescription>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          {request.events.map((event) => (
                            <div key={event.event_id} className="flex items-center space-x-2">
                              <CalendarIcon className="h-4 w-4" />
                              <span>{new Date(event.requested_date).toDateString()}</span>
                              <span>({event.application_hour[0].toUpperCase()+event.application_hour.slice(1)})</span>
                            </div>
                          ))}
                        </CardContent>
                      </Card>
                    ))
                )}
              </ScrollArea>
            </TabsContent>

            <TabsContent value="rejected">
              <ScrollArea className="h-[600px] w-full rounded-md border p-4">
                {data.filter((request) => request.status === "rejected").length === 0 ? (
                  <p>No rejected requests.</p>
                ) : (
                  data
                    .filter((request) => request.status === "rejected")
                    .map((request) => (
                      setRequestType(request.application_state),
                      <Card key={request.application_id} className="mb-4">
                        <CardHeader>
                          <div className="flex items-center space-x-4">
                            <div>
                              <CardTitle>{`Application ID: ${request.application_id}`}</CardTitle>
                              <CardDescription>{`Application Type: ${requestType}`}</CardDescription>
                              <CardDescription>{`Reason: ${request.reason}`}</CardDescription>
                              <CardDescription>{`Rejected by: ${request.approver_id}`}</CardDescription>
                              <CardDescription>{`Recurring: ${request.recurring ? "Yes" : "No"}`}</CardDescription>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          {request.events.map((event) => (
                            <div key={event.event_id} className="flex items-center space-x-2">
                              <CalendarIcon className="h-4 w-4" />
                              <span>{new Date(event.requested_date).toDateString()}</span>
                              <span>({event.application_hour[0].toUpperCase()+event.application_hour.slice(1)})</span>
                            </div>
                          ))}
                        </CardContent>
                      </Card>
                    ))
                )}
              </ScrollArea>
            </TabsContent>

          </Tabs>
        </CardContent>
        </ScrollArea>
      </Card>
    </div>
  );
}
