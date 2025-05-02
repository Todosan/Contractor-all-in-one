import axios from 'axios';

const API_URL = "http://localhost:8000";  // Replace with your actual backend URL

// Get All Invoices
export async function getInvoices() {
  try {
    const response = await axios.get(`${API_URL}/invoices/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching invoices:', error);
    throw new Error("Failed to fetch invoices");
  }
}

// Create New Invoice
export const createInvoice = async (invoiceData: {
  invoiceNumber: string;
  clientName: string;
  description: string;
  amount: number;
  dueDate: string;
  issuedAt: string;
  paid: boolean;
  taskIds: number[];
}) => {
  try {
    const response = await axios.post(`${API_URL}/invoices/`, invoiceData);
    return response.data;
  } catch (error) {
    console.error('Error creating invoice:', error);
    throw error;
  }
};

// Get Single Invoice
export async function getInvoice(id: number) {
  try {
    const response = await axios.get(`${API_URL}/invoices/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching invoice:', error);
    throw new Error("Failed to fetch invoice");
  }
}

// Update Invoice
export async function updateInvoice(id: number, invoice: { invoiceNumber: string; clientName: string; description: string; amount: number; dueDate: string; issuedAt: string; paid: boolean; taskIds: number[] }) {
  try {
    const response = await axios.put(`${API_URL}/invoices/${id}`, invoice);
    return response.data;
  } catch (error) {
    console.error('Error updating invoice:', error);
    throw new Error("Failed to update invoice");
  }
}

// Delete Invoice
export async function deleteInvoice(id: number) {
  try {
    const response = await axios.delete(`${API_URL}/invoices/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting invoice:', error);
    throw new Error("Failed to delete invoice");
  }
}
