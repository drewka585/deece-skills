# 1min.ai (Flux Schnell / Flux 2 Pro)

The prepaid lane, and therefore the **default**. The account is on a lifetime
deal, so these runs draw down a credit balance that is already paid for: zero
marginal dollars. Prefer 1min.ai over any real-money route unless the job needs
reference images.

| Field | Value |
|---|---|
| Aliases | `flux-schnell` (default draft), `flux-pro` |
| Model IDs | `black-forest-labs/flux-schnell`, `black-forest-labs/flux-2-pro` |
| Provider | 1min.ai |
| Method | Sync for images — finished image comes back in one call |
| Type | Image (video exists on the platform but is not wired, see below) |
| API key | `.env` -> `ONEMIN_API_KEY` |
| Docs | https://docs.1min.ai/docs/api/intro |
| Cost | **9,000 credits** (schnell) / **90,000 credits** (flux-2-pro) per image |
| Verified | **Yes** — both measured end to end 2026-07-31 on Drew's account |

## Credit economics

Measured by diffing `usedCredit` across sequential live calls, not from docs:

| Model | Credits/image | Images left from an 18.9M balance |
|---|---|---|
| `flux-schnell` | 9,000 | ~2,100 |
| `flux-2-pro` | 90,000 | ~210 |

The account also earns 15,000 free credits per daily login, which is roughly
1.6 schnell images a day if Drew logs in.

`flux-2-pro` costs 10x schnell, so it sits above `CREDIT_RUN_CEILING` (50,000)
and needs `--yes`. Draft on schnell, finish on pro.

## Endpoint

```
POST https://api.1min.ai/api/features
API-KEY: {ONEMIN_API_KEY}
Content-Type: application/json
```

Auth is the header literally named `API-KEY` — **not** `Authorization: Bearer`.
The intro docs page says Bearer and is wrong; `API-KEY` is what works.

## Request format

```json
{
  "type": "IMAGE_GENERATOR",
  "model": "black-forest-labs/flux-schnell",
  "promptObject": {
    "prompt": "...",
    "aspect_ratio": "16:9",
    "output_format": "png"
  }
}
```

`flux-2-pro` also accepts `steps`, `guidance`, `output_quality`,
`safety_tolerance`, `prompt_upsampling`, `seed`.

## Response handling

```
aiRecord.temporaryUrl                    the image URL (presigned S3, expires)
aiRecord.status                          "SUCCESS"
aiRecord.teamUser.usedCredit             running credit total  <- the balance signal
aiRecord.aiRecordDetail.resultObject[0]  the S3 object path
```

Download `temporaryUrl` immediately, it is presigned and expires.

**There is no GET balance endpoint.** Every plausible route
(`/api/users`, `/api/users/me`, `/api/teams/{id}`, `/api/user/credits`) returns
404. The only way to read credits is `teamUser.usedCredit` on a generation
response, which is why `generate_media.py` records it into the sidecar log as
`credits_used_to_date`. To know the balance, diff that against the UI figure.

Note `teamUser.creditLimit` reads 100,000,000 — that is a team-level cap, not
Drew's balance. Do not report it as available credit.

## Gotchas

- **Cloudflare 403 error code 1010.** 1min.ai sits behind Cloudflare, which
  blocks the default `Python-urllib/3.x` user agent. `curl` gets through,
  urllib does not. `generate_media.py` sends a browser UA on every request for
  this reason. Same failure class as the Supabase management API.
- **Model strings are exact.** `stability-ai/stable-diffusion-3.5-large` and
  `dall-e-3` both return `UNSUPPORTED_MODEL` even though the platform lists
  similar models in its UI. Errors come back as HTTP 200 with an `errorCode`
  field, so check the body, not the status.
- **No reference image support wired.** `IMAGE_GENERATOR` takes a text prompt
  only. The platform has separate `IMAGE_VARIATOR` and `IMAGE_EDITOR` features
  that are not built here. Passing `--ref` auto-switches to `nano-banana` and
  prints the swap.
- **Video is not wired.** 1min.ai hosts Veo3, Kling, Sora, Luma, Hailuo and
  more under `TEXT_TO_VIDEO`, which would move the whole expensive video lane
  onto prepaid credits — the single biggest saving available here. It returns
  `{}` and finishes asynchronously, and the "Get Result API" polling endpoint
  404s at every documented URL we tried. Wiring it needs the real endpoint,
  most cheaply captured from DevTools network traffic on the 1min.ai web app.
  The adapter fails loudly rather than pretending the job vanished.
