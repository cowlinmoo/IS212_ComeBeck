"use client";

import { headers } from "next/headers";
import { useState, useEffect } from "react";
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
import { cn } from "@/lib/utils";
import { format, addMonths, subMonths, isWeekend,isSameDay } from "date-fns";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { CalendarIcon } from "lucide-react";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertTriangle } from "lucide-react";

//formschema
const applyFormSchema = z.object({
  arangementType: z.string().default("WFH"),
  isMultiple: z.enum(["Yes", "No"], {
    required_error: "Please specify if this is for multiple dates.",
  }),
  singleDate: z
    .date({
      required_error: "Please select a date.",
    })
    .refine((date) => !isWeekend(date), { message: "Weekends are not allowed" })
    .optional(),
  multipleDate: z
    .array(
      z.date({
        required_error: "Please select dates (at least 2), excluding weekends.",
      })
    )
    .refine(
      (dates) => dates.length > 1 && dates.every((date) => !isWeekend(date)),
      { message: "Please select dates (at least 2), excluding weekends." }
    )
    .optional(),
  reason: z.string(),
});

interface IApplications {
  staffId: string;
  token: string;
}
const Applications: React.FC<IApplications> = ({ staffId, token }) => {

  // fetching wfh applications currently existing
  const [wfhApproved, setwfhApproved] = useState(Array);
  const [wfhPending, setwfhPending] = useState(Array);
  useEffect(() => {
    async function fetchData() {
      const headers = { Authorization: `Bearer ${token}` };
      try {
        const response = await fetch(
          "http://localhost:8080/api/application/staff/" + staffId,
          { headers }
        );
        if (!response.ok) {
          throw new Error(`Application API validation ERROR`);
        } else {
          const data = await response.json();
          var approvedApplications = new Array();
          var pendingApplications = new Array();
          if (data.length < 1) {
            approvedApplications = [];
            pendingApplications = [];
          } else {
            for (var application of data) {
              console.log(application);
              // check if application is approved or pending and add them to the array variables
              if (application["status"] == "approved") {
                for (var event of application["events"]) {
                  approvedApplications.push(event["requested_date"]);
                }
              } else if (application["status"] == "pending") {
                for (var event of application["events"]) {
                  pendingApplications.push(event["requested_date"]);
                }
              }
            }
            setwfhApproved(approvedApplications);
            setwfhPending(pendingApplications);
          }
        }
      } catch (error: any) {
        console.log("API fetching error.", error.message);
      }
    }
    fetchData();
  }, []);

  // restricted calendar
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
  useEffect(() => {
    const currentDate = new Date();
    setFromDate(subMonths(currentDate, 2));
    setToDate(addMonths(currentDate, 3));
  }, []);

  // disable weekends
  const isDateDisabled = (date: Date) => {
    return isWeekend(date) || date < fromDate || date > toDate;
  };

  //alert variable for existing approved and pending arrangements
  const [showAlertApproved, setShowAlertApproved] = useState(false);
  const [showAlertPending, setShowAlertPending] = useState(false);
  const [alertApprovedDates, setAlertApprovedDates] = useState("");
  const [alertPendingDates, setAlertPendingDates] = useState("");

  //variable to check if user selected more than 1 date for multiple dates calendar
  const [showMultipleDateAlert, setShowMultipleDateAlert] = useState(false)

  //check if selected date has already been approved user selected more than 1 date for multiple dates calendar
  const checkForAlertApproved = (date: Date | Date[] | undefined) => {
    //all dates to be alerted
    setAlertApprovedDates("")
    setShowAlertApproved(false)
    setShowMultipleDateAlert(false)
    console.log(date)
    console.log(isSameDay(date,"2024-10-10"))
    if (Array.isArray(date)) {
      setShowMultipleDateAlert(date.length<2)
      for (var d of date) {
        for (var i of wfhApproved){
          if (isSameDay(i,d)){
            setShowAlertApproved(true);
            setAlertApprovedDates(alertApprovedDates + " " + d.toLocaleDateString() )
          }
        }
      }
    } else if (date) {
      for (var i of wfhApproved){
        if (isSameDay(i,date)){
          setShowAlertApproved(true)
          setAlertApprovedDates(alertApprovedDates + " " + date.toLocaleDateString() )
          console.log(alertApprovedDates)
        }
      }
    } else {
      setShowAlertApproved(false)
    }
  };
  //check if selected date has a pending application
  const checkForAlertPending = (date: Date | Date[] | undefined) => {
    setShowAlertPending(false);
    setAlertPendingDates("")
    //all dates to be alerted
    if (Array.isArray(date)) {
      for (var d of date) {
        if (wfhPending.includes(d)) {
          setShowAlertPending(true);
          setAlertPendingDates(alertPendingDates + " " + d.toLocaleDateString())
        }
      }
    } else if (date) {
      if (wfhPending.includes(date)) {
        setShowAlertPending(true);
        setAlertPendingDates(alertPendingDates + " " + date.toLocaleDateString())
      }
    } else {
      setShowAlertPending(false);
    }
  };


  //Apply form
  const applyForm = useForm<z.infer<typeof applyFormSchema>>({
    resolver: zodResolver(applyFormSchema),
    defaultValues: {
      arrangementType: "WFH",
      isMultiple: "No",
      reason: "",
    },
  });

  //Submission for apply form
  function applySubmit(values: z.infer<typeof applyFormSchema>) {

  }


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
            <Form {...applyForm}>
              <form onSubmit={applyForm.handleSubmit(applySubmit)}>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Arrangement Type:</Label> <br></br>
                    <Label className="font-bold">WFH</Label>
                  </div>
                  {showAlertApproved && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Warning</AlertTitle>
                      <AlertDescription>
                        You have selected {alertApprovedDates}. The date(s)
                        cannot be selected as they have existing WFH
                        arrangements.
                      </AlertDescription>
                    </Alert>
                  )}
                  {showAlertPending && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Warning</AlertTitle>
                      <AlertDescription>
                        You have selected {alertPendingDates}. The date(s)
                        cannot be selected as they have pending WFH arrangement
                        applications yet to be approved.
                      </AlertDescription>
                    </Alert>
                  )}
                  {showMultipleDateAlert && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Warning</AlertTitle>
                      <AlertDescription>
                        Please select at least 2 dates for the multiple dates calendar option.
                      </AlertDescription>
                    </Alert>
                  )}
                  <FormField
                    control={applyForm.control}
                    name="isMultiple"
                    render={({ field }) => (
                      <FormItem className="space-y-3">
                        <FormLabel>Is this for multiple dates?</FormLabel>
                        <FormControl>
                          <RadioGroup
                            onValueChange={(value) => {
                              field.onChange(value)
                              if (value === "No") {
                                applyForm.setValue("multipleDate", undefined);
                                checkForAlertApproved(
                                  applyForm.getValues("singleDate")
                                );
                                checkForAlertPending(
                                  applyForm.getValues("singleDate")
                                );
                              } else {
                                applyForm.setValue("singleDate", undefined);
                                checkForAlertApproved(
                                  applyForm.getValues("multipleDate")
                                );
                                checkForAlertPending(
                                  applyForm.getValues("multipleDate")
                                );
                              }
                            }}
                            defaultValue={field.value}
                            className="flex flex-col space-y-1"
                          >
                            <FormItem className="flex items-center space-x-3 space-y-0">
                              <FormControl>
                                <RadioGroupItem value="Yes" />
                              </FormControl>
                              <FormLabel className="font-normal">Yes</FormLabel>
                            </FormItem>
                            <FormItem className="flex items-center space-x-3 space-y-0">
                              <FormControl>
                                <RadioGroupItem value="No" />
                              </FormControl>
                              <FormLabel className="font-normal">No</FormLabel>
                            </FormItem>
                          </RadioGroup>
                        </FormControl>
                      </FormItem>
                    )}
                  />
                  {applyForm.watch("isMultiple") === "No" && (
                    <FormField
                      control={applyForm.control}
                      name="singleDate"
                      render={({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel>Date:</FormLabel>
                          <Popover>
                            <PopoverTrigger asChild>
                              <FormControl>
                                <Button
                                  variant={"outline"}
                                  className={cn(
                                    "w-[240px] justify-start text-left font-normal",
                                    !field.value && "text-muted-foreground"
                                  )}
                                >
                                  {field.value ? (
                                    format(field.value, "PPP")
                                  ) : (
                                    <span>Pick a date</span>
                                  )}
                                  <CalendarIcon className="mr-2 h-4 w-4" />
                                </Button>
                              </FormControl>
                            </PopoverTrigger>
                            <PopoverContent>
                              <Calendar
                                mode="single"
                                selected={field.value}
                                onSelect={(date) => {
                                  field.onChange(date)
                                  checkForAlertApproved(date)
                                  checkForAlertPending(date)
                                }}
                                fromDate={fromDate}
                                toDate={toDate}
                                disabled={isDateDisabled}
                                initialFocus
                              />
                              <div className="p-3 border-t">
                                <p className="text-s text-muted-foreground">
                                  Selectable range:{" "}
                                  {format(fromDate, "MMM d, yyyy")} -{" "}
                                  {format(toDate, "MMM d, yyyy")}
                                </p>
                              </div>
                            </PopoverContent>
                          </Popover>
                        </FormItem>
                      )}
                    />
                  )}
                  {applyForm.watch("isMultiple") === "Yes" && (
                    <FormField
                      control={applyForm.control}
                      name="multipleDate"
                      render={({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel>Dates:</FormLabel>
                          <Popover>
                            <PopoverTrigger asChild>
                              <FormControl>
                                <Button
                                  variant={"outline"}
                                  className={cn(
                                    "w-[240px] justify-start text-left font-normal",
                                    !field.value && "text-muted-foreground"
                                  )}
                                >
                                  {field.value && field.value.length > 0 ? (
                                    `${field.value.length} date(s) selected`
                                  ) : (
                                    <span>Pick at least 2 dates</span>
                                  )}
                                  <CalendarIcon className="mr-2 h-4 w-4" />
                                </Button>
                              </FormControl>
                            </PopoverTrigger>
                            <PopoverContent>
                              <Calendar
                                mode="multiple"
                                selected={field.value}
                                onSelect={(dates) => {
                                  field.onChange(dates)
                                  checkForAlertApproved(dates)
                                  checkForAlertPending(dates)
                                }}
                                fromDate={fromDate}
                                toDate={toDate}
                                disabled={isDateDisabled}
                                initialFocus
                              />
                              <div className="p-3 border-t">
                                <p className="text-s text-muted-foreground">
                                  Selectable range:{" "}
                                  {format(fromDate, "MMM d, yyyy")} -{" "}
                                  {format(toDate, "MMM d, yyyy")}
                                </p>
                              </div>
                            </PopoverContent>
                          </Popover>
                        </FormItem>
                      )}
                    />
                  )}
                  <FormField
                    control={applyForm.control}
                    name="reason"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Reason for arrangement:</FormLabel>
                        <FormControl>
                          <Input
                            placeholder="Please provide a reason for your arrangement request."
                            {...field}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </CardContent>
                <CardFooter>
                  <Button type="submit">Submit Application</Button>
                </CardFooter>
              </form>
            </Form>
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
};
export default Applications;
