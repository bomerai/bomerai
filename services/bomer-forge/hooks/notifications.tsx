import { useNotificationContext } from "./notification-context";
import { NotificationType } from "./notification-context";

const useNotification = () => {
  const { addNotification } = useNotificationContext();

  const showNotification = (
    message: string,
    type: NotificationType = "info",
    options?: {
      title?: string;
      duration?: number;
      action?: {
        label: string;
        onClick: () => void;
      };
    }
  ) => {
    addNotification({
      message,
      type,
      ...options,
    });
  };

  return { showNotification };
};

export default useNotification;
