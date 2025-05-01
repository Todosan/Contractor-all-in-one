'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import {
  getTasks,
  createTask,
  deleteTask,
  toggleTask,
  updateTask,
} from '@/lib/api/task.api';

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  createdAt?: string;
  updatedAt?: string;
}

interface TaskContextType {
  tasks: Task[];
  loading: boolean;
  fetchTasks: () => void;
  addTask: (task: Omit<Task, 'id'>) => void;
  removeTask: (id: number) => void;
  toggleTaskStatus: (id: number, completed: boolean) => void;
  modifyTask: (id: number, data: Partial<Task>) => void;
}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const TaskProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await getTasks();
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (task: Omit<Task, 'id'>) => {
    try {
      const newTask = await createTask(task);
      setTasks((prev) => [...prev, newTask]);
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const removeTask = async (id: number) => {
    try {
      await deleteTask(id);
      setTasks((prev) => prev.filter((task) => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const toggleTaskStatus = async (id: number, completed: boolean) => {
    try {
      const updated = await toggleTask(id, completed);
      setTasks((prev) =>
        prev.map((task) => (task.id === id ? updated : task))
      );
    } catch (error) {
      console.error('Error toggling task:', error);
    }
  };

  const modifyTask = async (id: number, data: Partial<Task>) => {
    try {
      await updateTask(id, data);
      fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <TaskContext.Provider
      value={{
        tasks,
        loading,
        fetchTasks,
        addTask,
        removeTask,
        toggleTaskStatus,
        modifyTask,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
};

export const useTaskContext = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};
