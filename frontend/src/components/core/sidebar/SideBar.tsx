"use client";
import { useState, useEffect, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { FileText, Settings, Users, User } from "lucide-react";
import { useRouter, usePathname } from "next/navigation";
import useAuth from "@/lib/auth";

// Define the type for each tab
interface Tab {
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  path: string;
  requiresRole?: number;
}

// Define the tabs array with explicit typing
const tabs: Tab[] = [
  { name: "Profile", icon: User, path: "/profile" },
  { name: "Department Schedule", icon: Users, path: "/overview", requiresRole: 1 },
  { name: "Schedule", icon: FileText, path: "/schedule" },
  { name: "Arrangement Management", icon: Settings, path: "/arrangement" },
  { name: "Arrangement Approvals", icon: Settings, path: "/approvals" },
  { name: "Pending Arrangements", icon: Users, path: "/managementViewPending", requiresRole: 3 },
  { name: "Withdraw Arrangements", icon: Users, path: "/managementViewWithdraw", requiresRole: 3 }, 
];

export default function SideBar() {
  const router = useRouter();
  const pathname = usePathname();
  const { role } = useAuth(); // Access role directly from useAuth
  const [activeTab, setActiveTab] = useState<string>("");

  // Memoize filtered tabs based on role
  const filteredTabs = useMemo(
    () => tabs.filter((tab) => !tab.requiresRole || tab.requiresRole === role),
    [role]
  );

  // Set activeTab based on the current pathname
  useEffect(() => {
    const currentTab = filteredTabs.find((tab) => tab.path === pathname);
    if (currentTab) {
      setActiveTab(currentTab.name);
    }
  }, [pathname, filteredTabs]);

  // Define the type for the tab parameter in handleTabClick
  const handleTabClick = (tab: Tab) => {
    setActiveTab(tab.name);
    router.push(tab.path);
  };

  return (
    <div>
      <nav className="bg-white w-64 h-screen flex flex-col border-r">
        <div className="flex flex-col items-center justify-center py-5 space-y-2">
          <h2 className="text-xl font-bold">ComeBeck</h2>
          <h4 className="text-xs text-gray-500 ml-1">WFH Tracker</h4>
        </div>
        <div className="flex-1 overflow-y-auto">
          {filteredTabs.map((tab) => (
              <Button
                  key={tab.name}
                  variant={activeTab === tab.name ? "default" : "ghost"}
                  className="w-full justify-start rounded-none h-12"
                  onClick={() => handleTabClick(tab)}
              >
                <tab.icon className="mr-2 h-5 w-5"/>
                {tab.name}
              </Button>
          ))}
        </div>
      </nav>
    </div>
  );
}