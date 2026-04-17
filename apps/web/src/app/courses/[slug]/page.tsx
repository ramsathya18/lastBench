"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Button, Card } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";
import { CourseDetail } from "@/types/domain";

export default function CourseDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch(`/courses/${slug}`)
      .then((data) => setCourse(data))
      .catch((err: ApiError) => setError(err.message));
  }, [slug]);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!course) return <p>Loading...</p>;

  const first = course.modules?.[0]?.lessons?.[0];

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">{course.title}</h1>
      <p>{course.description}</p>
      <div className="flex items-center gap-3">
        <Button
          onClick={async () => {
            setError("");
            setStatus("");
            try {
              const res = await apiFetch(`/courses/${course.id}/enroll`, { method: "POST" });
              setStatus(res.message || "Enrolled");
            } catch (err) {
              setError((err as ApiError).message);
            }
          }}
        >
          Enroll
        </Button>
        {status && <span className="text-sm text-emerald-700">{status}</span>}
      </div>
      {first && (
        <Link href={`/learn/${course.slug}/${first.slug}`} className="text-blue-600 underline">
          Continue learning
        </Link>
      )}
      {course.modules?.map((m) => (
        <Card key={m.id}>
          <h3 className="font-semibold">{m.title}</h3>
          <ul className="list-disc pl-5 text-sm">
            {m.lessons.map((l) => (
              <li key={l.id}>{l.title}</li>
            ))}
          </ul>
        </Card>
      ))}
    </div>
  );
}
