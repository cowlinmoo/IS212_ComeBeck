/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { TabsContent } from "@/components/ui/tabs";
import { subWeeks, addWeeks, getYear, addYears,subYears, getMonth, addMonths, subMonths, format, isWeekend} from "date-fns";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Form,
  FormControl,
  FormDescription,
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
import { CheckCircle2, Loader2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableHead,
  TableCell,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { CalendarIcon } from "lucide-react";
import { Calendar } from "@/components/ui/calendar";
import { cn } from "@/lib/utils";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;

//formschema
const changeFormSchema = z.object({
  arrangementType: z.enum(["Pending Approval", "Approved"], {
    required_error: "Please specify your arrangement type",
  }),
  selectedArrangement: z
    .object({
      eventID: z.string(),
      applicationID: z.string()
    })
    .default({
      eventID: "",
      applicationID: "",
    }),
  singleDate: z
    .object({
      date: z.date(),
      hour: z.enum(["fullday", "am", "pm"]),
    })
    .optional(),
  reason: z.string(),
});

interface IApplications {
  staffId: string | undefined;
  token: string | undefined;
}
const Apply_Change: React.FC<IApplications> = ({ staffId, token }) => {
  const [isLoading, setIsLoading] = useState(false)
  //Success alert if form has been successfully submitted
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);
  //alert if no selection of arrangement
  const [showNoSelectionAlert, setShowNoSelectionAlert] = useState(false);
  //filtering
  const [filteredpendingArrangements, setFilteredPendingArrangements] =
    useState(Array);
  const [selectMonth, setSelectMonth] = useState<string>("");
  const [selectYear, setSelectYear] = useState<string>("");

  // fetching wfh applications currently existing
  const [appovedApplications, setApprovedApplications] = useState(Array);
  const [pendingApplications, setPendingApplications] = useState(Array);

  //all months for pending application filtering
  const [filterMonths, setFilterMonths] = useState(Array);

  

  useEffect(() => {
    async function fetchData() {
      const headers = { Authorization: `Bearer ${token}` };
      try {
        const response = await fetch(
          `${URL}/staff/` + staffId,
          { headers }
        );
        if (!response.ok) {
          throw new Error(`GET Application API validation ERROR`);
        } else {
          const data = await response.json();
          let approvedApplications = [];
          let pendingApplications = [];
          let filterMonths: number[]=[];
          if (data.length < 1) {
            pendingApplications = [];
            approvedApplications = [];
            filterMonths = [];
          } else {
            for (const application of data) {
              let type = "";
              if (application["status"] === "pending" && (application["application_state"]==="new_application"  ||
              ( (application["application_state"]==="change_request") &&  (application["status"]==="approved"))) ) {
                if (application["events"].length === 1) {
                  type = "Single";
                  const dateSplit =
                    application["events"][0]["requested_date"].split("-");
                  const date = new Date(
                    Number(dateSplit[0]),
                    Number(dateSplit[1]) - 1,
                    Number(dateSplit[2])
                  );
                  if (filterMonths.includes(getMonth(date))===false){
                    filterMonths.push(getMonth(date))
                  }
                  pendingApplications.push({
                    application_type: type,
                    date: date,
                    hour: application["events"][0]["application_hour"],
                    application_id: application["application_id"].toString(),
                    event_id: application["events"][0]["event_id"].toString(),
                  });
                } else {
                  if (application["recurring"] === true) {
                    type = "Recurring";
                    for (const event of application["events"]) {
                      const dateSplit = event["requested_date"].split("-");
                      const date = new Date(
                        Number(dateSplit[0]),
                        Number(dateSplit[1]) - 1,
                        Number(dateSplit[2])
                      );
                      pendingApplications.push({
                        application_type: type,
                        date: date,
                        hour: event["application_hour"],
                        application_id: application["application_id"].toString(),
                        event_id: event["event_id"].toString(),
                      });
                    }
                  } else {
                    type = "Multiple";
                    for (const event of application["events"]) {
                      const dateSplit = event["requested_date"].split("-");
                      const date = new Date(
                        Number(dateSplit[0]),
                        Number(dateSplit[1]) - 1,
                        Number(dateSplit[2])
                      );
                      pendingApplications.push({
                        application_type: type,
                        date: date,
                        hour: event["application_hour"],
                        application_id: application["application_id"].toString(),
                        event_id: event["event_id"].toString(),
                      });
                    }
                  }
                }
              } else if (application["status"] === "approved" &&  (application["application_state"]==="new_application"  ||
              ( (application["application_state"]==="change_request") &&  (application["status"]==="approved"))) ) {
                if (application["events"].length === 1) {
                  type = "Single";
                  const dateSplit =
                    application["events"][0]["requested_date"].split("-");
                  const date = new Date(
                    Number(dateSplit[0]),
                    Number(dateSplit[1]) - 1,
                    Number(dateSplit[2])
                  );
                  const currentDate = new Date();
                  if (date === currentDate) {
                    approvedApplications.push({
                      application_type: type,
                      date: date,
                      hour: application["events"][0]["application_hour"],
                      application_id: application["application_id"].toString(),
                      event_id: application["events"][0]["event_id"].toString(),
                    });
                  } else if (date > currentDate) {
                    const futureBoundary = addWeeks(currentDate, 2);
                    if (date <= futureBoundary) {
                      approvedApplications.push({
                        application_type: type,
                        date: date,
                        hour: application["events"][0]["application_hour"],
                        application_id: application["application_id"].toString(),
                        event_id: application["events"][0]["event_id"].toString(),
                      });
                    }
                  } else {
                    const pastBoundary = subWeeks(currentDate, 2);
                    if (date >= pastBoundary) {
                      approvedApplications.push({
                        application_type: type,
                        date: date,
                        hour: application["events"][0]["application_hour"],
                        application_id: application["application_id"].toString(),
                        event_id: application["events"][0]["event_id"].toString(),
                      });
                    }
                  }
                } else {
                  if (application["recurring"] === true) {
                    type = "Recurring";
                    const currentDate = new Date();
                    const futureBoundary = addWeeks(currentDate, 2);
                    const pastBoundary = subWeeks(currentDate, 2);
                    for (const event of application["events"]) {
                      const dateSplit = event["requested_date"].split("-");
                      const date = new Date(
                        Number(dateSplit[0]),
                        Number(dateSplit[1]) - 1,
                        Number(dateSplit[2])
                      );
                      if (date === currentDate) {
                        approvedApplications.push({
                          application_type: type,
                          date: date,
                          hour: event["application_hour"],
                          application_id: application["application_id"].toString(),
                          event_id: event["event_id"].toString(),
                        });
                      } else if (date > currentDate) {
                        if (date <= futureBoundary) {
                          approvedApplications.push({
                            application_type: type,
                            date: date,
                            hour: event["application_hour"],
                            application_id: application["application_id"].toString(),
                            event_id: event["event_id"].toString(),
                          });
                        }
                      } else {
                        if (date >= pastBoundary) {
                          approvedApplications.push({
                            application_type: type,
                            date: date,
                            hour: event["application_hour"],
                            application_id: application["application_id"].toString(),
                            event_id: event["event_id"].toString(),
                          });
                        }
                      }
                    }
                  } else {
                    type = "Multiple";
                    const currentDate = new Date();
                    const futureBoundary = addWeeks(currentDate, 2);
                    const pastBoundary = subWeeks(currentDate, 2);
                    for (const event of application["events"]) {
                      const dateSplit = event["requested_date"].split("-");
                      const date = new Date(
                        Number(dateSplit[0]),
                        Number(dateSplit[1]) - 1,
                        Number(dateSplit[2])
                      );
                      if (date === currentDate) {
                        approvedApplications.push({
                          application_type: type,
                          date: date,
                          hour: event["application_hour"],
                          application_id: application["application_id"].toString(),
                          event_id: event["event_id"].toString(),
                        });
                      } else if (date > currentDate) {
                        if (date <= futureBoundary) {
                          approvedApplications.push({
                            application_type: type,
                            date: date,
                            hour: event["application_hour"],
                            application_id: application["application_id"].toString(),
                            event_id: event["event_id"].toString(),
                          });
                        }
                      } else {
                        if (date >= pastBoundary) {
                          approvedApplications.push({
                            application_type: type,
                            date: date,
                            hour: event["application_hour"],
                            application_id: application["application_id"].toString(),
                            event_id: event["event_id"].toString(),
                          });
                        }
                      }
                    }
                  }
                }
              }
            }
            setApprovedApplications(approvedApplications);
            setPendingApplications(pendingApplications);
            setFilterMonths(filterMonths)
          }
        }
      } catch (error: any) {
        console.log("GET API fetching error.", error.message);
      }
    }
    fetchData();
  }, [staffId, token]);

  //filter
  useEffect(() => {
    const filtered = pendingApplications.filter((arrangement:any) => {
      const arrangementMonth = arrangement.date.getMonth();
      const arrangementYear = arrangement.date.getFullYear();
      return (
        (!selectMonth || arrangementMonth.toString() === selectMonth) &&
        (!selectYear || arrangementYear.toString() === selectYear)
      );
    });
    setFilteredPendingArrangements(filtered);
  }, [selectMonth, selectYear, pendingApplications]);

  //Alert variable if reason text area is not filled
  const [showEmptyReasonAlert, setShowEmptyReasonAlert] = useState(false);
  //Alert variable if no date selected when form is submitted
  const [showEmptyDateAlert, setShowEmptyDateAlert] = useState(false);

  //Apply form
  const changeForm = useForm<z.infer<typeof changeFormSchema>>({
    resolver: zodResolver(changeFormSchema),
    defaultValues: {
      arrangementType: "Pending Approval",
      selectedArrangement: { eventID: "", applicationID: "" },
      reason: "",
    },
  });
  function resetFilters() {
    setSelectMonth("");
    setSelectYear("");
    setFilteredPendingArrangements(pendingApplications);
  }
  // filter year boundaries
  const currentYear = getYear(new Date());
  const aheadYear = getYear(addYears(new Date(), 1));
  const behindYear = getYear(subYears(new Date(), 1));

  // restricted calendar
  const [fromDate, setFromDate] = useState<Date>(new Date());
  const [toDate, setToDate] = useState<Date>(new Date());

  useEffect(() => {
    const currentDate = new Date();
    setFromDate(subMonths(currentDate, 2));
    setToDate(addMonths(currentDate, 3));
  }, []);

  interface WFHEvent {
    event_id: string;
    date: Date;
    hour: 'fullday' | 'am' | 'pm';
  }

  interface WFHApplication {
    application_id: string;
    recurring: boolean;
    events: WFHEvent[]; 
  }
  const [wfhApplications, setwfhApplications] = useState<WFHApplication[]>([]);
  useEffect(() => {
    async function fetchData() {
      const headers = { Authorization: `Bearer ${token}` };
      try {
        const response = await fetch(`${URL}/staff/` + staffId, { headers });
        if (!response.ok) {
          throw new Error(`GET Application API validation ERROR`);
        } else {
          const data = await response.json();
          let applications: WFHApplication[] = [];
          if (data.length < 1) {
            applications = [];
          } else {
            applications = data.map((application: any) => ({
              application_id: application.application_id.toString(),
              recurring: application.recurring,
              events: application.events.map((event: any) => {
                const dateSplit = event.requested_date.split("-");
                return {
                  event_id: event.event_id,
                  date: new Date(
                    Number(dateSplit[0]),
                    Number(dateSplit[1]) - 1,
                    Number(dateSplit[2])
                  ),
                  hour: event.application_hour as 'fullday' | 'am' | 'pm',
                };
              }),
            }));
            setwfhApplications(applications);
          }
        }
      } catch (error: any) {
        console.log("GET API fetching error.", error.message);
      }
    }
    fetchData();
  }, [staffId, token]);
  // console.log(wfhApplications)

  // // disable weekends and all dates with existing wfh arrangements or pending wfh applications
  const isDateDisabled = (date: Date) => {
    let hasApplication = false;
    const dateCount: { [key: string]: number } = {};
    for (const application of wfhApplications) {
      for (const d of application.events){
        if ((d.date as Date).toDateString() === date.toDateString()) {
          if (d.hour === "fullday"){
            hasApplication = true;
            break;
          }
          if (d.date.toDateString() in dateCount){
            hasApplication = true;
            break
          }
          else{
            dateCount[d.date.toDateString()] = 1
          }
        }
      }
    }
    return (
      isWeekend(date) || date < fromDate || date > toDate || hasApplication
    );
  };
  const isAMButtonDisabled = (date:Date) =>{
    let hasApplication = false;
    for (const application of wfhApplications) {
      for (const d of application.events){
        if ((d.date as Date).toDateString() === date.toDateString()) {
          if (d.hour === "am"){
            hasApplication = true;
            break;
          }
        }
      }
    }
    return hasApplication
  }
  const isPMButtonDisabled = (date:Date) =>{
    let hasApplication = false;
    for (const application of wfhApplications) {
      for (const d of application.events){
        if ((d.date as Date).toDateString() === date.toDateString()) {
          if (d.hour === "pm"){
            hasApplication = true;
            break;
          }
        }
      }
    }
    return hasApplication

  }
  const isFULLDAYButtonDisabled = (date:Date) =>{
    let hasApplication = false;
    for (const application of wfhApplications) {
    for (const d of application.events) {
      if ((d.date as Date).toDateString() === date.toDateString()) {
        if (d.hour === "pm" || d.hour==="am"){
          hasApplication = true;
          break;
        }
      }
    }}
    return hasApplication

  }
  const [selectedDate, setSelectedDate] = useState<Date | undefined>()
  interface Arrangement {
    eventID: string, 
    applicationID: string
  }
  const [selectedArrangement, setSelectedArrangement] = useState<Arrangement>()


  //Submission for apply form
  async function applySubmit(values: z.infer<typeof changeFormSchema>) {
    setShowEmptyReasonAlert(false);
    setShowNoSelectionAlert(false);
    setShowEmptyDateAlert(false);
    if (values.reason.trim() === "") {
      setShowEmptyReasonAlert(true);
    } 
    if (!values.selectedArrangement.eventID) {
      setShowNoSelectionAlert(true);
    }
    if (!values.singleDate?.date) {
      setShowEmptyDateAlert(true)
    }
    if (values.reason !=="" && showNoSelectionAlert === false && values.singleDate) {
      const headers = {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        accept: "application/json",
      };
      //
      console.log(values.selectedArrangement.applicationID);
      console.log(values.selectedArrangement.eventID);
      
      const changeEvents = []
      let requested_date = ""
      let application_hour =""

      for (const application of wfhApplications){
        if (application.application_id === values.selectedArrangement.applicationID){
          let count = 0
          for (const event of application.events){
            count += 1
            console.log(event.event_id)
            console.log(values.selectedArrangement.eventID)
            console.log(typeof event.event_id )
            console.log(typeof values.selectedArrangement.eventID)

            if (event.event_id.toString() === values.selectedArrangement.eventID){
              if (count ==1){
                console.log(values.singleDate.date)
                requested_date = format(values.singleDate.date, "yyyy-MM-dd")
                application_hour = values.singleDate.hour
              }
              else{
                console.log(values.singleDate.date)
                changeEvents.push({
                  "application_hour":values.singleDate.hour,
                  "requested_date": format(values.singleDate.date, "yyyy-MM-dd")
                })
              }
            }
            else{
              if (count ==1){
                console.log(event.date)
                requested_date = format(event.date, "yyyy-MM-dd")
                application_hour = event.hour
              }
              else{
                console.log(event.date)
                changeEvents.push({
                  "application_hour":event.hour,
                  "requested_date": format(event.date, "yyyy-MM-dd")
                })
              }
            }
          }
        }
      }
      const content = {
        "location": "Home",
        "reason": values.reason,
        "requested_date": requested_date,
        "application_hour": application_hour,
        "description": "",
        "staff_id": staffId,
        "events": changeEvents 
      };
        console.log(content);
        setIsLoading(true)
        try {
          const response = await fetch(
            `${URL}/` +
              values.selectedArrangement.applicationID,
            { headers: headers, method: "PUT", body: JSON.stringify(content) }
          );
          if (!response.ok) {
            console.log(await response.json());
            throw new Error(`POST Application API validation ERROR`);
          } else {
            console.log(response.json());
            
            setShowSuccessAlert(true);
            //reset form once submission is successful
            changeForm.reset();
            //set timeout for alert
            setTimeout(() => setShowSuccessAlert(false), 5000);
          }
        } catch (error: any) {
          console.log("POST API fetching error.", error.message);
        }
        finally {
          setIsLoading(false)
        }
    }
  
  }

  return (
    <TabsContent value="change">
      <Card>
        <CardHeader>
          <CardTitle>Change Arrangement</CardTitle>
          <CardDescription>
            Change an approved arrangement or a pending request.
          </CardDescription>
        </CardHeader>
        <Form {...changeForm}>
          <form onSubmit={changeForm.handleSubmit(applySubmit)}>
            <CardContent className="space-y-4">
              {showEmptyReasonAlert && (
                <Alert variant="destructive">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>Warning</AlertTitle>
                  <AlertDescription>
                    Please indicate the reason for your change.
                  </AlertDescription>
                </Alert>
              )}
              {showNoSelectionAlert && (
                <Alert variant="destructive">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>Warning</AlertTitle>
                  <AlertDescription>
                    No arrangement has been chosen
                  </AlertDescription>
                </Alert>
              )}
              {isLoading && (
                <div className="flex justify-center items-center">
                  <Loader2 className="h-6 w-6 animate-spin" />
                  <span className="ml-2">Submitting change request...</span>
                </div>
              )}
              {showSuccessAlert && (
                <Alert
                  variant="default"
                  className="bg-green-100 border-green-500"
                >
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  <AlertTitle className="text-green-800">Success</AlertTitle>
                  <AlertDescription className="text-green-700">
                    Your change request has been
                    successfully submitted.
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
              <FormField
                control={changeForm.control}
                name="arrangementType"
                render={({ field }) => (
                  <FormItem className="space-y-3">
                    <FormLabel>
                      Select which arrangement would you like to
                      change?
                    </FormLabel>
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        className="flex flex-col space-y-1"
                      >
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="Pending Approval" />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Pending Approval
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="Approved" />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Approved{" "}
                          </FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                  </FormItem>
                )}
              />
              {changeForm.watch("arrangementType") ===
                "Pending Approval" && (
                <>
                  <div className="space-y-4">
                    <div className="flex space-x-4">
                      <Select
                        onValueChange={setSelectMonth}
                        value={selectMonth}
                      >
                        <SelectTrigger className="w-[180px]">
                          <SelectValue placeholder="Select month" />
                        </SelectTrigger>
                        <SelectContent>
                          {filterMonths.map((month:any) => (
                            <SelectItem key={month} value={month.toString()}>
                            {new Date(2000, month, 1).toLocaleString(
                              "default",
                              { month: "long" }
                            )}
                          </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <Select onValueChange={setSelectYear} value={selectYear}>
                        <SelectTrigger className="w-[180px]">
                          <SelectValue placeholder="Select year" />
                        </SelectTrigger>
                        <SelectContent>
                          {[behindYear, currentYear, aheadYear].map((year) => (
                            <SelectItem key={year} value={year.toString()}>
                              {year}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <Button
                        type="button"
                        variant="outline"
                        size="icon"
                        onClick={resetFilters}
                        className="h-10 px-6"
                      >
                        Reset
                      </Button>
                    </div>
                  </div>
                  <FormField
                    control={changeForm.control}
                    name="selectedArrangement"
                    render={({ field }) => (
                      <FormItem className="flex flex-col">
                        <FormLabel>
                          Select a pending arrangement to change
                        </FormLabel>
                        <FormControl>
                          <Table>
                            <TableHeader>
                              <TableRow>
                                <TableHead className="w-[100px]">
                                  Select
                                </TableHead>
                                <TableHead>Application ID</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Time</TableHead>
                              </TableRow>
                            </TableHeader>
                            <TableBody>
                              {filteredpendingArrangements.map(
                                (arrangement:any) => (
                                  <TableRow key={arrangement.event_id}>
                                    <TableCell className="font-medium">
                                      <RadioGroup
                                        onValueChange={(value) =>{
                                          field.onChange({
                                            eventID: value,
                                            applicationID:
                                              arrangement.application_id,
                                          })
                                          setSelectedArrangement({
                                            eventID: value,
                                            applicationID:
                                              arrangement.application_id,
                                          })
                                        }}
                                        value={field.value.eventID}
                                        className="space-y-1"
                                      >
                                        <RadioGroupItem
                                          value={arrangement.event_id}
                                          id={arrangement.event_id}
                                        />
                                        <label
                                          htmlFor={arrangement.event_id}
                                          className="flex items-center space-x-2 cursor-pointer"
                                        >
                                          <span className="sr-only">
                                            Select arrangement
                                          </span>
                                        </label>
                                      </RadioGroup>
                                    </TableCell>
                                    <TableCell>
                                      {arrangement.application_id}
                                    </TableCell>
                                    <TableCell>
                                      {arrangement.date.toLocaleDateString()}
                                    </TableCell>
                                    <TableCell>
                                      {arrangement.application_type}
                                    </TableCell>
                                    <TableCell>
                                      {arrangement.hour}
                                    </TableCell>
                                  </TableRow>
                                )
                              )}
                            </TableBody>
                          </Table>
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </>
              )}
              {changeForm.watch("arrangementType") === "Approved" && (
                <FormField
                  control={changeForm.control}
                  name="selectedArrangement"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>
                        Select a WFH arrangement to change
                      </FormLabel>
                      <FormControl>
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead className="w-[100px]">
                                Select
                              </TableHead>
                              <TableHead>Application ID</TableHead>
                              <TableHead>Date</TableHead>
                              <TableHead>Type</TableHead>
                              <TableHead>Time</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {appovedApplications.map((arrangement:any) => (
                              <TableRow key={arrangement.event_id}>
                                <TableCell className="font-medium">
                                  <RadioGroup
                                    onValueChange={(value) =>{
                                      field.onChange({
                                        eventID: value,
                                        applicationID:
                                          arrangement.application_id,
                                      })
                                      setSelectedArrangement({
                                        eventID: value,
                                        applicationID:
                                          arrangement.application_id,
                                      })
                                    }}
                                    value={field.value.eventID}
                                    className="space-y-1"
                                  >
                                    <RadioGroupItem
                                      value={arrangement.event_id}
                                      id={arrangement.event_id}
                                    />
                                    <label
                                      htmlFor={arrangement.event_id}
                                      className="flex items-center space-x-2 cursor-pointer"
                                    >
                                      <span className="sr-only">
                                        Select arrangement
                                      </span>
                                    </label>
                                  </RadioGroup>
                                </TableCell>
                                <TableCell>
                                  {arrangement.application_id}
                                </TableCell>
                                <TableCell>
                                  {arrangement.date.toLocaleDateString()}
                                </TableCell>
                                <TableCell>
                                  {arrangement.application_type}
                                </TableCell>
                                <TableCell>
                                  {arrangement.hour}
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </FormControl>
                      <FormDescription>
                        Only arrangements that are 2 weeks ahead and before
                        current date can be withdrawn
                      </FormDescription>
                    </FormItem>
                  )}
                />
              )}
              {selectedArrangement && (
                <FormField
                control={changeForm.control}
                name="singleDate.date"
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
                            if (date) {
                              
                              setSelectedDate(date)
                            }
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
                )}/>
              )}
              {selectedDate && (
                  <FormField
                  control={changeForm.control}
                  name={`singleDate.hour`}
                  render={({ field }) => (
                    <FormItem className="space-y-3">
                      <FormLabel>{format(selectedDate, "PPP")}</FormLabel>
                      <FormDescription  hidden={!isAMButtonDisabled(selectedDate)} >There is an existing AM wfh arrangement for this day</FormDescription>
                      <FormDescription hidden={!isPMButtonDisabled(selectedDate)}>There is an existing PM wfh arrangement for this day</FormDescription>
                      <FormControl>
                        <RadioGroup
                          onValueChange={field.onChange}
                          defaultValue={field.value}
                          className="flex space-x-4"
                        >
                          <FormItem className="flex items-center space-x-2 space-y-0">
                            <FormControl>
                              <RadioGroupItem value="fullday" id="r1" hidden={isFULLDAYButtonDisabled(selectedDate)}/>
                            </FormControl>
                            <FormLabel className="font-normal" hidden={isFULLDAYButtonDisabled(selectedDate)}>Full Day</FormLabel>
                          </FormItem>
                          <FormItem className="flex items-center space-x-2 space-y-0">
                            <FormControl>
                              <RadioGroupItem value="am" hidden={isAMButtonDisabled(selectedDate)}/>
                            </FormControl>
                            <FormLabel className="font-normal" hidden={isAMButtonDisabled(selectedDate)}>AM</FormLabel>
                          </FormItem>
                          <FormItem className="flex items-center space-x-2 space-y-0">
                            <FormControl>
                              <RadioGroupItem value="pm" hidden={isPMButtonDisabled(selectedDate)} />
                            </FormControl>
                            <FormLabel className="font-normal" hidden={isPMButtonDisabled(selectedDate)}>PM</FormLabel>
                          </FormItem>
                        </RadioGroup>
                      </FormControl>
                    </FormItem>
                  )}
                />
                  )}

              <FormField
                control={changeForm.control}
                name="reason"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Reason for change:</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Please provide a reason for your change request."
                        {...field}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />
            </CardContent>
            <CardFooter>
              <Button type="submit">Confirm Change</Button>
            </CardFooter>
          </form>
        </Form>
      </Card>
    </TabsContent>
  );
};
export default Apply_Change;
