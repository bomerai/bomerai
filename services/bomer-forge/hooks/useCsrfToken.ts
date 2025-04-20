import { useEffect } from "react";
import Cookies from "js-cookie";

export function useCsrfToken(): string | undefined {
  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/auth/csrf/`,
          {
            method: "GET",
            credentials: "include",
            mode: "cors",
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch CSRF token");
        }

        const data = await response.json();
        if (data.csrfToken) {
          Cookies.set("csrftoken", data.csrfToken);
        }
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    };

    // Fetch token on mount
    fetchCsrfToken();

    // Set up interval to refresh token
    const intervalId = setInterval(fetchCsrfToken, 1000 * 60 * 30); // Refresh every 30 minutes

    return () => clearInterval(intervalId);
  }, []);

  return Cookies.get("csrftoken");
}
