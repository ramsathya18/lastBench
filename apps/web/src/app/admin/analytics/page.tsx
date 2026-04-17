"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";

export default function AdminAnalyticsPage() {
  const [data, setData] = useState<Record<string, number>>({});
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch("/admin/analytics/overview")
      .then(setData)
      .catch((err: ApiError) => setError(err.message));
  }, []);

  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Analytics</h1>
      <div className="grid gap-4 md:grid-cols-3">
        {Object.entries(data).map(([key, value]) => (
          <Card key={key}>
            <p className="text-sm text-slate-600">{key.replaceAll("_", " ")}</p>
            <p className="text-2xl font-semibold">{value}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
