import { tokenStore } from "@/lib/auth";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
  }
}

export async function apiFetch(path: string, init?: RequestInit) {
  const token = tokenStore.get();
  const headers = new Headers(init?.headers || {});
  if (!headers.has("Content-Type") && init?.body) headers.set("Content-Type", "application/json");
  if (token && !headers.has("Authorization")) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API}${path}`, { ...init, headers, cache: "no-store" });
  if (!res.ok) {
    const text = await res.text();
    let message = text;
    try {
      const payload = JSON.parse(text);
      message = payload?.error?.message || payload?.detail || text;
    } catch {
      // keep raw text fallback
    }
    throw new ApiError(message || "Request failed", res.status);
  }

  if (res.status === 204) return null;
  return res.json();
}
