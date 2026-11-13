# Sync Labs sync-3 lip sync

Use this route for a video plus an authentic audio guide when a specific face must be
selected. The adapter is `execution/sync_lipsync.py`; do not hand-write a paid request.

| Field | Value |
|---|---|
| Alias | `sync-3` (dedicated lip-sync adapter; intentionally absent from the general registry) |
| Model ID | `sync-3` |
| Provider | Sync Labs direct API |
| Method | Async: one keyed POST, then GET status polling |
| Type | Lip-sync video |
| API key | `.env` or process environment: `SYNC_API_KEY` (fallback `SYNCLABS_API_KEY`) |
| Estimate | `POST https://api.sync.so/v2/generations/estimate` |
| Generate | `POST https://api.sync.so/v2/generate` |
| Status | `GET https://api.sync.so/v2/generate/{id}` |
| Verified | No real generation has run through this adapter |

Official docs: [estimate](https://sync.so/docs/api-reference/api/generate-api/estimate-cost),
[create](https://sync.so/docs/api-reference/api/generate-api/create),
[get](https://sync.so/docs/api-reference/api/generate-api/get),
[assets](https://sync.so/docs/developer-guides/asset-uploads),
[speaker selection](https://sync.so/docs/developer-guides/speaker-selection), and
[idempotency](https://sync.so/docs/api-reference/guides/idempotency).

## Yola/Shawn prepared packet

The approved local inputs are private and remain local until a paid run is explicitly
approved:

```bash
VIDEO=generations/yola-shawn-lipsync-input-h264.mp4
AUDIO=research/dope-as-yola/2026-10-02/reel/edit/audio/yola-quoted-reaction-8.041667s-guide.wav
VIDEO_SHA=886e0f47c036d7300f4788ef441ee678df0a41e9dd67ba3ad95dd523772d3889
AUDIO_SHA=30bbee18e1d8fa6c56c3d0e009d9a415c192ef29b20717665b798300ac0f8845

python3 execution/sync_lipsync.py preflight \
  --video "$VIDEO" --audio "$AUDIO" --target-frame 0 --target-x 320 --target-y 460 \
  --expected-video-sha256 "$VIDEO_SHA" --expected-audio-sha256 "$AUDIO_SHA" --dry-run
```

`preflight` is fully offline: it does not read a key, call the network, write a receipt,
upload media, or spend money. It requires silent H.264 video at exactly 1080x1918 and the
original mono 48 kHz 24-bit PCM WAV guide. Durations must match within 1 ms. The audio hash
prevents a processed, reverb, FX, or replacement track from silently becoming the mouth-sync
input. Face coordinates are validated in the native 1080x1918 coordinate space.

## Quote, approval, and submit

With an own-account key connected, obtain the authenticated exact estimate. This endpoint
does not upload or fetch media and does not create a generation:

```bash
python3 execution/sync_lipsync.py estimate \
  --video "$VIDEO" --audio "$AUDIO" --target-frame 0 --target-x 320 --target-y 460 \
  --expected-video-sha256 "$VIDEO_SHA" --expected-audio-sha256 "$AUDIO_SHA" \
  --receipt generations/yola-shawn-lipsync-sync3-estimate.json
```

Show Drew the exact USD estimate and wait for one explicit approval. A credit-billed plan,
missing/zero/unknown USD estimate, stale receipt, changed input hash, or shared-ledger total
over `$15` blocks submission. The estimate is a quote, never an actual invoice.

After approval, one command authorizes one run:

```bash
python3 execution/sync_lipsync.py submit \
  --video "$VIDEO" --audio "$AUDIO" --target-frame 0 --target-x 320 --target-y 460 \
  --expected-video-sha256 "$VIDEO_SHA" --expected-audio-sha256 "$AUDIO_SHA" \
  --estimate-receipt generations/yola-shawn-lipsync-sync3-estimate.json --yes
```

Only after `--yes`, a matching estimate, and the cap check does the adapter request private
upload slots, PUT the bytes without the API key, and register `USER` assets. It then writes
the action receipt and idempotency key before making exactly one `POST /v2/generate` with:

```json
{
  "model": "sync-3",
  "input": [
    {"type": "video", "assetId": "..."},
    {"type": "audio", "assetId": "..."}
  ],
  "options": {
    "sync_mode": "cut_off",
    "active_speaker_detection": {
      "auto_detect": false,
      "frame_number": 0,
      "coordinates": [320, 460]
    }
  }
}
```

The official `Idempotency-Key` contract protects the action, but the adapter deliberately
does not retry the paid POST. A timeout or `IDEMPOTENCY_*`/503 response is recorded as an
unknown outcome. If Sync returned `generationId`, recover only with:

```bash
python3 execution/sync_lipsync.py resume --receipt generations/sync-lipsync-action-ACTION_UUID.json
```

`resume` performs status GETs and a result download; it never uploads or creates a new job.
If the unknown response has no generation ID, contact Sync support with the receipt. Never
use a fresh key or unkeyed request to bypass an unknown outcome.

On acceptance, the authenticated estimate is reserved in the shared generation ledger with
`cost_basis=provider estimate reserved for cap; actual charge unavailable`. The action
receipt keeps `actual_charge_usd: null` because Sync's generation status does not expose an
invoice amount. Download failure is recoverable with `resume` and never authorizes a second
generation.
