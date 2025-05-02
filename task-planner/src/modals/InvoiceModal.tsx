import React, { useState } from 'react';
import { createInvoice } from '../lib/api/invoice.api';  // Import the API function

interface InvoiceModalProps {
  onClose: () => void;
}

const InvoiceModal: React.FC<InvoiceModalProps> = ({ onClose }) => {
  const [clientName, setClientName] = useState('');
  const [amount, setAmount] = useState(0);
  const [invoiceDate, setInvoiceDate] = useState(new Date().toISOString().split('T')[0]); // Auto generate current date
  const [invoiceNumber, setInvoiceNumber] = useState(`INV-${Date.now()}`); // Auto generate invoice number based on current timestamp
  const [description, setDescription] = useState(`Invoice #${invoiceNumber}`);

  const handleSaveInvoice = async () => {
    // Convert the date string to a proper Date object
    const date = new Date(invoiceDate);
    
    const invoiceData = {
      invoiceNumber: invoiceNumber,
      clientName: clientName,
      description: description,
      amount: amount,
      dueDate: date.toISOString(),
      issuedAt: date.toISOString(),
      paid: false,
      taskIds: []
    };

    try {
      const savedInvoice = await createInvoice(invoiceData);
      console.log('Invoice saved:', savedInvoice);
      setClientName('');
      setAmount(0);
      setInvoiceNumber(`INV-${Date.now()}`);
      setDescription(`Invoice #${invoiceNumber}`);
      onClose();
    } catch (error) {
      console.error('Error saving invoice:', error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="relative bg-white p-6 rounded-md w-96">
        <h2 className="text-2xl font-semibold mb-4">Create New Invoice</h2>

        {/* Invoice Form Fields */}
        <div className="mb-4">
          <label htmlFor="number" className="block text-lg">Invoice Number</label>
          <input
            type="text"
            id="number"
            value={invoiceNumber}
            disabled
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="invoiceDate" className="block text-lg">Invoice Date</label>
          <input
            type="date"
            id="invoiceDate"
            value={invoiceDate}
            disabled
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="clientName" className="block text-lg">Client Name</label>
          <input
            type="text"
            id="clientName"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="amount" className="block text-lg">Amount</label>
          <input
            type="number"
            id="amount"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
            required
            step="0.01"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="dueDate" className="block text-lg">Due Date</label>
          <input
            type="date"
            id="dueDate"
            value={invoiceDate}
            onChange={(e) => setInvoiceDate(e.target.value)}
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
            required
          />
        </div>

        <div className="mb-4">
          <label htmlFor="description" className="block text-lg">Description</label>
          <input
            type="text"
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
            required
          />
        </div>

        <div className="flex justify-end gap-4">
          <button
            onClick={onClose}
            className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600"
          >
            Cancel
          </button>
          <button
            onClick={handleSaveInvoice}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          >
            Save Invoice
          </button>
        </div>
      </div>
    </div>
  );
};

export default InvoiceModal;
