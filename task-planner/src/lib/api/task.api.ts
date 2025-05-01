import { Task } from '@/types';
import axios from 'axios';

const API_URL = "http://localhost:8000"; // Replace with your actual backend URL

// Get All Tasks
export async function getTasks() {
  try {
    const response = await axios.get(`${API_URL}/tasks/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw new Error("Failed to fetch tasks");
  }
}

// Delete Task
export async function deleteTask(id: number) {
  try {
    const response = await axios.delete(`${API_URL}/tasks/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting task:', error);
    throw new Error("Failed to delete task");
  }
}

// Toggle Task Completion
export async function toggleTask(id: number, completed: boolean) {
  try {
    const response = await axios.put(`${API_URL}/tasks/${id}`, { completed });
    return response.data;
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw new Error("Failed to toggle task");
  }
}

// Create New Task
export async function createTask(task: { title: string; description?: string; completed?: boolean }) {
  try {
    const response = await axios.post(`${API_URL}/tasks/`, task);
    return response.data;
  } catch (error) {
    console.error('Error creating task:', error);
    throw new Error("Failed to create task");
  }
}

// Update Task
export const updateTask = async (taskId: number, data: Partial<Task>) => {
  try {
    const response = await axios.put(`${API_URL}/tasks/${taskId}`, data);
    return response.data;
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
};

