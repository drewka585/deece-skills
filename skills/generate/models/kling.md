# Kling 3.0

The sensible general-purpose video default: good motion, fair price, faster
than Veo. This is what `--kind video` picks when nobody names a model.

| Field | Value |
|---|---|
| Alias | `kling` |
| Model ID | `kling-3.0/video` |
| Provider | Kie AI |
| Method | **Async** — create task, poll by taskId |
| Type | Video |
| API key | `.env` -> `KIE_API_KEY` — **NOT FUNDED YET** |
| Docs | https://docs.kie.ai |
| Cost | ~$0.20/sec. A 5s clip is ~$1.00 |
| Verified | **No.** Written from docs, never run. |

std is 720p, pro is 1080p. Clips run 3 to 15 seconds.

## Endpoint

```
POST https://api.kie.ai/api/v1/jobs/createTask
GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId={id}
Authorization: Bearer {KIE_API_KEY}
```

Kie uses `Bearer`, fal uses `Key`, Google uses a header key. Three providers,
three shapes — this is the thing that trips people up.

## Request format

```json
{"model": "kling-3.0/video",
 "input": {"prompt": "...", "aspect_ratio": "16:9", "duration": 5}}
```

## Response handling

Create returns `data.taskId`. Poll `recordInfo` every 10s until
`data.state == "success"`, then the file URL is inside `data.resultJson`
(a JSON **string** in some responses — parse it if the URL walker misses).
Download immediately, result URLs expire in hours.

## Notes

- Unfunded. Until `KIE_API_KEY` exists, video routes to `veo-fast` on Google.
- **References are not wired for Kie.** Kie wants a public URL and has a file
  upload endpoint for turning local images into one; that upload step is not
  built. The script errors clearly rather than silently dropping the reference.
  Use `veo` (start frame) or `seedance` (multi-reference) for ref-driven video.
