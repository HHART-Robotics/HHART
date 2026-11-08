import { expect, test } from "vitest";

import { checkName, listing, route } from "./recordings.ts";

test("a recording's name cannot leave the store or hide in it", () => {
  expect(checkName("run_2026-11-07.mcap")).toBeNull();
  expect(checkName("bag.zip")).toBeNull();
  for (const bad of ["../x.mcap", "a/b.mcap", "a\\b.mcap", ".x.mcap", "x.mcap.part", "notes.txt", ""]) {
    expect(checkName(bad), bad).not.toBeNull();
  }
});

test("routes are health, the listing, and one recording by name", () => {
  expect(route("GET", "/api/health")).toEqual({ action: "health" });
  expect(route("GET", "/api/recordings")).toEqual({ action: "list" });
  expect(route("PUT", "/api/recordings/run%201.mcap")).toEqual({ action: "save", name: "run 1.mcap" });
  expect(route("GET", "/api/recordings/a.db3")).toEqual({ action: "get", name: "a.db3" });
  expect(route("DELETE", "/api/recordings/a.db3")).toBeNull();
  expect(route("GET", "/api/recordings/a/b.db3")).toBeNull();
  expect(route("GET", "/api/recordings/%E0%A4%A.mcap")).toBeNull();
});

test("the listing is newest first and skips anything that is not a recording", () => {
  const entries = [{ name: "old.mcap", bytes: 1, modified_ms: 1 }, { name: ".new.mcap.part", bytes: 2, modified_ms: 3 },
    { name: "new.mcap", bytes: 3, modified_ms: 2 }];
  expect(listing(entries).map((e) => e.name)).toEqual(["new.mcap", "old.mcap"]);
});
