---
name: generate
description: Generate images and videos via AI model APIs. Routes to the cheapest capable model, quotes cost before any paid video run, and files every output flat into generations/ with a prompt log. Use when Drew says /generate, generate an image, generate a video, make a thumbnail, create a key visual, mock up a graphic, animate this, image for the deck/newsletter/landing page, or asks for a picture or clip of anything.
---

# /generate

One command for media. Layer 2 (you) picks the model and enforces the money
rules; Layer 3 (`execution/generate_media.py`) does the API call, the polling,
the download, and the log. **Never hand-roll an API call for this.** If a model
is missing, add a row to `MODELS` in the script and a recipe in `models/`.

## Models

| Task | Alias | Model | Recipe |
|---|---|---|---|
| **Image, default draft** | `flux-schnell` | Flux Schnell (prepaid) | [models/onemin.md](models/onemin.md) |
| Image, quality on prepaid | `flux-pro` | Flux 2 Pro (prepaid) | [models/onemin.md](models/onemin.md) |
| Image with references | `nano-banana` | Nano Banana 2 Lite | [models/nano-banana.md](models/nano-banana.md) |
| Image, one step up | `nano-banana-hd` | Nano Banana 2 | [models/nano-banana.md](models/nano-banana.md) |
| Image, hero/final | `nano-banana-pro` | Nano Banana 2 Pro | [models/nano-banana.md](models/nano-banana.md) |
| Image with readable text | `gpt-image` | GPT Image 2 | [models/gpt-image.md](models/gpt-image.md) |
| Photoreal faces, thumbnail finals | `gpt-image-hd` | GPT Image 2 @ quality=high | [models/gpt-image.md](models/gpt-image.md) |
| Video, default | `kling` | Kling 3.0 | [models/kling.md](models/kling.md) |
| Video, draft lane | `veo-fast` | Veo 3.1 Fast | [models/veo.md](models/veo.md) |
| Video, hero | `veo` | Veo 3.1 | [models/veo.md](models/veo.md) |
| Reference-to-video | `seedance` | Seedance 2.0 Fast | [models/seedance.md](models/seedance.md) |

**Read the recipe file before the first run of any model in a session.** It has
the request shape, the response shape, and the gotchas.

## What is actually funded right now

| Provider | Status | Covers |
|---|---|---|
| **1min.ai** | **Prepaid, lifetime deal** | `flux-schnell`, `flux-pro` — costs no real money |
| Google AI Studio | Funded (billed to Cloud) | `nano-banana*`, `veo*` |
| OpenAI | Funded (billed) | `gpt-image`, `gpt-image-hd` |
| fal.ai | Key valid, **balance $0** | `seedance` — 403 "Exhausted balance" until topped up |
| Kie AI / WaveSpeed | **No key** | `kling` — exits with a signup message |

`python3 execution/generate_media.py list` is the live source of truth.

**1min.ai is the lane to prefer.** The credits are already bought, so a draft
there costs nothing at the margin while `nano-banana` costs real cents. Measured
rates: 9,000 credits a schnell image, 90,000 a flux-2-pro image, against an
18.9M balance — about 2,100 or 210 images. It has no reference-image support,
so `--ref` auto-switches to Google and says so.

Video is the one lane still on real money ($1.20 to $2.40 a clip). 1min.ai
hosts Veo3/Kling/Sora on prepaid credits and wiring that is the biggest saving
left on the table — see the gotchas in [models/onemin.md](models/onemin.md).

## Provider routing

1. Default to the **lowest-cost provider that runs the model well**.
2. If the cheapest route lacks the model, has no key, fails auth, or errors,
   fall back to the next provider.
3. **Never hide a provider swap.** Say which route ran and why.

## Usage

```bash
python3 execution/generate_media.py list                    # routes + prices + key status
python3 execution/generate_media.py --prompt "..." --dry-run  # quote, spends nothing

# default: prepaid 1min.ai, no real money
python3 execution/generate_media.py --prompt "dark charcoal banner, lime glow" --project deece

python3 execution/generate_media.py \
  --prompt "wide shot of a lime gradient key visual, dark background" \
  --model nano-banana --project deece --aspect 16:9 \
  --ref generations/refs/deece-logo.png

python3 execution/generate_media.py --prompt "slow push in" \
  --model veo --duration 8 --yes        # --yes required for anything paid
```

`--dry-run` calls nothing and writes nothing. Use it to quote.

## Output

- Every file lands **flat** in `generations/`. No subfolders, ever.
- Reference images live in `generations/refs/` and are the only thing in there.
- Naming: `{project}_{prompt-slug}_{timestamp}.{ext}` — the script does this.
- The gallery at `generations/gallery.html` rebuilds after every save. Open it
  in a browser; it needs no server.
- Generated media is gitignored. The sidecar `.json` logs and `refs/` **do**
  sync, so the prompt library survives across the Mac and the PC.

## Rules

1. **Quote the cost and wait for Drew's explicit go before any paid video run.**
   Quoting is not approval. One approval = one run. The script enforces this in
   two currencies: it refuses anything over $0.05 of real money, or over 50,000
   prepaid credits, without `--yes`.
2. **Draft cheap, finish pretty — and prefer prepaid over paid.** Iterate on
   `flux-schnell` (prepaid, no real money). Only rerun the same prompt on a
   quality model once Drew picks a favourite. Reach for a real-money route only
   when the job needs something prepaid can't do: references, or text in image.
   Same for video: prove the motion on `veo-fast` before paying for `veo`.
3. **Never describe a logo or a face in text.** Pass the real file with `--ref`.
   A described logo comes back wrong every time — wrong shape, wrong colours,
   invented detail. If the reference is missing, stop and ask Drew for it.
   (See also the memory note on AI likeness from reference photos: pin the
   person count, never describe the face.)
4. **One generation at a time.** Run them sequentially to avoid rate limits.
5. **Never invent a model id.** A 404 means the provider shipped a new version:
   open their model page, copy the id fresh, update `MODELS` in the script and
   the recipe file. That is the only maintenance this system needs.
6. After every save the script writes the sidecar log. Don't skip it and don't
   write it by hand.

## Adding a model

1. Add a row to `MODELS` in `execution/generate_media.py` (alias, provider,
   model_id, kind, cost, `verified=False`).
2. Copy `models/_template.md`, fill it from the provider's docs.
3. Add a row to the table above.
4. First successful real run: flip `verified=True` and record the confirmed
   response shape in the recipe.

## Related

- **YouTube thumbnails: don't use `/generate` directly.** Read
  `directives/thumbnail_forge.md` and use `execution/thumbnail_forge.py`, which
  wraps this script in a generate -> critique -> regenerate loop and refuses to
  hand back an image the critic has not passed. `execution/thumbnail_gen.py` and
  `execution/wealth_strategist_thumbnail.py` remain the right tools for a fixed
  template. `/generate` is for everything else.
- Any generated image that ends up on a page or in an email still has to pass
  `/test-improve` before it ships.
