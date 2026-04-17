"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";

export default function AdminCourseDetail() {
  const { id } = useParams<{ id: string }>();
  const [course, setCourse] = useState<any>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch("/courses").then((rows) => setCourse(rows.find((x: any) => String(x.id) === id)));
  }, [id]);

  if (!course) return <p>Loading...</p>;

  return (
    <div className="space-y-3">
      <h1 className="text-xl font-bold">Edit Course #{id}</h1>
      <input className="w-full border p-2" value={course.title} onChange={(e) => setCourse({ ...course, title: e.target.value })} />
      <input className="w-full border p-2" value={course.slug} onChange={(e) => setCourse({ ...course, slug: e.target.value })} />
      <textarea className="w-full border p-2" value={course.description ?? ""} onChange={(e) => setCourse({ ...course, description: e.target.value })} />
      <select className="w-full border p-2" value={course.status} onChange={(e) => setCourse({ ...course, status: e.target.value })}>
        <option value="draft">Draft</option>
        <option value="published">Published</option>
      </select>
      <Button
        onClick={async () => {
          setMessage("");
          setError("");
          try {
            await apiFetch(`/admin/courses/${id}`, {
              method: "PATCH",
              body: JSON.stringify({
                title: course.title,
                slug: course.slug,
                description: course.description || "",
                difficulty: course.difficulty || "beginner",
                estimated_minutes: course.estimated_minutes || 60,
                tags: course.tags || [],
                thumbnail_url: course.thumbnail_url || "",
                status: course.status,
              }),
            });
            setMessage("Course updated.");
          } catch (err) {
            setError((err as ApiError).message);
          }
        }}
      >
        Save changes
      </Button>
      {message && <p className="text-sm text-emerald-700">{message}</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
