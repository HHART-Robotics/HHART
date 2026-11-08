import { formatValue, type Values } from "@hhart/ui/core";

export const BRAND = "robot1";

// Anything not listed gets generic panel or form
export const OWN_VIEWS = ["status", "fault", "error", "capability", "motors", "drive", "stop", "release", "switch"] as const;

export function motorsReadouts(motors?: Values) {
  return [
    { label: "Left", value: formatValue(motors?.left_pct), unit: "%" },
    { label: "Right", value: formatValue(motors?.right_pct), unit: "%" },
  ];
}
