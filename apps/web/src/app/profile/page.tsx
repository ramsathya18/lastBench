"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

export default function ProfilePage() {
  const [me, setMe] = useState<any>();
  useEffect(() => {
    apiFetch("/auth/me").then(setMe).catch(() => setMe(null));
  }, []);
  return (
    <div>
      <h1 className="text-2xl font-bold">Profile</h1>
      <pre>{JSON.stringify(me, null, 2)}</pre>
    </div>
  );
}
