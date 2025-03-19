"use client";

import { useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useState } from "react";

type LoggedUser = {
  email: string;
  id: string;
};

interface AuthContextType {
  user: LoggedUser | null;
  isLoading: boolean;
  error: Error | null;
}

export const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: false,
  error: null,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();
  const [user, setUser] = useState<LoggedUser | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      console.log("fetching user...");
      try {
        setIsLoading(true);
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/auth/user/`,
          {
            credentials: "include",
          }
        );
        const data = await response.json();
        if (response.ok) {
          setUser({
            email: data.email,
            id: data.id,
          });
          setIsLoading(false);
        } else {
          setError(new Error(data.error));
          setIsLoading(false);
          router.push("/login");
        }
      } catch (error) {
        console.error(error);
        setError(null);
        setIsLoading(false);
        router.push("/login");
      }
    };
    fetchUser();
  }, []);

  if (error) {
    console.error(error);
    router.push("/login");
  }

  if (!error && isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
