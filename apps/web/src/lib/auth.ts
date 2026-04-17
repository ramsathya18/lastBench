"use client";

export const tokenStore = {
  get: () => (typeof window === "undefined" ? "" : localStorage.getItem("access_token") || ""),
  set: (token: string) => localStorage.setItem("access_token", token),
  clear: () => localStorage.removeItem("access_token"),
};
