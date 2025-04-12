import React from "react";
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";
import { Notification as NotificationType } from "@/hooks/notification-context";

interface NotificationProps {
  notification: NotificationType;
  onClose: (id: string) => void;
}

const Notification: React.FC<NotificationProps> = ({
  notification,
  onClose,
}) => {
  const { id, type, message, title, action } = notification;

  const getIcon = () => {
    switch (type) {
      case "success":
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case "error":
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case "warning":
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case "info":
      default:
        return <Info className="h-5 w-5 text-blue-500" />;
    }
  };

  const getBgColor = () => {
    switch (type) {
      case "success":
        return "bg-green-50 border-green-200";
      case "error":
        return "bg-red-50 border-red-200";
      case "warning":
        return "bg-yellow-50 border-yellow-200";
      case "info":
      default:
        return "bg-blue-50 border-blue-200";
    }
  };

  return (
    <div
      className={cn(
        "flex items-start p-4 mb-2 rounded-md border shadow-sm transition-all duration-300 ease-in-out",
        getBgColor()
      )}
      role="alert"
    >
      <div className="flex-shrink-0 mr-3">{getIcon()}</div>
      <div className="flex-1">
        {title && <h3 className="text-sm font-medium mb-1">{title}</h3>}
        <p className="text-sm">{message}</p>
        {action && (
          <button
            onClick={action.onClick}
            className="mt-2 text-sm font-medium underline hover:no-underline"
          >
            {action.label}
          </button>
        )}
      </div>
      <button
        onClick={() => onClose(id)}
        className="flex-shrink-0 ml-3 text-gray-400 hover:text-gray-600"
        aria-label="Close"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

export default Notification;
