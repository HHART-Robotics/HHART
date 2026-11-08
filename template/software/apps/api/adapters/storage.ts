import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import type { Readable } from "node:stream";
import { pipeline } from "node:stream/promises";
import type { Entry } from "../core/recordings.ts";

export type Store = {
  list(): Promise<Entry[]>;
  save(name: string, stream: Readable): Promise<void>;
  exists(name: string): Promise<boolean>;
  open(name: string): Readable;
};

export function directoryStore(dir: string): Store {
  const at = (name: string) => path.join(dir, name);
  return {
    async list() {
      await fsp.mkdir(dir, { recursive: true });
      const names = await fsp.readdir(dir);
      return Promise.all(names.map(async (name) => {
        const s = await fsp.stat(at(name));
        return { name, bytes: s.size, modified_ms: s.mtimeMs };
      }));
    },
    // Write then rename, dropped upload never shows as recording
    async save(name, stream) {
      await fsp.mkdir(dir, { recursive: true });
      const part = at(`.${name}.part`);
      await pipeline(stream, fs.createWriteStream(part));
      await fsp.rename(part, at(name));
    },
    exists(name) {
      return fsp.access(at(name)).then(() => true, () => false);
    },
    open(name) {
      return fs.createReadStream(at(name));
    },
  };
}
