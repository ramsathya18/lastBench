import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Learning Platform MVP</h1>
      <p>Host project-based learning content with quizzes and sandbox tasks.</p>
      <Link href="/courses" className="text-blue-600 underline">Browse catalog</Link>
    </div>
  );
}
