

export function setTokens(access, refresh) {
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
}

export function getAccessToken() {
    return localStorage.getItem('access');
}

export function getRefreshToken() {
    return localStorage.getItem('refresh');
}

export function clearTokens() {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
}