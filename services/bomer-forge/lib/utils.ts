import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const formatDate = (str: string) => {
  const dateTimeArray = new Date(str)
    .toLocaleTimeString("en-us", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
    .replace(/,/g, "")
    .split(/\s/g);

  const [month, day, year] = dateTimeArray;

  return `${day}-${month}-${year}`;
};

export const formatTime = (str: string) => {
  return new Date(str).toLocaleTimeString("en-us", {
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  });
};

export const getTimeAgo = (datetimeStr: string) => {
  const now = new Date();
  const datetime = new Date(datetimeStr);
  const diffInSeconds = Math.floor((now.getTime() - datetime.getTime()) / 1000);

  // Less than a minute
  if (diffInSeconds < 60) {
    return "Just now";
  }

  // Less than an hour
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return `${diffInMinutes} min${diffInMinutes > 1 ? "s" : ""} ago`;
  }

  // Less than a day
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return `${diffInHours} hour${diffInHours > 1 ? "s" : ""} ago`;
  }

  // Between one and three days
  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays <= 3) {
    return `${diffInDays} day${diffInDays > 1 ? "s" : ""} ago`;
  }

  // Greater than 3 days
  return formatDate(datetimeStr);
};
