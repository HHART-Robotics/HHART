import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Linked @hhart/ui would otherwise bundle second React and three
export default defineConfig({
  plugins: [react()],
  resolve: { dedupe: ["react", "react-dom", "three"] },
  server: { port: 3000 },
});
