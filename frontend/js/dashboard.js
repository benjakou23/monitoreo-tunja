requireAuth();

// ── HELPER EXTRACTOR ──────────────────────────────────────
function extractList(res, key) {
  if (!res?.ok) return [];
  const raw = res.data;
  if (Array.isArray(raw))              return raw;
  if (Array.isArray(raw?.data))        return raw.data;
  if (Array.isArray(raw?.data?.[key])) return raw.data[key];
  return [];
}

// ── USUARIO SIDEBAR ───────────────────────────────────────
const _user = getUser();
(() => {
  const name  = _user.full_name || _user.username || 'Admin';
  const role  = typeof _user.role === 'object'
    ? (_user.role?.name || 'usuario')
    : (_user.role || 'usuario');
  const avatar = (name[0] || 'A').toUpperCase();
  const el = id => document.getElementById(id);
  if (el('sidebarName'))   el('sidebarName').textContent   = name;
  if (el('sidebarRole'))   el('sidebarRole').textContent   = role;
  if (el('sidebarAvatar')) el('sidebarAvatar').textContent = avatar;
})();


// Control de acceso por rol
const _role = typeof _user.role === 'object' ? _user.role?.name : _user.role;

function hasRole(...roles) {
  return roles.includes(_role);
}

// Ocultar secciones según rol
document.addEventListener('DOMContentLoaded', () => {
  // Solo admin ve usuarios
  if (!hasRole('admin')) {
    document.querySelector('[data-section="users"]')?.remove();
  }
  // Solo admin y tecnico pueden crear dispositivos
  if (!hasRole('admin', 'tecnico')) {
    document.querySelector('[onclick="openDeviceModal()"]')?.remove();
    document.querySelector('[onclick="openLocationModal()"]')?.remove();
  }
  // Viewer solo ve, no puede crear nada
  if (hasRole('viewer')) {
    document.querySelectorAll('.btn-primary').forEach(b => {
      if (b.textContent.includes('Nuevo') || b.textContent.includes('Crear')) {
        b.style.display = 'none';
      }
    });
  }
});
// ── RELOJ ─────────────────────────────────────────────────
setInterval(() => {
  const cl = document.getElementById('clock');
  if (cl) cl.textContent =
    new Date().toLocaleTimeString('es-CO', { hour12: false });
}, 1000);

// ── NAVEGACIÓN ────────────────────────────────────────────
const SECTION_TITLES = {
  overview:  'Dashboard',
  devices:   'Dispositivos',
  locations: 'Ubicaciones',
  metrics:   'Métricas',
  alerts:    'Alertas',
  users:     'Usuarios',
};

document.querySelectorAll('.nav-item[data-section]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    navigateTo(link.dataset.section);
  });
});

document.querySelectorAll('.card-link[data-section]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    navigateTo(link.dataset.section);
  });
});

function navigateTo(sec) {
  document.querySelectorAll('.nav-item').forEach(n =>
    n.classList.toggle('active', n.dataset.section === sec));
  document.querySelectorAll('.section').forEach(s =>
    s.classList.toggle('active', s.id === `section-${sec}`));
  const pt = document.getElementById('pageTitle');
  if (pt) pt.textContent = SECTION_TITLES[sec] || sec;
  ({
    overview:  loadOverview,
    devices:   loadDevices,
    locations: loadLocations,
    metrics:   loadMetrics,
    alerts:    loadAlerts,
    users:     loadUsers,
  })[sec]?.();
}

