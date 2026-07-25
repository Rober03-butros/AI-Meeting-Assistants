/* ============================================================
   AI Meeting Assistant — shared runtime
   Config, API client (auto token-refresh), auth guard,
   toasts, modals, theme, icons, helpers.
   ============================================================ */

/**
 * API base URL resolution.
 *
 * Priority:
 *   1. window.API_BASE  — explicit override, always wins.
 *   2. ''               — SAME ORIGIN. Used when the page is served by the backend
 *                         itself (FastAPI StaticFiles). Requests become relative
 *                         ("/auth/login"), so the browser sends NO CORS preflight
 *                         and no CORS config is needed at all.
 *   3. http://127.0.0.1:8000 — fallback for a standalone dev server (port 5500 etc.),
 *                         which IS cross-origin and DOES require CORSMiddleware.
 *
 * Heuristic: if we're not on a known static-dev-server port, assume the backend
 * is serving us and stay same-origin.
 */
function resolveApiBase() {
  if (typeof window === 'undefined') return '';
  if (window.API_BASE !== undefined) return window.API_BASE;      // explicit wins ('' allowed)

  const { protocol, port } = window.location;

  // Opened directly from disk (file://) — must point at the backend.
  if (protocol === 'file:') return 'http://127.0.0.1:8000';

  // Common standalone static-server ports => backend lives elsewhere.
  const DEV_STATIC_PORTS = ['3000', '4200', '5173', '5500', '8080', '8081'];
  if (DEV_STATIC_PORTS.includes(port)) return 'http://127.0.0.1:8000';

  // Otherwise assume the backend is serving these files: stay same-origin.
  return '';
}

export const CONFIG = {
  get API() { return resolveApiBase(); },
};

/* ---------- tiny DOM helpers ---------- */
export const $  = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

export function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === 'class') node.className = v;
    else if (k === 'html') node.innerHTML = v;
    else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
    else if (v !== null && v !== undefined && v !== false) node.setAttribute(k, v);
  }
  children.flat().forEach(c => node.append(c?.nodeType ? c : document.createTextNode(String(c))));
  return node;
}

/* ---------- token store ---------- */
export const Tokens = {
  get access()  { return localStorage.getItem('access_token'); },
  get refresh() { return localStorage.getItem('refresh_token'); },
  set({ access_token, refresh_token }) {
    if (access_token)  localStorage.setItem('access_token', access_token);
    if (refresh_token) localStorage.setItem('refresh_token', refresh_token);
  },
  clear() {
    ['access_token', 'refresh_token'].forEach(k => localStorage.removeItem(k));
  },
};

/* ---------- icons ---------- */
const ICONS = {
  logo:     '<path d="M12 2a4 4 0 0 0-4 4v6a4 4 0 0 0 8 0V6a4 4 0 0 0-4-4Z"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/>',
  mic:      '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10a7 7 0 0 1-14 0M12 17v5M8 22h8"/>',
  video:    '<rect x="2" y="6" width="14" height="12" rx="3"/><path d="m22 8-6 4 6 4V8Z"/>',
  list:     '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
  logout:   '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
  home:     '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M9 22V12h6v10"/>',
  plus:     '<path d="M12 5v14M5 12h14"/>',
  trash:    '<path d="M3 6h18M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M10 11v6M14 11v6"/>',
  search:   '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
  chevron:  '<path d="m9 18 6-6-6-6"/>',
  arrow:    '<path d="M5 12h14M13 5l7 7-7 7"/>',
  check:    '<path d="M20 6 9 17l-5-5"/>',
  checkCirc:'<circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 6-6"/>',
  alert:    '<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
  info:     '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
  eye:      '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
  eyeOff:   '<path d="M10.6 5.2A9.9 9.9 0 0 1 12 5c6 0 10 7 10 7a17 17 0 0 1-3.2 3.9M6.6 6.6A17 17 0 0 0 2 12s4 7 10 7a9.7 9.7 0 0 0 5.4-1.6"/><path d="m2 2 20 20M9.9 9.9a3 3 0 0 0 4.2 4.2"/>',
  mail:     '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m2 7 10 6 10-6"/>',
  lock:     '<rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  user:     '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  users:    '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M17 4.5a4 4 0 0 1 0 7.4M22 21a6.5 6.5 0 0 0-4-6"/>',
  doc:      '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M9 13h6M9 17h4"/>',
  sparkle:  '<path d="M12 3v4M12 17v4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M3 12h4M17 12h4M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
  sun:      '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  moon:     '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/>',
  stop:     '<rect x="6" y="6" width="12" height="12" rx="2"/>',
  clock:    '<circle cx="12" cy="12" r="10"/><path d="M12 7v5l3 2"/>',
  inbox:    '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5h13l3.5 7v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6Z"/>',
  download: '<path d="M12 3v12M7 11l5 5 5-5"/><path d="M5 21h14"/>',
};

