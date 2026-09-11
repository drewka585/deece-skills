# GPT Image 2

Reach for it when the image needs **readable text** (signs, posters, menus,
packaging, UI mockups, slide plates) or a **photoreal human face**. It is
noticeably more photoreal than `flux-schnell` on skin and faces, which is why
thumbnail finals go here.

| Field | Value |
|---|---|
| Aliases | `gpt-image` (quality=medium, ~$0.04), `gpt-image-hd` (quality=high, ~$0.17) |
| Model ID | `gpt-image-2` |
| Provider | **OpenAI direct** (was routed to fal.ai, which was never funded) |
| Method | Sync |
| Type | Image |
| API key | `.env` -> `OPENAI_API_KEY` — funded |
| Docs | https://platform.openai.com/docs/api-reference/images |
| Verified | **Yes**, both endpoints, 2026-07-31 |

## Two endpoints, chosen by whether refs are passed

**No `--ref` → `POST /v1/images/generations`**, JSON body:

```json
{"model": "gpt-image-2", "prompt": "...", "size": "1536x1024", "quality": "medium", "n": 1}
```

**With `--ref` → `POST /v1/images/edits`**, `multipart/form-data`. The `image[]`
field repeats, once per reference. This is the whole reason to use the model: it
keeps a real face or logo intact instead of regenerating a lookalike.

## Sizes

Only three are accepted. `OPENAI_SIZES` maps our aspect flag onto the nearest
one and the caller crops after:

| Aspect | Size sent |
|---|---|
| 16:9, 3:2, 4:3 | `1536x1024` |
| 1:1 | `1024x1024` |
| 9:16, 2:3, 3:4 | `1024x1536` |

## Response (verified)

```json
{"data": [{"b64_json": "<base64 png>"}]}
```

Always base64, never a URL. Decode `data[0].b64_json` straight to disk.

## Gotchas

- **`input_fidelity` is gpt-image-1 only.** Sending it to gpt-image-2 returns
  `400 image_generation_user_error` / `code: invalid_input_fidelity_model`.
  gpt-image-2 already edits at high fidelity, so the param is only added when
  `model_id` starts with `gpt-image-1`. Verified: with the param omitted, a
  reference image came back preserved exactly.
- **Nothing comes back 1280x720.** Every thumbnail path resizes after generation.
- The model renders text even when you did not ask for it. For thumbnails, tell
  it explicitly not to (`thumbnail_forge.py`'s `BASE_STYLE` does) and overlay the
  headline with PIL so it is pixel-exact.

## Related

For YouTube thumbnails do not call this directly — `directives/thumbnail_forge.md`
and `execution/thumbnail_forge.py` wrap it in a critic loop.
