import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { applyTheme, readTheme } from "@hhart/ui";
import "@hhart/ui/styles.css";
import App from "./App.tsx";

// Before first paint, avoids theme flash
applyTheme(readTheme());

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
