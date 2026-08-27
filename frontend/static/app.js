/**
 * Gestiva Security (GestivaSec V1) — Reactive Frontend Application Engine
 * Integrates Dashboard, Live Telemetry Widgets, Chart.js, Assets, Incidents, Synthetic Probing & Audit Log APIs.
 * Aligned with GestivaOne Corporate Identity & Responsive Clean Titles.
 */
document.addEventListener("DOMContentLoaded", () => {
    const AUTH_API_URL = "/api/v1/auth";
    const ASSETS_API_URL = "/api/v1/assets";
    const PROBING_API_URL = "/api/v1/probing";
    const DASHBOARD_TELEMETRY_URL = "/api/v1/soc/dashboard/telemetry";
    const AUDIT_API_URL = "/api/v1/audit/logs";
    const DETECTION_ALERTS_URL = "/api/v1/detection/alerts";

    // AUTH SESSION HELPERS
    function getAuthToken() { return localStorage.getItem("gestivasec_token"); }
    function setAuthToken(token) { localStorage.setItem("gestivasec_token", token); }
    function clearAuthToken() { localStorage.removeItem("gestivasec_token"); }

    function getSelectedOrgId() {
        const selectOrg = document.getElementById("select-organization");
        return selectOrg ? selectOrg.value : "00000000-0000-0000-0000-000000000001";
    }

    function getHeaders() {
        const headers = { 
            "Content-Type": "application/json",
            "X-Organization-ID": getSelectedOrgId() 
        };
        const token = getAuthToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
        return headers;
    }

    // CHART.JS INITIALIZATION FOR LIVE TELEMETRY
    let liveTrafficChart = null;

    function initTrafficChart() {
        const ctx = document.getElementById("liveTrafficChart");
        if (!ctx) return;

        liveTrafficChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ["10s ago", "8s ago", "6s ago", "4s ago", "2s ago", "1s ago", "Now"],
                datasets: [
                    {
                        label: 'Tráfico de Red (Mbps)',
                        data: [20, 25, 18, 30, 28, 35, 24.5],
                        borderColor: '#7B61FF',
                        backgroundColor: 'rgba(123, 97, 255, 0.12)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Latencia Promedio (ms)',
                        data: [14, 15, 12, 18, 16, 20, 14],
                        borderColor: '#FF2E4C',
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#A0A0AB', font: { family: 'Inter', size: 11 } } }
                },
                scales: {
                    x: { ticks: { color: '#A0A0AB' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#A0A0AB' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }

    // WIDGET POLLING ENGINE
    async function updateSOCTelemetry() {
        try {
            if (window.GestivaLayout) window.GestivaLayout.setRealtimeStatus(window.GestivaUIState.REFRESHING);
            const response = await fetch(DASHBOARD_TELEMETRY_URL, { headers: getHeaders() });
            if (!response.ok) {
                if (window.GestivaLayout) window.GestivaLayout.setRealtimeStatus(window.GestivaUIState.OFFLINE);
                return;
            }

            const data = await response.json();
            if (window.GestivaLayout) {
                window.GestivaLayout.setRealtimeStatus(window.GestivaUIState.REALTIME_CONNECTED);
                window.GestivaLayout.setHighSeverityAlarm(data.critical_alerts_count > 0);
            }

            // Update 10 Widget UI Values
            document.getElementById("widget-hosts-online").textContent = data.hosts_online;
            document.getElementById("widget-total-hosts").textContent = data.total_hosts;
            document.getElementById("widget-critical-alerts").textContent = data.critical_alerts_count;
            document.getElementById("widget-down-services").textContent = data.down_services_count;
            document.getElementById("widget-traffic-mbps").textContent = data.traffic_mbps;
            document.getElementById("widget-cpu-pct").textContent = data.cpu_usage_pct;
            document.getElementById("widget-ram-pct").textContent = data.ram_usage_pct;
            document.getElementById("widget-events-min").textContent = data.events_per_minute;
            document.getElementById("widget-expiring-tls").textContent = data.expiring_tls_certs_count;
            document.getElementById("widget-connected-users").textContent = data.connected_users_count;
            document.getElementById("widget-active-sessions").textContent = data.active_sessions_count;

            // Update Progress Bar Gauges
            const cpuBar = document.getElementById("gauge-cpu-bar");
            if (cpuBar) cpuBar.style.width = `${Math.min(data.cpu_usage_pct, 100)}%`;

            const ramBar = document.getElementById("gauge-ram-bar");
            if (ramBar) ramBar.style.width = `${Math.min(data.ram_usage_pct, 100)}%`;

            // Update Live Chart
            if (liveTrafficChart) {
                liveTrafficChart.data.labels = data.traffic_labels;
                liveTrafficChart.data.datasets[0].data = data.traffic_data_mbps;
                liveTrafficChart.data.datasets[1].data = data.latency_series_ms;
                liveTrafficChart.update('none');
            }

            // Update Core Services Status Table
            const servicesTbody = document.getElementById("services-status-body");
            if (servicesTbody && data.services_status) {
                servicesTbody.innerHTML = data.services_status.map(s => `
                    <tr>
                        <td><strong>${s.name}</strong></td>
                        <td><span class="badge ${s.status === 'ONLINE' ? 'badge-success' : 'badge-danger'}">${s.status}</span></td>
                        <td><code>${s.latency}</code></td>
                    </tr>
                `).join('');
            }
        } catch (e) {
            console.error("Telemetry update error:", e);
            if (window.GestivaLayout) window.GestivaLayout.setRealtimeStatus(window.GestivaUIState.OFFLINE);
        }
    }

    // MODULE 2: NAVIGATION TAB SWITCHING & CLEAN TITLES
    const menuSocDashboard = document.getElementById("menu-soc-dashboard");
    const menuIncidents = document.getElementById("menu-incidents");
    const menuAssets = document.getElementById("menu-assets");
    const menuObservability = document.getElementById("menu-observability");
    const menuAudit = document.getElementById("menu-audit");

    const sectionSocDashboard = document.getElementById("section-soc-dashboard");
    const sectionIncidents = document.getElementById("section-incidents");
    const sectionAssets = document.getElementById("section-assets");
    const sectionObservability = document.getElementById("section-observability");
    const sectionAudit = document.getElementById("section-audit");

    const pageHeading = document.getElementById("page-heading");
    const pageSubheading = document.getElementById("page-subheading");

    function setActiveTab(tab) {
        [menuSocDashboard, menuIncidents, menuAssets, menuObservability, menuAudit].forEach(m => m && m.classList.remove("active"));
        [sectionSocDashboard, sectionIncidents, sectionAssets, sectionObservability, sectionAudit].forEach(s => s && (s.style.display = "none"));

        if (tab === "soc-dashboard") {
            menuSocDashboard.classList.add("active");
            sectionSocDashboard.style.display = "block";
            pageHeading.textContent = "Dashboard";
            pageSubheading.textContent = "Monitoreo telemétrico en vivo";
            updateSOCTelemetry();
        } else if (tab === "incidents") {
            if (menuIncidents) menuIncidents.classList.add("active");
            if (sectionIncidents) sectionIncidents.style.display = "block";
            pageHeading.textContent = "Incidentes & Alertas";
            pageSubheading.textContent = "Gestión de hallazgos y respuestas tácticas";
            loadIncidents();
        } else if (tab === "assets") {
            menuAssets.classList.add("active");
            sectionAssets.style.display = "block";
            pageHeading.textContent = "Activos Digitales";
            pageSubheading.textContent = "Gestión de infraestructura corporativa";
            loadAssets();
        } else if (tab === "observability") {
            menuObservability.classList.add("active");
            sectionObservability.style.display = "block";
            pageHeading.textContent = "Observabilidad Sintética";
            pageSubheading.textContent = "Pruebas de disponibilidad y latencia";
            loadProbes();
        } else if (tab === "audit") {
            menuAudit.classList.add("active");
            sectionAudit.style.display = "block";
            pageHeading.textContent = "Traza de Auditoría";
            pageSubheading.textContent = "Registro inmutable de eventos";
            loadAuditLogs();
        }
    }

    if (menuSocDashboard) menuSocDashboard.addEventListener("click", (e) => { e.preventDefault(); setActiveTab("soc-dashboard"); });
    if (menuIncidents) menuIncidents.addEventListener("click", (e) => { e.preventDefault(); setActiveTab("incidents"); });
    if (menuAssets) menuAssets.addEventListener("click", (e) => { e.preventDefault(); setActiveTab("assets"); });
    if (menuObservability) menuObservability.addEventListener("click", (e) => { e.preventDefault(); setActiveTab("observability"); });
    if (menuAudit) menuAudit.addEventListener("click", (e) => { e.preventDefault(); setActiveTab("audit"); });

    // INTERACTIVE DASHBOARD CARD ROUTING
    document.querySelectorAll(".clickable-card[data-route]").forEach(card => {
        card.addEventListener("click", () => {
            const route = card.getAttribute("data-route");
            if (route === "traffic-chart") {
                const chartEl = document.getElementById("section-traffic-chart");
                if (chartEl) chartEl.scrollIntoView({ behavior: 'smooth' });
            } else {
                setActiveTab(route);
            }
        });
    });

    // LOAD INCIDENTS TABLE
    async function loadIncidents() {
        const tableBody = document.getElementById("incidents-table-body");
        if (!tableBody) return;

        if (window.GestivaLayout) {
            window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADING, { type: 'table', colCount: 6, rowCount: 3 });
        }

        try {
            const response = await fetch(DETECTION_ALERTS_URL, { headers: getHeaders() });
            const alerts = await response.json();

            if (!response.ok) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                        title: "ERROR AL CARGAR ALERTAS",
                        message: "Falla al recuperar alertas del motor de detección.",
                        onRetry: loadIncidents
                    });
                }
                return;
            }

            if (!alerts || alerts.length === 0) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.EMPTY, {
                        title: "SIN ALERTAS ACTIVAS",
                        message: "No se han detectado alertas ni incidentes en esta organización.",
                        icon: "fa-solid fa-shield-check"
                    });
                } else {
                    tableBody.innerHTML = `<tr><td colspan="6" class="text-center">No hay alertas activas en esta organización.</td></tr>`;
                }
                return;
            }

            tableBody.innerHTML = alerts.map(a => `
                <tr>
                    <td><span class="badge ${a.severity === 'P1_CRITICAL' ? 'badge-danger' : 'badge-warning'}">${a.severity}</span></td>
                    <td><strong>${a.title}</strong></td>
                    <td><code>${a.mitre_attack_id}</code></td>
                    <td><code>${a.source_ip}</code></td>
                    <td><span class="badge badge-info">${a.status}</span></td>
                    <td>
                        <button class="btn btn-secondary btn-sm btn-contain-alert" data-alert-id="${a.alert_id}">Contener Alerta</button>
                    </td>
                </tr>
            `).join('');

            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADED);
            }
        } catch (e) {
            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                    title: "ERROR DE CONEXIÓN",
                    message: "No se pudo conectar con el servidor para obtener los incidentes.",
                    onRetry: loadIncidents
                });
            } else {
                tableBody.innerHTML = `<tr><td colspan="6" class="text-center">Error de conexión al cargar alertas.</td></tr>`;
            }
        }
    }

    const btnRefreshIncidents = document.getElementById("btn-refresh-incidents");
    if (btnRefreshIncidents) btnRefreshIncidents.addEventListener("click", loadIncidents);

    // LOAD ASSETS TABLE WITH 12-STATE MACHINE
    async function loadAssets() {
        const tableBody = document.getElementById("assets-table-body");
        if (!tableBody) return;

        if (window.GestivaLayout) {
            window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADING, { type: 'table', colCount: 6, rowCount: 3 });
        }

        try {
            const response = await fetch(ASSETS_API_URL, { headers: getHeaders() });
            const assets = await response.json();

            if (!response.ok) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                        title: "ERROR AL CARGAR ACTIVOS",
                        message: "Falla en la respuesta de la API de activos.",
                        onRetry: loadAssets
                    });
                }
                return;
            }

            if (!assets || assets.length === 0) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.EMPTY, {
                        title: "SIN ACTIVOS REGISTRADOS",
                        message: "No hay activos registrados para la organización seleccionada.",
                        icon: "fa-solid fa-boxes-stacked",
                        actionText: "Registrar Activo",
                        onAction: () => document.getElementById("asset-modal")?.classList.add("active")
                    });
                } else {
                    tableBody.innerHTML = `<tr><td colspan="6" class="text-center">No hay activos registrados en esta organización.</td></tr>`;
                }
                return;
            }

            tableBody.innerHTML = assets.map(a => `
                <tr>
                    <td><strong>${a.name}</strong></td>
                    <td><code>${a.target_url}</code></td>
                    <td><span class="badge ${a.criticality === 'P1_CRITICAL' ? 'badge-danger' : 'badge-warning'}">${a.criticality}</span></td>
                    <td>${a.owner_email}</td>
                    <td><span class="badge badge-success">${a.status}</span></td>
                    <td>
                        <button class="btn btn-secondary btn-sm btn-probe" data-asset-id="${a.id}">Sondeo Sintético</button>
                    </td>
                </tr>
            `).join('');

            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADED);
            }

            // Attach Probe Button Handlers
            document.querySelectorAll(".btn-probe").forEach(btn => {
                btn.addEventListener("click", async () => {
                    const assetId = btn.getAttribute("data-asset-id");
                    btn.disabled = true;
                    btn.textContent = "Sondeando...";
                    try {
                        const probeResp = await fetch(`${PROBING_API_URL}/probe`, {
                            method: "POST",
                            headers: getHeaders(),
                            body: JSON.stringify({ asset_id: assetId })
                        });
                        const result = await probeResp.json();
                        if (probeResp.ok) {
                            showToast(`Sondeo exitoso: ${result.http_code} (${result.response_time_ms}ms)`, "success");
                            loadProbes(); // Refresh probe history
                        } else {
                            showToast(`Falla de sondeo: ${result.detail || 'Error'}`, "error");
                        }
                    } catch (err) {
                        showToast("Error de conexión al ejecutar sondeo.", "error");
                    } finally {
                        btn.disabled = false;
                        btn.textContent = "Sondeo Sintético";
                    }
                });
            });
        } catch (e) {
            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                    title: "ERROR DE CONEXIÓN",
                    message: "No se pudo conectar con el servidor para obtener los activos.",
                    onRetry: loadAssets
                });
            } else {
                tableBody.innerHTML = `<tr><td colspan="6" class="text-center">Error de conexión al cargar activos.</td></tr>`;
            }
        }
    }

    const btnRefreshAssets = document.getElementById("btn-refresh-assets");
    if (btnRefreshAssets) btnRefreshAssets.addEventListener("click", loadAssets);

    // MODULE 3: REPAIR SYNTHETIC OBSERVABILITY VIEW
    async function loadProbes() {
        const tableBody = document.getElementById("probes-table-body");
        if (!tableBody) return;

        if (window.GestivaLayout) {
            window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADING, { type: 'table', colCount: 6, rowCount: 3 });
        }

        try {
            const response = await fetch(`${PROBING_API_URL}/probes`, { headers: getHeaders() });
            const probes = await response.json();

            if (!response.ok) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                        title: "ERROR DE EVALUACIONES SINTÉTICAS",
                        message: "No se pudo consultar el historial de sondajes.",
                        onRetry: loadProbes
                    });
                }
                return;
            }

            if (!probes || probes.length === 0) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.EMPTY, {
                        title: "SIN EVALUACIONES REGISTRADAS",
                        message: "No se han ejecutado sondajes sintéticos en esta sesión.",
                        icon: "fa-solid fa-chart-line"
                    });
                } else {
                    tableBody.innerHTML = `<tr><td colspan="6" class="text-center">No hay registros de sondajes sintéticos aún.</td></tr>`;
                }
                return;
            }

            tableBody.innerHTML = probes.map(p => `
                <tr>
                    <td>${new Date(p.timestamp || Date.now()).toLocaleString()}</td>
                    <td><code>${p.target_url || p.asset_id}</code></td>
                    <td><span class="badge ${(p.status_code || p.http_code || 200) === 200 ? 'badge-success' : 'badge-danger'}">${p.status_code || p.http_code || 200}</span></td>
                    <td><code>${p.latency_ms !== undefined ? p.latency_ms : (p.response_time_ms || 0)} ms</code></td>
                    <td><span class="badge ${p.is_successful !== false ? 'badge-success' : 'badge-danger'}">${p.is_successful !== false ? 'HEALTHY' : 'FAILURE'}</span></td>
                    <td><small>${JSON.stringify(p.evidence_id ? { evidence_id: p.evidence_id } : { status: 'OK' })}</small></td>
                </tr>
            `).join('');

            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADED);
            }
        } catch (e) {
            console.error("Probes fetch error:", e);
            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                    title: "ERROR DE CONEXIÓN",
                    message: "Falla de red al obtener evaluaciones sintéticas.",
                    onRetry: loadProbes
                });
            } else {
                tableBody.innerHTML = `<tr><td colspan="6" class="text-center">Error al obtener evaluaciones sintéticas.</td></tr>`;
            }
        }
    }

    const btnRefreshProbes = document.getElementById("btn-refresh-probes");
    if (btnRefreshProbes) btnRefreshProbes.addEventListener("click", loadProbes);

    // LOAD AUDIT LOGS TABLE WITH 12-STATE MACHINE
    async function loadAuditLogs() {
        const tableBody = document.getElementById("audit-table-body");
        if (!tableBody) return;

        if (window.GestivaLayout) {
            window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADING, { type: 'table', colCount: 5, rowCount: 3 });
        }

        try {
            const response = await fetch(AUDIT_API_URL, { headers: getHeaders() });
            const logs = await response.json();

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) {
                    if (window.GestivaLayout) {
                        window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.PERMISSION_DENIED, { roleRequired: "SOC_ANALYST" });
                    }
                    return;
                }
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                        title: "ERROR DE AUDITORÍA",
                        message: "No se pudo recuperar el log de auditoría.",
                        onRetry: loadAuditLogs
                    });
                }
                return;
            }

            if (!logs || logs.length === 0) {
                if (window.GestivaLayout) {
                    window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.EMPTY, {
                        title: "TRAZA VACÍA",
                        message: "No hay registros de auditoría almacenados.",
                        icon: "fa-solid fa-shield-halved"
                    });
                } else {
                    tableBody.innerHTML = `<tr><td colspan="5" class="text-center">No hay registros de auditoría almacenados.</td></tr>`;
                }
                return;
            }

            tableBody.innerHTML = logs.map(l => `
                <tr>
                    <td>${new Date(l.timestamp).toLocaleString()}</td>
                    <td><span class="badge badge-warning">${l.action}</span></td>
                    <td>${l.actor_email}</td>
                    <td><code>${l.resource_type}:${l.resource_id}</code></td>
                    <td><code>${l.ip_address}</code></td>
                </tr>
            `).join('');

            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody, window.GestivaUIState.LOADED);
            }
        } catch (e) {
            if (window.GestivaLayout) {
                window.GestivaLayout.setState(tableBody.parentElement || tableBody, window.GestivaUIState.ERROR, {
                    title: "CONEXIÓN NO DISPONIBLE",
                    message: "Inicie sesión con credenciales válidas para acceder a la auditoría.",
                    onRetry: loadAuditLogs
                });
            } else {
                tableBody.innerHTML = `<tr><td colspan="5" class="text-center">Inicie sesión para acceder a la traza de auditoría.</td></tr>`;
            }
        }
    }

    const btnRefreshAudit = document.getElementById("btn-refresh-audit");
    if (btnRefreshAudit) btnRefreshAudit.addEventListener("click", loadAuditLogs);

    // MODULE 1: MODAL CLOSING FIX & ASSET REGISTRATION HANDLERS
    const loginModal = document.getElementById("login-modal");
    const assetModal = document.getElementById("asset-modal");

    const btnOpenLoginModal = document.getElementById("btn-open-login-modal");
    const btnCloseLoginModal = document.getElementById("btn-close-login-modal");
    const btnCancelLoginModal = document.getElementById("btn-cancel-login-modal");

    const btnOpenAssetModal = document.getElementById("btn-open-asset-modal");
    const btnCloseAssetModal = document.getElementById("btn-close-asset-modal");
    const btnCancelAssetModal = document.getElementById("btn-cancel-asset-modal");
    const formCreateAsset = document.getElementById("form-create-asset");

    function closeAllModals() {
        if (loginModal) loginModal.classList.remove("active");
        if (assetModal) assetModal.classList.remove("active");
    }

    if (btnOpenLoginModal) btnOpenLoginModal.addEventListener("click", () => loginModal?.classList.add("active"));
    if (btnCloseLoginModal) btnCloseLoginModal.addEventListener("click", closeAllModals);
    if (btnCancelLoginModal) btnCancelLoginModal.addEventListener("click", closeAllModals);

    if (btnOpenAssetModal) btnOpenAssetModal.addEventListener("click", () => assetModal?.classList.add("active"));
    if (btnCloseAssetModal) btnCloseAssetModal.addEventListener("click", closeAllModals);
    if (btnCancelAssetModal) btnCancelAssetModal.addEventListener("click", closeAllModals);

    // ESCAPE KEY CLOSES ALL MODALS
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" || e.keyCode === 27) {
            closeAllModals();
        }
    });

    // CREATE ASSET FORM SUBMISSION
    if (formCreateAsset) {
        formCreateAsset.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("asset-name").value.trim();
            const target_url = document.getElementById("asset-url").value.trim();
            const criticality = document.getElementById("asset-criticality").value;
            const owner_email = document.getElementById("asset-owner").value.trim();
            const btnSubmit = formCreateAsset.querySelector("button[type='submit']");

            if (btnSubmit) {
                btnSubmit.disabled = true;
                btnSubmit.textContent = "Registrando...";
            }

            try {
                const response = await fetch(ASSETS_API_URL, {
                    method: "POST",
                    headers: getHeaders(),
                    body: JSON.stringify({ name, target_url, criticality, owner_email })
                });
                const result = await response.json();
                if (!response.ok) throw new Error(result.detail || "Error al registrar activo.");

                showToast(`Activo ${result.name} registrado exitosamente.`, "success");
                closeAllModals();
                formCreateAsset.reset();
                loadAssets();
            } catch (err) {
                showToast(err.message, "error");
            } finally {
                if (btnSubmit) {
                    btnSubmit.disabled = false;
                    btnSubmit.textContent = "Registrar Activo";
                }
            }
        });
    }

    // LOGIN & LOGOUT HANDLERS
    const formLogin = document.getElementById("form-login");
    const btnLogout = document.getElementById("btn-logout");

    if (formLogin) {
        formLogin.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("login-email").value.trim();
            const password = document.getElementById("login-password").value;

            try {
                const response = await fetch(`${AUTH_API_URL}/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });
                const result = await response.json();
                if (!response.ok) throw new Error(result.detail || "Error al autenticar.");

                setAuthToken(result.access_token);
                showToast(`Sesión iniciada exitosamente para ${result.email}`, "success");
                closeAllModals();
                checkAuthSession();
            } catch (err) {
                showToast(err.message, "error");
            }
        });
    }

    if (btnLogout) {
        btnLogout.addEventListener("click", async () => {
            try {
                await fetch(`${AUTH_API_URL}/logout`, { method: "POST", headers: getHeaders() });
            } catch (e) {}
            clearAuthToken();
            showToast("Sesión cerrada y token revocado.", "success");
            checkAuthSession();
        });
    }

    async function checkAuthSession() {
        const userEmailSpan = document.getElementById("user-email");
        const userRoleSpan = document.getElementById("user-role");
        const token = getAuthToken();

        if (!token) {
            if (userEmailSpan) userEmailSpan.textContent = "Sesión no iniciada";
            if (userRoleSpan) userRoleSpan.textContent = "INVITADO";
            if (btnOpenLoginModal) btnOpenLoginModal.style.display = "inline-flex";
            return;
        }

        try {
            const response = await fetch(`${AUTH_API_URL}/me`, { headers: getHeaders() });
            if (response.ok) {
                const user = await response.json();
                if (userEmailSpan) userEmailSpan.textContent = user.email;
                if (userRoleSpan) userRoleSpan.textContent = user.role;
                if (btnOpenLoginModal) btnOpenLoginModal.style.display = "none";
            } else {
                clearAuthToken();
                if (userEmailSpan) userEmailSpan.textContent = "Sesión no iniciada";
                if (userRoleSpan) userRoleSpan.textContent = "INVITADO";
                if (btnOpenLoginModal) btnOpenLoginModal.style.display = "inline-flex";
            }
        } catch (e) {
            clearAuthToken();
        }
    }

    // TOAST SYSTEM
    function showToast(message, type = "success") {
        const container = document.getElementById("toast-container");
        if (!container) return;
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    // INITIALIZATION & REAL-TIME POLLING LOOP
    initTrafficChart();
    checkAuthSession();
    updateSOCTelemetry();
    setInterval(updateSOCTelemetry, 3000); // Live polling every 3s
});
