# Serving the frontend — two options

## Option A (recommended): let FastAPI serve the pages — **no CORS at all**

This is how your old pages were working. Same origin ⇒ the browser never sends an
`OPTIONS` preflight ⇒ the `400 Bad Request` disappears without touching CORS.

Copy the `app/` frontend folder into your project (e.g. as `frontend/`), then at the
**very bottom** of `app/main.py`, *after* all your `include_router(...)` calls:

```python
from fastapi.staticfiles import StaticFiles

# MUST be last: a mount at "/" swallows any route declared after it.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```

Then open:

```
http://127.0.0.1:8000/login.html
```

The frontend auto-detects it's on the backend's origin and issues **relative**
requests (`/auth/login`), exactly like a same-origin page. Nothing else to configure.

---

## Option B: separate static server (Live Server, `python -m http.server 5500`)

This **is** cross-origin, so CORS is mandatory. In `app/main.py`, above your routers:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   # ← narrowing this causes 400 on preflight
)
```

Two gotchas that produce exactly your `400 OPTIONS`:

- `allow_origins=["*"]` **cannot** be combined with `allow_credentials=True` — the
  middleware stops echoing the origin and the preflight fails.
- If a requested header isn't listed in `allow_headers`, Starlette returns **400**.
  Keep `["*"]`.

`localhost` and `127.0.0.1` are *different origins*. List both.

---

## Forcing the API URL manually

The auto-detection can always be overridden. Add this **before** the module script
on any page:

```html
<script>window.API_BASE = "http://127.0.0.1:8000";</script>
```

Set it to `""` (empty string) to force same-origin relative requests.
