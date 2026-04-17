"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch, ApiError } from "@/lib/api";
import { Course } from "@/types/domain";

export default function AdminCoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      setCourses(await apiFetch("/courses"));
    } catch (err) {
      setError((err as ApiError).message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-3">
      <h1 className="text-xl font-bold">Admin Courses</h1>
      <Link className="text-blue-600 underline" href="/admin/courses/new">New Course</Link>
      {error && <p className="text-sm text-red-600">{error}</p>}
      <table className="w-full border bg-white text-sm">
        <thead>
          <tr className="border-b bg-slate-50">
            <th className="p-2 text-left">Title</th>
            <th className="p-2 text-left">Status</th>
            <th className="p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {courses.map((c) => (
            <tr key={c.id} className="border-b">
              <td className="p-2">{c.title}</td>
              <td className="p-2">{c.status}</td>
              <td className="p-2">
                <Link className="mr-3 underline" href={`/admin/courses/${c.id}`}>Edit</Link>
                <button
                  className="text-red-700 underline"
                  onClick={async () => {
                    try {
                      await apiFetch(`/admin/courses/${c.id}`, { method: "DELETE" });
                      await load();
                    } catch (err) {
                      setError((err as ApiError).message);
                    }
                  }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
