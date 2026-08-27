/**
 * Gestiva Security (GestivaSec V1 Enterprise SOC Platform)
 * Master Layout Framework & 12 Mandatory Screen State Machine Engine
 * 
 * Spec Alignment:
 * - Documents/04_Governance/GESTIVASEC_UI_STATE_MACHINES.md
 * - Documents/03_Frontend/GESTIVASEC_FRONTEND_ARCHITECTURE_GUIDE.md
 * - Documents/03_Frontend/GESTIVASEC_UI_ANTI_PATTERNS.md
 * 
 * Mandatory 12 Screen States Enforced:
 * 1.  UNINITIALIZED         - Component before mount. Zero DOM rendering.
 * 2.  LOADING               - Skeleton loaders active across cards and tables (NO generic spinners).
 * 3.  LOADED                - Target data successfully rendered.
 * 4.  REFRESHING            - Background polling update in progress (subtle status indicator, grid untouched).
 * 5.  PARTIAL_FAILURE       - Secondary widget failed to load; primary grid operational with warning badge.
 * 6.  OFFLINE               - Backend unreachable; display topbar/header warning badge, preserve view state.
 * 7.  ERROR                 - Full API failure; render clean error container with manual [ Retry Query ] button.
 * 8.  EMPTY                 - Query returned 0 records; custom domain empty illustration & action button.
 * 9.  READ_ONLY             - User has view-only permissions; hide/disable mutation controls.
 * 10. PERMISSION_DENIED     - RBAC access denied container with request access option.
 * 11. REALTIME_CONNECTED    - Polling active every 3s; green connectivity indicator in footer/topbar.
 * 12. REALTIME_RECONNECTING - Network reconnect loop active; orange reconnecting badge in footer/topbar.
 */

// 1. MANDATORY 12 SCREEN STATES CONSTANT REGISTRY
const GestivaUIState = Object.freeze({
    UNINITIALIZED: 'UNINITIALIZED',
    LOADING: 'LOADING',
    LOADED: 'LOADED',
    REFRESHING: 'REFRESHING',
    PARTIAL_FAILURE: 'PARTIAL_FAILURE',
    OFFLINE: 'OFFLINE',
    ERROR: 'ERROR',
    EMPTY: 'EMPTY',
    READ_ONLY: 'READ_ONLY',
    PERMISSION_DENIED: 'PERMISSION_DENIED',
    REALTIME_CONNECTED: 'REALTIME_CONNECTED',
    REALTIME_RECONNECTING: 'REALTIME_RECONNECTING'
});

