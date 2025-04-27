// src/components/Timer.tsx
import React, { useState, useEffect } from "react";

const Timer: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [time, setTime] = useState(0);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (isRunning) {
      interval = setInterval(() => {
        setTime((prev) => prev + 1);
      }, 1000);
    } else if (!isRunning && time !== 0) {
      clearInterval(interval!);
    }
    return () => clearInterval(interval!);
  }, [isRunning, time]);

  const startStopTimer = () => {
    setIsRunning(!isRunning);
  };

  return (
    <div className="timer-container bg-blue-500 text-white p-4 rounded-full">
      <span>{`${Math.floor(time / 60)}:${time % 60}`}</span>
      <button
        className="ml-4 bg-red-500 p-2 rounded-full"
        onClick={startStopTimer}
      >
        {isRunning ? "Stop" : "Start"}
      </button>
    </div>
  );
};

export default Timer;
