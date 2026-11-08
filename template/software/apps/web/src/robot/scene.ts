// Swap in robot's CAD export, e.g.
// gltfRobot("/models/robot1.glb", { draco: "/draco/", scale: 0.001, origin_m: [0, 0, 0] }) for glTF in mm,
// and own environment (MICROPIRO's is its pipe)

import { boxRobot, floorGrid } from "@hhart/ui";

export const ROBOT_MODEL = boxRobot({ length_m: 0.3, width_m: 0.2 }); // Width must match TRACK_M in core/ros_messages.py
export const ENVIRONMENT = floorGrid();
