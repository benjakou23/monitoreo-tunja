if (getToken() &&
   (location.pathname.includes('index.html') || location.pathname.endsWith('/'))) {
  location.href = 'dashboard.html';
}

function requireAuth() {
  if (!getToken()) location.href = 'index.html';
}

async function doLogin(username, password) {
  const res = await apiFetch('AUTH', '/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
  if (res && res.ok) {
    sessionStorage.setItem('hsr_token', res.data.data.token);
    sessionStorage.setItem('hsr_user',  JSON.stringify(res.data.data.user));
    return { ok: true };
  }
  return { ok: false, message: res?.data?.message || 'Credenciales incorrectas' };
}