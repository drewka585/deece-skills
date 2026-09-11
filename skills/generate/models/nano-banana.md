# Nano Banana 2 (Gemini image models)

Everyday images. Cheap, fast, unusually good at honouring reference images.
This is the default lane: draft on Lite, finish on Pro only once Drew picks one.

| Field | Value |
|---|---|
| Aliases | `nano-banana` (Lite), `nano-banana-hd`, `nano-banana-pro` |
| Model IDs | `gemini-3.1-flash-lite-image`, `gemini-3.1-flash-image`, `gemini-3-pro-image` |
| Provider | Google AI Studio |
| Method | Sync — the finished image comes back in one call |
| Type | Image |
| API key | `.env` -> `GOOGLE_AI_API_KEY` (funded, already in use) |
| Docs | https://ai.google.dev/gemini-api/docs/image-generation |
| Cost | ~$0.034 (Lite) / ~$0.06 / ~$0.14 per 1K image |
| Verified | Model IDs confirmed live on Drew's key 2026-07-31. Request shape is the same one `execution/thumbnail_gen.py` has used in production. |

## Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model-id}:generateContent
```

Auth is the header `x-goog-api-key: {GOOGLE_AI_API_KEY}`. The provider docs also
show `?key=` in the URL; the header works and keeps the key out of logs and
shell history, so use the header.

## Request format

```json
{
  "contents": [{"parts": [
    {"inline_data": {"mime_type": "image/png", "data": "<base64 reference>"}},
    {"text": "the prompt"}
  ]}],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {"aspectRatio": "16:9"}
  }
}
```

References are passed **inline as base64** — no upload step, no public URL.
This is why Google is the right route for anything logo- or face-driven.
Repeat the `inline_data` part for each reference.

## Response handling

```
candidates[0].content.parts[] -> the part carrying inlineData
  .inlineData.data      base64 image bytes
  .inlineData.mimeType  gives you the extension
```

Note the casing flip: the request uses `inline_data`, the response returns
`inlineData`. The script accepts either.

## Notes

- `responseModalities: ["IMAGE"]` is required or you get text back describing
  the picture instead of the picture.
- Text rendered inside the image is unreliable at small sizes. If the words
  must be legible, use `gpt-image`, or generate a clean plate and overlay the
  text deterministically (`execution/thumbnail_gen.py` does this with PIL).
- Aspect ratio is a hint, not a guarantee. Check the output dimensions before
  handing anything to a layout.
