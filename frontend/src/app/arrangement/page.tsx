import { Header } from "@/components/core/header/Header";
import Applications from "@/components/arrangement/applications/Applications";
import SideBar from "@/components/core/sidebar/SideBar";

export default function Component() {
  return (
    <div className="flex h-screen text-black bg-gray-100">
      {/* Left Navbar */}
      <SideBar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header />
        {/* Page Content */}
        <Applications />
      </div>
    </div>
  );
}
