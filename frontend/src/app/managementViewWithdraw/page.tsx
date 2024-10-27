'use client';

import useAuth from "@/lib/auth";
import { Header } from "@/components/core/header/Header";
import SideBar from "@/components/core/sidebar/SideBar";
import { useEffect, useState } from "react";
import { GetAcceptedApplications, WithdrawApplicationEvent } from "./api";
import ViewWithdraw from "@/components/arrangement/managementViewWithdraw/ViewWithdraw";
import { ApprovedApplication } from "@/components/arrangement/managementViewWithdraw/ViewWithdraw";

export default function Component() {
  const { token, userId, pageLoading } = useAuth();
  const [applications, setApplications] = useState([]);
  const [withdrawing, setWithdrawing] = useState(false);

  useEffect(() => {
    if (token) {
      const fetchApplications = async () => {
        try {
          let data = await GetAcceptedApplications(token);
          console.log(data);
          data = data.filter((application: ApprovedApplication) => application.approver_id === Number(userId));
          setApplications(data);
        } catch (error) {
          console.error('Error fetching applications:', error);
        }
      };
      fetchApplications();
    }
  }, [token, userId]);

  const handleWithdraw = async (selectedEvents: { applicationId: number; eventId: number }[]) => {
    try {
      // Create an array of promises
      const promises = selectedEvents.map(({ applicationId, eventId }) =>
        WithdrawApplicationEvent(token || '', applicationId, eventId, Number(userId))
      );

      // Use Promise.all to run all requests concurrently
      setWithdrawing(true);
      await Promise.all(promises);
      setWithdrawing(false);

      console.log('All selected events have been withdrawn successfully');
      // reload the page
      window.location.reload();
    } catch (error) {
      console.error('Error withdrawing events:', error);
    }
  };

  return (
    <div className="flex h-screen text-black bg-gray-100">
      <SideBar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />

        {/* Page Content */}
        {pageLoading || (!pageLoading && token === undefined) ? (
          <div className='flex flex-col items-center justify-center h-full w-full'>
            {/* Spinner */}
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
            <p className="text-gray-600">Loading withdraw arrangement page...</p>
          </div>
        ) : withdrawing ? (
          <div className="fixed top-0 left-0 z-50 w-full h-full bg-black bg-opacity-50 flex items-center justify-center">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-2"></div>
            <p className="text-white">Withdrawing...</p>
          </div>
        ) : (
          <ViewWithdraw
            data={applications}
            onWithdraw={handleWithdraw}
          />
        )}
      </div>
    </div>
  );
}