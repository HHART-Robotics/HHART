import fs from "node:fs";
import { expect, test } from "vitest";

import { INITIAL_STATE, decode, drive, release, stop, switchCapability, type Describe, type Message } from "@hhart/ui/core";
import { motorsReadouts } from "./robot.ts";

// Regen with hhart contract
const golden = JSON.parse(fs.readFileSync(new URL("./contract.golden.json", import.meta.url), "utf8")) as Message[];
const describe = golden.find((m) => m.type === "describe") as Describe;
const byType = Object.fromEntries(golden.map((m) => [m.type, m]));

test("every message the robot sends is decoded once it is described", () => {
  const outgoing = describe.messages.filter((m) => m.direction === "out").map((m) => m.name);
  let state = decode(INITIAL_STATE, describe);
  for (const name of outgoing) state = decode(state, byType[name]);
  expect(Object.keys(state.latest).sort()).toEqual([...outgoing].sort());
});

test("the interface's commands are the ones the contract defines", () => {
  expect(drive(byType.drive.direction as "forward", byType.drive.pct as number)).toEqual(byType.drive);
  expect(stop()).toEqual(byType.stop);
  expect(release()).toEqual(byType.release);
  expect(switchCapability(byType.switch.name as string, byType.switch.running as boolean)).toEqual(byType.switch);
});

test("the motors read as a dash until the device reports", () => {
  expect(motorsReadouts().map((r) => r.value)).toEqual(["-", "-"]);
  expect(motorsReadouts({ left_pct: -40, right_pct: 40 }).map((r) => r.value)).toEqual(["-40", "40"]);
});
