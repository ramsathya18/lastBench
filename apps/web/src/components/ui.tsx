import { PropsWithChildren } from "react";

export function Card({ children }: PropsWithChildren) {
  return <div className="rounded-xl border bg-white p-4 shadow-sm">{children}</div>;
}

export function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button {...props} className={`rounded-md bg-slate-900 px-3 py-2 text-white ${props.className || ""}`} />;
}
