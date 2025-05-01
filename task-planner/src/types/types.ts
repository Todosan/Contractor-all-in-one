export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  startDate: string;
  dueDate: string;
  priority: 'low' | 'medium' | 'high';
  status: 'todo' | 'in_progress' | 'completed';
  invoiceId: number | null; // Link to invoice
  hourEntries: HourEntry[]; // Link to hour entries
  scheduleEvents: ScheduleEvent[]; // Link to schedule events
}

export interface Invoice {
  id: number;
  invoiceNumber: string;
  clientName: string;
  clientEmail: string;
  issueDate: string;
  dueDate: string;
  status: 'draft' | 'sent' | 'paid' | 'overdue';
  totalAmount: number;
  currency: string;
  tasks: Task[]; // Link to tasks
  hourEntries: HourEntry[]; // Link to hour entries
  scheduleEvents: ScheduleEvent[]; // Link to schedule events
}

export interface HourEntry {
  id: number;
  taskId: number;
  date: string;
  hours: number;
  rate: number;
  description: string;
}

export interface ScheduleEvent {
  id: number;
  title: string;
  start: string;
  end: string;
  description: string;
  allDay: boolean;
}