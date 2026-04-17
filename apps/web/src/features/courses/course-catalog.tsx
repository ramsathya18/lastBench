"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";
import { Course } from "@/types/domain";

export default function CourseCatalog() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch("/courses")
      .then(setCourses)
      .catch((err: ApiError) => setError(err.message));
  }, []);

  if (error) return <p className="text-sm text-red-600">{error}</p>;
  if (!courses.length) return <p className="text-sm text-slate-600">No published courses yet.</p>;

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {courses.map((c) => (
        <Card key={c.id}>
          <h3 className="font-semibold">{c.title}</h3>
          <p className="text-sm">{c.description}</p>
          <p className="mt-2 text-xs uppercase text-slate-500">{c.difficulty} · {c.estimated_minutes} min</p>
          <Link className="mt-2 inline-block text-blue-600 underline" href={`/courses/${c.slug}`}>
            View course
          </Link>
        </Card>
      ))}
    </div>
  );
}
