import React from "react";

interface CircularProgressProps {
  progress: number;
  width?: number;
  height?: number;
}

export const CircularProgress = ({
  progress,
  width = 140,
  height = 140,
}: CircularProgressProps) => {
  const strokeWidth = 6;
  const radius = 100 / 2 - strokeWidth * 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <svg
      aria-label="label"
      aria-valuemax={100}
      aria-valuemin={0}
      aria-valuenow={progress}
      height={height}
      role="progressbar"
      width={width}
      viewBox="0 0 100 100"
      version="1.1"
      xmlns="http://www.w3.org/2000/svg"
      className="overflow-visible"
    >
      {/* Background circle */}
      <circle
        cx="50"
        cy="50"
        r={radius}
        strokeWidth={strokeWidth}
        className="fill-transparent stroke-gray-200 dark:stroke-gray-700"
        strokeLinecap="square"
      />

      {/* Progress circle */}
      <circle
        cx="50"
        cy="50"
        data-testid="progress-bar-bar"
        r={radius}
        strokeWidth={strokeWidth}
        strokeDasharray={`${circumference} ${circumference}`}
        strokeDashoffset={offset}
        className="fill-transparent stroke-blue-600 dark:stroke-blue-500 origin-center animate-spin duration-500"
        style={{ animationDuration: "2s" }}
        strokeLinecap="square"
      />
    </svg>
  );
};
