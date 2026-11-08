import http from "node:http";
import { directoryStore } from "./adapters/storage.ts";
import { checkName, listing, route } from "./core/recordings.ts";

const PORT = Number(process.env.API_PORT ?? 8081);
const store = directoryStore(process.env.API_STORE ?? "recordings");

function reply(res: http.ServerResponse, status: number, body: unknown): void {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
}

async function handle(req: http.IncomingMessage, res: http.ServerResponse): Promise<void> {
  const r = route(req.method, new URL(req.url ?? "/", "http://api").pathname);
  if (r === null) return reply(res, 404, { error: "not found" });
  if (r.action === "health") return reply(res, 200, { ok: true });
  if (r.action === "list") return reply(res, 200, listing(await store.list()));
  const bad = checkName(r.name);
  if (bad) return reply(res, 400, { error: bad });
  if (r.action === "save") {
    await store.save(r.name, req);
    return reply(res, 201, { name: r.name });
  }
  if (!(await store.exists(r.name))) return reply(res, 404, { error: `no recording ${r.name}` });
  res.writeHead(200, { "content-type": "application/octet-stream" });
  store.open(r.name).pipe(res);
}

http.createServer((req, res) => {
  handle(req, res).catch((err: unknown) => reply(res, 500, { error: String(err instanceof Error ? err.message : err) }));
}).listen(PORT, () => console.log(`research API on http://localhost:${PORT}/api`));
