# AI Meeting Assistant — Frontend

A rebuilt, responsive, accessible frontend for your FastAPI backend. No frameworks, no build step — plain ES modules.

## Run

```bash
cd app
python3 -m http.server 5500
# open http://localhost:5500/login.html
```

> Open via a server, **not** `file://` — ES modules and `getDisplayMedia` require an origin (localhost or HTTPS).

## Configure the API base URL

Defaults to `http://localhost:8000`. Override per page by adding **before** the module script:

```html
<script>window.API_BASE = "https://api.yourdomain.com";</script>
```

## Files

| File | Purpose |
|---|---|
| `assets/css/app.css` | Design system: tokens, dark/light themes, components, responsive layout |
| `assets/js/app.js` | API client (auto token refresh), auth guard, toasts, modal, theme, icons, formatters |
| `login.html` / `register.html` / `verify.html` | Auth flow with inline validation, password strength, 6-box OTP |
| `home.html` | Dashboard: greeting, stats, quick actions, recent meetings |
| `meetings.html` | Searchable + sortable meeting list |
| `recorder.html` | Recorder with live timer, audio level meter, playback, retry upload |
| `meeting.html` | Detail view: summary/transcript tabs, audio, participants, delete |

## What changed vs. the originals

**Architecture**
- One shared CSS + JS layer instead of copy-pasted `<script>` blocks and inline styles.
- `api()` wrapper: JSON/FormData handling, uniform error messages, `AbortError` passthrough.
- **Automatic token refresh** — on `401` it calls `/auth/refresh` once (de-duplicated across concurrent requests) and retries; only logs out if that fails.
- Login redirects preserve the intended page via `?next=`.

**UX**
- Toast notifications and a styled `<dialog>` confirm replacing `alert()` / `confirm()`.
- Skeleton loaders, empty states, and error states with retry on every data view.
- Button loading spinners; forms submit on Enter and can't double-submit.
- OTP: auto-advance, backspace-back, full-code paste, auto-submit, resend cooldown.
- Recorder: title validated *before* capture starts (the old code recorded then discarded), live level meter, mic toggle, "stop sharing" detection, unload warning, local playback + download so a failed upload never loses the recording, codec feature-detection.
- Meeting detail: summary/transcript tabs, copy + download transcript, participant search with Enter key.
- Dark/light theme toggle, persisted.

**Correctness & security**
- All user/API content is escaped before insertion — the originals used `innerHTML` with raw server data (XSS risk).
- Query params are `encodeURIComponent`-encoded.
- Timestamps parsed as UTC and rendered in the user's locale with relative time.
- `AudioContext` and media tracks are properly closed on stop, so the browser's recording indicator clears.

**Accessibility & responsiveness**
- Fluid `clamp()` type/spacing, mobile-first; nav collapses to icons under 620px.
- Labels on every input, `aria-invalid`, `aria-live` toasts, real tab semantics, visible focus rings, 44px touch targets, `prefers-reduced-motion` and `prefers-color-scheme` support.

## Backend endpoints used

`POST /auth/register` · `POST /auth/login` · `POST /auth/refresh` *(new — see below)* · `POST /auth/logout` · `GET /auth/me`
`POST /verify/verify-email` · `POST /verify/resend-verification`
`GET /meetings` · `POST /meetings/upload` · `GET /meetings/{id}` · `DELETE /meetings/{id}` · `GET /meetings/{id}/audio` · `POST /meetings/{id}/participants?user_id=`
`GET /users/search?email=`

⚠️ **`POST /auth/refresh`** is the only endpoint not in your original pages. It should accept `{ "refresh_token": "..." }` and return `{ "access_token": "...", "refresh_token": "..." }`. If your backend doesn't have it yet, everything still works — users just get signed out when the access token expires, as before.

Also ensure CORS allows your frontend origin with the `Authorization` header.
