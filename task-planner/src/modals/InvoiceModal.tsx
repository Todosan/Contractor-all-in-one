import React, { useState } from 'react';
import { createInvoice } from '../lib/api/invoice.api';  // Import the API function

interface InvoiceModalProps {
  onClose: () => void;
}

const InvoiceModal: React.FC<InvoiceModalProps> = ({ onClose }) => {
  const [clientName, setClientName] = useState('');
  const [amount, setAmount] = useState(0);
  const [invoiceDate] = useState(new Date().toISOString().split('T')[0]); // Auto generate current date
  const [invoiceNumber] = useState(`INV-${Date.now()}`); // Auto generate invoice number based on current timestamp

  const handleSaveInvoice = async () => {
    const invoiceData = {
      description: `Invoice #${invoiceNumber}`,
      amount,
      issuedAt: invoiceDate,
      dueDate: invoiceDate,
      client: clientName,
    };

    try {
      const savedInvoice = await createInvoice(invoiceData);  // Send data to backend
      console.log('Invoice saved:', savedInvoice);
      setClientName('');
      setAmount(0);
      onClose();  // Close modal after saving
    } catch (error) {
      console.error('Error saving invoice:', error);
    }
  };

  return (
    <div className="modal-content p-6 bg-white rounded-lg shadow-lg w-full max-w-lg mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Create New Invoice</h2>

      {/* Invoice Form Fields */}
      <div className="mb-4">
        <label htmlFor="invoiceNumber" className="block text-lg">Invoice Number</label>
        <input
          type="text"
          id="invoiceNumber"
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
        />
      </div>

      <div className="flex justify-end gap-4">
        <button
          onClick={onClose}
          className="btn bg-gray-500 text-white hover:bg-gray-600"
        >
          Cancel
        </button>
        <button
          onClick={handleSaveInvoice}
          className="btn bg-blue-500 text-white hover:bg-blue-600"
        >
          Save Invoice
        </button>
      </div>
    </div>
  );
};

export default InvoiceModal;
