function resolveApiBase() {
  if (typeof window === 'undefined') return '';
  if (window.API_BASE !== undefined) return window.API_BASE;

  const { protocol, port } = window.location;

  if (protocol === 'file:') return 'http://127.0.0.1:8000';

  const DEV_STATIC_PORTS = ['3000', '4200', '5173', '5500', '8080', '8081'];
  if (DEV_STATIC_PORTS.includes(port)) return 'http://127.0.0.1:8000';

  return '';
}

export const CONFIG = {
  get API() { return resolveApiBase(); },
};

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
  bell:     '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
};

export function icon(name, size = 20) {
  return `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor"
    stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ''}</svg>`;
}


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


export function busy(btn, on = true) {
  if (!btn) return;
  btn.classList.toggle('is-loading', on);
  btn.disabled = on;
}

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
  if (refreshInFlight) return refreshInFlight; 
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



export async function api(path, opts = {}) {
  const { method = 'GET', body, auth = true, raw = false, signal, cache, _retried } = opts;

  const headers = { Accept: 'application/json', ...(opts.headers || {}) };
  let payload = body;

  if (body !== undefined && !(body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }
  if (auth && Tokens.access) headers.Authorization = `Bearer ${Tokens.access}`;

  let res;
  try {
    res = await fetch(`${CONFIG.API}${path}`, { method, headers, body: payload, signal, ...(cache ? { cache } : {}) });
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
  } catch {  }
  Tokens.clear();
  location.href = 'login.html';
}


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
        <span id="notifSlot"></span>
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


  try { mountNotifications(); }
  catch (e) { console.error('[appbar] notification bell failed:', e); }
  try { startTranscriptionWatcher(); }
  catch (e) { console.error('[appbar] watcher failed to start:', e); }

  const mq = window.matchMedia('(max-width: 620px)');
  const applyMq = () => $$('.nav-label', bar).forEach(s => s.classList.toggle('sr-only', mq.matches));
  applyMq();
  mq.addEventListener('change', applyMq);
}


export const TSTATUS = { IDLE: 'idle', PROCESSING: 'processing', DONE: 'done', FAILED: 'failed' };

const S_PROCESSING = ['processing', 'pending', 'queued', 'running', 'in_progress',
                      'inprogress', 'transcribing', 'started', 'busy', 'working'];
const S_FAILED     = ['failed', 'error', 'failure', 'cancelled', 'canceled'];
const S_DONE       = ['done', 'completed', 'complete', 'success', 'succeeded', 'finished', 'ready'];


export function transcriptionStatus(m) {
  const raw = String(m?.status ?? m?.transcription_status ?? m?.state ?? '').toLowerCase().trim();
  const text = (typeof m?.transcripts === 'string' ? m.transcripts : m?.transcript) || '';

  if (S_PROCESSING.includes(raw)) return TSTATUS.PROCESSING;
  if (S_FAILED.includes(raw))     return TSTATUS.FAILED;
  if (text.trim())                return TSTATUS.DONE;
  if (S_DONE.includes(raw))       return TSTATUS.DONE;
  if (raw) return null;  
  return TSTATUS.IDLE;
}

export function hasTranscript(m) {
  const text = (typeof m?.transcripts === 'string' ? m.transcripts : m?.transcript) || '';
  return !!text.trim();
}

export function hasSummary(m) {
  return !!String(m?.summary || '').trim();
}


let _actx = null;
let _audioUnlocked = false;

function getCtx() {
  if (!_actx) {
    const C = window.AudioContext || window.webkitAudioContext;
    if (!C) return null;
    _actx = new C();
  }
  return _actx;
}

export function enableChime() {
  const unlock = async () => {
    const ctx = getCtx();
    if (!ctx) return;
    try {
      if (ctx.state === 'suspended') await ctx.resume();
      const buf = ctx.createBuffer(1, 1, 22050);
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.connect(ctx.destination);
      src.start(0);
      _audioUnlocked = ctx.state === 'running';
    } catch {}
  };

  ['pointerdown', 'keydown', 'touchstart', 'click'].forEach(e =>
    window.addEventListener(e, unlock, { passive: true }));

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden && _actx?.state === 'suspended') _actx.resume().catch(() => {});
  });
}

