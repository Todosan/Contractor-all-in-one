import React, { useState } from 'react';
import { useTaskContext } from '../context/TaskContext';

const TaskList: React.FC = () => {
  const { tasks, addTask, removeTask, toggleTaskStatus, modifyTask } = useTaskContext();
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');

  const handleCreateTask = () => {
    if (newTaskTitle.trim()) {
      addTask({
        title: newTaskTitle,
        description: newTaskDescription,
        completed: false,
      });
      setNewTaskTitle('');
      setNewTaskDescription('');
    }
  };

  const handleUpdateTask = (taskId: number) => {
    const updatedTask = { title: 'Updated Task', completed: true }; // Example
    modifyTask(taskId, updatedTask);
  };

  const handleDeleteTask = (taskId: number) => {
    removeTask(taskId);
  };

  return (
    <div>
      <div>
        <input
          type="text"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          placeholder="Task title"
        />
        <textarea
          value={newTaskDescription}
          onChange={(e) => setNewTaskDescription(e.target.value)}
          placeholder="Task description"
        />
        <button onClick={handleCreateTask}>Create Task</button>
      </div>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <span>{task.title}</span> <br />
            <span>{task.completed ? 'Completed' : 'Not Completed'}</span>
            <button onClick={() => handleUpdateTask(task.id)}>Complete</button>
            <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;
