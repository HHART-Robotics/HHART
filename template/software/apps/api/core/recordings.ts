export const KINDS = [".mcap", ".db3", ".zip"]; // .zip for bag directories

export type Entry = { name: string; bytes: number; modified_ms: number };
export type Route = { action: "health" } | { action: "list" } | { action: "save"; name: string } | { action: "get"; name: string };

// Null if safe, else reason. No separators, so names can't escape store
export function checkName(name: string): string | null {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(name)) {
    return "a name is letters, digits, dots, dashes and underscores, starting with a letter or digit";
  }
  if (!KINDS.some((kind) => name.endsWith(kind))) return `a recording ends in ${KINDS.join(", ")}`;
  return null;
}

export function route(method: string | undefined, path: string): Route | null {
  if (method === "GET" && path === "/api/health") return { action: "health" };
  if (method === "GET" && path === "/api/recordings") return { action: "list" };
  const match = path.match(/^\/api\/recordings\/([^/]+)$/);
  if (!match) return null;
  let name: string;
  try {
    name = decodeURIComponent(match[1]);
  } catch {
    return null; // Malformed %-escape
  }
  if (method === "PUT") return { action: "save", name };
  if (method === "GET") return { action: "get", name };
  return null;
}

export function listing(entries: Entry[]): Entry[] {
  return entries.filter((e) => checkName(e.name) === null).sort((a, b) => b.modified_ms - a.modified_ms);
}
