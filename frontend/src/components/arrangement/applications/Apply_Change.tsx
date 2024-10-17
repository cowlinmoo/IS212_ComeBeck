/* eslint-disable @typescript-eslint/no-explicit-any */
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
import {  TabsContent } from "@/components/ui/tabs";
import { Calendar } from "@/components/ui/calendar";

// import {  addMonths, subMonths } from "date-fns";

// import * as z from "zod";


// const changeFormSchema = z.object({
//   arangementType: z.string().default("WFH"),
//   isMultiple: z.enum(["Yes", "No"], {
//     required_error: "Please specify if this is for multiple dates.",
//   }),
//   singleDate: z
//     .date({
//       required_error: "Please select a date.",
//     })
//     .refine((date) => !isWeekend(date), { message: "Weekends are not allowed" })
//     .optional(),
//   multipleDate: z
//     .array(
//       z.date({
//         required_error: "Please select dates (at least 2), excluding weekends.",
//       })
//     )
//     .refine(
//       (dates) => dates.length > 1 && dates.every((date) => !isWeekend(date)),
//       { message: "Please select dates (at least 2), excluding weekends." }
//     )
//     .optional(),
//   isRecurring: z.enum(["Yes","No"]).optional(),
//   recurringType: z.enum(["Weekly","Monthly"]).optional(),
//   endDate: z.date({
//     required_error: "Please select a date.",
//   })
//   .refine((date) => !isWeekend(date), { message: "Weekends are not allowed" })
//   .optional(),
//   reason: z.string(),
// });

interface IApply_Change {
  staffId: string | undefined;
  token: string | undefined;
}
const Apply_Change: React.FC<IApply_Change> = ({ staffId, token }) => {
  // fetching wfh applications currently existing
//   const [wfhApplications, setwfhApplications] = useState(Array);
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
            // setwfhApplications(applications)
          }
        }
      } catch (error:any) {
        console.log("GET API fetching error.", error.message);
      }
    }
    fetchData();
  },[token, staffId]);

//   // restricted calendar
//   const [fromDate, setFromDate] = useState<Date>(new Date());
//   const [toDate, setToDate] = useState<Date>(new Date());

  const [selectedDates, setSelectedDates] = useState<Date[]>([]);
 
  const handleDateSelect = (date: Date) => {
    setSelectedDates((prev) =>
      prev.some((d) => d.toDateString() === date.toDateString())
        ? prev.filter((d) => d.toDateString() !== date.toDateString())
        : [...prev, date]
    );
  };
//   useEffect(() => {
//     // const currentDate = new Date();
//     // setFromDate(subMonths(currentDate, 2));
//     // setToDate(addMonths(currentDate, 3));
//   },[]);

//   //end date variables and restriction
//   const [fromEndDate, setFromEndDate] = useState<Date>(new Date());
//   const [toEndDate, setToEndDate] = useState<Date>(new Date());
//   useEffect(() => {
//     const currentDate = fromEndDate;
//     setToEndDate(addMonths(currentDate, 3));
//   },[fromEndDate]);

  // disable weekends and all dates with existing wfh arrangements or pending wfh applications
//   const isDateDisabled = (date: Date) => {
//     let hasApplication = false
//     for (const d of wfhApplications){
//       if (d.toDateString() === date.toDateString()){
//         hasApplication = true
//         break
//       }
//     }
//     return isWeekend(date) || date < fromDate || date > toDate || hasApplication ;
//   };
//   const onlyDisableWeekend = (date: Date) => {
//     return isWeekend(date) || date < fromDate || date > toDate ;
//   };

  //Apply form
//   const applyForm = useForm<z.infer<typeof changeFormSchema>>({
//     resolver: zodResolver(changeFormSchema),
//     defaultValues: {
//       arrangementType: "WFH",
//       isMultiple: "No",
//       isRecurring: "No",
//       reason: "",
//     },
//   });

  return (
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
  );
};
export default Apply_Change;
