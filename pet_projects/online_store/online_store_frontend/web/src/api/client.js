import { setTokens, getAccessToken, getRefreshToken, clearTokens } from "../auth/token.js";


const API_BASE = 'http://127.0.0.1:8000/api';

export async function apiFetch(url, options = {}, retried = false) {
    const access = getAccessToken();
    const refresh = getRefreshToken();


    const headers = {
            ...(options.headers || {}),
            ...(access ? {Authorization: `Store ${access}`} : {}),
        };

    const res = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers,
    });
    if (res.status !== 401) return res;
    if (retried === true) return res;
    if (!refresh) {
        clearTokens();
        window.location.href = '/login';
        return res;
    }

    const refreshRes = await fetch(`${API_BASE}/token/refresh/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({refresh: refresh}),
    });

    if (!refreshRes.ok) {
        clearTokens();
        window.location.href = '/login';
        return res;
    }

    const data = await refreshRes.json();

    setTokens(data.access, data.refresh ?? refresh);

    return apiFetch(url, options, true);

}

