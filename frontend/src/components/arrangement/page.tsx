"use client";

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar } from "@/components/ui/calendar"
// import { CalendarIcon } from "lucide-react"

export default function StaffArrangement() {
  const [selectedDates, setSelectedDates] = useState<Date[]>([])
  const [activeTab, setActiveTab] = useState("apply")

  const handleDateSelect = (date: Date) => {
    setSelectedDates(prev => 
      prev.some(d => d.toDateString() === date.toDateString())
        ? prev.filter(d => d.toDateString() !== date.toDateString())
        : [...prev, date]
    )
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
              <CardDescription>Submit a new arrangement request.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="arrangement-type">Arrangement Type</Label>
                <Input id="arrangement-type" placeholder="e.g., Work from home, Flexible hours" />
              </div>
              <div className="space-y-2">
                <Label>Select Dates</Label>
                <Calendar
                  mode="multiple"
                  selected={selectedDates}
                  onSelect={()=>handleDateSelect}
                  className="rounded-md border"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="reason">Reason for Arrangement</Label>
                <Textarea id="reason" placeholder="Please provide a reason for your arrangement request." />
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
              <CardDescription>Modify an existing arrangement for specific days.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="existing-arrangement">Existing Arrangement</Label>
                <Input id="existing-arrangement" placeholder="Select existing arrangement" />
              </div>
              <div className="space-y-2">
                <Label>Select Dates to Change</Label>
                <Calendar
                  mode="multiple"
                  selected={selectedDates}
                  onSelect={()=>handleDateSelect}
                  className="rounded-md border"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new-arrangement">New Arrangement</Label>
                <Input id="new-arrangement" placeholder="e.g., Office work, Different hours" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="change-reason">Reason for Change</Label>
                <Textarea id="change-reason" placeholder="Please provide a reason for changing your arrangement." />
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
              <CardDescription>Withdraw an approved arrangement or cancel a pending request.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="arrangement-to-withdraw">Select Arrangement</Label>
                <Input id="arrangement-to-withdraw" placeholder="Select arrangement to withdraw" />
              </div>
              <div className="space-y-2">
                <Label>Select Dates to Withdraw</Label>
                <Calendar
                  mode="multiple"
                  selected={selectedDates}
                  onSelect={()=>handleDateSelect}
                  className="rounded-md border"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="withdraw-reason">Reason for Withdrawal</Label>
                <Textarea id="withdraw-reason" placeholder="Please provide a reason for withdrawing your arrangement." />
              </div>
            </CardContent>
            <CardFooter>
              <Button>Confirm Withdrawal</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}