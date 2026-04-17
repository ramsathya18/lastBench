"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui";
import { apiFetch } from "@/lib/api";

export default function DashboardPage() {
  const [enrollments, setEnrollments] = useState<any[]>([]);
  const [progress, setProgress] = useState<Record<number, any>>({});

  useEffect(() => {
    apiFetch("/me/enrollments").then(async (rows) => {
      setEnrollments(rows);
      const data = await Promise.all(
        rows.map((r: any) => apiFetch(`/me/courses/${r.course_id}/progress`).catch(() => null))
      );
      const map: Record<number, any> = {};
      data.forEach((p) => {
        if (p) map[p.course_id] = p;
      });
      setProgress(map);
    });
  }, []);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Learner Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <p className="text-sm">Enrolled Courses</p>
          <p className="text-2xl font-bold">{enrollments.length}</p>
        </Card>
      </div>
      <div className="space-y-2">
        {enrollments.map((e) => {
          const p = progress[e.course_id];
          return (
            <Card key={e.id}>
              <p className="font-medium">Course #{e.course_id}</p>
              <p className="text-sm">Progress: {p?.completion_percent ?? 0}% ({p?.completed_lessons ?? 0}/{p?.total_lessons ?? 0})</p>
              <Link href="/courses" className="text-blue-600 underline">Open course catalog</Link>
              {p?.last_lesson_slug && <p className="text-xs text-slate-500">Last lesson slug: {p.last_lesson_slug}</p>}
            </Card>
          );
        })}
      </div>
    </div>
  );
}
