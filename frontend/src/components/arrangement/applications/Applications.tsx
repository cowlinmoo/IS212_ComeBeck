"use client";
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
import { format, addMonths, subMonths, isWeekend } from "date-fns";
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
import { CheckCircle2 } from "lucide-react";

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
  isRecurring: z.enum(["Yes","No"]).optional(),
  recurringType: z.enum(["Weekly","Monthly"]).optional(),
  endDate: z.date({
    required_error: "Please select a date.",
  })
  .refine((date) => !isWeekend(date), { message: "Weekends are not allowed" })
  .optional(),
  reason: z.string(),
});

interface IApplications {
  staffId: string;
  token: string;
}
const Applications: React.FC<IApplications> = ({ staffId, token }) => {
  // fetching wfh applications currently existing
  const [wfhApplications, setwfhApplications] = useState(Array);
  useEffect(() => {
    async function fetchData() {
      const headers = { Authorization: `Bearer ${token}` };
      try {
        const response = await fetch(
          "http://localhost:8080/api/application/staff/" + staffId,
          { headers }
        );
        if (!response.ok) {
          throw new Error(`GET Application API validation ERROR`);
        } else {
          const data = await response.json();
          let applications = []
          if (data.length < 1) {
            applications = []
          } else {
            for (const application of data) {
              console.log(application);
              for (const event of application["events"]) {
                const dateSplit = event["requested_date"].split("-")
                applications.push(new Date(Number(dateSplit[0]), Number(dateSplit[1])-1, Number(dateSplit[2])));
                  }
            }
            setwfhApplications(applications)
          }
        }
      } catch (error:any) {
        console.log("GET API fetching error.", error.message);
      }
    }
    fetchData();
  },[staffId, token]);

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
  },[]);

  //end date variables and restriction
  const [fromEndDate, setFromEndDate] = useState<Date>(new Date());
  const [toEndDate, setToEndDate] = useState<Date>(new Date());
  useEffect(() => {
    const currentDate = fromEndDate;
    setToEndDate(addMonths(currentDate, 3));
  },[fromEndDate]);

  // disable weekends and all dates with existing wfh arrangements or pending wfh applications
  const isDateDisabled = (date: Date) => {
    let hasApplication = false
    for (const d of wfhApplications){
      if (d.toDateString() === date.toDateString()){
        hasApplication = true
        break
      }
    }
    return isWeekend(date) || date < fromDate || date > toDate || hasApplication ;
  };
  const onlyDisableWeekend = (date: Date) => {
    return isWeekend(date) || date < fromDate || date > toDate ;
  };

  //variable to check if user selected more than 1 date for multiple dates calendar
  const [showMultipleDateAlert, setShowMultipleDateAlert] = useState(false);
  //Alert variable if no date selected when form is submitted
  const [showEmptyDateAlert, setShowEmptyDateAlert] = useState(false);
  const checkMultipleDate=(date:Date | Date[] | undefined)=>{
    if (Array.isArray(date)){
      setShowMultipleDateAlert(date.length<2)
    }
    else if (date){
      setShowMultipleDateAlert(false)
    }
  }
  //Alert variable if reason text area is not filled
  const [showEmptyReasonAlert, setShowEmptyReasonAlert] = useState(false);
  //Apply form
  const applyForm = useForm<z.infer<typeof applyFormSchema>>({
    resolver: zodResolver(applyFormSchema),
    defaultValues: {
      arrangementType: "WFH",
      isMultiple: "No",
      isRecurring: "No",
      reason: "",
    },
  });

  //Success alert if form has been successfully submitted
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);

  //Submission for apply form
  async function applySubmit(values: z.infer<typeof applyFormSchema>) {
    if (values.reason.trim() === "") {
      setShowEmptyReasonAlert(true);
    } else {
      setShowEmptyReasonAlert(false);
    }
    setShowEmptyDateAlert(
      (values.isMultiple === "No" && !values.singleDate && values.isRecurring==="No") ||
        (values.isMultiple === "Yes" &&
          (!values.multipleDate || values.multipleDate.length === 0)) || 
          (values.isMultiple === "No" && values.isRecurring==="Yes" && (!values.endDate))
    );
    if (
      showEmptyReasonAlert === false &&
      showMultipleDateAlert === false 
    ) {
      const headers = { "Authorization": `Bearer ${token}`, "Content-Type": "application/json", "accept": "application/json"};
      //singleDate selected/ recurring date 
      if (values.singleDate) {
        let content = {}
        if (values.isRecurring==="No"){
          content = {
            location: "Home",
            reason: values.reason,
            description: "",
            requested_date: format(values.singleDate, "yyyy-MM-dd"),
            staff_id: staffId,
            recurring: false,
          };
        }
        else if (values.isRecurring==="Yes" && !values.endDate===false){
          if (values.recurringType==="Weekly"){
            content = {
              location: "Home",
              reason: values.reason,
              description: "",
              requested_date: format(values.singleDate, "yyyy-MM-dd"),
              staff_id: staffId,
              recurring: true,
              recurrence_type: "weekly",
              end_date: format(values.endDate,"yyyy-MM-dd")
            };
          }
          else if (values.recurringType==="Monthly" && !values.endDate===false){
            content = {
              location: "Home",
              reason: values.reason,
              description: "",
              requested_date: format(values.singleDate, "yyyy-MM-dd"),
              staff_id: staffId,
              recurring: true,
              recurrence_type: "monthly",
              end_date: format(values.endDate,"yyyy-MM-dd")
            };
          }
        }
        console.log(content);
        try {
          const response = await fetch(
            "http://localhost:8080/api/application/",
            { headers: headers, method: "POST", body: JSON.stringify(content) }
          );
          if (!response.ok) {
            console.log(await response.json());
            throw new Error(`POST Application API validation ERROR`);
          } else {
            console.log(response.json());
            setShowSuccessAlert(true);
            //reset form once submission is successful
            applyForm.reset();
            //set timeout for alert
            setTimeout(() => setShowSuccessAlert(false), 5000);
          }
        } catch (error: any) {
          console.log("POST API fetching error.", error.message);
        }
      } 
      //multiple dates selected
      else if (values.multipleDate) {
        const events = [];
        let count = 0;
        for (const d of values.multipleDate) {
          count += 1;
          if (count !== 1) {
            events.push({"requested_date":format(d, "yyyy-MM-dd")});
          }
        }
        console.log(values.multipleDate[0])
        console.log(events)
        const multiContent = {
          location: "Home",
          reason: values.reason,
          requested_date: format(values.multipleDate[0], "yyyy-MM-dd"),
          description: "",
          staff_id: staffId,
          recurring: false,
          events: events,
        };
        try {
          const response = await fetch(
            "http://localhost:8080/api/application/",
            {
              headers: headers,
              method: "POST",
              body: JSON.stringify(multiContent),
            }
          );
          if (!response.ok) {
            console.log(await response.json());
            throw new Error(`POST Application API validation ERROR`);
          } else {
            console.log(response.json());
            setShowSuccessAlert(true);
            //reset form once submission is successful
            applyForm.reset();
            //set timeout for alert
            setTimeout(() => setShowSuccessAlert(false), 5000);
          }
        } catch (error: any) {
          console.log("POST API fetching error.", error.message);
        }
      }
    }
  }

  return (
    <div className="container mx-auto p-4">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full h-full grid-cols-3 bg-white text-black ">
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
                  {showMultipleDateAlert && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Warning</AlertTitle>
                      <AlertDescription>
                        Please select at least 2 dates for the multiple dates
                        calendar option.
                      </AlertDescription>
                    </Alert>
                  )}
                  {showEmptyReasonAlert && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Warning</AlertTitle>
                      <AlertDescription>
                        Please indicate the reason for your application.
                      </AlertDescription>
                    </Alert>
                  )}
                  {showEmptyDateAlert && (
                    <Alert variant="destructive">
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle>Warning</AlertTitle>
                      <AlertDescription>
                        No date has been selected.
                      </AlertDescription>
                    </Alert>
                  )}
                  {showSuccessAlert && (
                    <Alert
                      variant="default"
                      className="bg-green-100 border-green-500"
                    >
                      <CheckCircle2 className="h-4 w-4 text-green-600" />
                      <AlertTitle className="text-green-800">
                        Success
                      </AlertTitle>
                      <AlertDescription className="text-green-700">
                        Your WFH request has been successfully submitted.
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
                              field.onChange(value);
                              if (value === "No") {
                                applyForm.setValue("multipleDate", undefined);
                              } else {
                                applyForm.setValue("singleDate", undefined);
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
                    <>
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
                                  field.onChange(date);
                                  setFromEndDate(date)
                                  
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
                    <FormField
                    control={applyForm.control}
                    name="isRecurring"
                    render= {({field})=> (
                      <FormItem>
                        <FormLabel>Is a recurring arrangement?</FormLabel>
                        <FormControl>
                            <RadioGroup
                            onValueChange={(value)=>{
                              field.onChange(value)
                              if (value === "No"){
                                applyForm.setValue("dateRange", undefined)
                              }
                            }}
                            defaultValue= {field.value}
                            className="flex flex-col space-y-1"
                            >
                              <FormItem className="flex items-center space-x-3 space-y-0">
                                <FormControl>
                                  <RadioGroupItem value = "Yes"/>
                                </FormControl>
                                <FormLabel className="font-normal">
                                  Yes
                                </FormLabel>
                              </FormItem>
                              <FormItem className="flex items-center space-x-3 space-y-0">
                              <FormControl>
                                  <RadioGroupItem value = "No"/>
                                </FormControl>
                                <FormLabel className="font-normal">
                                  No
                                </FormLabel>
                              </FormItem>
                            </RadioGroup>
                          </FormControl>
                      </FormItem>
                    )}/>
                    
                    {applyForm.watch("isRecurring") === "Yes" && (
                      <>
                      <FormField
                      control={applyForm.control}
                      name="recurringType"
                      render= {({field})=> (
                        <FormItem>
                          <FormLabel>What is the recurring type?</FormLabel>
                          <FormControl>
                            <RadioGroup
                            onValueChange={(value)=>{
                              field.onChange(value)
                            }}
                            defaultValue= {field.value}
                            className="flex flex-col space-y-1"
                            >
                              <FormItem className="flex items-center space-x-3 space-y-0">
                                <FormControl>
                                  <RadioGroupItem value = "Weekly"/>
                                </FormControl>
                                <FormLabel className="font-normal">
                                  Weekly
                                </FormLabel>
                              </FormItem>
                              <FormItem className="flex items-center space-x-3 space-y-0">
                              <FormControl>
                                  <RadioGroupItem value = "Monthly"/>
                                </FormControl>
                                <FormLabel className="font-normal">
                                  Monthly
                                </FormLabel>
                              </FormItem>
                            </RadioGroup>
                          </FormControl>
                        </FormItem>
                      )}/>
                      <FormField
                      control={applyForm.control}
                      name="endDate"
                      render={({ field }) => (
                        <FormItem className="flex flex-col">
                          <FormLabel>End date for recurring arrangement:</FormLabel>
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
                                  field.onChange(date);
                                  
                                }}
                                fromDate={fromEndDate}
                                toDate={toEndDate}
                                disabled={onlyDisableWeekend}
                                initialFocus
                              />
                              <div className="p-3 border-t">
                                <p className="text-s text-muted-foreground">
                                  Selectable range:{" "}
                                  {format(fromEndDate, "MMM d, yyyy")} -{" "}
                                  {format(toEndDate, "MMM d, yyyy")}
                                </p>
                              </div>
                            </PopoverContent>
                          </Popover>
                        </FormItem>
                      )}
                    />
                      </>
                    )
                    }
                    </>
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
                                  field.onChange(dates);
                                  checkMultipleDate(dates);
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
                          <Textarea
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