export function icon(name, size = 20) {
  return `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor"
    stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ''}</svg>`;
}

/* ---------- theme ---------- */
export const Theme = {
  init() {
    const saved = localStorage.getItem('theme');
    const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    document.documentElement.dataset.theme = saved || (prefersLight ? 'light' : 'dark');
  },
  toggle() {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('theme', next);
    return next;
  },
};
Theme.init();

/* ---------- toasts ---------- */
let toastHost;
export function toast(message, type = 'info', ms = 4000) {
  if (!toastHost) {
    toastHost = el('div', { class: 'toasts', role: 'status', 'aria-live': 'polite' });
    document.body.append(toastHost);
  }
  const glyph = type === 'ok' ? 'checkCirc' : type === 'error' ? 'alert' : 'info';
  const node = el('div', { class: `toast toast--${type}` });
  node.innerHTML = `<span class="toast__icon">${icon(glyph, 19)}</span><span>${escapeHtml(message)}</span>`;
  toastHost.append(node);
  const kill = () => { node.classList.add('out'); setTimeout(() => node.remove(), 220); };
  node.addEventListener('click', kill);
  setTimeout(kill, ms);
}

export function escapeHtml(str = '') {
  return String(str).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/* ---------- confirm dialog (replaces window.confirm) ---------- */
export function confirmDialog({ title = 'Are you sure?', body = '', confirmText = 'Confirm', danger = false }) {
  return new Promise(resolve => {
    const dlg = el('dialog', { class: 'modal' });
    dlg.innerHTML = `
      <div class="stack">
        <h3>${escapeHtml(title)}</h3>
        ${body ? `<p class="muted">${escapeHtml(body)}</p>` : ''}
        <div class="row" style="justify-content:flex-end;margin-top:6px">
          <button class="btn btn--ghost" data-act="cancel">Cancel</button>
          <button class="btn ${danger ? 'btn--danger' : 'btn--primary'}" data-act="ok">${escapeHtml(confirmText)}</button>
        </div>
      </div>`;
    document.body.append(dlg);
    const done = v => { dlg.close(); dlg.remove(); resolve(v); };
    dlg.querySelector('[data-act="cancel"]').onclick = () => done(false);
    dlg.querySelector('[data-act="ok"]').onclick = () => done(true);
    dlg.addEventListener('cancel', e => { e.preventDefault(); done(false); });
    dlg.showModal();
  });
}

/* ---------- button loading state ---------- */
export function busy(btn, on = true) {
  if (!btn) return;
  btn.classList.toggle('is-loading', on);
  btn.disabled = on;
}

/* ============================================================
   API client
   ============================================================ */
export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

function readDetail(data, fallback) {
  if (!data) return fallback;
  const d = data.detail ?? data.message ?? data.error;
  if (typeof d === 'string') return d;
  if (Array.isArray(d)) return d.map(x => x.msg || x.detail || JSON.stringify(x)).join(', ');
  return fallback;
}

let refreshInFlight = null;

async function refreshSession() {
  if (refreshInFlight) return refreshInFlight;           // de-dupe concurrent 401s
  const refresh_token = Tokens.refresh;
  if (!refresh_token) return false;

  refreshInFlight = (async () => {
    try {
      const res = await fetch(`${CONFIG.API}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      if (!data.access_token) return false;
      Tokens.set(data);
      return true;
    } catch { return false; }
    finally { setTimeout(() => { refreshInFlight = null; }, 0); }
  })();

  return refreshInFlight;
}

/**
 * api(path, { method, body, auth, raw, signal })
 * - JSON in / JSON out by default; pass FormData as body and headers are handled.
 * - On 401 with a refresh token present, retries once after refreshing.
 */
export async function api(path, opts = {}) {
  const { method = 'GET', body, auth = true, raw = false, signal, _retried } = opts;

  const headers = { Accept: 'application/json', ...(opts.headers || {}) };
  let payload = body;

  if (body !== undefined && !(body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }
  if (auth && Tokens.access) headers.Authorization = `Bearer ${Tokens.access}`;

  let res;
  try {
    res = await fetch(`${CONFIG.API}${path}`, { method, headers, body: payload, signal });
  } catch (err) {
    if (err.name === 'AbortError') throw err;
    throw new ApiError('Network error — is the server running?', 0, null);
  }

  if (res.status === 401 && auth && !_retried) {
    if (await refreshSession()) return api(path, { ...opts, _retried: true });
    Tokens.clear();
    if (!location.pathname.endsWith('login.html')) {
      location.href = `login.html?next=${encodeURIComponent(location.pathname + location.search)}`;
    }
    throw new ApiError('Session expired. Please sign in again.', 401, null);
  }

  if (raw) {
    if (!res.ok) throw new ApiError(`Request failed (${res.status})`, res.status, null);
    return res;
  }

  const text = await res.text();
  let data = null;
  if (text) { try { data = JSON.parse(text); } catch { data = { detail: text }; } }

  if (!res.ok) throw new ApiError(readDetail(data, `Request failed (${res.status})`), res.status, data);
  return data;
}

/* ---------- auth guard ---------- */
export function requireAuth() {
  if (!Tokens.access) {
    location.replace(`login.html?next=${encodeURIComponent(location.pathname + location.search)}`);
    return false;
  }
  return true;
}

export function redirectIfAuthed() {
  if (Tokens.access) location.replace('home.html');
}

export async function logout() {
  try {
    await api('/auth/logout', {
      method: 'POST',
      body: { refresh_token: Tokens.refresh, access_token: Tokens.access },
    });
  } catch { /* logout locally regardless */ }
  Tokens.clear();
  location.href = 'login.html';
}

/* ---------- app bar ---------- */
export function mountAppBar({ active = '', user = null } = {}) {
  const bar = $('#appbar');
  if (!bar) return;
  const links = [
    { id: 'home',     href: 'home.html',     label: 'Home',     ic: 'home' },
    { id: 'recorder', href: 'recorder.html', label: 'Record',   ic: 'mic' },
    { id: 'meetings', href: 'meetings.html', label: 'Meetings', ic: 'list' },
  ];
  bar.innerHTML = `
    <div class="appbar__inner">
      <a class="brand" href="home.html">
        <span class="brand__mark">${icon('logo', 19)}</span>
        <span class="brand__text">AI Meeting<span> Assistant</span></span>
      </a>
      <nav class="appbar__nav">
        ${links.map(l => `
          <a class="btn btn--ghost btn--sm" href="${l.href}"
             ${l.id === active ? 'aria-current="page" style="color:var(--brand)"' : ''}>
            ${icon(l.ic, 16)}<span class="nav-label">${l.label}</span>
          </a>`).join('')}
        <button class="btn btn--icon btn--ghost" id="themeBtn" title="Toggle theme" aria-label="Toggle theme">
          ${icon('sun', 18)}
        </button>
        <button class="btn btn--icon btn--ghost" id="logoutBtn" title="Sign out" aria-label="Sign out">
          ${icon('logout', 18)}
        </button>
      </nav>
    </div>`;

  const paint = () => {
    $('#themeBtn').innerHTML = icon(document.documentElement.dataset.theme === 'light' ? 'moon' : 'sun', 18);
  };
  paint();
  $('#themeBtn').onclick = () => { Theme.toggle(); paint(); };
  $('#logoutBtn').onclick = async () => {
    if (await confirmDialog({ title: 'Sign out?', body: 'You will need to sign in again.', confirmText: 'Sign out' })) logout();
  };

  // Collapse nav labels on small screens
  const mq = window.matchMedia('(max-width: 620px)');
  const applyMq = () => $$('.nav-label', bar).forEach(s => s.classList.toggle('sr-only', mq.matches));
  applyMq();
  mq.addEventListener('change', applyMq);
}

/* ---------- formatting ---------- */
export function formatDate(value) {
  if (!value) return '—';
  const d = new Date(/Z|[+-]\d\d:?\d\d$/.test(value) ? value : value + 'Z');
  if (isNaN(d)) return String(value);
  return d.toLocaleString(undefined, {
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
  });
}

export function relativeTime(value) {
  if (!value) return '';
  const d = new Date(/Z|[+-]\d\d:?\d\d$/.test(value) ? value : value + 'Z');
  if (isNaN(d)) return '';
  const secs = (d - Date.now()) / 1000;
  const rtf = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' });
  const units = [['year', 31536000], ['month', 2592000], ['week', 604800],
                 ['day', 86400], ['hour', 3600], ['minute', 60], ['second', 1]];
  for (const [unit, s] of units) {
    if (Math.abs(secs) >= s || unit === 'second') return rtf.format(Math.round(secs / s), unit);
  }
}

export function initials(name = '?') {
  return name.trim().split(/\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase() || '?';
}

export function formatDuration(totalSeconds) {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  const pad = n => String(n).padStart(2, '0');
  return h ? `${pad(h)}:${pad(m)}:${pad(sec)}` : `${pad(m)}:${pad(sec)}`;
}
