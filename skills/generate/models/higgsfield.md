# Higgsfield (pay-per-use API): Kling 3.0 Pro + Seedance 2.5, image-to-video

Both models animate from a START FRAME you supply, with an optional END FRAME. There is
no text-to-video here: no `--ref`, no run. Use `veo-fast`, `veo` or `sora` for text-only.

| Field | Value |
|---|---|
| Alias | `kling` (Kling 3.0 Pro), `seedance-2.5` (Seedance 2.5) |
| Model ID | `kling-video/v3.0/pro/image-to-video`, `bytedance/seedance-2.5/image-to-video` |
| Provider | Higgsfield (`api.higgsfield.ai`), prepaid credits, pay-per-use |
| Method | **Async**: upload frames, submit, poll `status_url` |
| Type | Video (silent: audio is switched off in both) |
| API key | `.env` -> `HF_KEY`, format `key-id:key-secret` (one colon). Balance loaded by Drew. |
| Docs | https://docs.higgsfield.ai/docs/models/kling-3/pro-image-to-video.md , https://docs.higgsfield.ai/docs/models/seedance-2-5/image-to-video.md |
| Cost | Kling ~$0.112/s list, Seedance 1080p ~$1.137/s list (table below) |
| Verified | **Kling 3.0 Pro verified live 2026-10-02** (request 6857bde8, start+end frame, completed in 216s, 1924x1076 24fps MP4, at most $1.26). **Seedance 2.5 verified live 2026-10-08** (request 80d52b2c, 4s 720p image-to-video, ~$1.85 at list, 1270x726 24fps h264 97-frame silent mp4, ~3.5 min incl. flux-dev start still). See Response handling below. |

`kling` used to point at Kie AI (no key). It now routes here; the old route is `kling-kie`.

## CLI

```
python3 execution/generate_media.py --prompt "..." --model kling --ref START.png \
    --end-frame END.png --duration 10 --yes
python3 execution/generate_media.py --prompt "..." --model seedance-2.5 --ref START.png \
    --end-frame END.png --duration 8 --resolution 1080p --yes
```

Add `--dry-run` (no network, no `--yes` needed) to get the quote. `--ref` is the first
frame, `--end-frame` the last. `--aspect` is ignored: see Notes. The usual `--yes` gate
and the cumulative `GENERATE_USD_CAP` ($40 default since 2026-10-08) both apply.

## Endpoints (base `https://api.higgsfield.ai`, header `Authorization: Key KEYID:SECRET`)

```
POST /files/generate-upload-url   {"content_type": "image/png"}
      -> public_url, upload_url, upload_headers   (slot expires in 1 hour)
PUT  <upload_url>                 raw bytes + upload_headers, NO Higgsfield credentials
POST /<model id>                  generation body + header Idempotency-Key: <uuid4>
      -> {status:"queued", request_id, status_url, cancel_url}
GET  /requests/{request_id}/status        (the status_url)
POST /requests/{request_id}/cancel        (only works before processing starts)
POST /estimate/<model id>         same body as the generation; returns credits + usd
```

Upload accepts JPEG, PNG, WebP, GIF (plus WAV, MP4 for other models). Generation URLs must
be public: `asset://` references are rejected.

## Request format

Kling 3.0 Pro (a non-empty `prompt` is required by the docs):

```json
{"prompt": "...", "image_url": "<start>", "last_image_url": "<end>",
 "duration": 10, "sound": "off"}
```

`duration` 3 to 15, default 5. `sound` is the STRING `"on"`/`"off"` (default on), not a
boolean. Unused: `cfg_scale`, `elements`, `multi_shots`, `multi_prompt`. There is NO
`aspect_ratio` and NO `resolution` param on this endpoint.

Seedance 2.5 (`additionalProperties: false`, so an unknown field is a 422):

```json
{"prompt": "...", "image_url": "<start>", "end_image_url": "<end>",
 "duration": 8, "resolution": "1080p", "generate_audio": false}
```

`duration` 4 to 30, default 5. `resolution` 480p/720p/1080p, default 720p (the script
defaults to 1080p). `bitrate_mode` standard/high, default high, left alone. `prompt` is
optional. NO `aspect_ratio`.

## Response handling

