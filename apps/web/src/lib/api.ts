import { tokenStore } from "@/lib/auth";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
  }
}

function parseErrorMessage(text: string): string {
  try {
    const payload = JSON.parse(text);
    return payload?.error?.message || payload?.detail || text;
  } catch {
    return text;
  }
}

async function performFetch(path: string, init?: RequestInit, overrideToken?: string) {
  const token = overrideToken ?? tokenStore.getAccess();
  const headers = new Headers(init?.headers || {});
  if (!headers.has("Content-Type") && init?.body) headers.set("Content-Type", "application/json");
  if (token && !headers.has("Authorization")) headers.set("Authorization", `Bearer ${token}`);
  return fetch(`${API}${path}`, { ...init, headers, cache: "no-store" });
}

export async function apiFetch(path: string, init?: RequestInit) {
  let res = await performFetch(path, init);

  if (res.status === 401 && path !== "/auth/refresh") {
    const refresh = tokenStore.getRefresh();
    if (refresh) {
      const refreshRes = await performFetch("/auth/refresh", {
        method: "POST",
        body: JSON.stringify({ refresh_token: refresh }),
      }, "");
      if (refreshRes.ok) {
        const tokens = await refreshRes.json();
        tokenStore.setTokens(tokens.access_token, tokens.refresh_token);
        res = await performFetch(path, init, tokens.access_token);
      } else {
        tokenStore.clear();
      }
    }
  }

  if (!res.ok) {
    const text = await res.text();
    throw new ApiError(parseErrorMessage(text) || "Request failed", res.status);
  }

  if (res.status === 204) return null;
  return res.json();
}
