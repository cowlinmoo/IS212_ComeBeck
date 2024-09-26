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
import { format, addMonths, subMonths } from "date-fns";
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
import * as  z  from "zod";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

//formschema
const applyFormSchema = z.object({
  arangement_type: z.string().default("WFH"),
  isMultiple: z.enum(["Yes", "No"], {
    required_error: "Please specify if this is for multiple dates.",
  }),
  singleDate: z
    .date({
      required_error: "Please select a date.",
    })
    .optional(),
  multipleDate: z
    .array(z.date())
    .refine((dates) => dates.length > 1, {
      required_error: "Please select dates (at least 2).",
    })
    .optional(),
  reason: z.string(),
});
export default function Applications() {
  //restricted calendar
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

  //Apply form
  const apply_form = useForm<z.infer<typeof applyFormSchema>>({
    resolver: zodResolver(applyFormSchema),
    defaultValues: {
      arrangement_type: "WFH",
      isMultiple: "No",
      reason: "",
    },
  });

  //Submission for apply form
  function applySubmit(values: z.infer<typeof applyFormSchema>) {}

  //check if selcted date conflicts with existing arrangements

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
            <Form {...apply_form}>
              <form onSubmit={apply_form.handleSubmit(applySubmit)}>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Arrangement Type:</Label> <br></br>
                    <Label className="font-bold">WFH</Label>
                  </div>
                  <FormField
                    control={apply_form.control}
                    name="isMultiple"
                    render={({ field }) => (
                      <FormItem className="space-y-3">
                        <FormLabel>Is this for multiple dates?</FormLabel>
                        <FormControl>
                          <RadioGroup
                            onValueChange={(value)=>{field.onChange(value)
                            if (value === "No"){
                              apply_form.setValue("multipleDate", undefined)
                            } else{
                              apply_form.setValue("singleDate", undefined)
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
                  {apply_form.watch("isMultiple") === "No" && (
                      <FormField
                        control={apply_form.control}
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
                                  onSelect={field.onChange}
                                  fromDate={fromDate}
                                  toDate={toDate}
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
                  {apply_form.watch("isMultiple") === "Yes" && (
                    <FormField
                      control={apply_form.control}
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
                                onSelect={field.onChange}
                                fromDate={fromDate}
                                toDate={toDate}
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
                    control={apply_form.control}
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
}
