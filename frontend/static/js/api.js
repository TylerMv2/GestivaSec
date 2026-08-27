// Gestiva Observability API Client

const API_BASE = '/api';

async function apiRequest(endpoint, method = 'GET', body = null) {
    const config = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (body) {
        config.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);
        if (response.status === 204) {
            return null;
        }
        if (!response.ok) {
            const errData = await response.json().catch(() => ({detail: response.statusText}));
            throw new Error(errData.detail || `API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Request to ${endpoint} failed:`, error);
        throw error;
    }
}

const API = {
    // Dashboard endpoints
    getDashboard: () => apiRequest('/dashboard'),
    
    // Network endpoints
    getNetwork: () => apiRequest('/network'),
    
    // Traffic endpoints
    getTraffic: (limit = 100) => apiRequest(`/traffic?limit=${limit}`),
    
    // Alerts endpoints
    getAlerts: (status = null, limit = 100) => {
        const query = status ? `?status=${status}&limit=${limit}` : `?limit=${limit}`;
        return apiRequest(`/alerts${query}`);
    },
    acknowledgeAlert: (id) => apiRequest(`/alerts/${id}/acknowledge`, 'POST'),
    resolveAlert: (id) => apiRequest(`/alerts/${id}/resolve`, 'POST'),
    
    // Logs endpoints
    getLogs: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return apiRequest(`/logs?${query}`);
    },
    
    // Hosts endpoints
    getHosts: () => apiRequest('/hosts'),
    getHost: (id) => apiRequest(`/hosts/${id}`),
    createHost: (hostData) => apiRequest('/hosts', 'POST', hostData),
    updateHost: (id, hostData) => apiRequest(`/hosts/${id}`, 'PUT', hostData),
    deleteHost: (id) => apiRequest(`/hosts/${id}`, 'DELETE'),
    
    // Services endpoints
    getServices: () => apiRequest('/services'),
    
    // Certificates endpoints
    getCertificates: () => apiRequest('/certificates'),
    
    // Topology endpoints
    getTopology: () => apiRequest('/topology'),
    
    // History endpoints
    getHistory: (hostId, metricName, timeframe = '24h') => 
        apiRequest(`/history?host_id=${hostId}&metric_name=${metricName}&timeframe=${timeframe}`),
        
    // Statistics endpoints
    getTrends: () => apiRequest('/statistics/trends'),
    
    // Settings endpoints
    getSettings: () => apiRequest('/settings'),
    updateSetting: (moduleName, settingsData) => apiRequest(`/settings/${moduleName}`, 'PUT', settingsData),
    
    // Vercel endpoints
    getVercelStatus: () => apiRequest('/vercel/status'),
    getVercelDeployments: (limit = 5) => apiRequest(`/vercel/deployments?limit=${limit}`),
    getVercelAnalytics: () => apiRequest('/vercel/analytics'),
    getVercelFirewall: (limit = 5) => apiRequest(`/vercel/firewall?limit=${limit}`)
};

// Global search function
async function globalSearch(query) {
    if (!query || query.trim() === "") return { hosts: [], logs: [], alerts: [] };
    
    try {
        const [hosts, alerts, logsRes] = await Promise.all([
            API.getHosts(),
            API.getAlerts(),
            API.getLogs({ search: query, limit: 10 })
        ]);
        
        const q = query.toLowerCase();
        
        const filteredHosts = hosts.filter(h => 
            h.hostname.toLowerCase().includes(q) || 
            h.ip.includes(q) || 
            h.classification.toLowerCase().includes(q)
        );
        
        const filteredAlerts = alerts.filter(a => 
            a.description.toLowerCase().includes(q) || 
            a.source.toLowerCase().includes(q)
        );
        
        return {
            hosts: filteredHosts,
            alerts: filteredAlerts,
            logs: logsRes.logs
        };
    } catch (e) {
        console.error("Global search error:", e);
        return { hosts: [], logs: [], alerts: [] };
    }
}
