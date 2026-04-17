"use client";
import { useParams } from "next/navigation";

export default function AdminModulePage() {
  const { id, moduleId } = useParams<{ id: string; moduleId: string }>();
  return <div><h1 className="text-xl font-bold">Course {id} / Module {moduleId}</h1></div>;
}
