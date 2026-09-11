# Seedance 2.0 Fast

Reference-to-video. Feed it up to 9 images and it animates them. The right pick
when the clip has to feature a real product, logo or person rather than
whatever the model imagines from a text prompt.

| Field | Value |
|---|---|
| Alias | `seedance` |
| Model ID | `bytedance/seedance-2.0/fast/reference-to-video` |
| Provider | fal.ai |
| Method | Sync via `fal.run` (blocks; can be a long block) |
| Type | Video |
| API key | `.env` -> `FAL_KEY` — **NOT FUNDED YET** |
| Docs | https://fal.ai/models/bytedance/seedance-2.0 |
| Cost | ~$0.24/sec at 720p. A 5s clip is ~$1.21 |
| Verified | **No.** Written from docs, never run. |

## Endpoint

```
POST https://fal.run/bytedance/seedance-2.0/fast/reference-to-video
Authorization: Key {FAL_KEY}
```

## Request format

```json
{"prompt": "...", "aspect_ratio": "16:9", "duration": 5,
 "reference_image_urls": ["data:image/png;base64,...", "..."]}
```

Up to 9 references. The script sends `data:` URIs so local files work without
an upload step — confirm on first real run.

## Response handling

`video.url` -> download immediately.

## Notes

- Unfunded until `FAL_KEY` is set.
- A sync call that renders video can block for minutes. If it times out, check
  whether fal has moved this model to a queue endpoint
  (`https://queue.fal.run/...`), which would make it async and need a poll loop.
