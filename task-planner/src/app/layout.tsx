import './globals.css';
import { TaskProvider } from '@/context/TaskContext';

export const metadata = {
  title: 'My App',
  description: 'Freelancer Toolkit',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <TaskProvider>
          {children}
        </TaskProvider>
      </body>
    </html>
  );
}
