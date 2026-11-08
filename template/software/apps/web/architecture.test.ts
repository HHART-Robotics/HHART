import fs from "node:fs";
import { expect, test } from "vitest";

const IO_GLOBALS = [
  "document", "window", "localStorage", "sessionStorage", "navigator", "WebSocket", "fetch",
  "XMLHttpRequest", "getComputedStyle", "requestAnimationFrame", "setTimeout", "setInterval", "process",
];

function violations(source: string): string[] {
  const code = source.replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
  const found: string[] = [];
  for (const [, from] of code.matchAll(/\bimport\b[^"'`;]*["'`]([^"'`]+)["'`]/g)) {
    if (!from.startsWith("./") && from !== "@hhart/ui/core") found.push(`imports ${from}`);
  }
  for (const name of IO_GLOBALS) {
    if (new RegExp(`\\b${name}\\b`).test(code)) found.push(`uses ${name}`);
  }
  return found;
}

for (const dir of ["./src/core/"]) {
  test(`${dir} imports only itself and touches no I/O`, () => {
    const core = new URL(dir, import.meta.url);
    const modules = fs.readdirSync(core).filter((f) => f.endsWith(".ts") && !f.endsWith(".test.ts"));
    expect(modules.length).toBeGreaterThanOrEqual(1); // Empty folder would pass by checking nothing
    const offenders = modules.flatMap((f) => violations(fs.readFileSync(new URL(f, core), "utf8")).map((v) => `${f}: ${v}`));
    expect(offenders).toEqual([]);
  });
}

test("the check rejects what it should", () => {
  expect(violations('import React from "react";')).toEqual(["imports react"]);
  expect(violations('import fs from "node:fs";')).toEqual(["imports node:fs"]);
  expect(violations('import { decode } from "@hhart/ui";')).toEqual(["imports @hhart/ui"]);
  expect(violations('import { decode } from "@hhart/ui/core";')).toEqual([]);
  expect(violations("const ws = new WebSocket(url);")).toEqual(["uses WebSocket"]);
});
