// src/modals/TaskModal.tsx
'use client';
import React, { useState, useEffect } from 'react';
import { Task } from '../types/types';
import { createTask, updateTask } from '../lib/api/task.api';

interface TaskModalProps {
  onClose: () => void;
}

const TaskModal: React.FC<TaskModalProps> = ({ onClose }) => {
  const [taskTitle, setTaskTitle] = useState('');
  const [isEditMode, setIsEditMode] = useState(false);
  const [currentTask, setCurrentTask] = useState<Task | null>(null);

  useEffect(() => {
    if (currentTask) {
      setTaskTitle(currentTask.title);
      setIsEditMode(true);
    }
  }, [currentTask]);

  const handleSaveTask = async () => {
    try {
      if (isEditMode && currentTask) {
        await updateTask(currentTask.id, { title: taskTitle, completed: currentTask.completed });
      } else {
        await createTask({ title: taskTitle, completed: false });
      }
      setTaskTitle('');
      setIsEditMode(false);
      setCurrentTask(null);
      onClose();
    } catch (error) {
      console.error('Error saving task:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSaveTask();
    console.log('Task saved:', taskTitle);
  };

  return (
    <div className="modal-content p-6 bg-white rounded-lg shadow-lg w-full max-w-lg mx-auto">
      <h2 className="text-2xl font-semibold mb-4">{isEditMode ? 'Edit Task' : 'Add New Task'}</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="taskTitle" className="block text-lg">Task Title</label>
          <input
            type="text"
            id="taskTitle"
            value={taskTitle}
            onChange={(e) => setTaskTitle(e.target.value)}
            className="mt-2 p-2 w-full border border-gray-300 rounded-md"
            required
          />
        </div>

        <div className="flex justify-end gap-4">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Save Task
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskModal;
