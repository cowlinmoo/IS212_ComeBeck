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
import { TabsContent } from "@/components/ui/tabs";
import { subWeeks, addWeeks, getYear, addYears,subYears, getMonth } from "date-fns";
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
import { CheckCircle2 } from "lucide-react";
import {
  Table,
  TableBody,
  TableHead,
  TableCell,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/application`;

//formschema
const withdrawalFormSchema = z.object({
  arrangementType: z.enum(["Pending Approval", "Approved"], {
    required_error: "Please specify your arrangement type",
  }),
  selectedArrangement: z
    .object({
      eventID: z.string(),
      applicationID: z.string()
    })
    .refine((data) => data.eventID !== "", {
      message: "Please select an arrangement to withdraw.",
    }),
  reason: z.string(),
});

interface IApplications {
  staffId: string | undefined;
  token: string | undefined;
}
const Apply_Withdrawal: React.FC<IApplications> = ({ staffId, token }) => {
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
              if (application["status"] === "pending" && application["application_state"]==="new_application") {
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
              } else if (application["status"] === "approved" && application["application_state"]==="new_application") {
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
  //Apply form
  const withdrawalForm = useForm<z.infer<typeof withdrawalFormSchema>>({
    resolver: zodResolver(withdrawalFormSchema),
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


  //Submission for apply form
  async function applySubmit(values: z.infer<typeof withdrawalFormSchema>) {
    if (values.reason.trim() === "") {
      setShowEmptyReasonAlert(true);
    } else {
      setShowEmptyReasonAlert(false);
    }
    if (values.selectedArrangement.eventID === "") {
      setShowNoSelectionAlert(true);
    }
    if (values.reason !=="" && showNoSelectionAlert === false) {
      const headers = {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        accept: "application/json",
      };
      //
      console.log(values.selectedArrangement.applicationID);
      console.log(values.selectedArrangement.eventID);
        const content = {
          status: "withdrawn",
          editor_id: staffId,
          withdraw_reason: values.reason,
        };
        console.log(content);
        try {
          const response = await fetch(
            `${URL}/withdraw/` +
              values.selectedArrangement.applicationID +
              "/" +
              values.selectedArrangement.eventID,
            { headers: headers, method: "PUT", body: JSON.stringify(content) }
          );
          if (!response.ok) {
            console.log(await response.json());
            throw new Error(`POST Application API validation ERROR`);
          } else {
            console.log(response.json());
            setShowSuccessAlert(true);
            //reset form once submission is successful
            withdrawalForm.reset();
            //set timeout for alert
            setTimeout(() => setShowSuccessAlert(false), 5000);
          }
        } catch (error: any) {
          console.log("POST API fetching error.", error.message);
        }
        
    }
  }

  return (
    <TabsContent value="withdraw">
      <Card>
        <CardHeader>
          <CardTitle>Withdraw Arrangement</CardTitle>
          <CardDescription>
            Withdraw an approved arrangement or cancel a pending request.
          </CardDescription>
        </CardHeader>
        <Form {...withdrawalForm}>
          <form onSubmit={withdrawalForm.handleSubmit(applySubmit)}>
            <CardContent className="space-y-4">
              {showEmptyReasonAlert && (
                <Alert variant="destructive">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertTitle>Warning</AlertTitle>
                  <AlertDescription>
                    Please indicate the reason for your withdrawal/cancellation.
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
              {showSuccessAlert && (
                <Alert
                  variant="default"
                  className="bg-green-100 border-green-500"
                >
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  <AlertTitle className="text-green-800">Success</AlertTitle>
                  <AlertDescription className="text-green-700">
                    Your WFH withdrawal/cancellation request has been
                    successfully submitted.
                  </AlertDescription>
                </Alert>
              )}
              <FormField
                control={withdrawalForm.control}
                name="arrangementType"
                render={({ field }) => (
                  <FormItem className="space-y-3">
                    <FormLabel>
                      Select which arrangement would you like to
                      withdraw/cancel?
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
                            Pending Approval (Cancel)
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="Approved" />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Approved (Withdraw){" "}
                          </FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                  </FormItem>
                )}
              />
              {withdrawalForm.watch("arrangementType") ===
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
                    control={withdrawalForm.control}
                    name="selectedArrangement"
                    render={({ field }) => (
                      <FormItem className="flex flex-col">
                        <FormLabel>
                          Select a pending arrangement to withdraw
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
                                        onValueChange={(value) =>
                                          field.onChange({
                                            eventID: value,
                                            applicationID:
                                              arrangement.application_id,
                                          })
                                        }
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
              {withdrawalForm.watch("arrangementType") === "Approved" && (
                <FormField
                  control={withdrawalForm.control}
                  name="selectedArrangement"
                  render={({ field }) => (
                    <FormItem className="flex flex-col">
                      <FormLabel>
                        Select a WFH arrangement to withdraw
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
                                    onValueChange={(value) =>
                                      field.onChange({
                                        eventID: value,
                                        applicationID:
                                          arrangement.application_id,
                                      })
                                    }
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
              <FormField
                control={withdrawalForm.control}
                name="reason"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Reason for withdrawal/cancellation:</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Please provide a reason for your withdrawal/cancellation request."
                        {...field}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />
            </CardContent>
            <CardFooter>
              <Button type="submit">Confirm Withdrawal</Button>
            </CardFooter>
          </form>
        </Form>
      </Card>
    </TabsContent>
  );
};
export default Apply_Withdrawal;
