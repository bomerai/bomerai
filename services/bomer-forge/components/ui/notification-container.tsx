import React from "react";
import { useNotificationContext } from "@/hooks/notification-context";
import Notification from "./notification";

const NotificationContainer: React.FC = () => {
  const { notifications, removeNotification } = useNotificationContext();

  if (notifications.length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 w-full max-w-md">
      {notifications.map((notification) => (
        <Notification
          key={notification.id}
          notification={notification}
          onClose={removeNotification}
        />
      ))}
    </div>
  );
};

export default NotificationContainer;
