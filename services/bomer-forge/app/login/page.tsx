import GoogleOAuthButton from "@/components/auth/google-oauth-button";

export default function Login() {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <GoogleOAuthButton />
    </div>
  );
}
