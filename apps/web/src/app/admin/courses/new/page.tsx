"use client";

import { useState } from "react";
import { Button } from "@/components/ui";
import { apiFetch, ApiError } from "@/lib/api";

export default function NewCoursePage() {
  const [title, setTitle] = useState("");
  const [slug, setSlug] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("draft");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  return (
    <form
      className="space-y-2"
      onSubmit={async (e) => {
        e.preventDefault();
        setError("");
        setMessage("");
        try {
          await apiFetch("/admin/courses", {
            method: "POST",
            body: JSON.stringify({
              title,
              slug,
              description,
              difficulty: "beginner",
              estimated_minutes: 60,
              tags: [],
              thumbnail_url: "",
              status,
            }),
          });
          setMessage("Course created.");
        } catch (err) {
          setError((err as ApiError).message);
        }
      }}
    >
      <h1 className="text-xl font-bold">New Course</h1>
      <input className="w-full border p-2" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
      <input className="w-full border p-2" placeholder="Slug" value={slug} onChange={(e) => setSlug(e.target.value)} required />
      <textarea className="w-full border p-2" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
      <select className="w-full border p-2" value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="draft">Draft</option>
        <option value="published">Published</option>
      </select>
      <Button type="submit">Create</Button>
      {message && <p className="text-sm text-emerald-700">{message}</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}
    </form>
  );
}
