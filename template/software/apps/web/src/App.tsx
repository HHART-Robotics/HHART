import { useCallback, useEffect, useState } from "react";
import {
  CameraPanel, CapabilityPanel, CommandForm, Drawer, DrivePanel, FaultsPanel, MessagePanel, PoseHud, SceneView,
  STOP_EVENT, Shell, TopBar, applyTheme, formsOf, panelsOf, readTheme, stop, useBridge, type Theme,
} from "@hhart/ui";
import { BRAND, OWN_VIEWS, motorsReadouts } from "./core/robot.ts";
import { ENVIRONMENT, ROBOT_MODEL } from "./robot/scene.ts";

function RosNotes() {
  return (
    <div className="cap-notes">
      <p>On the robot, after <code>source /opt/ros/jazzy/setup.bash</code>:</p>
      <p><code>ros2 topic pub --rate 5 /cmd_vel geometry_msgs/msg/Twist "{"{linear: {x: 0.1}}"}"</code></p>
      <p><code>ros2 run teleop_twist_keyboard teleop_twist_keyboard</code></p>
      <p>Put the robot on blocks first. It stops 0.5 s after the last /cmd_vel message. After an operator stop, ROS
        can't drive until Release.</p>
    </div>
  );
}

export default function App() {
  const { state, connected, send } = useBridge();
  const [theme, setTheme] = useState<Theme>(readTheme);
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);
  const toggleTheme = useCallback(() => setTheme((t) => {
    const next = t === "dark" ? "light" : "dark";
    applyTheme(next);
    return next;
  }), []);
  // Lets drive panel drop held drive, stop sent regardless
  const halt = useCallback(() => {
    window.dispatchEvent(new Event(STOP_EVENT));
    send(stop());
  }, [send]);

  return (
    <Shell
      topBar={
        <TopBar brand={BRAND} connected={connected} route={state.latest.status?.route as string | undefined}
          chips={state.capabilities.ros?.running ? <span className="chip chip-neutral">ROS 2 on</span> : null}
          theme={theme} onToggleTheme={toggleTheme} onStop={halt} />
      }
      left={
        <>
          <DrivePanel send={send} disabled={!connected} />
          <FaultsPanel faults={state.faults} error={state.latest.error} />
        </>
      }
      centre={
        <SceneView environment={ENVIRONMENT} robotModel={ROBOT_MODEL} pose={null} state={state} theme={theme} title="Robot">
          <PoseHud title="Motors" readouts={motorsReadouts(state.latest.motors)} />
        </SceneView>
      }
      right={
        <>
          <CameraPanel />
          {panelsOf(state.contract, OWN_VIEWS).map((m) => <MessagePanel key={m.name} message={m} state={state} now={now} />)}
          {formsOf(state.contract, OWN_VIEWS).map((m) => <CommandForm key={m.name} message={m} send={send} disabled={!connected} />)}
        </>
      }
      drawer={
        <Drawer tabs={[{
          id: "ros", label: "ROS 2", render: () => (
            <CapabilityPanel name="ros" label="ROS 2" capabilities={state.capabilities} connected={connected} send={send}>
              <RosNotes />
            </CapabilityPanel>
          ),
        }]} />
      }
    />
  );
}
