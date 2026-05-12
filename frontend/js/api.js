const SERVICES = {
  AUTH:      'http://localhost:5010',
  USERS:     'http://localhost:5011',
  DEVICES:   'http://localhost:5012',
  LOCATIONS: 'http://localhost:5013',
  METRICS:   'http://localhost:5014',
  ALERTS:    'http://localhost:5015',
};

function getToken() { return sessionStorage.getItem('hsr_token'); }

function getUser() {
  try { return JSON.parse(sessionStorage.getItem('hsr_user') || '{}'); }
  catch { return {}; }
}

function logout() {
  sessionStorage.clear();
  window.location.href = 'index.html';
}

async function apiFetch(service, endpoint, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  try {
    const res = await fetch(`${SERVICES[service]}${endpoint}`, {
      ...options,
      headers: { ...headers, ...(options.headers || {}) },
    });
    if (res.status === 401) { logout(); return null; }
    const json = await res.json();
    return { ok: res.ok, status: res.status, data: json };
  } catch (err) {
    console.error(`[${service}] ${endpoint}`, err);
    return { ok: false, data: { message: 'Error de conexión con el servidor' } };
  }
}