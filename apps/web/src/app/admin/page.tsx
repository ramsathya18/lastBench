import Link from "next/link";

export default function AdminPage() {
  return <div className="space-y-3"><h1 className="text-2xl font-bold">Admin Panel</h1><Link className="text-blue-600 underline" href="/admin/courses">Manage Courses</Link><br/><Link className="text-blue-600 underline" href="/admin/analytics">Analytics</Link></div>;
}
