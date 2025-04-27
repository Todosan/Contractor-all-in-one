// src/app/page.tsx
'use client';
import { useState } from 'react';
import Timer from '../components/Timer';
import Calendar from '../components/Calender';
import TaskModal from '../modals/TaskModal';
import InvoiceModal from '../modals/InvoiceModal';
import Sidebar from '../components/Siderbar';
import Modal from '../modals/GeneralModal';

export default function Home() {
  const [taskOpen, setTaskOpen] = useState(false); // State to open Task modal
  const [invoiceOpen, setInvoiceOpen] = useState(false); // State to open Invoice modal
  const [sidebarOpen, setSidebarOpen] = useState(false); // State to control sidebar visibility

  // Function to toggle the sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <main className="min-h-screen bg-white p-6">
      {/* Sidebar */}
      <button
  onClick={toggleSidebar}
  className="p-2 m-2 bg-gray-800 text-white rounded-md"
>
  ☰ Menu
</button>
      <Sidebar
        isOpen={sidebarOpen}
        toggleSidebar={toggleSidebar}
        setTaskOpen={setTaskOpen} // Pass the state setter for Task modal
        setInvoiceOpen={setInvoiceOpen} // Pass the state setter for Invoice modal
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Timer */}
        <section className="col-span-1">
          <h2 className="text-xl font-semibold mb-2">Timer</h2>
          <Timer />
        </section>

        {/* Calendar */}
        <section className="col-span-2">
          <h2 className="text-xl font-semibold mb-2">Calendar</h2>
          <Calendar />
        </section>
      </div>

      {/* Modals */}
      <Modal isOpen={taskOpen} onClose={() => setTaskOpen(false)}>
        <TaskModal onClose={() => setTaskOpen(false)} />
      </Modal>

      <Modal isOpen={invoiceOpen} onClose={() => setInvoiceOpen(false)}>
        <InvoiceModal onClose={() => setInvoiceOpen(false)} />
      </Modal>
    </main>
  );
}
