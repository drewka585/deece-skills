# Gemini Omni 1.1 Flash

Token-priced image-to-video through Google's synchronous Interactions REST API.
The route is prepared for one 8-second, portrait, 720p comparison test and has
not made a paid generation call.

| Field | Value |
|---|---|
| Alias | `omni` |
| Model ID | `gemini-omni-1.1-flash` |
| Provider | Google AI Studio |
| Method | Synchronous `POST /v1beta/interactions` |
| Type | Image-to-video; one `--ref` start frame required |
| API key | `.env` -> `GOOGLE_AI_API_KEY` |
| Docs | https://ai.google.dev/gemini-api/docs/omni |
| Pricing | $1.50/M input tokens; $9/M text output including thought; $17.50/M video output |
| Verified | **Yes.** One live image-to-video run completed 2026-10-02: 8.000s, 720x1280, 24fps, AAC. |

## Endpoint and request

```text
POST https://generativelanguage.googleapis.com/v1beta/interactions
```

The script sends the reference image inline before the text, prefixes the text
with `<FIRST_FRAME>`, and requests inline 720p video. The original CLI prompt is
preserved in the sidecar; the prefix only binds the image's role, following the
official prompt-tag guidance.

```json
{
  "model": "gemini-omni-1.1-flash",
  "input": [
    {"type": "image", "data": "<base64>", "mime_type": "image/png"},
    {"type": "text", "text": "<FIRST_FRAME> <prompt>"}
  ],
  "response_format": {
    "type": "video",
    "aspect_ratio": "9:16",
    "resolution": "720p"
  },
  "generation_config": {"max_output_tokens": 46336},
  "background": false,
  "store": false,
  "stream": false
}
```

The paid POST is never retried. A transport timeout is an unknown outcome, not
permission to submit again.

## Duration and honest cost guard

The Omni guide does not document a duration request field. `--duration 8` is
therefore a prompt-driven target and price estimate, not a promise that the
provider will return exactly 8 seconds. The exact test prompt says "eight-second".

The general Interactions API documents `generation_config.max_output_tokens`.
Google prices 720p Omni video at 5,792 tokens/second, so the prepared route sends
`46,336` as the maximum output tokens for an 8-second request:

```text
5,792 tokens/s * 8s * $17.50 / 1,000,000 = $0.81088 video output
```

This caps response output tokens if Omni honors the documented generic field,
but it is not a strict total-dollar cap. Input tokens cost $1.50/M and text or
thought tokens cost $9/M; the docs provide no separate thought-token cap. Quote
the run as **about $0.81 video output plus small variable input/thought charges**.
Never translate that into a guaranteed final total before a real response.

The first live run returned exactly 8.000 seconds from the prompt-driven request.
That is one observation, not evidence of a hidden duration field. Its usage was
1,352 input tokens, 511 thought tokens, and 47,242 total output tokens; the video
modality was exactly 46,336 tokens, matching the requested `max_output_tokens`,
while total output exceeded that number. Therefore the field bounded the video
payload in this run but did not create a strict all-in token or dollar cap. The
sidecar's `$0.833362` is explicitly an upper estimate from usage, not an invoice.

Only 720p is exposed in this route. The docs call 1080p and 4K upscaled outputs,
but the pricing page does not publish a different token rate for them. Do not
quote or expose those resolutions until a supported billing rule is documented.

## Response and receipt

The REST API does not return the SDK-only `output_video` helper. The script scans
`steps[].content[]` for `type: "video"` or a `video/*` MIME type and accepts
base64 `data`. This route requests inline delivery and refuses response URIs
before sending credentials; it prints the interaction ID for manual recovery.
Do not resubmit a completed interaction without fresh paid-run approval.

The sidecar records the response `usage` object and a separate cost receipt.
When `output_tokens_by_modality` is complete, it calculates the public-list-price
cost from those modalities. When that breakdown is absent, it records an upper
estimate using the video rate for all output tokens and labels it as an estimate.

## Prepared comparison command

```bash
python3 execution/generate_media.py \
  --model omni --kind video \
  --prompt "$(<research/dope-as-yola/2026-10-02/reel/edit/ANIMATION_TEST_PROMPT.txt)" \
  --ref generations/yola-shawn-car-door-serious-start.png \
  --aspect 9:16 --duration 8 --resolution 720p \
  --project yola-omni --dry-run
```

Remove `--dry-run` and add `--yes` only after Drew explicitly approves this
new Omni charge. One approval authorizes one POST.

## Reference-role tags

- `<FIRST_FRAME>` binds the first image as the starting frame.
- `<LAST_FRAME>` binds a second image as the final interpolation frame and must
  be paired with `<FIRST_FRAME>`; this route does not expose a last frame yet.
- `<IMAGE_REF_N>` treats an image as a subject/style/object reference rather
  than a literal starting frame. Images are zero-indexed.
- The longer declaration form, such as
  `[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2]`, is for
  mixed source/reference inputs. This one-frame test does not need it.
