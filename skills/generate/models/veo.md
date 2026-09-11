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
| Docs | https://ai.google.dev/gemini-api/docs/video |
| Cost | ~$0.30/sec (`veo`), ~$0.15/sec (`veo-fast`). An 8s clip is ~$2.40 / ~$1.20 |
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
  "parameters": {"aspectRatio": "16:9", "durationSeconds": 8}
}
```

The `image` field is the start frame and is optional. Veo takes one start
frame, not a set of references — for multi-reference animation use `seedance`.

## Response handling

Submit returns `{"name": "models/veo-.../operations/..."}`. Poll that name every
10s until `done: true`, then the file URL is nested under
`response.generateVideoResponse.generatedSamples[].video.uri`. Google has moved
this field between versions, so the script walks the response for the first
media URL rather than hardcoding the path.

**The download needs the API key header too** — the returned URI is not public.
Result URLs expire, so download immediately.

## Notes

- Clips are 8s at 720p. Ask for a long video and you get a short one.
- Renders take minutes. The script polls for up to 20 minutes then gives up.
- This is the single biggest bill risk in the skill. The `--yes` gate exists
  for this model. Never batch Veo runs.
