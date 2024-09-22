"use client";

import { useState, useEffect} from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar } from "@/components/ui/calendar";
import {cn} from "@/lib/utils";
import {format, addMonths, subMonths} from "date-fns";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover"
import { CalendarIcon } from "lucide-react"

export default function Applications() {
  //restricted calendar
  const [date,setDate] = useState<Date|undefined>(new Date());
  const [fromDate, setFromDate] = useState<Date>(new Date());
  const [toDate, setToDate] = useState<Date>(new Date());

  const [selectedDates, setSelectedDates] = useState<Date[]>([]);
  const [activeTab, setActiveTab] = useState("apply");

  const handleDateSelect = (date: Date) => {
    setSelectedDates((prev) =>
      prev.some((d) => d.toDateString() === date.toDateString())
        ? prev.filter((d) => d.toDateString() !== date.toDateString())
        : [...prev, date]
    );
  };
  useEffect(()=>{
    const currentDate = new Date();
    setFromDate(subMonths(currentDate, 2))
    setToDate(addMonths(currentDate, 3))
  },[])

  return (
    <div className="container mx-auto p-4">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3 bg-white text-black">
          <TabsTrigger value="apply">Apply for arrangement</TabsTrigger>
          <TabsTrigger value="change">Change arrangement</TabsTrigger>
          <TabsTrigger value="withdraw">Withdraw arrangement</TabsTrigger>
        </TabsList>
        <TabsContent value="apply">
          <Card>
            <CardHeader>
              <CardTitle>Apply for Arrangement</CardTitle>
              <CardDescription>
                Submit a new arrangement request.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Arrangement Type:</Label> <br></br>
                <Label className="font-bold">WFH</Label>
              </div>
              <div className="space-y-2">
                <Label>Date:</Label><br></br>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                    variant={"outline"}
                    className={cn(
                      "w-[280px] justify-start text-left font-normal", !date && "text-muted-foreground"
                    )}>
                  <CalendarIcon className="mr-2 h-4 w-4"/>
                  {date ? format (date,"PPP") : <span>Pick a date</span>}
                  </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={date}
                      onSelect={setDate}
                      fromDate={fromDate}
                      toDate={toDate}
                      initialFocus
                    />
                  <div className="p-3 border-t">
                    <p className="">
                      Selectable range: {format(fromDate, "MMM d, yyyy")} - {format(toDate,"MMM d, yyyy")}
                    </p>
                  </div>  
                  </PopoverContent>

                </Popover>

              </div>
              <div className="space-y-2">
                <Label htmlFor="reason">Reason for Arrangement</Label>
                <Textarea
                  id="reason"
                  placeholder="Please provide a reason for your arrangement request."
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Submit Application</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="change">
          <Card>
            <CardHeader>
              <CardTitle>Change Arrangement</CardTitle>
              <CardDescription>
                Modify an existing arrangement for specific days.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="existing-arrangement">
                  Existing Arrangement
                </Label>
                <Input
                  id="existing-arrangement"
                  placeholder="Select existing arrangement"
                />
              </div>
              <div className="space-y-2">
                <Label>Select Dates to Change</Label>
                <Calendar
                  mode="multiple"
                  selected={selectedDates}
                  onSelect={() => handleDateSelect}
                  className="rounded-md border"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new-arrangement">New Arrangement</Label>
                <Input
                  id="new-arrangement"
                  placeholder="e.g., Office work, Different hours"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="change-reason">Reason for Change</Label>
                <Textarea
                  id="change-reason"
                  placeholder="Please provide a reason for changing your arrangement."
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Submit Change Request</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="withdraw">
          <Card>
            <CardHeader>
              <CardTitle>Withdraw Arrangement</CardTitle>
              <CardDescription>
                Withdraw an approved arrangement or cancel a pending request.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="arrangement-to-withdraw">
                  Select Arrangement
                </Label>
                <Input
                  id="arrangement-to-withdraw"
                  placeholder="Select arrangement to withdraw"
                />
              </div>
              <div className="space-y-2">
                <Label>Select Dates to Withdraw</Label>
                <Calendar
                  mode="multiple"
                  selected={selectedDates}
                  onSelect={() => handleDateSelect}
                  className="rounded-md border"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="withdraw-reason">Reason for Withdrawal</Label>
                <Textarea
                  id="withdraw-reason"
                  placeholder="Please provide a reason for withdrawing your arrangement."
                />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Confirm Withdrawal</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
