import { Invoice } from '@/types';
import { createContext, useContext, useState, ReactNode } from 'react';

interface InvoiceContextType {
  invoices: Invoice[];
  setInvoices: React.Dispatch<React.SetStateAction<Invoice[]>>;
  selectedInvoice: Invoice | null;
  selectInvoice: (invoice: Invoice) => void;
  clearSelectedInvoice: () => void;
}

const InvoiceContext = createContext<InvoiceContextType | undefined>(undefined);

export function InvoiceProvider({ children }: { children: ReactNode }) {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);

  const selectInvoice = (invoice: Invoice) => {
    setSelectedInvoice(invoice);
  };

  const clearSelectedInvoice = () => {
    setSelectedInvoice(null);
  };

  return (
    <InvoiceContext.Provider value={{ invoices, setInvoices, selectedInvoice, selectInvoice, clearSelectedInvoice }}>
      {children}
    </InvoiceContext.Provider>
  );
}

export function useInvoice() {
  const context = useContext(InvoiceContext);
  if (context === undefined) {
    throw new Error('useInvoice must be used within an InvoiceProvider');
  }
  return context;
}