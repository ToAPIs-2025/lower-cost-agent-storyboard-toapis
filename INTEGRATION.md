# Project-specific integration plan

Pinned upstream: https://github.com/Yuuhann1999/agent-storyboard/tree/9924c97f04e1b76dabebe8fa376a5a224285aa90

沿用原有 generation task claim / complete，将本地 PNG、MP4 通过 sourcePath 回填；不替换 Codex 内置 image_gen。

The pinned local app accepted actual PNG and MP4 files through task claim/complete, persisted ready state and served matching bytes. Browser UI and a native ToAPIs model provider are not certified.

## API differences

- Bearer generation key to HTTPS `https://toapis.com` only; image `POST /v1/images/generations`, video `POST /v1/videos/generations`.
- An async task `id` is not OpenAI `data[0]`. Persist it before polling `GET /v1/images/generations/:id` or `/v1/videos/generations/:id`; wait for `completed`, then download `result.data[0].url` without forwarding credentials.
- Local first-frame upload uses `POST /v1/uploads/images`; use `image_with_roles` with `role=first_frame` only for a reviewed I2V preset. Reference editing, mask repaint and arbitrary multimodal inputs are not enabled by this example.
- Match model, quality, resolution, image count, duration, mode and audio to the exact same-key pricing rules. `billing.status=settled` and explicit costs confirm a charge; missing billing stays unknown.
- No automatic paid POST retry. Keep state/receipts private; changing a run ID can cost again.

## Remaining acceptance

1. Confirm the maintainer's desired contribution route and image/video owner.
2. Wire only the supported preset to the normal settings/registry/worker. Do not replace existing defaults or referrals.
3. Verify native create, restart/resume, readable failure, cancel semantics, download and final result placement.
4. Run upstream checks for affected modules and a real application task before calling this native integration accepted.

## Information needed from the maintainer

Target version; preferred Provider identity/configuration; native task cancellation and result persistence contract; permitted example/docs location; existing sponsorship/referral conditions.

## Verified local attachment

Start the original app. Generate an image/video separately, then run:

```bash
python attach_storyboard.py --origin http://127.0.0.1:43218 --project PROJECT_ID --shot SHOT_ID --kind image --file /absolute/path/to/output.png
```

The helper queues one task, claims it, then completes with `sourcePath`. Review existing pending tasks before retrying attachment. See `integration/validation-report.json`. The refreshed local acceptance uses this guide's own Seedance 2.5 clip; attaching existing media incurs no new generation fee.
