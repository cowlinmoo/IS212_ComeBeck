"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home, FileText, Settings } from "lucide-react";
import { useRouter, usePathname } from "next/navigation";

const tabs = [
  { name: "Home", icon: Home, path: "/profile" },
  { name: "Schedule", icon: FileText, path: "/schedule" },
  { name: "Arrangement Management", icon: Settings, path: "/arrangement" },
];

export default function SideBar() {
  const router = useRouter();
  const pathname = usePathname();
  const [activeTab, setActiveTab] = useState("");

  // Set activeTab based on the current pathname
  useEffect(() => {
    const currentTab = tabs.find((tab) => tab.path === pathname);
    if (currentTab) {
      setActiveTab(currentTab.name);
    }
  }, [pathname]);

  const handleTabClick = (tab: { name: string; path: string }) => {
    setActiveTab(tab.name);
    router.push(tab.path); // Navigate to the selected tab's path
  };

  return (
    <div>
      <nav className="bg-white w-64 h-screen flex flex-col border-r">
        <div className="flex items-center justify-center py-5">
          <h2 className="text-xl font-bold">ComeBeck</h2>
        </div>
        <div className="flex-1 overflow-y-auto">
          {tabs.map((tab) => (
            <Button
              key={tab.name}
              variant={activeTab === tab.name ? "default" : "ghost"}
              className="w-full justify-start rounded-none h-12"
              onClick={() => handleTabClick(tab)}
            >
              <tab.icon className="mr-2 h-5 w-5" />
              {tab.name}
            </Button>
          ))}
        </div>
      </nav>
    </div>
  );
}
