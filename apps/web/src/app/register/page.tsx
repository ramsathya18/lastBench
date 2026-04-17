"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { Button, Card } from "@/components/ui";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [msg, setMsg] = useState("");

  return (
    <Card>
      <form className="space-y-3" onSubmit={async (e) => {
        e.preventDefault();
        await apiFetch("/auth/register", {method:"POST", body:JSON.stringify({email,password,full_name:fullName})});
        setMsg("Registered. Please login.");
      }}>
        <h1 className="text-xl font-semibold">Create account</h1>
        <input className="w-full rounded border p-2" placeholder="Full name" value={fullName} onChange={(e)=>setFullName(e.target.value)} />
        <input className="w-full rounded border p-2" placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} />
        <input className="w-full rounded border p-2" type="password" placeholder="Password" value={password} onChange={(e)=>setPassword(e.target.value)} />
        <Button type="submit">Register</Button>
        <p>{msg}</p>
      </form>
    </Card>
  );
}
