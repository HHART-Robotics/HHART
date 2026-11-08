# api

Optional HTTP API for uploading and downloading recordings (rosbag2 `.mcap`,
`.db3`, or a zipped bag directory). The operator UI doesn't use it. No auth,
so keep it on the lab network.

```text
pnpm api                                      # from repo root. API_PORT (8081), API_STORE (./recordings)
curl -T run.mcap http://localhost:8081/api/recordings/run.mcap
curl http://localhost:8081/api/recordings     # newest first
curl -O http://localhost:8081/api/recordings/run.mcap
```

Files are stored in a folder (`adapters/storage.ts`). Implement `Store` to use
something else.
