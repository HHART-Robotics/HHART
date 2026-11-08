import fs from "node:fs";
import { expect, test } from "vitest";

const IO_GLOBALS = ["fetch", "setTimeout", "setInterval", "process", "require"];

function violations(source: string): string[] {
  const code = source.replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
  const found: string[] = [];
  for (const [, from] of code.matchAll(/\bimport\b[^"'`;]*["'`]([^"'`]+)["'`]/g)) {
    if (!from.startsWith("./")) found.push(`imports ${from}`);
  }
  for (const name of IO_GLOBALS) {
    if (new RegExp(`\\b${name}\\b`).test(code)) found.push(`uses ${name}`);
  }
  return found;
}

test("core/ imports only itself and touches no I/O", () => {
  const core = new URL("./core/", import.meta.url);
  const modules = fs.readdirSync(core).filter((f) => f.endsWith(".ts") && !f.endsWith(".test.ts"));
  expect(modules.length).toBeGreaterThanOrEqual(1); // Empty folder would pass by checking nothing
  const offenders = modules.flatMap((f) => violations(fs.readFileSync(new URL(f, core), "utf8")).map((v) => `${f}: ${v}`));
  expect(offenders).toEqual([]);
});

test("the check rejects what it should", () => {
  expect(violations('import fs from "node:fs";')).toEqual(["imports node:fs"]);
  expect(violations('import http from "http";')).toEqual(["imports http"]);
  expect(violations("const dir = process.cwd();")).toEqual(["uses process"]);
  expect(violations('import { route } from "./recordings.ts";')).toEqual([]);
});
