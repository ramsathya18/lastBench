"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { tokenStore } from "@/lib/auth";

export default function ProfilePage() {
  const [me, setMe] = useState<any>();
  useEffect(() => { apiFetch("/auth/me", { headers: { Authorization: `Bearer ${tokenStore.get()}` } }).then(setMe); }, []);
  return <div><h1 className="text-2xl font-bold">Profile</h1><pre>{JSON.stringify(me, null, 2)}</pre></div>;
}
