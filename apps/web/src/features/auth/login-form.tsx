"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { tokenStore } from "@/lib/auth";
import { Button, Card } from "@/components/ui";

export default function LoginForm() {
  const [email, setEmail] = useState("learner@demo.local");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const router = useRouter();

  return (
    <Card>
      <form
        className="space-y-3"
        onSubmit={async (e) => {
          e.preventDefault();
          setError("");
          try {
            const data = await apiFetch("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
            tokenStore.setTokens(data.access_token, data.refresh_token);
            router.push("/dashboard");
          } catch {
            setError("Login failed");
          }
        }}
      >
        <h1 className="text-xl font-semibold">Sign in</h1>
        <input className="w-full rounded border p-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full rounded border p-2" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <Button type="submit">Login</Button>
      </form>
    </Card>
  );
}