export async function chime(kind = 'success') {
  if (localStorage.getItem('mute_sounds') === '1') return false;
  const ctx = getCtx();
  if (!ctx) return false;

  try {
    if (ctx.state === 'suspended') await ctx.resume();  
  } catch {  }

  if (ctx.state !== 'running') {
    console.warn('[chime] AudioContext is "' + ctx.state + '" — click the page once to enable sound.');
    return false;
  }


  const now = ctx.currentTime + 0.03;
  const notes = kind === 'error' ? [[622.25, 0], [466.16, 0.16]]
                                 : [[1046.5, 0], [1318.5, 0.13]];

  const master = ctx.createGain();
  master.gain.value = 0.0001;
  master.gain.setValueAtTime(0.22, now);
  master.connect(ctx.destination);

  for (const [freq, offset] of notes) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, now + offset);

    const t0 = now + offset;
    gain.gain.setValueAtTime(0.0001, t0);
    gain.gain.exponentialRampToValueAtTime(1, t0 + 0.015); 
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.42); 

    osc.connect(gain).connect(master);
    osc.start(t0);
    osc.stop(t0 + 0.45);
  }
  return true;
}

export function notifyDesktop(title, body) {
  try {
    if (!('Notification' in window)) return;
    if (Notification.permission === 'granted' && document.hidden) {
      new Notification(title, { body, icon: undefined, tag: 'ai-meeting' });
    }
  } catch {}
}

export function requestNotifyPermission() {
  try {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission().catch(() => {});
    }
  } catch { }
}


const NOTES_KEY = 'notifications';
const NOTES_MAX = 30;

function safeAgo(at) {
  const n = Number(at);
  if (!Number.isFinite(n) || n <= 0) return '';
  try { return relativeTime(new Date(n).toISOString()) || ''; } catch { return ''; }
}