// ── TOAST ─────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const icons = { success: '✓', error: '✕', warn: '⚠' };
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.innerHTML = `<span>${icons[type] || 'i'}</span> ${msg}`;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ── MODALES ───────────────────────────────────────────────
function openModal(id)  { document.getElementById(id)?.classList.add('open'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('open'); }

document.querySelectorAll('.modal-backdrop').forEach(m => {
  m.addEventListener('click', e => { if (e.target === m) m.classList.remove('open'); });
});

// ── BADGES ────────────────────────────────────────────────
function statusBadge(s) {
  const map = {
    activo:        ['badge-success', 'Activo'],
    inactivo:      ['badge-slate',   'Inactivo'],
    mantenimiento: ['badge-warn',    'Mantenimiento'],
    falla:         ['badge-danger',  'Falla'],
    activa:        ['badge-danger',  'Activa'],
    reconocida:    ['badge-warn',    'Reconocida'],
    resuelta:      ['badge-success', 'Resuelta'],
    normal:        ['badge-success', 'Normal'],
    warning:       ['badge-warn',    'Warning'],
    critical:      ['badge-danger',  'Crítico'],
    true:          ['badge-success', 'Activo'],
    false:         ['badge-slate',   'Inactivo'],
  };
  const key = String(s).toLowerCase();
  const [cls, label] = map[key] || ['badge-slate', s || '—'];
  return `<span class="badge ${cls}"><span class="badge-dot"></span>${label}</span>`;
}

function sevBadge(name, color) {
  if (!name) return '<span class="badge badge-slate">—</span>';
  const c = color || '#8DA4BC';
  return `<span class="badge" style="background:${c}22;color:${c};border:1px solid ${c}44">
    <span class="badge-dot" style="background:${c}"></span>${name}
  </span>`;
}

function fmtDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('es-CO', {
    dateStyle: 'short', timeStyle: 'short'
  });
}