**Verified 2026-10-02 (`kling`, request 6857bde8):** 10s start+end frame, 1344x752 start
frame in, 1924x1076 24fps 241-frame silent mp4 out, queued -> in_progress -> completed in
216s. The shape below held exactly.

**Verified 2026-10-08 (`seedance-2.5`, request 80d52b2c-85cb-4fa7-b1a5-2fa30e1ce146):** 4s, 720p, start frame only (flux-dev still), no end frame. Output 1270x726 (NOT exact 16:9; follows the start frame) 24fps h264, 97 frames, 4.04s, no audio stream, 1.8 MB. Request shape and polling held with no code change. Wired into `execution/broll_generate.py` (generated B-roll for the AI edit pipeline). Gotcha: the ledger cap (`GENERATE_USD_CAP`, default $15) was already exceeded at $29.01 cumulative, so the run refused until the cap was overridden per-process for this one approved run.

Poll `status_url` (script: 2s, backing off to 10s, GET retried on 5xx, 30 minute cap).
Status values: `queued`, `in_progress`, `completed`, `failed`, `nsfw`, `canceled`.

- `completed`: the file is at `video.url` (script falls back to the URL walker). Download
  it at once: outputs are kept at least 7 days, then may be removed.
- `failed`, `nsfw`: NOT charged. Credits reserved at accept time are refunded
  automatically. The script exits non-zero and prints the `request_id`.
- `canceled`: refunded only if it was canceled while queued.
- Poll timeout or Ctrl-C: the job keeps running and may still bill. The script prints the
  `request_id` and `status_url`. If the job completed but the download failed, the script
  still writes the spend to the ledger.

HTTP errors come back as `{"detail": ...}` with an `X-Correlation-ID` header (the script
prints it, quote it to support). 400 = bad params OR the concurrency cap (max 4 queued or
running at once), 401 bad creds, 403 `Insufficient credits`, 404, 422, 423 model blocked,
503 model disabled.

## Pricing

USD per second, from `POST /estimate/<model id>` on 2026-10-02 (documented as
non-generating; it was called, no generation was). Source:
https://docs.higgsfield.ai/docs/concepts/billing-and-retention.md

| Model | Tier | List $/s | 8s | 10s |
|---|---|---|---|---|
| Kling 3.0 Pro | (no tiers) | 0.112 | 0.90 | 1.12 |
| Seedance 2.5 | 480p | 0.2056 | 1.64 | 2.06 |
| Seedance 2.5 | 720p | 0.4622 | 3.70 | 4.62 |
| Seedance 2.5 | 1080p | 1.1372 | 9.10 | 11.37 |

- The account's own Kling estimate came back $0.952 for 10s ($0.0952/s), which is list
  minus a 15% discount. The script quotes LIST so a quote never under-states.
- Seedance figures are 16:9, no video input, before any discount. Public pricing page:
  https://open.higgsfield.ai/pricing
- Drew is claiming a promo that lowers both. Do not lower the numbers in `MODELS` until a
  funded run's balance delta shows the promo is applied.
- Credits expire one year after they are added.
- At the old $15 `GENERATE_USD_CAP` (now $40), one Seedance 10s 1080p run ($11.37) fits and a second
  does not. Kling 10s is $1.12.

## Notes

- **Framing follows the start frame.** Neither endpoint takes aspect or resolution (Kling)
  or aspect (Seedance). For 16:9 output, feed a 16:9 start frame. `--aspect` is ignored
  and the script says so.
- **Plain HTTP, not the `higgsfield_client` SDK.** The SDK retries POSTs on 408/429/5xx up
  to 3 times with NO Idempotency-Key, so a flaky submit can create two billed jobs. The
  script sends an `Idempotency-Key` and never retries the job-creating POST. Reusing a
  key with different params returns 422. The docs call the header optional on one page
  and required on another; we always send it. The docs say an ambiguous timeout can be
  retried with the same key; the script does not rely on that and stops instead.
- Only the first `--ref` is used (one start frame). More than one is refused.
- The status and download requests send the key only to `api.higgsfield.ai`. The signed
  upload PUT and the output download carry no credentials.
- Kling's silent output is deliberate (`sound: off`). Remove `audio_off` in `MODELS` to
  get generated audio.
- Other Kling 3.0 variants exist (standard, turbo, 4k image-to-video). Not wired.