export const Notes = {
  all() {
    try {
      const raw = JSON.parse(localStorage.getItem(NOTES_KEY) || '[]');
      if (!Array.isArray(raw)) return [];
      return raw.filter(n => n && typeof n === 'object' && typeof n.title === 'string');
    } catch { return []; }
  },
  unread() { return this.all().filter(n => !n.read).length; },


  add({ id, title, body = '', kind = 'ok', href = '' }) {
    const list = this.all();
    if (id && list.some(n => n.id === id)) return false;
    list.unshift({ id: id || `n_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
                   title, body, kind, href, at: Date.now(), read: false });
    try { localStorage.setItem(NOTES_KEY, JSON.stringify(list.slice(0, NOTES_MAX))); } catch {}
    try { window.dispatchEvent(new CustomEvent('notes:changed')); } catch {}
    return true;
  },
  markAllRead() {
    const list = this.all().map(n => ({ ...n, read: true }));
    try { localStorage.setItem(NOTES_KEY, JSON.stringify(list)); } catch {}
    try { window.dispatchEvent(new CustomEvent('notes:changed')); } catch {}
  },
  clear() {
    try { localStorage.removeItem(NOTES_KEY); } catch {}
    try { window.dispatchEvent(new CustomEvent('notes:changed')); } catch {}
  },
};

window.addEventListener('storage', e => {
  if (e.key === NOTES_KEY) try { window.dispatchEvent(new CustomEvent('notes:changed')); } catch {}
});

export function mountNotifications() {
  const host = $('#notifSlot');
  if (!host) return;

  host.innerHTML = `
    <div class="notif">
      <button class="btn btn--icon btn--ghost" id="notifBtn" aria-label="Notifications" aria-expanded="false">
        ${icon('bell', 18)}<span class="notif__dot hidden" id="notifDot"></span>
      </button>
      <div class="notif__panel hidden" id="notifPanel" role="dialog" aria-label="Notifications">
        <div class="notif__head">
          <strong>Notifications</strong>
          <button class="btn btn--sm btn--ghost" id="notifClear" type="button">Clear</button>
        </div>
        <div class="notif__list" id="notifList"></div>
      </div>
    </div>`;

  const btn = $('#notifBtn'), panel = $('#notifPanel'), dot = $('#notifDot');

  const paint = () => {
   try {
    const list = Notes.all();
    const n = list.filter(x => !x.read).length;
    dot.classList.toggle('hidden', !n);
    dot.textContent = n > 9 ? '9+' : String(n || '');

    $('#notifList').innerHTML = list.length ? list.map(x => `
      <a class="notif__item ${x.read ? '' : 'is-unread'}" ${x.href ? `href="${x.href}"` : ''}>
        <span class="notif__icon notif__icon--${x.kind}">
          ${icon(x.kind === 'error' ? 'alert' : 'checkCirc', 16)}
        </span>
        <span class="grow">
          <span class="notif__title">${escapeHtml(x.title)}</span>
          ${x.body ? `<span class="notif__body">${escapeHtml(x.body)}</span>` : ''}
          <span class="notif__time">${escapeHtml(safeAgo(x.at))}</span>
        </span>
      </a>`).join('')
      : `<p class="faint" style="padding:18px;text-align:center">No notifications yet.</p>`;
   } catch (e) {
     console.error('[bell] render failed:', e);
     $('#notifList').innerHTML = `<p class="faint" style="padding:18px;text-align:center">No notifications yet.</p>`;
   }
  };

  const close = () => { panel.classList.add('hidden'); btn.setAttribute('aria-expanded', 'false'); };

  btn.onclick = e => {
    e.stopPropagation();
    const open = panel.classList.toggle('hidden') === false;
    btn.setAttribute('aria-expanded', String(open));
    if (open) { Notes.markAllRead(); paint(); }
  };
  $('#notifClear').onclick = e => { e.stopPropagation(); Notes.clear(); paint(); };
  panel.addEventListener('click', e => e.stopPropagation());
  document.addEventListener('click', close);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  window.addEventListener('notes:changed', paint);

  paint();
}

const WATCH_SEEN  = 'watch_seen';       
const WATCH_LEASE = 'watch_lease';  
const TAB_ID = `t_${Math.random().toString(36).slice(2, 9)}`;
const LEASE_MS = 12000;

let watchTimer = null;
let watchDelay = 8000;

function readSeen() {
  try { return JSON.parse(localStorage.getItem(WATCH_SEEN) || '{}'); } catch { return {}; }
}
function writeSeen(map) {
  try { localStorage.setItem(WATCH_SEEN, JSON.stringify(map)); } catch {}
}

function mergeSeen(updates) {
  const current = readSeen();
  for (const [k, v] of Object.entries(updates)) {
    if (current[k] === TSTATUS.PROCESSING && v !== TSTATUS.PROCESSING
        && !terminalThisTick.has(k)) continue;  
    current[k] = v;
  }
  writeSeen(current);
  return current;
}
let terminalThisTick = new Set();


function claimLease() {
  let lease = null;
  try { lease = JSON.parse(localStorage.getItem(WATCH_LEASE) || 'null'); } catch {}
  const now = Date.now();
  if (lease && lease.tab !== TAB_ID && now - lease.at < LEASE_MS) return false;
  try { localStorage.setItem(WATCH_LEASE, JSON.stringify({ tab: TAB_ID, at: now })); } catch {}
  return true;
}


function releaseLease() {
  try {
    const lease = JSON.parse(localStorage.getItem(WATCH_LEASE) || 'null');
    if (lease && lease.tab === TAB_ID) localStorage.removeItem(WATCH_LEASE);
  } catch {}
}

function localMarker(id) {
  try {
    const t = Number(localStorage.getItem(`transcribing:${id}`));
    if (!t) return false;
    if (Date.now() - t > 60 * 60 * 1000) { localStorage.removeItem(`transcribing:${id}`); return false; }
    return true;
  } catch { return false; }
}

function runStamp(id) {
  try { return localStorage.getItem(`transcribing:${id}`) || 'x'; } catch { return 'x'; }
}


export const SEG_API = {
  status:        id  => `/meetings/${id}/segments/status`,
  segment:       id  => `/segment/segment/${id}`,
  listAll:       id  => `/segment/get_all_segments/${id}`,
  getOne:        sid => `/segment/get_segment/${sid}`,
  summariseOne:  sid => `/summarize/summarize/${sid}`,
  summariseAll:  id  => `/summarize/summarize_all/${id}`,
  summarised:    id  => `/summarize/get_summarized_segments/${id}`,
};

export function segmentCounts(res) {
  const arr = Array.isArray(res) ? res
            : Array.isArray(res?.segments) ? res.segments
            : Array.isArray(res?.segments_data) ? res.segments_data
            : Array.isArray(res?.summarized_segments) ? res.summarized_segments
            : [];
  const total = Number(res?.segments_count ?? res?.summarized_count ?? arr.length) || arr.length;
  const summarised = arr.filter(x => String(x?.summary || '').trim()).length;
  return { total, summarised, list: arr };
}


export const JOB = { TRANSCRIBE: 'transcribe', SEGMENT: 'segment', SUMMARIZE: 'summarize' };
const JOB_TTL = 60 * 60 * 1000; 

const jobKey = (kind, id) => `job:${kind}:${id}`;

export function jobStart(kind, id) {
  const k = jobKey(kind, id);
  if (jobRunning(kind, id)) return false;
  try { localStorage.setItem(k, String(Date.now())); } catch {}
  emitJobsChanged(kind, id, true);
  return true;
}

function emitJobsChanged(kind, id, running) {
  try {
    window.dispatchEvent(new CustomEvent('jobs:changed', { detail: { kind, id, running } }));
  } catch {}
}

export function jobRunning(kind, id) {
  try {
    const t = Number(localStorage.getItem(jobKey(kind, id)));
    if (!t) return false;
    if (Date.now() - t > JOB_TTL) { localStorage.removeItem(jobKey(kind, id)); return false; }
    return true;
  } catch { return false; }
}

export function jobStamp(kind, id) {
  try { return localStorage.getItem(jobKey(kind, id)) || 'x'; } catch { return 'x'; }
}

export function jobEnd(kind, id) {
  try { localStorage.removeItem(jobKey(kind, id)); } catch {} 
  emitJobsChanged(kind, id, false);
}

export function jobsOfKind(kind) {
  const out = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (!k || !k.startsWith(`job:${kind}:`)) continue;
      const id = k.slice(`job:${kind}:`.length);
      if (jobRunning(kind, id)) out.push(id);
    }
  } catch {}
  return out;
}

const JOB_LABEL = {
  [JOB.SEGMENT]:   { done: 'Segmentation complete', fail: 'Segmentation failed',
                     okBody: 'has been split into topics.', failBody: 'could not be segmented.' },
  [JOB.SUMMARIZE]: { done: 'Summary ready',         fail: 'Summarisation failed',
                     okBody: 'has been summarised.',  failBody: 'could not be summarised.' },
};


export function notifyJob(kind, id, title, ok = true) {
  const stamp = jobStamp(kind, id);
  if (stamp === 'x') return false;
  const L = JOB_LABEL[kind];
  if (!L) { jobEnd(kind, id); return false; }
  const name = title || 'Meeting';

  const added = Notes.add({
    id: `${kind}_${ok ? 'done' : 'fail'}_${id}_${stamp}`,
    kind: ok ? 'ok' : 'error',
    href: `meeting.html?id=${encodeURIComponent(id)}`,
    title: ok ? L.done : L.fail,
    body: `\u201C${name}\u201D ${ok ? L.okBody : L.failBody}`,
  });

  jobEnd(kind, id);
  if (!added) return false;

  chime(ok ? 'success' : 'error');
  toast(`\u201C${name}\u201D ${ok ? L.okBody : L.failBody}`, ok ? 'ok' : 'error', ok ? 6000 : 8000);
  notifyDesktop(ok ? L.done : L.fail, name);
  return true;
}


export function notifyTranscription(id, title, ok = true) {
  const key = String(id);
  terminalThisTick.add(key);
  const stamp = runStamp(key);
  const name = title || 'Meeting';
  const added = Notes.add({
    id: `${ok ? 'done' : 'fail'}_${key}_${stamp}`,
    kind: ok ? 'ok' : 'error',
    href: `meeting.html?id=${encodeURIComponent(key)}`,
    title: ok ? 'Transcription complete' : 'Transcription failed',
    body: ok ? `\u201C${name}\u201D has been transcribed.`
             : `\u201C${name}\u201D could not be transcribed. Open it to retry.`,
  });
  if (!added) return false;

  mergeSeen({ [key]: ok ? TSTATUS.DONE : TSTATUS.FAILED });
  try { localStorage.removeItem(`transcribing:${key}`); } catch {}

  chime(ok ? 'success' : 'error');
  toast(ok ? `\u201C${name}\u201D has been transcribed`
           : `\u201C${name}\u201D failed to transcribe`, ok ? 'ok' : 'error', ok ? 7000 : 8000);
  notifyDesktop(ok ? 'Transcription complete' : 'Transcription failed', name);
  return true;
}


export function trackTranscription(id) {
  const key = String(id);
  try { localStorage.setItem(`transcribing:${key}`, String(Date.now())); } catch {}
  mergeSeen({ [key]: TSTATUS.PROCESSING }); 
  schedule(2500);
}

async function watchTick() {
  if (!Tokens.access) return schedule(30000);
  if (document.hidden) return schedule(watchDelay);
  if (!claimLease()) return schedule(3000);

  try {
    const data = await api('/meetings', { cache: 'no-store' });
    const list = Array.isArray(data) ? data
               : Array.isArray(data?.items) ? data.items
               : Array.isArray(data?.results) ? data.results
               : Array.isArray(data?.meetings) ? data.meetings : [];

    let seen = readSeen();
    let anyRunning = false;
    terminalThisTick = new Set();

    const watched = list.filter(m => {
      const id = String(m.id);
      return seen[id] === TSTATUS.PROCESSING || localMarker(id);
    });

    const resolved = new Map();
    await Promise.all(watched.map(async m => {
      const id = String(m.id);
      if (transcriptionStatus(m) === TSTATUS.DONE
          || transcriptionStatus(m) === TSTATUS.FAILED) return;
      try {
        const full = await api(`/meetings/${encodeURIComponent(m.id)}`, { cache: 'no-store' });
        const st = transcriptionStatus(full);
        if (st) resolved.set(id, st);
      } catch {}
    }));


    seen = readSeen();

    for (const m of list) {
      const id = String(m.id);
      let st = resolved.get(id) ?? transcriptionStatus(m);

      if (st !== TSTATUS.PROCESSING && st !== TSTATUS.DONE && st !== TSTATUS.FAILED
          && localMarker(id)) st = TSTATUS.PROCESSING;

      if (st === TSTATUS.PROCESSING) {
        anyRunning = true;
        seen[id] = TSTATUS.PROCESSING;
        continue;
      }

      const was = seen[id];
      const name = m.title || 'Meeting';

      if (was === TSTATUS.PROCESSING && st === TSTATUS.DONE) {
        terminalThisTick.add(id);
        notifyTranscription(id, name, true);
      } else if (was === TSTATUS.PROCESSING && st === TSTATUS.FAILED) {
        terminalThisTick.add(id);
        notifyTranscription(id, name, false);
      }

      if (st) seen[id] = st;
    }

    mergeSeen(seen);
    try {
      window.dispatchEvent(new CustomEvent('meetings:refreshed', {
        detail: { list, finished: [...terminalThisTick] },
      }));
    } catch {}
    schedule(anyRunning ? 6000 : 25000);
  } catch (err) {
    if (err.status === 401) return;
    schedule(Math.min(watchDelay * 2, 60000));
  }
}

function schedule(ms) {
  watchDelay = ms;
  clearTimeout(watchTimer);
  watchTimer = setTimeout(watchTick, ms);
}

export function startTranscriptionWatcher() {
  if (watchTimer) return;
  enableChime();
  requestNotifyPermission();
  schedule(1500);


  window.__notifyTest = async () => {
    Notes.add({ id: `test_${Date.now()}`, kind: 'ok', title: 'Test notification',
                body: 'If you can hear a chime, audio is working.' });
    const played = await chime('success');
    toast('Test notification fired', 'ok');
    return played ? 'chime played' : 'CHIME BLOCKED — see __audioState()';
  };

  window.__audioState = () => {
    const ctx = _actx;
    return {
      contextCreated: !!ctx,
      state: ctx ? ctx.state : 'none (no gesture yet)',
      unlocked: _audioUnlocked,
      muted: localStorage.getItem('mute_sounds') === '1',
      hint: !ctx ? 'Click anywhere on the page, then retry.'
          : ctx.state !== 'running' ? 'Context suspended — click the page once.'
          : localStorage.getItem('mute_sounds') === '1' ? 'Muted via the bell/mute toggle.'
          : 'Audio looks healthy.',
    };
  };
  window.__notifyState = () => ({
    tab: TAB_ID,
    hasToken: !!Tokens.access,
    seen: readSeen(),
    markers: Object.keys(localStorage).filter(k => k.startsWith('transcribing:')),
    notifications: Notes.all().length,
    muted: localStorage.getItem('mute_sounds') === '1',
    nextPollMs: watchDelay,
  });
  window.__notifyReset = () => {
    try {
      Object.keys(localStorage)
        .filter(k => k.startsWith('transcribing:') || k === WATCH_SEEN
                  || k === WATCH_LEASE || k === NOTES_KEY)
        .forEach(k => localStorage.removeItem(k));
    } catch {}
    try { window.dispatchEvent(new CustomEvent('notes:changed')); } catch {}
    schedule(500);
    return 'watcher state cleared — press Transcribe again';
  };

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) schedule(800);
  });
  window.addEventListener('pagehide', () => { releaseLease(); clearTimeout(watchTimer); });
  window.addEventListener('beforeunload', () => { releaseLease(); clearTimeout(watchTimer); });
}

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
