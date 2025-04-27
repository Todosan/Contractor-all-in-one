// src/components/Sidebar.tsx
import React from 'react';
import { FaTasks, FaClock, FaFileInvoice, FaCog } from 'react-icons/fa'; // Import icons
import Link from 'next/link';

interface SidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
  setTaskOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setInvoiceOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar, setTaskOpen, setInvoiceOpen }) => {
  return (
    <div
      className={`fixed top-0 left-0 w-64 h-full bg-gray-800 text-white transform ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } transition-transform ease-in-out duration-300 z-50`}
    >
      <div className="flex justify-between items-center p-4">
        <h2 className="text-xl font-semibold">Developer Tools</h2>
        <button
          onClick={toggleSidebar}
          className="text-white text-2xl font-bold"
        >
          &times;
        </button>
      </div>

      <div className="p-4">
        <ul>
          <li className="mb-4">
            <button
              onClick={() => setTaskOpen(true)}  // Trigger Task modal
              className="flex items-center text-lg text-white hover:text-gray-300">
              <FaTasks className="mr-2" />
              Task Planner
            </button>
          </li>
          <li className="mb-4">
            <button
              onClick={() => setInvoiceOpen(true)}  // Trigger Invoice modal
              className="flex items-center text-lg text-white hover:text-gray-300">
              <FaFileInvoice className="mr-2" />
              Invoice Creator
            </button>
          </li>
          <li className="mb-4">
            <Link href="/time-entries" className="flex items-center text-lg text-white hover:text-gray-300" passHref>
                <FaClock className="mr-2" />
                Time Entries
            </Link>
          </li>
          <li className="mb-4">
            <Link href="/settings" className="flex items-center text-lg text-white hover:text-gray-300" passHref>
                <FaCog className="mr-2" />
                Settings
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
