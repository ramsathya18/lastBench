"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";

export default function AdminModulePage() {
  const { id, moduleId } = useParams<{ id: string; moduleId: string }>();
  const [lessons, setLessons] = useState<any[]>([]);
  const [title, setTitle] = useState("");
  const [slug, setSlug] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const courses = await apiFetch(`/courses`);
      const courseMeta = courses.find((c: any) => String(c.id) === id);
      if (!courseMeta?.slug) throw new Error("Course not found");
      const course = await apiFetch(`/courses/${courseMeta.slug}`);
      const module = course.modules.find((m: any) => String(m.id) === moduleId);
      setLessons(module?.lessons || []);
    } catch (err) {
      setError((err as ApiError).message);
    }
  }

  useEffect(() => {
    load();
  }, [id, moduleId]);

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Course {id} / Module {moduleId}</h1>
      {error && <p className="text-sm text-red-600">{error}</p>}

      <form
        className="space-y-2 rounded border bg-white p-3"
        onSubmit={async (e) => {
          e.preventDefault();
          setMessage("");
          setError("");
          try {
            await apiFetch(`/admin/modules/${moduleId}/lessons`, {
              method: "POST",
              body: JSON.stringify({
                title,
                slug,
                summary: "",
                lesson_type: "article",
                content_markdown: "New lesson content",
                estimated_minutes: 10,
                sort_order: lessons.length + 1,
                status: "draft",
              }),
            });
            setTitle("");
            setSlug("");
            setMessage("Lesson created");
            await load();
          } catch (err) {
            setError((err as ApiError).message);
          }
        }}
      >
        <h2 className="font-semibold">Add lesson</h2>
        <input className="w-full border p-2" placeholder="Lesson title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <input className="w-full border p-2" placeholder="Lesson slug" value={slug} onChange={(e) => setSlug(e.target.value)} required />
        <Button type="submit">Create lesson</Button>
      </form>

      {message && <p className="text-sm text-emerald-700">{message}</p>}

      <div className="rounded border bg-white p-3">
        <h2 className="mb-2 font-semibold">Lessons</h2>
        <ul className="list-disc pl-5">
          {lessons.map((lesson) => (
            <li key={lesson.id}>{lesson.title} ({lesson.status})</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
