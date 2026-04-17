"use client";

const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

function getStorage() {
  if (typeof window === "undefined") return null;
  return localStorage;
}

export const tokenStore = {
  getAccess: () => getStorage()?.getItem(ACCESS_KEY) || "",
  getRefresh: () => getStorage()?.getItem(REFRESH_KEY) || "",
  setTokens: (accessToken: string, refreshToken: string) => {
    const storage = getStorage();
    if (!storage) return;
    storage.setItem(ACCESS_KEY, accessToken);
    storage.setItem(REFRESH_KEY, refreshToken);
  },
  clear: () => {
    const storage = getStorage();
    if (!storage) return;
    storage.removeItem(ACCESS_KEY);
    storage.removeItem(REFRESH_KEY);
  },
};
