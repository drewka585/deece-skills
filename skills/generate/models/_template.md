# Model Name

One line on what this model is best at and when to pick it.

| Field | Value |
|---|---|
| Alias | the-alias-used-in-`--model` |
| Model ID | the-exact-model-id |
| Provider | Google AI Studio / fal.ai / Kie AI / WaveSpeed AI |
| Method | Sync (instant reply) or Async (submit, then poll) |
| Type | Image or Video |
| API key | `.env` -> KEY_NAME |
| Docs | link to the provider's page for this model |
| Cost | rough price per image / per second |
| Verified | yes / no (has a real run ever succeeded?) |

## Endpoint

```
POST https://...
```

## Request format

The exact JSON body from the docs: prompt, aspect ratio, resolution,
reference image fields.

## Response handling

Where the media lives in the reply: a base64 field, or a URL to download.
For async: the status endpoint and the field that says "done".

## Notes

Gotchas: rate limits, max sizes, content rules, upload quirks.
