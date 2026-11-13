# Veo 3.1

Highest-quality video, especially animating from a start frame. Slow, and the
most expensive thing this skill can do. Prove the motion on `veo-fast` first.

| Field | Value |
|---|---|
| Aliases | `veo`, `veo-fast` |
| Model IDs | `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview` |
| Provider | Google AI Studio |
| Method | **Async** — submit, get an operation name, poll |
| Type | Video |
| API key | `.env` -> `GOOGLE_AI_API_KEY` (funded) |
| Docs | https://ai.google.dev/gemini-api/docs/veo?hl=en |
| Cost | `veo`: $0.40/sec at 720p/1080p, $0.60/sec at 4k. `veo-fast`: $0.10/sec at 720p, $0.12/sec at 1080p, $0.30/sec at 4k. An 8s 1080p clip is $3.20 / $0.96 |
| Verified | Model IDs confirmed live 2026-07-31. **Request/response shape written from docs, never run.** |

A `veo-3.1-lite-generate-preview` also exists on the key if an even cheaper
draft lane is wanted later.

## Endpoint

```
POST   https://generativelanguage.googleapis.com/v1beta/models/{model-id}:predictLongRunning
GET    https://generativelanguage.googleapis.com/v1beta/{operation-name}     # poll
```

## Request format

```json
{
  "instances": [{
    "prompt": "the prompt",
    "image": {"bytesBase64Encoded": "<base64>", "mimeType": "image/png"}
  }],
  "parameters": {
    "aspectRatio": "16:9",
    "durationSeconds": 8,
    "resolution": "1080p"
  }
}
```

The `image` field is the start frame and is optional. Veo takes one start
frame, not a set of references — for multi-reference animation use `seedance`.
The REST `resolution` field belongs inside `parameters`. Supported values are
`720p`, `1080p`, and `4k`; 1080p and 4k require an 8-second duration.

## Response handling

Submit returns `{"name": "models/veo-.../operations/..."}`. Poll that name every
10s until `done: true`, then the file URL is nested under
`response.generateVideoResponse.generatedSamples[].video.uri`. Google has moved
this field between versions, so the script walks the response for the first
media URL rather than hardcoding the path.

**The download needs the API key header too** — the returned URI is not public.
Result URLs expire, so download immediately.

## Notes

- Clips may be 4s, 6s, or 8s. Use 8s for 1080p or 4k.
- Renders take minutes. The script polls for up to 20 minutes then gives up.
- This is the single biggest bill risk in the skill. The `--yes` gate exists
  for this model. Never batch Veo runs.
