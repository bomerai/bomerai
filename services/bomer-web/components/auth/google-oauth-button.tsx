"use client";

import { CredentialResponse, GoogleLogin } from "@react-oauth/google";
import { useRouter } from "next/navigation";

export default function GoogleOAuthButton() {
  const router = useRouter();
  const onSuccess = async (credentialResponse: CredentialResponse) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_FORGE_SERVICE_API_URL}/api/v1/auth/google/`,
      {
        method: "POST",
        body: JSON.stringify({ client_token: credentialResponse.credential }),
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const data = await response.json();
    console.log(data);
    router.push("/");
  };

  return (
    <GoogleLogin
      onSuccess={onSuccess}
      onError={() => {
        console.log("Login Failed");
      }}
    />
  );
}