// ── HELPERS DOM ───────────────────────────────────────────
function set(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}
function setHTML(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

// ══════════════════════════════════════════════════════════
//  OVERVIEW
// ══════════════════════════════════════════════════════════
async function loadOverview() {
  const [devR, altR, locR, usrR] = await Promise.all([
    apiFetch('DEVICES',   '/api/devices/'),
    apiFetch('ALERTS',    '/api/alerts/summary'),
    apiFetch('LOCATIONS', '/api/locations/'),
    apiFetch('USERS',     '/api/users/'),
  ]);

  // Dispositivos
  if (devR?.ok) {
    const d = extractList(devR, 'devices');
    set('totalDevices',   d.length);
    set('activeDevices',  d.filter(x => x.status === 'activo').length);
    set('warningDevices', d.filter(x => x.status === 'mantenimiento').length);

    const counts = {};
    d.forEach(x => { counts[x.status] = (counts[x.status] || 0) + 1; });
    const colors = {
      activo:        'var(--success)',
      inactivo:      'var(--slate)',
      mantenimiento: 'var(--warning)',
      falla:         'var(--danger)',
    };
    const labels = {
      activo:        'Activo',
      inactivo:      'Inactivo',
      mantenimiento: 'Mantenimiento',
      falla:         'Falla',
    };
    setHTML('deviceStatusList',
      Object.entries(counts).map(([s, c]) => `
        <div class="status-item">
          <div class="status-item-label">
            <span class="status-dot-sm"
              style="background:${colors[s] || 'var(--slate)'}"></span>
            ${labels[s] || s}
          </div>
          <span class="status-count">${c}</span>
        </div>`).join('') ||
      '<div class="empty-state"><p>Sin datos</p></div>');
  }

  // Alertas resumen
  if (altR?.ok) {
    const total = altR.data?.data?.total_active ?? 0;
    set('activeAlerts', total);
    const b = document.getElementById('alertsBadge');
    if (b) { b.textContent = total; b.style.display = total > 0 ? '' : 'none'; }
  }

  // Totales
  if (locR?.ok) set('totalLocations', extractList(locR, 'locations').length);
  if (usrR?.ok) set('totalUsers',     extractList(usrR, 'users').length);

  // Alertas recientes
  const recR = await apiFetch('ALERTS', '/api/alerts/?status=activa&limit=6');
  if (recR?.ok) {
    const list = extractList(recR, 'alerts');
    setHTML('recentAlerts', list.length
      ? list.map(a => {
          const color = a.severity?.color || '#8DA4BC';
          return `
            <div class="alert-item">
              <div class="alert-severity"
                style="background:${color};box-shadow:0 0 6px ${color}66"></div>
              <div style="flex:1">
                <div class="alert-item-title">${a.title}</div>
                <div class="alert-item-meta">
                  Dispositivo #${a.device_id || '—'} · ${fmtDate(a.created_at)}
                </div>
              </div>
              ${statusBadge(a.status)}
            </div>`;
        }).join('')
      : '<div class="empty-state"><p>Sin alertas activas 🎉</p></div>');
  }
}

// ══════════════════════════════════════════════════════════
//  DEVICES
// ══════════════════════════════════════════════════════════
let allDevices = [];

async function loadDevices() {
  setHTML('devicesBody',
    '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-dim)">Cargando...</td></tr>');

  const res = await apiFetch('DEVICES', '/api/devices/');
  if (!res?.ok) {
    setHTML('devicesBody',
      `<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--danger)">
        ${res?.data?.message || 'Error de conexión'}
      </td></tr>`);
    return;
  }

  allDevices = extractList(res, 'devices');
  renderDevices(allDevices);

  // Poblar selects en alertas y métricas
  const alertSel = document.getElementById('alertDevice');
  if (alertSel) {
    alertSel.innerHTML =
      '<option value="">— Sin dispositivo —</option>' +
      allDevices.map(d =>
        `<option value="${d.id}">${d.name}</option>`).join('');
  }
  const metSel = document.getElementById('metricsDeviceFilter');
  if (metSel) {
    const prev = metSel.value;
    metSel.innerHTML =
      '<option value="">Todos los dispositivos</option>' +
      allDevices.map(d =>
        `<option value="${d.id}">${d.name}</option>`).join('');
    if (prev) metSel.value = prev;
  }
}

function renderDevices(list) {
  if (!list.length) {
    setHTML('devicesBody',
      '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-dim)">Sin resultados</td></tr>');
    return;
  }
  setHTML('devicesBody', list.map(d => `
    <tr>
      <td>#${d.id}</td>
      <td style="color:var(--white);font-weight:500">${d.name}</td>
      <td><code>${d.ip_address || '—'}</code></td>
      <td>${d.device_type?.name || '—'}</td>
      <td>${statusBadge(d.status)}</td>
      <td>${d.location_id ? `Ubic. #${d.location_id}` : '—'}</td>
      <td>
        <button class="btn-action"
          onclick='openEditDeviceModal(${JSON.stringify(d).replace(/'/g,"&#39;")})'>
          Editar
        </button>
        <button class="btn-action"
          onclick="changeDeviceStatus(${d.id})">
          Estado
        </button>
        <button class="btn-action del"
          onclick="confirmDeleteDevice(${d.id}, '${d.name.replace(/'/g,"\\'")}')">
          Eliminar
        </button>
      </td>
    </tr>`).join(''));
}

// Filtros en tiempo real
document.getElementById('deviceSearch')?.addEventListener('input', () => {
  const q = document.getElementById('deviceSearch').value.toLowerCase();
  renderDevices(allDevices.filter(d =>
    d.name.toLowerCase().includes(q) ||
    (d.ip_address || '').includes(q)));
});

document.getElementById('deviceStatusFilter')?.addEventListener('change', () => {
  const s = document.getElementById('deviceStatusFilter').value;
  renderDevices(s ? allDevices.filter(d => d.status === s) : allDevices);
});

// Abrir modal NUEVO dispositivo
async function openDeviceModal() {
  document.getElementById('deviceId').value     = '';
  document.getElementById('deviceName').value   = '';
  document.getElementById('deviceIp').value     = '';
  document.getElementById('deviceMac').value    = '';
  document.getElementById('deviceDesc').value   = '';
  document.getElementById('deviceStatus').value = 'activo';
  document.getElementById('deviceModalTitle').textContent = 'Nuevo Dispositivo';
  await loadTypesIntoSelect(null);
  await loadLocationsIntoSelect('deviceLocation', null);
  openModal('deviceModal');
}

// Abrir modal EDITAR dispositivo
async function openEditDeviceModal(d) {
  document.getElementById('deviceId').value     = d.id;
  document.getElementById('deviceName').value   = d.name        || '';
  document.getElementById('deviceIp').value     = d.ip_address  || '';
  document.getElementById('deviceMac').value    = d.mac_address || '';
  document.getElementById('deviceDesc').value   = d.description || '';
  document.getElementById('deviceStatus').value = d.status      || 'activo';
  document.getElementById('deviceModalTitle').textContent = 'Editar Dispositivo';
  await loadTypesIntoSelect(d.device_type?.id || null);
  await loadLocationsIntoSelect('deviceLocation', d.location_id || null);
  openModal('deviceModal');
}

async function loadTypesIntoSelect(selectedId = null) {
  const res = await apiFetch('DEVICES', '/api/device-types/');
  if (!res?.ok) return;
  const types = extractList(res, 'device_types');
  const sel   = document.getElementById('deviceType');
  if (!sel) return;
  sel.innerHTML = types.map(t =>
    `<option value="${t.id}" ${t.id == selectedId ? 'selected' : ''}>${t.name}</option>`
  ).join('');
}

async function loadLocationsIntoSelect(selId, selectedId = null) {
  const res = await apiFetch('LOCATIONS', '/api/locations/');
  if (!res?.ok) return;
  const locs = extractList(res, 'locations');
  const sel  = document.getElementById(selId);
  if (!sel) return;
  sel.innerHTML =
    '<option value="">— Sin ubicación —</option>' +
    locs.map(l =>
      `<option value="${l.id}" ${l.id == selectedId ? 'selected' : ''}>${l.name}</option>`
    ).join('');
}

async function saveDevice() {
  const id = document.getElementById('deviceId').value;
  const payload = {
    name:           document.getElementById('deviceName').value.trim(),
    ip_address:     document.getElementById('deviceIp').value.trim()   || null,
    mac_address:    document.getElementById('deviceMac').value.trim()  || null,
    device_type_id: parseInt(document.getElementById('deviceType').value)     || null,
    status:         document.getElementById('deviceStatus').value,
    location_id:    parseInt(document.getElementById('deviceLocation').value) || null,
    description:    document.getElementById('deviceDesc').value.trim() || null,
  };

  if (!payload.name) { showToast('El nombre es obligatorio', 'error'); return; }

  const res = id
    ? await apiFetch('DEVICES', `/api/devices/${id}`,
        { method: 'PUT',  body: JSON.stringify(payload) })
    : await apiFetch('DEVICES', '/api/devices/',
        { method: 'POST', body: JSON.stringify(payload) });

  if (res?.ok) {
    showToast(id ? 'Dispositivo actualizado ✓' : 'Dispositivo creado ✓');
    closeModal('deviceModal');
    loadDevices();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error al guardar', 'error');
  }
}

async function confirmDeleteDevice(id, name) {
  if (!confirm(`¿Eliminar "${name}"?\nEsta acción no se puede deshacer.`)) return;
  const res = await apiFetch('DEVICES', `/api/devices/${id}`, { method: 'DELETE' });
  if (res?.ok) {
    showToast('Dispositivo eliminado');
    loadDevices();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error al eliminar', 'error');
  }
}

async function changeDeviceStatus(id) {
  const dev = allDevices.find(d => d.id === id);
  if (!dev) return;
  const statuses = ['activo', 'inactivo', 'mantenimiento', 'falla'];
  const options  = statuses.filter(s => s !== dev.status);
  const choice   = prompt(
    `Dispositivo: "${dev.name}"\nEstado actual: ${dev.status}\n\n` +
    `Nuevo estado:\n${options.map((s, i) => `${i + 1}. ${s}`).join('\n')}\n\nEscriba el número:`
  );
  if (!choice) return;
  const newStatus = options[parseInt(choice) - 1];
  if (!newStatus) { showToast('Opción inválida', 'error'); return; }

  const res = await apiFetch('DEVICES', `/api/devices/${id}/status`, {
    method: 'PATCH',
    body:   JSON.stringify({ status: newStatus }),
  });
  if (res?.ok) {
    showToast(`Estado cambiado → ${newStatus} ✓`);
    loadDevices();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

// ══════════════════════════════════════════════════════════
//  LOCATIONS
// ══════════════════════════════════════════════════════════
let allLocations = [];

async function loadLocations() {
  setHTML('locationsBody',
    '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-dim)">Cargando...</td></tr>');

  const res = await apiFetch('LOCATIONS', '/api/locations/');
  if (!res?.ok) {
    setHTML('locationsBody',
      `<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--danger)">
        ${res?.data?.message || 'Error de conexión'}
      </td></tr>`);
    return;
  }

  allLocations = extractList(res, 'locations');
  renderLocations(allLocations);
}

function renderLocations(list) {
  if (!list.length) {
    setHTML('locationsBody',
      '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-dim)">Sin resultados</td></tr>');
    return;
  }
  setHTML('locationsBody', list.map(l => `
    <tr>
      <td>#${l.id}</td>
      <td style="color:var(--white);font-weight:500">${l.name}</td>
      <td>${l.building || '—'}</td>
      <td>${l.floor    || '—'}</td>
      <td>${l.room     || '—'}</td>
      <td>${l.is_active
        ? '<span class="badge badge-success"><span class="badge-dot"></span>Activa</span>'
        : '<span class="badge badge-slate"><span class="badge-dot"></span>Inactiva</span>'}</td>
      <td>
        <button class="btn-action"
          onclick='openEditLocationModal(${JSON.stringify(l).replace(/'/g,"&#39;")})'>
          Editar
        </button>
        <button class="btn-action del"
          onclick="confirmDeleteLocation(${l.id}, '${l.name.replace(/'/g,"\\'")}')">
          Desactivar
        </button>
      </td>
    </tr>`).join(''));
}

document.getElementById('locationSearch')?.addEventListener('input', () => {
  const q = document.getElementById('locationSearch').value.toLowerCase();
  renderLocations(allLocations.filter(l =>
    l.name.toLowerCase().includes(q) ||
    (l.building || '').toLowerCase().includes(q)));
});

function openLocationModal() {
  document.getElementById('locationId').value        = '';
  document.getElementById('locationName').value      = '';
  document.getElementById('locationBuilding').value  = '';
  document.getElementById('locationFloor').value     = '';
  document.getElementById('locationRoom').value      = '';
  document.getElementById('locationStatus').value    = 'activo';
  document.getElementById('locationModalTitle').textContent = 'Nueva Ubicación';
  openModal('locationModal');
}

function openEditLocationModal(l) {
  document.getElementById('locationId').value        = l.id;
  document.getElementById('locationName').value      = l.name     || '';
  document.getElementById('locationBuilding').value  = l.building || '';
  document.getElementById('locationFloor').value     = l.floor    || '';
  document.getElementById('locationRoom').value      = l.room     || '';
  document.getElementById('locationStatus').value    = l.is_active ? 'activo' : 'inactivo';
  document.getElementById('locationModalTitle').textContent = 'Editar Ubicación';
  openModal('locationModal');
}

async function saveLocation() {
  const id = document.getElementById('locationId').value;
  const payload = {
    name:      document.getElementById('locationName').value.trim(),
    building:  document.getElementById('locationBuilding').value.trim() || null,
    floor:     document.getElementById('locationFloor').value.trim()    || null,
    room:      document.getElementById('locationRoom').value.trim()     || null,
    is_active: document.getElementById('locationStatus').value === 'activo',
  };

  if (!payload.name) { showToast('El nombre es obligatorio', 'error'); return; }

  const res = id
    ? await apiFetch('LOCATIONS', `/api/locations/${id}`,
        { method: 'PUT',  body: JSON.stringify(payload) })
    : await apiFetch('LOCATIONS', '/api/locations/',
        { method: 'POST', body: JSON.stringify(payload) });

  if (res?.ok) {
    showToast(id ? 'Ubicación actualizada ✓' : 'Ubicación creada ✓');
    closeModal('locationModal');
    loadLocations();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error al guardar', 'error');
  }
}

async function confirmDeleteLocation(id, name) {
  if (!confirm(`¿Desactivar la ubicación "${name}"?`)) return;
  const res = await apiFetch('LOCATIONS', `/api/locations/${id}`, { method: 'DELETE' });
  if (res?.ok) {
    showToast('Ubicación desactivada');
    loadLocations();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

// ══════════════════════════════════════════════════════════
//  METRICS
// ══════════════════════════════════════════════════════════
async function loadDevicesForSelects() {
  const r = await apiFetch('DEVICES', '/api/devices/');
  if (r?.ok) allDevices = extractList(r, 'devices');
}

async function loadMetrics() {
  setHTML('metricsBody',
    '<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-dim)">Cargando...</td></tr>');

  if (!allDevices.length) await loadDevicesForSelects();

  const deviceId = document.getElementById('metricsDeviceFilter')?.value || '';
  const status   = document.getElementById('metricsStatusFilter')?.value  || '';
  let   url      = '/api/metrics/?limit=100';
  if (deviceId) url += `&device_id=${deviceId}`;
  if (status)   url += `&status=${status}`;

  const res = await apiFetch('METRICS', url);
  if (!res?.ok) {
    setHTML('metricsBody',
      `<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--danger)">
        ${res?.data?.message || 'Error de conexión'}
      </td></tr>`);
    return;
  }

  const metrics = extractList(res, 'metrics');
  if (!metrics.length) {
    setHTML('metricsBody',
      '<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-dim)">Sin métricas registradas</td></tr>');
    return;
  }

  const devMap = {};
  allDevices.forEach(d => { devMap[d.id] = d.name; });

  setHTML('metricsBody', metrics.map(m => `
    <tr>
      <td>#${m.id}</td>
      <td style="color:var(--white)">${devMap[m.device_id] || `#${m.device_id}`}</td>
      <td>${m.metric_type?.name || '—'}</td>
      <td style="font-family:monospace">
        <strong>${m.value}</strong> ${m.unit || ''}
      </td>
      <td>${statusBadge(m.status)}</td>
      <td>${fmtDate(m.recorded_at)}</td>
    </tr>`).join(''));
}

document.getElementById('metricsDeviceFilter')?.addEventListener('change', loadMetrics);
document.getElementById('metricsStatusFilter')?.addEventListener('change', loadMetrics);

// ══════════════════════════════════════════════════════════
//  ALERTS
// ══════════════════════════════════════════════════════════
let allAlerts     = [];
let allSeverities = [];

async function loadAlerts() {
  setHTML('alertsBody',
    '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-dim)">Cargando...</td></tr>');

  const status = document.getElementById('alertStatusFilter')?.value || '';
  const url    = status
    ? `/api/alerts/?status=${status}&limit=100`
    : '/api/alerts/?limit=100';

  const [alertRes, sevRes] = await Promise.all([
    apiFetch('ALERTS', url),
    apiFetch('ALERTS', '/api/severities/'),
  ]);

  if (sevRes?.ok) {
    allSeverities = extractList(sevRes, 'severities');
    const sel = document.getElementById('alertSeverity');
    if (sel) {
      sel.innerHTML = allSeverities.map(s =>
        `<option value="${s.id}">${s.name}</option>`).join('');
    }
  }

  if (!alertRes?.ok) {
    setHTML('alertsBody',
      `<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--danger)">
        ${alertRes?.data?.message || 'Error de conexión'}
      </td></tr>`);
    return;
  }

  allAlerts = extractList(alertRes, 'alerts');
  renderAlerts(allAlerts);

  const count = allAlerts.filter(a => a.status === 'activa').length;
  const b = document.getElementById('alertsBadge');
  if (b) { b.textContent = count; b.style.display = count > 0 ? '' : 'none'; }
}

function renderAlerts(list) {
  const sevFilter = document.getElementById('alertSeverityFilter')?.value || '';
  const filtered  = sevFilter
    ? list.filter(a => (a.severity?.name || '').toLowerCase() === sevFilter)
    : list;

  if (!filtered.length) {
    setHTML('alertsBody',
      '<tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-dim)">Sin alertas</td></tr>');
    return;
  }

  setHTML('alertsBody', filtered.map(a => {
    const color = a.severity?.color || '#8DA4BC';
    return `
      <tr>
        <td>#${a.id}</td>
        <td style="color:var(--white);font-weight:500">${a.title}</td>
        <td>${sevBadge(a.severity?.name, color)}</td>
        <td>${statusBadge(a.status)}</td>
        <td>${a.device_id ? `#${a.device_id}` : '—'}</td>
        <td>${fmtDate(a.created_at)}</td>
        <td>
          ${a.status === 'activa'
            ? `<button class="btn-action" onclick="ackAlert(${a.id})">Reconocer</button>` : ''}
          ${a.status !== 'resuelta'
            ? `<button class="btn-action" onclick="resolveAlert(${a.id})">Resolver</button>` : ''}
          <button class="btn-action del" onclick="confirmDeleteAlert(${a.id})">Eliminar</button>
        </td>
      </tr>`;
  }).join(''));
}

document.getElementById('alertStatusFilter')?.addEventListener('change', loadAlerts);
document.getElementById('alertSeverityFilter')?.addEventListener('change',
  () => renderAlerts(allAlerts));

async function openAlertModal() {
  document.getElementById('alertTitle').value = '';
  document.getElementById('alertDesc').value  = '';
  if (!allDevices.length) await loadDevicesForSelects();
  const sel = document.getElementById('alertDevice');
  if (sel) {
    sel.innerHTML =
      '<option value="">— Sin dispositivo —</option>' +
      allDevices.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
  }
  if (!allSeverities.length) {
    const r = await apiFetch('ALERTS', '/api/severities/');
    if (r?.ok) {
      allSeverities = extractList(r, 'severities');
      const s = document.getElementById('alertSeverity');
      if (s) s.innerHTML = allSeverities.map(x =>
        `<option value="${x.id}">${x.name}</option>`).join('');
    }
  }
  openModal('alertModal');
}

async function saveAlert() {
  const payload = {
    title:       document.getElementById('alertTitle').value.trim(),
    message:     document.getElementById('alertDesc').value.trim(),
    severity_id: parseInt(document.getElementById('alertSeverity').value),
    device_id:   parseInt(document.getElementById('alertDevice').value) || null,
  };

  if (!payload.title)       { showToast('El título es obligatorio', 'error');    return; }
  if (!payload.message)     { showToast('El mensaje es obligatorio', 'error');   return; }
  if (!payload.severity_id) { showToast('Seleccione una severidad', 'error');    return; }

  const res = await apiFetch('ALERTS', '/api/alerts/', {
    method: 'POST',
    body:   JSON.stringify(payload),
  });

  if (res?.ok) {
    showToast('Alerta creada ✓');
    closeModal('alertModal');
    loadAlerts();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error al crear', 'error');
  }
}

async function ackAlert(id) {
  const uid = getUser()?.id || 1;
  const res = await apiFetch('ALERTS', `/api/alerts/${id}/acknowledge`, {
    method: 'PATCH',
    body:   JSON.stringify({ user_id: uid }),
  });
  if (res?.ok) {
    showToast('Alerta reconocida ✓', 'warn');
    loadAlerts();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

async function resolveAlert(id) {
  const uid = getUser()?.id || 1;
  const res = await apiFetch('ALERTS', `/api/alerts/${id}/resolve`, {
    method: 'PATCH',
    body:   JSON.stringify({ user_id: uid, message: 'Resuelta desde el dashboard' }),
  });
  if (res?.ok) {
    showToast('Alerta resuelta ✓');
    loadAlerts();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

async function confirmDeleteAlert(id) {
  if (!confirm('¿Eliminar esta alerta permanentemente?')) return;
  const res = await apiFetch('ALERTS', `/api/alerts/${id}`, { method: 'DELETE' });
  if (res?.ok) {
    showToast('Alerta eliminada');
    loadAlerts();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

// ══════════════════════════════════════════════════════════
//  USERS
// ══════════════════════════════════════════════════════════
let allUsers = [];

async function loadUsers() {
  setHTML('usersBody',
    '<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-dim)">Cargando...</td></tr>');

  const res = await apiFetch('USERS', '/api/users/');
  if (!res?.ok) {
    setHTML('usersBody',
      `<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--danger)">
        ${res?.data?.message || 'Error de conexión'}
      </td></tr>`);
    return;
  }

  allUsers = extractList(res, 'users');
  renderUsers(allUsers);
}

function renderUsers(list) {
  if (!list.length) {
    setHTML('usersBody',
      '<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-dim)">Sin usuarios</td></tr>');
    return;
  }
  setHTML('usersBody', list.map(u => {
    const roleName = typeof u.role === 'object'
      ? (u.role?.name || '—')
      : (u.role || '—');
    return `
      <tr>
        <td>#${u.id}</td>
        <td style="color:var(--white);font-weight:500">${u.username}</td>
        <td>${u.email}</td>
        <td>
          <span class="badge badge-info">
            <span class="badge-dot"></span>${roleName}
          </span>
        </td>
        <td>${u.is_active
          ? '<span class="badge badge-success"><span class="badge-dot"></span>Activo</span>'
          : '<span class="badge badge-slate"><span class="badge-dot"></span>Inactivo</span>'}</td>
        <td>
          <button class="btn-action"
            onclick="toggleUserStatus(${u.id}, '${u.username}', ${u.is_active})">
            ${u.is_active ? 'Desactivar' : 'Activar'}
          </button>
          <button class="btn-action del"
            onclick="confirmDeleteUser(${u.id}, '${u.username}')">
            Eliminar
          </button>
        </td>
      </tr>`;
  }).join(''));
}

document.getElementById('userSearch')?.addEventListener('input', () => {
  const q = document.getElementById('userSearch').value.toLowerCase();
  renderUsers(allUsers.filter(u =>
    u.username.toLowerCase().includes(q) ||
    u.email.toLowerCase().includes(q) ||
    (u.full_name || '').toLowerCase().includes(q)));
});

async function openUserModal() {
  document.getElementById('newUsername').value = '';
  document.getElementById('newEmail').value    = '';
  document.getElementById('newPassword').value = '';

  const rolesRes = await apiFetch('USERS', '/api/roles/');
  if (rolesRes?.ok) {
    const roles = extractList(rolesRes, 'roles');
    document.getElementById('newRole').innerHTML =
      roles.map(r => `<option value="${r.id}">${r.name}</option>`).join('');
  }
  openModal('userModal');
}

async function saveUser() {
  const payload = {
    username:  document.getElementById('newUsername').value.trim(),
    email:     document.getElementById('newEmail').value.trim(),
    password:  document.getElementById('newPassword').value,
    role_id:   parseInt(document.getElementById('newRole').value) || null,
    full_name: null,
  };

  if (!payload.username) { showToast('El usuario es obligatorio', 'error');    return; }
  if (!payload.email)    { showToast('El email es obligatorio', 'error');      return; }
  if (!payload.password) { showToast('La contraseña es obligatoria', 'error'); return; }

  const res = await apiFetch('USERS', '/api/users/', {
    method: 'POST',
    body:   JSON.stringify(payload),
  });

  if (res?.ok) {
    showToast('Usuario creado ✓');
    closeModal('userModal');
    loadUsers();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error al crear', 'error');
  }
}

async function toggleUserStatus(id, username, isActive) {
  if (!confirm(`¿${isActive ? 'Desactivar' : 'Activar'} al usuario "${username}"?`)) return;
  const res = await apiFetch('USERS', `/api/users/${id}/toggle`, { method: 'PATCH' });
  if (res?.ok) {
    showToast(`Usuario ${isActive ? 'desactivado' : 'activado'} ✓`);
    loadUsers();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

async function confirmDeleteUser(id, username) {
  if (!confirm(`¿Eliminar al usuario "${username}"?\nSe desactivará su cuenta.`)) return;
  const res = await apiFetch('USERS', `/api/users/${id}`, { method: 'DELETE' });
  if (res?.ok) {
    showToast('Usuario eliminado');
    loadUsers();
    loadOverview();
  } else {
    showToast(res?.data?.message || 'Error', 'error');
  }
}

// ══════════════════════════════════════════════════════════
//  INIT
// ══════════════════════════════════════════════════════════
loadOverview();
setInterval(loadOverview, 30000);