// 2. MASTER LAYOUT & STATE MACHINE ENGINE
class GestivaLayoutManager {
    constructor() {
        this.containerStates = new WeakMap();
        this.realtimeState = GestivaUIState.REALTIME_CONNECTED;
        this.userRole = 'SOC_ADMIN'; // Default RBAC role
        this.alarmActive = false;
        this.registeredRetries = new Map();
        
        // Auto-initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initLayout());
        } else {
            this.initLayout();
        }
    }

    /**
     * Initializes global status indicators, telemetry counters, and DOM hooks
     */
    initLayout() {
        this.ensureTelemetryStatusBar();
        this.applyRBAC(this.userRole);
    }

    /**
     * Enforces explicit state transition for a given DOM container/element
     * @param {HTMLElement|string} target - Container element or selector
     * @param {string} state - One of GestivaUIState enum values
     * @param {Object} options - Custom parameters (onRetry, onAction, title, message, colCount, etc.)
     */
    setState(target, state, options = {}) {
        const container = typeof target === 'string' ? document.querySelector(target) : target;
        if (!container) return;

        // Verify valid state
        if (!Object.values(GestivaUIState).includes(state)) {
            console.warn(`[GestivaLayout] Invalid screen state: ${state}`);
            return;
        }

        const prevState = this.containerStates.get(container) || GestivaUIState.UNINITIALIZED;
        this.containerStates.set(container, state);
        container.setAttribute('data-ui-state', state);

        switch (state) {
            case GestivaUIState.UNINITIALIZED:
                container.style.display = 'none';
                container.innerHTML = '';
                break;

            case GestivaUIState.LOADING:
                container.style.display = '';
                if (options.type === 'table' || container.tagName === 'TBODY' || container.querySelector('table')) {
                    this.renderSkeletonTable(container, options.colCount || 5, options.rowCount || 4);
                } else if (options.type === 'metrics' || container.classList.contains('metrics-grid')) {
                    this.renderSkeletonMetrics(container, options.count || 4);
                } else {
                    this.renderSkeletonCard(container);
                }
                break;

            case GestivaUIState.LOADED:
                container.style.display = '';
                container.classList.remove('state-loading', 'state-error');
                break;

            case GestivaUIState.REFRESHING:
                // Preserve existing content, show subtle polling activity badge in topbar/footer
                this.setRealtimeStatus(GestivaUIState.REFRESHING);
                break;

            case GestivaUIState.PARTIAL_FAILURE:
                // Show warning badge over container without destroying main content
                this.renderPartialFailureBadge(container, options.message || 'Falla parcial en componente secundario');
                break;

            case GestivaUIState.OFFLINE:
                this.setRealtimeStatus(GestivaUIState.OFFLINE);
                this.renderOfflineNotification(container);
                break;

            case GestivaUIState.ERROR:
                this.renderErrorState(container, {
                    title: options.title || 'FALLA EN PIPELINE DE TELEMETRÍA',
                    message: options.message || 'No se pudo obtener la información desde el servidor backend.',
                    onRetry: options.onRetry
                });
                break;

            case GestivaUIState.EMPTY:
                this.renderEmptyState(container, {
                    title: options.title || 'SIN REGISTROS DETECTADOS',
                    message: options.message || 'La consulta actual no devolvió resultados en la base de datos.',
                    icon: options.icon || 'fa-solid fa-folder-open',
                    actionText: options.actionText,
                    onAction: options.onAction
                });
                break;

            case GestivaUIState.READ_ONLY:
                this.applyReadOnlyMode(container);
                break;

            case GestivaUIState.PERMISSION_DENIED:
                this.renderPermissionDeniedState(container, {
                    roleRequired: options.roleRequired || 'SOC_ANALYST'
                });
                break;

            case GestivaUIState.REALTIME_CONNECTED:
                this.setRealtimeStatus(GestivaUIState.REALTIME_CONNECTED);
                break;

            case GestivaUIState.REALTIME_RECONNECTING:
                this.setRealtimeStatus(GestivaUIState.REALTIME_RECONNECTING);
                break;
        }

        // Fire custom state change event
        container.dispatchEvent(new CustomEvent('gestivaStateChange', {
            detail: { prevState, newState: state, options }
        }));
    }

    /**
     * 1. LOADING STATE: Renders Skeleton Loaders for Table Rows (NO generic spinners)
     */
    renderSkeletonTable(container, colCount = 5, rowCount = 4) {
        const tbody = container.tagName === 'TBODY' ? container : (container.querySelector('tbody') || container);
        let html = '';
        for (let r = 0; r < rowCount; r++) {
            html += `<tr class="skeleton-row">`;
            for (let c = 0; c < colCount; c++) {
                const widthClass = c === 0 ? 'full' : (c % 2 === 0 ? 'medium' : 'short');
                html += `<td><div class="skeleton-line ${widthClass}"></div></td>`;
            }
            html += `</tr>`;
        }
        tbody.innerHTML = html;
    }

    /**
     * 1. LOADING STATE: Renders Skeleton Cards for Metric Grids
     */
    renderSkeletonMetrics(container, count = 4) {
        let html = '';
        for (let i = 0; i < count; i++) {
            html += `
                <div class="metric-card glass skeleton-card">
                    <div class="skeleton-line short" style="height: 36px; width: 36px; border-radius: 8px; margin-bottom: 8px;"></div>
                    <div style="width: 100%;">
                        <div class="skeleton-line short" style="margin-bottom: 6px;"></div>
                        <div class="skeleton-line full" style="height: 22px;"></div>
                    </div>
                </div>
            `;
        }
        container.innerHTML = html;
    }

    /**
     * 1. LOADING STATE: Renders Skeleton Loader for General Container Card
     */
    renderSkeletonCard(container) {
        container.innerHTML = `
            <div class="skeleton-card glass" style="padding: 1.5rem;">
                <div class="skeleton-line medium" style="height: 20px; margin-bottom: 1rem;"></div>
                <div class="skeleton-line full" style="margin-bottom: 0.5rem;"></div>
                <div class="skeleton-line full" style="margin-bottom: 0.5rem;"></div>
                <div class="skeleton-line short"></div>
            </div>
        `;
    }

    /**
     * 2. LIVE TELEMETRY POLLING STATE: Updates Realtime Indicators (Top Bar & Footer)
     */
    setRealtimeStatus(state) {
        this.realtimeState = state;
        const statusBadge = document.getElementById('realtime-status-badge') || this.createRealtimeBadge();
        if (!statusBadge) return;

        statusBadge.className = 'realtime-badge';

        switch (state) {
            case GestivaUIState.REALTIME_CONNECTED:
                statusBadge.classList.add('connected');
                statusBadge.innerHTML = `<span class="realtime-dot"></span> LIVE POLLING 3S`;
                break;
            case GestivaUIState.REFRESHING:
                statusBadge.classList.add('connected');
                statusBadge.innerHTML = `<span class="realtime-dot" style="animation: pulse-dot 0.5s infinite;"></span> ACTUALIZANDO...`;
                break;
            case GestivaUIState.REALTIME_RECONNECTING:
                statusBadge.classList.add('reconnecting');
                statusBadge.innerHTML = `<span class="realtime-dot"></span> RECONECTANDO...`;
                break;
            case GestivaUIState.OFFLINE:
                statusBadge.classList.add('offline');
                statusBadge.innerHTML = `<span class="realtime-dot"></span> OFFLINE / PIPELINE CAÍDO`;
                break;
        }
    }

    /**
     * Creates status badge if missing in DOM
     */
    createRealtimeBadge() {
        const topbar = document.querySelector('.topbar-actions') || document.querySelector('.topbar');
        if (!topbar) return null;
        const badge = document.createElement('div');
        badge.id = 'realtime-status-badge';
        badge.className = 'realtime-badge connected';
        badge.innerHTML = `<span class="realtime-dot"></span> LIVE POLLING 3S`;
        topbar.prepend(badge);
        return badge;
    }

    /**
     * 3. EMPTY / NO RESULTS STATE: Custom Domain Illustration & Action Button
     */
    renderEmptyState(container, { title, message, icon, actionText, onAction }) {
        const containerId = container.id || `empty-${Math.random().toString(36).substr(2, 9)}`;
        container.id = containerId;

        container.innerHTML = `
            <div class="gestiva-empty-container">
                <div class="empty-icon"><i class="${icon || 'fa-solid fa-inbox'}"></i></div>
                <h3>${title || 'SIN REGISTROS DETECTADOS'}</h3>
                <p>${message || 'No se encontraron datos coincidentes para la organización activa.'}</p>
                ${actionText ? `<button class="btn btn-secondary btn-sm btn-empty-action" id="btn-action-${containerId}">${actionText}</button>` : ''}
            </div>
        `;

        if (actionText && typeof onAction === 'function') {
            const btn = container.querySelector(`#btn-action-${containerId}`);
            if (btn) btn.addEventListener('click', onAction);
        }
    }

    /**
     * 4. ERROR / PIPELINE DISCONNECT STATE: Render SOC Dark Error Container with manual [ Retry Query ]
     */
    renderErrorState(container, { title, message, onRetry }) {
        const containerId = container.id || `err-${Math.random().toString(36).substr(2, 9)}`;
        container.id = containerId;

        container.innerHTML = `
            <div class="gestiva-error-container">
                <div class="error-icon"><i class="fa-solid fa-triangle-exclamation"></i></div>
                <h3>${title || 'FALLA EN PIPELINE DE TELEMETRÍA'}</h3>
                <p>${message || 'Error de conexión con el backend de Gestiva Security.'}</p>
                <button class="btn btn-primary btn-sm btn-retry-query" id="btn-retry-${containerId}">
                    <i class="fa-solid fa-rotate-right"></i> [ Reintentar Consulta ]
                </button>
            </div>
        `;

        if (typeof onRetry === 'function') {
            const btn = container.querySelector(`#btn-retry-${containerId}`);
            if (btn) btn.addEventListener('click', () => {
                this.setState(container, GestivaUIState.LOADING);
                onRetry();
            });
        }
    }

    /**
     * Render Offline Notification Badge over current screen
     */
    renderOfflineNotification(container) {
        let existingBanner = container.querySelector('.gestiva-offline-banner');
        if (!existingBanner) {
            existingBanner = document.createElement('div');
            existingBanner.className = 'gestiva-offline-banner';
            existingBanner.style.cssText = `
                background: rgba(255, 0, 85, 0.15);
                border: 1px solid var(--danger);
                color: #fff;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 0.8rem;
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-family: var(--font-body);
            `;
            existingBanner.innerHTML = `<i class="fa-solid fa-wifi-slash" style="color:var(--danger)"></i> <span><strong>PIPELINE DESCONECTADO:</strong> Mostrando última información conocida.</span>`;
            container.prepend(existingBanner);
        }
    }

    /**
     * Render Partial Failure Badge
     */
    renderPartialFailureBadge(container, msg) {
        let badge = container.querySelector('.gestiva-partial-failure-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.className = 'gestiva-partial-failure-badge';
            badge.style.cssText = `
                background: rgba(255, 204, 0, 0.15);
                border: 1px solid var(--warning);
                color: var(--warning);
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 0.75rem;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 8px;
            `;
            badge.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> <span>${msg}</span>`;
            container.prepend(badge);
        }
    }

    /**
     * 5. HIGH-SEVERITY ALARM FLASH STATE (Subtle border glow on critical alert detection)
     * @param {boolean} active - True to activate subtle magenta/red glowing pulse border
     * @param {HTMLElement|string|null} targetElement - Target element or null for active critical widgets
     */
    setHighSeverityAlarm(active = true, targetElement = null) {
        this.alarmActive = active;
        const targets = targetElement 
            ? [typeof targetElement === 'string' ? document.querySelector(targetElement) : targetElement]
            : document.querySelectorAll('.cyber-card.critical, .metric-card.critical-card, #alert-card, #status-banner');

        targets.forEach(el => {
            if (!el) return;
            if (active) {
                el.classList.add('alarm-flash-critical');
            } else {
                el.classList.remove('alarm-flash-critical');
            }
        });
    }

    /**
     * 9. READ_ONLY STATE & RBAC ENFORCEMENT
     */
    applyReadOnlyMode(container = document.body) {
        const mutationControls = container.querySelectorAll('.btn-primary, [data-mutation="true"], .btn-probe, button[type="submit"]');
        mutationControls.forEach(btn => {
            btn.style.display = 'none';
            btn.setAttribute('disabled', 'true');
        });

        const badge = document.createElement('span');
        badge.className = 'read-only-badge';
        badge.textContent = 'MODO LECTURA (READ-ONLY)';
        const header = container.querySelector('.card-header') || container;
        if (header && !header.querySelector('.read-only-badge')) {
            header.appendChild(badge);
        }
    }

    /**
     * 10. PERMISSION DENIED STATE
     */
    renderPermissionDeniedState(container, { roleRequired }) {
        container.innerHTML = `
            <div class="gestiva-permission-container">
                <div style="font-size: 2.5rem; color: var(--warning); margin-bottom: 0.5rem;">
                    <i class="fa-solid fa-user-lock"></i>
                </div>
                <h3 style="font-family: var(--font-heading); color: var(--text-main); font-size: 1.2rem;">ACCESO RESTRINGIDO POR RBAC</h3>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.4rem;">
                    Su rol actual no posee permisos para ver esta sección. Permiso requerido: <code>${roleRequired}</code>.
                </p>
                <button class="btn btn-secondary btn-sm" style="margin-top: 1rem;" onclick="alert('Solicitud de elevación de privilegios enviada al SOC Admin.')">
                    <i class="fa-solid fa-key"></i> Solicitar Elevación de Privilegios
                </button>
            </div>
        `;
    }

    /**
     * Global telemetry status bar in footer
     */
    ensureTelemetryStatusBar() {
        const footer = document.querySelector('footer');
        if (footer && !document.getElementById('layout-telemetry-bar')) {
            const bar = document.createElement('div');
            bar.id = 'layout-telemetry-bar';
            bar.style.cssText = `
                margin-top: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 15px;
                font-family: var(--font-mono, monospace);
                font-size: 0.7rem;
                color: var(--text-muted);
            `;
            bar.innerHTML = `
                <span>STATE ENGINE: <strong style="color:var(--primary)">12-STATE ACTIVE</strong></span>
                <span>|</span>
                <span>SECURITY LEVEL: <strong style="color:var(--success)">SOC V1 COMPLIANT</strong></span>
            `;
            footer.appendChild(bar);
        }
    }
}

// Instantiate Global Master Layout Instance
window.GestivaUIState = GestivaUIState;
window.GestivaLayout = new GestivaLayoutManager();
