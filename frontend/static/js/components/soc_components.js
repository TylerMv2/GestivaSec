/**
 * GESTIVA SECURITY (GESTIVASEC V1 ENTERPRISE SOC PLATFORM)
 * Re-usable Atomic UI Components for SOC Operations
 *
 * Strict Compliance:
 * - ARB-0016 Architecture Freeze Directive
 * - GESTIVASEC_FRONTEND_ARCHITECTURE_GUIDE.md
 * - GESTIVASEC_DESIGN_HANDOFF.md
 * - GESTIVASEC_UI_ANTI_PATTERNS.md
 *
 * Components:
 * 1. RealTimeTelemetryStreamWidget (3s polling visual refresh, zero layout shift)
 * 2. AssetUUIDIntelligenceCard (displays ip_history, OS fingerprint, status machine)
 * 3. EventLogViewerTable (column sorting, quick filtering, raw GES JSON inspector drawer)
 * 4. ThreatSeverityBadges & IncidentResponseActions (Contain, Quarantine confirmation, Dismiss)
 * 5. CommandPalette (Ctrl+K shortcut instant asset/IP/alert/log search)
 */

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof exports === 'object') {
        module.exports = factory();
    } else {
        root.SOCComponents = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    // Global Component Styles Injection
    let stylesInjected = false;
    function injectComponentStyles() {
        if (stylesInjected || typeof document === 'undefined') return;
        const styleId = 'gestivasec-soc-component-styles';
        if (document.getElementById(styleId)) return;

        const css = `
        /* ==========================================================================
           GESTIVASEC SOC COMPONENTS STYLESHEET
           High-Density SOC Operational Dark Mode & Zero Layout Shift
           ========================================================================== */

        :root {
            --soc-bg-dark: #070913;
            --soc-bg-card: rgba(13, 20, 36, 0.85);
            --soc-bg-drawer: rgba(10, 15, 28, 0.96);
            --soc-border: rgba(0, 240, 255, 0.2);
            --soc-border-glow: rgba(0, 240, 255, 0.4);
            --soc-cyan: #00f0ff;
            --soc-magenta: #ff0055;
            --soc-purple: #c77dff;
            --soc-success: #00ff66;
            --soc-warning: #ffcc00;
            --soc-orange: #ff6600;
            --soc-text-main: #f3f4f6;
            --soc-text-muted: #8b9bb4;
            --soc-font-heading: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            --soc-font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        }

        /* 1. Real-Time Telemetry Stream Widget (Zero Layout Shift) */
        .soc-telemetry-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            width: 100%;
            contain: layout style;
        }

        .soc-telemetry-card {
            background: var(--soc-bg-card);
            border: 1px solid var(--soc-border);
            border-radius: 10px;
            padding: 1rem 1.25rem;
            min-height: 100px;
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
            position: relative;
            overflow: hidden;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            box-sizing: border-box;
        }

        .soc-telemetry-card:hover {
            border-color: var(--soc-cyan);
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.25);
        }

        .soc-telemetry-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .soc-telemetry-title {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            color: var(--soc-text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .soc-telemetry-icon {
            font-size: 1.1rem;
            color: var(--soc-cyan);
            opacity: 0.8;
        }

        .soc-telemetry-body {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            margin-top: 0.25rem;
        }

        .soc-telemetry-value {
            font-family: var(--soc-font-heading);
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff;
            font-variant-numeric: tabular-nums;
            letter-spacing: -0.5px;
            transition: color 0.3s ease;
        }

        .soc-telemetry-unit {
            font-size: 0.75rem;
            color: var(--soc-text-muted);
            font-weight: 500;
            margin-left: 0.25rem;
        }

        .soc-telemetry-status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.65rem;
            font-family: var(--soc-font-mono);
            padding: 0.15rem 0.5rem;
            border-radius: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }

        .soc-telemetry-status-badge.online {
            background: rgba(0, 255, 102, 0.12);
            color: var(--soc-success);
            border: 1px solid rgba(0, 255, 102, 0.3);
        }

        .soc-telemetry-status-badge.reconnecting {
            background: rgba(255, 204, 0, 0.12);
            color: var(--soc-warning);
            border: 1px solid rgba(255, 204, 0, 0.3);
        }

        .soc-telemetry-status-badge.offline {
            background: rgba(255, 0, 85, 0.12);
            color: var(--soc-magenta);
            border: 1px solid rgba(255, 0, 85, 0.3);
        }

        .soc-pulse-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }

        .soc-pulse-dot.online {
            background: var(--soc-success);
            box-shadow: 0 0 8px var(--soc-success);
            animation: socPulse 1.5s infinite;
        }

        .soc-pulse-dot.reconnecting {
            background: var(--soc-warning);
            box-shadow: 0 0 8px var(--soc-warning);
            animation: socPulse 0.8s infinite;
        }

        .soc-pulse-dot.offline {
            background: var(--soc-magenta);
            box-shadow: 0 0 8px var(--soc-magenta);
        }

        @keyframes socPulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(1.2); }
            100% { opacity: 1; transform: scale(1); }
        }

        .soc-telemetry-gauge-bar {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 0.4rem;
        }

        .soc-telemetry-gauge-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--soc-cyan), var(--soc-success));
            border-radius: 2px;
            transition: width 0.4s ease, background 0.3s ease;
        }

        .soc-telemetry-gauge-fill.warning {
            background: linear-gradient(90deg, var(--soc-warning), var(--soc-orange));
        }

        .soc-telemetry-gauge-fill.danger {
            background: linear-gradient(90deg, var(--soc-orange), var(--soc-magenta));
        }

        .soc-value-flash {
            animation: socFlash 0.5s ease-out;
        }

        @keyframes socFlash {
            0% { color: var(--soc-cyan); text-shadow: 0 0 10px var(--soc-cyan); }
            100% { color: #ffffff; text-shadow: none; }
        }

        /* 2. Asset UUID Intelligence Card */
        .soc-asset-card {
            background: var(--soc-bg-card);
            border: 1px solid var(--soc-border);
            border-radius: 12px;
            padding: 1.5rem;
            backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            color: var(--soc-text-main);
        }

        .soc-asset-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 1rem;
            margin-bottom: 1.25rem;
            gap: 1rem;
        }

        .soc-asset-uuid-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-family: var(--soc-font-mono);
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--soc-cyan);
            background: rgba(0, 240, 255, 0.08);
            border: 1px solid rgba(0, 240, 255, 0.3);
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            word-break: break-all;
        }

        .soc-copy-btn {
            background: none;
            border: none;
            color: var(--soc-text-muted);
            cursor: pointer;
            font-size: 0.85rem;
            transition: color 0.2s ease;
        }

        .soc-copy-btn:hover {
            color: var(--soc-cyan);
        }

        .soc-asset-details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .soc-asset-field-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--soc-text-muted);
            margin-bottom: 0.25rem;
        }

        .soc-asset-field-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: #ffffff;
        }

        .soc-asset-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.65rem;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .soc-status-DISCOVERED { background: rgba(199, 125, 255, 0.15); color: var(--soc-purple); border: 1px solid var(--soc-purple); }
        .soc-status-REGISTERED { background: rgba(0, 240, 255, 0.15); color: var(--soc-cyan); border: 1px solid var(--soc-cyan); }
        .soc-status-ACTIVE { background: rgba(0, 255, 102, 0.15); color: var(--soc-success); border: 1px solid var(--soc-success); }
        .soc-status-UNDER_MAINTENANCE { background: rgba(255, 204, 0, 0.15); color: var(--soc-warning); border: 1px solid var(--soc-warning); }
        .soc-status-ISOLATED { background: rgba(255, 0, 85, 0.2); color: var(--soc-magenta); border: 1px solid var(--soc-magenta); box-shadow: 0 0 10px rgba(255, 0, 85, 0.3); }
        .soc-status-DECOMMISSIONED { background: rgba(139, 155, 180, 0.15); color: var(--soc-text-muted); border: 1px solid var(--soc-text-muted); }

        .soc-ip-history-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
            margin-top: 0.75rem;
        }

        .soc-ip-history-table th {
            text-align: left;
            padding: 0.5rem;
            color: var(--soc-text-muted);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.7rem;
            text-transform: uppercase;
        }

        .soc-ip-history-table td {
            padding: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-family: var(--soc-font-mono);
        }

        /* 3. Event Log Viewer Table & Inspector Drawer */
        .soc-table-wrapper {
            background: var(--soc-bg-card);
            border: 1px solid var(--soc-border);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        }

        .soc-table-toolbar {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.25rem;
            background: rgba(0, 0, 0, 0.25);
            border-bottom: 1px solid var(--soc-border);
        }

        .soc-search-input {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--soc-border);
            border-radius: 6px;
            padding: 0.5rem 0.85rem;
            color: #ffffff;
            font-size: 0.85rem;
            outline: none;
            min-width: 240px;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .soc-search-input:focus {
            border-color: var(--soc-cyan);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.25);
        }

        .soc-select-filter {
            background: rgba(9, 13, 24, 0.9);
            border: 1px solid var(--soc-border);
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            color: #ffffff;
            font-size: 0.82rem;
            outline: none;
            cursor: pointer;
        }

        .soc-select-filter option {
            background: #090d18;
            color: #ffffff;
        }

        .soc-log-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        .soc-log-table th {
            padding: 0.85rem 1rem;
            text-align: left;
            color: var(--soc-text-muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--soc-border);
            background: rgba(0, 0, 0, 0.3);
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }

        .soc-log-table th:hover {
            color: var(--soc-cyan);
        }

        .soc-log-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            vertical-align: middle;
        }

        .soc-log-table tbody tr {
            transition: background 0.15s ease;
        }

        .soc-log-table tbody tr:hover {
            background: rgba(0, 240, 255, 0.04);
        }

        .soc-table-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 1.25rem;
            background: rgba(0, 0, 0, 0.25);
            border-top: 1px solid var(--soc-border);
            font-size: 0.8rem;
            color: var(--soc-text-muted);
        }

        /* Slide-Over Inspector Drawer (Context Preservation Rule AP-NAV-01) */
        .soc-drawer-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.65);
            backdrop-filter: blur(4px);
            z-index: 2000;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }

        .soc-drawer-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .soc-inspector-drawer {
            position: fixed;
            top: 0; right: -520px;
            width: 100%;
            max-width: 520px;
            height: 100vh;
            background: var(--soc-bg-drawer);
            border-left: 1px solid var(--soc-border);
            box-shadow: -10px 0 40px rgba(0, 0, 0, 0.6);
            z-index: 2001;
            display: flex;
            flex-direction: column;
            transition: right 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .soc-drawer-overlay.active .soc-inspector-drawer {
            right: 0;
        }

        .soc-drawer-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--soc-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.3);
        }

        .soc-drawer-title {
            font-family: var(--soc-font-heading);
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--soc-cyan);
        }

        .soc-drawer-close {
            background: none;
            border: none;
            color: var(--soc-text-muted);
            font-size: 1.4rem;
            cursor: pointer;
            transition: color 0.2s ease;
        }

        .soc-drawer-close:hover {
            color: var(--soc-magenta);
        }

        .soc-drawer-body {
            padding: 1.5rem;
            overflow-y: auto;
            flex-grow: 1;
        }

        .soc-json-viewer {
            background: rgba(5, 7, 15, 0.95);
            border: 1px solid var(--soc-border);
            border-radius: 8px;
            padding: 1rem;
            font-family: var(--soc-font-mono);
            font-size: 0.78rem;
            color: #00ffcc;
            overflow-x: auto;
            white-space: pre-wrap;
            line-height: 1.5;
        }

        /* 4. Threat Severity Badges & Response Actions */
        .soc-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 0.72rem;
            font-family: var(--soc-font-mono);
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .soc-badge-P1_CRITICAL, .soc-badge-CRITICAL {
            background: rgba(255, 0, 85, 0.15);
            color: var(--soc-magenta);
            border: 1px solid var(--soc-magenta);
            box-shadow: 0 0 8px rgba(255, 0, 85, 0.3);
        }

        .soc-badge-P2_HIGH, .soc-badge-HIGH {
            background: rgba(255, 102, 0, 0.15);
            color: var(--soc-orange);
            border: 1px solid var(--soc-orange);
        }

        .soc-badge-P3_MEDIUM, .soc-badge-MEDIUM {
            background: rgba(255, 204, 0, 0.15);
            color: var(--soc-warning);
            border: 1px solid var(--soc-warning);
        }

        .soc-badge-P4_LOW, .soc-badge-LOW, .soc-badge-INFO {
            background: rgba(0, 240, 255, 0.15);
            color: var(--soc-cyan);
            border: 1px solid var(--soc-cyan);
        }

        .soc-action-btn-group {
            display: inline-flex;
            gap: 0.5rem;
            align-items: center;
        }

        .soc-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            padding: 0.45rem 0.9rem;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid transparent;
            outline: none;
            user-select: none;
        }

        .soc-btn-contain {
            background: rgba(0, 240, 255, 0.1);
            color: var(--soc-cyan);
            border-color: rgba(0, 240, 255, 0.3);
        }

        .soc-btn-contain:hover {
            background: rgba(0, 240, 255, 0.25);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
        }

        .soc-btn-quarantine {
            background: rgba(255, 0, 85, 0.15);
            color: var(--soc-magenta);
            border-color: rgba(255, 0, 85, 0.4);
        }

        .soc-btn-quarantine:hover {
            background: rgba(255, 0, 85, 0.3);
            box-shadow: 0 0 12px rgba(255, 0, 85, 0.5);
        }

        .soc-btn-dismiss {
            background: rgba(139, 155, 180, 0.1);
            color: var(--soc-text-muted);
            border-color: rgba(139, 155, 180, 0.3);
        }

        .soc-btn-dismiss:hover {
            background: rgba(139, 155, 180, 0.2);
            color: #ffffff;
        }

        /* 5. Command Palette / Quick Search Modal */
        .soc-palette-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(3, 5, 12, 0.8);
            backdrop-filter: blur(16px);
            z-index: 3000;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding-top: 10vh;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s ease, visibility 0.2s ease;
        }

        .soc-palette-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .soc-palette-modal {
            width: 90%;
            max-width: 640px;
            background: rgba(12, 17, 32, 0.95);
            border: 1px solid var(--soc-cyan);
            border-radius: 14px;
            box-shadow: 0 0 40px rgba(0, 240, 255, 0.25), 0 20px 50px rgba(0,0,0,0.7);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transform: translateY(-10px) scale(0.98);
            transition: transform 0.2s ease;
        }

        .soc-palette-overlay.active .soc-palette-modal {
            transform: translateY(0) scale(1);
        }

        .soc-palette-search-box {
            display: flex;
            align-items: center;
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--soc-border);
            background: rgba(0, 0, 0, 0.3);
            gap: 0.75rem;
        }

        .soc-palette-search-icon {
            font-size: 1.2rem;
            color: var(--soc-cyan);
        }

        .soc-palette-input {
            flex-grow: 1;
            background: none;
            border: none;
            outline: none;
            color: #ffffff;
            font-family: var(--soc-font-heading);
            font-size: 1.1rem;
        }

        .soc-palette-shortcut-badge {
            font-family: var(--soc-font-mono);
            font-size: 0.7rem;
            color: var(--soc-text-muted);
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
        }

        .soc-palette-results {
            max-height: 380px;
            overflow-y: auto;
            padding: 0.5rem;
        }

        .soc-palette-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.15s ease;
        }

        .soc-palette-item:hover, .soc-palette-item.selected {
            background: rgba(0, 240, 255, 0.12);
        }

        .soc-palette-item-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .soc-palette-item-icon {
            width: 32px;
            height: 32px;
            border-radius: 6px;
            background: rgba(0, 240, 255, 0.1);
            color: var(--soc-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
        }

        .soc-palette-item-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #ffffff;
        }

        .soc-palette-item-sub {
            font-size: 0.75rem;
            color: var(--soc-text-muted);
        }

        .soc-palette-footer {
            padding: 0.65rem 1.25rem;
            background: rgba(0, 0, 0, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.72rem;
            color: var(--soc-text-muted);
        }

        /* Modal Overlay for Action Confirmations (AP-NTF-02) */
        .soc-modal-backdrop {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            z-index: 3500;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.25s ease, visibility 0.25s ease;
        }

        .soc-modal-backdrop.active {
            opacity: 1;
            visibility: visible;
        }

        .soc-modal-dialog {
            background: var(--soc-bg-card);
            border: 1px solid var(--soc-magenta);
            border-radius: 12px;
            width: 90%;
            max-width: 460px;
            padding: 1.5rem;
            box-shadow: 0 0 30px rgba(255, 0, 85, 0.3);
            color: #ffffff;
        }

        .soc-modal-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            color: var(--soc-magenta);
        }

        .soc-modal-title {
            font-family: var(--soc-font-heading);
            font-size: 1.1rem;
            font-weight: 700;
        }

        .soc-modal-body {
            font-size: 0.88rem;
            color: var(--soc-text-main);
            margin-bottom: 1.5rem;
            line-height: 1.5;
        }

        .soc-modal-footer {
            display: flex;
            justify-content: flex-end;
            gap: 0.75rem;
        }
        `;

        const styleEl = document.createElement('style');
        styleEl.id = styleId;
        styleEl.innerHTML = css;
        document.head.appendChild(styleEl);
        stylesInjected = true;
    }

    // Initialize styles immediately upon script load
    injectComponentStyles();

    // Helper: Organization Header Retrieval
    function getOrgHeader() {
        if (typeof document !== 'undefined') {
            const orgInput = document.getElementById('select-organization');
            if (orgInput && orgInput.value) return orgInput.value;
        }
        return '00000000-0000-0000-0000-000000000001';
    }

    // Helper: Safe HTML escape
    function escapeHtml(str) {
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    /* ==========================================================================
       COMPONENT 1: Real-Time Telemetry Stream Widget
       (3s Polling Refresh, Zero Layout Shift, Visual Indicators)
       ========================================================================== */
    class RealTimeTelemetryStreamWidget {
        constructor(containerId, options = {}) {
            this.container = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
            this.options = Object.assign({
                endpoint: '/api/v1/soc/dashboard/telemetry',
                pollingIntervalMs: 3000,
                onDataUpdate: null,
                onError: null
            }, options);

            this.timer = null;
            this.status = 'reconnecting'; // 'online', 'reconnecting', 'offline'
            this.consecutiveFailures = 0;
            this.lastData = null;

            if (this.container) {
                this.initLayout();
            }
        }

        initLayout() {
            this.container.classList.add('soc-telemetry-container');
            this.container.innerHTML = `
                <div class="soc-telemetry-card" id="soc-widget-card-eps">
                    <div class="soc-telemetry-header">
                        <span class="soc-telemetry-title">Event Ingestion (EPS)</span>
                        <i class="fa-solid fa-bolt soc-telemetry-icon"></i>
                    </div>
                    <div class="soc-telemetry-body">
                        <span class="soc-telemetry-value" id="soc-val-eps">--</span>
                        <span class="soc-telemetry-status-badge reconnecting" id="soc-badge-status">
                            <span class="soc-pulse-dot reconnecting" id="soc-dot-status"></span>
                            <span id="soc-txt-status">CONNECTING</span>
                        </span>
                    </div>
                    <div class="soc-telemetry-gauge-bar">
                        <div class="soc-telemetry-gauge-fill" id="soc-gauge-eps" style="width: 0%;"></div>
                    </div>
                </div>

                <div class="soc-telemetry-card" id="soc-widget-card-hosts">
                    <div class="soc-telemetry-header">
                        <span class="soc-telemetry-title">Hosts Online / Total</span>
                        <i class="fa-solid fa-server soc-telemetry-icon"></i>
                    </div>
                    <div class="soc-telemetry-body">
                        <div>
                            <span class="soc-telemetry-value" id="soc-val-hosts-online">--</span>
                            <span class="soc-telemetry-unit" id="soc-val-hosts-total">/ --</span>
                        </div>
                    </div>
                    <div class="soc-telemetry-gauge-bar">
                        <div class="soc-telemetry-gauge-fill" id="soc-gauge-hosts" style="width: 0%;"></div>
                    </div>
                </div>

                <div class="soc-telemetry-card" id="soc-widget-card-alerts">
                    <div class="soc-telemetry-header">
                        <span class="soc-telemetry-title">Critical Alerts (P1/P2)</span>
                        <i class="fa-solid fa-triangle-exclamation soc-telemetry-icon" style="color:var(--soc-magenta);"></i>
                    </div>
                    <div class="soc-telemetry-body">
                        <span class="soc-telemetry-value" id="soc-val-alerts" style="color:var(--soc-magenta);">--</span>
                    </div>
                    <div class="soc-telemetry-gauge-bar">
                        <div class="soc-telemetry-gauge-fill danger" id="soc-gauge-alerts" style="width: 0%;"></div>
                    </div>
                </div>

                <div class="soc-telemetry-card" id="soc-widget-card-cpu">
                    <div class="soc-telemetry-header">
                        <span class="soc-telemetry-title">SOC Infra CPU Load</span>
                        <i class="fa-solid fa-microchip soc-telemetry-icon"></i>
                    </div>
                    <div class="soc-telemetry-body">
                        <span class="soc-telemetry-value" id="soc-val-cpu">--%</span>
                    </div>
                    <div class="soc-telemetry-gauge-bar">
                        <div class="soc-telemetry-gauge-fill" id="soc-gauge-cpu" style="width: 0%;"></div>
                    </div>
                </div>
            `;
        }

        async fetchTelemetry() {
            try {
                const response = await fetch(this.options.endpoint, {
                    headers: {
                        'Accept': 'application/json',
                        'X-Organization-ID': getOrgHeader()
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP Error ${response.status}`);
                }

                const data = await response.json();
                this.consecutiveFailures = 0;
                this.updateStatus('online', 'LIVE (3s)');
                this.updateValues(data);
                this.lastData = data;

                if (typeof this.options.onDataUpdate === 'function') {
                    this.options.onDataUpdate(data);
                }
            } catch (err) {
                this.consecutiveFailures++;
                if (this.consecutiveFailures > 2) {
                    this.updateStatus('offline', 'OFFLINE');
                } else {
                    this.updateStatus('reconnecting', 'RECONNECTING');
                }

                if (typeof this.options.onError === 'function') {
                    this.options.onError(err);
                }
            }
        }

        updateStatus(statusClass, labelText) {
            const badge = document.getElementById('soc-badge-status');
            const dot = document.getElementById('soc-dot-status');
            const txt = document.getElementById('soc-txt-status');

            if (!badge || !dot || !txt) return;

            badge.className = `soc-telemetry-status-badge ${statusClass}`;
            dot.className = `soc-pulse-dot ${statusClass}`;
            txt.textContent = labelText;
        }

        updateValues(data) {
            // Update values without layout shift
            const epsVal = document.getElementById('soc-val-eps');
            const hostsOnline = document.getElementById('soc-val-hosts-online');
            const hostsTotal = document.getElementById('soc-val-hosts-total');
            const alertsVal = document.getElementById('soc-val-alerts');
            const cpuVal = document.getElementById('soc-val-cpu');

            const gaugeEps = document.getElementById('soc-gauge-eps');
            const gaugeHosts = document.getElementById('soc-gauge-hosts');
            const gaugeAlerts = document.getElementById('soc-gauge-alerts');
            const gaugeCpu = document.getElementById('soc-gauge-cpu');

            if (epsVal && data.events_per_minute !== undefined) {
                const eps = Math.round(data.events_per_minute / 60);
                epsVal.textContent = eps.toLocaleString();
                epsVal.classList.add('soc-value-flash');
                setTimeout(() => epsVal.classList.remove('soc-value-flash'), 500);

                const epsPct = Math.min(100, Math.max(5, (eps / 500) * 100));
                if (gaugeEps) gaugeEps.style.width = `${epsPct}%`;
            }

            if (hostsOnline && hostsTotal && data.hosts_online !== undefined) {
                hostsOnline.textContent = data.hosts_online;
                hostsTotal.textContent = `/ ${data.total_hosts || data.hosts_online}`;
                const hostPct = data.total_hosts ? (data.hosts_online / data.total_hosts) * 100 : 100;
                if (gaugeHosts) gaugeHosts.style.width = `${hostPct}%`;
            }

            if (alertsVal && data.critical_alerts_count !== undefined) {
                alertsVal.textContent = data.critical_alerts_count;
                const alertPct = Math.min(100, (data.critical_alerts_count / 20) * 100);
                if (gaugeAlerts) gaugeAlerts.style.width = `${alertPct}%`;
            }

            if (cpuVal && data.cpu_usage_pct !== undefined) {
                cpuVal.textContent = `${Math.round(data.cpu_usage_pct)}%`;
                if (gaugeCpu) {
                    gaugeCpu.style.width = `${data.cpu_usage_pct}%`;
                    if (data.cpu_usage_pct > 85) gaugeCpu.className = 'soc-telemetry-gauge-fill danger';
                    else if (data.cpu_usage_pct > 65) gaugeCpu.className = 'soc-telemetry-gauge-fill warning';
                    else gaugeCpu.className = 'soc-telemetry-gauge-fill';
                }
            }
        }

        start() {
            this.fetchTelemetry();
            this.timer = setInterval(() => this.fetchTelemetry(), this.options.pollingIntervalMs);
        }

        stop() {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        }

        destroy() {
            this.stop();
            if (this.container) this.container.innerHTML = '';
        }
    }

    /* ==========================================================================
       COMPONENT 2: Asset UUID Intelligence Card
       (Primary UUID Identity, Forensic IP History, OS Fingerprint, Lifecycle State)
       ========================================================================== */
    class AssetUUIDIntelligenceCard {
        static render(assetData, containerOrElement) {
            const data = Object.assign({
                asset_uuid: 'ast_00000000-0000-0000-0000-000000000000',
                name: 'Unknown Security Asset',
                os_fingerprint: 'Linux Kernel 6.5.0-35-generic x86_64',
                status: 'ACTIVE',
                criticality: 'HIGH',
                risk_score: 45,
                organization_id: getOrgHeader(),
                ip_history: [
                    { ip: '192.168.1.105', interface: 'eth0', allocated_at: '2026-07-26T10:00:00Z', active: true },
                    { ip: '10.0.4.12', interface: 'vnic0', allocated_at: '2026-07-20T08:30:00Z', active: false }
                ]
            }, assetData);

            const statusClass = `soc-status-${data.status}`;

            const html = `
            <div class="soc-asset-card">
                <div class="soc-asset-header">
                    <div>
                        <div style="font-size: 0.72rem; color: var(--soc-text-muted); text-transform: uppercase; letter-spacing: 0.5px;">GESTIVASEC ASSET IDENTITY</div>
                        <h3 style="font-family: var(--soc-font-heading); font-size: 1.25rem; font-weight: 700; margin-top: 0.2rem; color: #ffffff;">${escapeHtml(data.name)}</h3>
                    </div>
                    <span class="soc-asset-status-pill ${statusClass}">
                        <i class="fa-solid fa-circle" style="font-size: 0.5rem;"></i> ${escapeHtml(data.status)}
                    </span>
                </div>

                <div style="margin-bottom: 1.25rem;">
                    <div class="soc-asset-field-label">PRIMARY IMMUTABLE KEY (ASSET UUID)</div>
                    <div class="soc-asset-uuid-badge">
                        <span>${escapeHtml(data.asset_uuid)}</span>
                        <button class="soc-copy-btn" onclick="navigator.clipboard.writeText('${data.asset_uuid}')" title="Copy UUID">
                            <i class="fa-regular fa-copy"></i>
                        </button>
                    </div>
                </div>

                <div class="soc-asset-details-grid">
                    <div>
                        <div class="soc-asset-field-label">OS FINGERPRINT</div>
                        <div class="soc-asset-field-value" style="font-size:0.85rem;"><i class="fa-brands fa-linux" style="color:var(--soc-cyan);"></i> ${escapeHtml(data.os_fingerprint)}</div>
                    </div>
                    <div>
                        <div class="soc-asset-field-label">CRITICALITY</div>
                        <div class="soc-asset-field-value"><span class="soc-badge soc-badge-${data.criticality}">${escapeHtml(data.criticality)}</span></div>
                    </div>
                    <div>
                        <div class="soc-asset-field-label">EXPOSURE RISK SCORE</div>
                        <div class="soc-asset-field-value" style="color: ${data.risk_score > 70 ? 'var(--soc-magenta)' : data.risk_score > 40 ? 'var(--soc-warning)' : 'var(--soc-success)'}">
                            ${data.risk_score} / 100
                        </div>
                    </div>
                </div>

                <div>
                    <div class="soc-asset-field-label" style="margin-bottom: 0.5rem;"><i class="fa-solid fa-clock-rotate-left"></i> FORENSIC IP HISTORY LOG (ip_history)</div>
                    <table class="soc-ip-history-table">
                        <thead>
                            <tr>
                                <th>IP Address</th>
                                <th>Interface</th>
                                <th>Allocated Timestamp</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${(data.ip_history || []).map(ip => `
                                <tr>
                                    <td style="color: var(--soc-cyan);">${escapeHtml(ip.ip)}</td>
                                    <td>${escapeHtml(ip.interface || 'eth0')}</td>
                                    <td>${escapeHtml(new Date(ip.allocated_at).toLocaleString())}</td>
                                    <td>
                                        <span style="font-size:0.7rem; color:${ip.active ? 'var(--soc-success)' : 'var(--soc-text-muted)'}">
                                            ${ip.active ? '● ACTIVE' : '○ HISTORICAL'}
                                        </span>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
            `;

            if (typeof containerOrElement === 'string') {
                const target = document.getElementById(containerOrElement);
                if (target) target.innerHTML = html;
            } else if (containerOrElement && containerOrElement.appendChild) {
                containerOrElement.innerHTML = html;
            }

            return html;
        }
    }

    /* ==========================================================================
       COMPONENT 3: Event Log Viewer Table & Raw GES JSON Inspector Drawer
       (Column Sorting, Quick Filtering, Sliding Inspector Panel)
       ========================================================================== */
    class EventLogViewerTable {
        constructor(containerId, options = {}) {
            this.container = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
            this.options = Object.assign({
                events: [],
                onRowClick: null,
                pageSize: 10
            }, options);

            this.events = this.options.events;
            this.filteredEvents = [...this.events];
            this.sortColumn = 'timestamp';
            this.sortAscending = false;
            this.currentPage = 1;
            this.searchQuery = '';
            this.selectedSeverity = 'ALL';
            this.selectedCategory = 'ALL';

            if (this.container) {
                this.initDrawer();
                this.render();
            }
        }

        initDrawer() {
            let drawerOverlay = document.getElementById('soc-global-inspector-drawer-overlay');
            if (!drawerOverlay) {
                drawerOverlay = document.createElement('div');
                drawerOverlay.id = 'soc-global-inspector-drawer-overlay';
                drawerOverlay.className = 'soc-drawer-overlay';
                drawerOverlay.innerHTML = `
                    <div class="soc-inspector-drawer">
                        <div class="soc-drawer-header">
                            <div class="soc-drawer-title"><i class="fa-solid fa-code"></i> GES Normalization Inspector</div>
                            <button class="soc-drawer-close" onclick="SOCComponents.EventLogViewerTable.closeDrawer()">&times;</button>
                        </div>
                        <div class="soc-drawer-body">
                            <div style="margin-bottom: 1rem; font-size: 0.8rem; color: var(--soc-text-muted);">
                                Standardized GestivaSec Event Schema (GES) JSON Payload:
                            </div>
                            <pre class="soc-json-viewer" id="soc-drawer-json-content">Select an event row to inspect payload...</pre>
                            <div style="margin-top: 1.25rem; display: flex; gap: 0.75rem;">
                                <button class="soc-btn soc-btn-contain" onclick="SOCComponents.EventLogViewerTable.copyDrawerJson()">
                                    <i class="fa-regular fa-copy"></i> Copy GES JSON
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                document.body.appendChild(drawerOverlay);

                drawerOverlay.addEventListener('click', (e) => {
                    if (e.target === drawerOverlay) {
                        SOCComponents.EventLogViewerTable.closeDrawer();
                    }
                });
            }
        }

        static openDrawer(gesJsonObj) {
            const overlay = document.getElementById('soc-global-inspector-drawer-overlay');
            const codeEl = document.getElementById('soc-drawer-json-content');
            if (overlay && codeEl) {
                codeEl.textContent = JSON.stringify(gesJsonObj, null, 2);
                overlay.classList.add('active');
            }
        }

        static closeDrawer() {
            const overlay = document.getElementById('soc-global-inspector-drawer-overlay');
            if (overlay) overlay.classList.remove('active');
        }

        static copyDrawerJson() {
            const codeEl = document.getElementById('soc-drawer-json-content');
            if (codeEl) {
                navigator.clipboard.writeText(codeEl.textContent);
            }
        }

        setEvents(newEvents) {
            this.events = newEvents || [];
            this.applyFilters();
        }

        applyFilters() {
            let result = [...this.events];

            if (this.searchQuery.trim()) {
                const q = this.searchQuery.toLowerCase();
                result = result.filter(ev => {
                    return (ev.category && ev.category.toLowerCase().includes(q)) ||
                           (ev.action && ev.action.toLowerCase().includes(q)) ||
                           (ev.source_ip && ev.source_ip.toLowerCase().includes(q)) ||
                           (ev.destination_asset_uuid && ev.destination_asset_uuid.toLowerCase().includes(q)) ||
                           (ev.payload && JSON.stringify(ev.payload).toLowerCase().includes(q));
                });
            }

            if (this.selectedSeverity !== 'ALL') {
                result = result.filter(ev => ev.severity === this.selectedSeverity);
            }

            if (this.selectedCategory !== 'ALL') {
                result = result.filter(ev => ev.category === this.selectedCategory);
            }

            // Sort
            result.sort((a, b) => {
                let valA = a[this.sortColumn] || '';
                let valB = b[this.sortColumn] || '';
                if (valA < valB) return this.sortAscending ? -1 : 1;
                if (valA > valB) return this.sortAscending ? 1 : -1;
                return 0;
            });

            this.filteredEvents = result;
            this.currentPage = 1;
            this.renderTableBody();
        }

        handleSort(column) {
            if (this.sortColumn === column) {
                this.sortAscending = !this.sortAscending;
            } else {
                this.sortColumn = column;
                this.sortAscending = true;
            }
            this.applyFilters();
        }

        render() {
            this.container.className = 'soc-table-wrapper';

            const categories = Array.from(new Set(this.events.map(e => e.category).filter(Boolean)));

            this.container.innerHTML = `
                <div class="soc-table-toolbar">
                    <input type="text" class="soc-search-input" id="soc-table-search" placeholder="Search GES logs (IP, Action, Asset)...">
                    <div style="display:flex; gap:0.75rem; align-items:center;">
                        <select class="soc-select-filter" id="soc-table-filter-severity">
                            <option value="ALL">All Severities</option>
                            <option value="P1_CRITICAL">P1_CRITICAL</option>
                            <option value="P2_HIGH">P2_HIGH</option>
                            <option value="P3_MEDIUM">P3_MEDIUM</option>
                            <option value="P4_LOW">P4_LOW</option>
                        </select>
                        <select class="soc-select-filter" id="soc-table-filter-category">
                            <option value="ALL">All Categories</option>
                            ${categories.map(c => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('')}
                        </select>
                    </div>
                </div>

                <div style="overflow-x: auto;">
                    <table class="soc-log-table">
                        <thead>
                            <tr>
                                <th data-col="timestamp">Timestamp <i class="fa-solid fa-sort"></i></th>
                                <th data-col="severity">Severity <i class="fa-solid fa-sort"></i></th>
                                <th data-col="category">Category <i class="fa-solid fa-sort"></i></th>
                                <th data-col="action">Action <i class="fa-solid fa-sort"></i></th>
                                <th data-col="source_ip">Source IP</th>
                                <th data-col="destination_asset_uuid">Destination Asset UUID</th>
                                <th>Inspect GES</th>
                            </tr>
                        </thead>
                        <tbody id="soc-log-table-body">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>

                <div class="soc-table-footer">
                    <div id="soc-table-pagination-info">Showing 0-0 of 0 logs</div>
                    <div style="display:flex; gap:0.5rem;">
                        <button class="soc-btn soc-btn-dismiss" id="soc-table-prev-btn"><i class="fa-solid fa-chevron-left"></i> Prev</button>
                        <button class="soc-btn soc-btn-dismiss" id="soc-table-next-btn">Next <i class="fa-solid fa-chevron-right"></i></button>
                    </div>
                </div>
            `;

            // Bind Event Listeners
            const searchInput = this.container.querySelector('#soc-table-search');
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    this.searchQuery = e.target.value;
                    this.applyFilters();
                });
            }

            const severitySelect = this.container.querySelector('#soc-table-filter-severity');
            if (severitySelect) {
                severitySelect.addEventListener('change', (e) => {
                    this.selectedSeverity = e.target.value;
                    this.applyFilters();
                });
            }

            const categorySelect = this.container.querySelector('#soc-table-filter-category');
            if (categorySelect) {
                categorySelect.addEventListener('change', (e) => {
                    this.selectedCategory = e.target.value;
                    this.applyFilters();
                });
            }

            const headers = this.container.querySelectorAll('th[data-col]');
            headers.forEach(h => {
                h.addEventListener('click', () => {
                    this.handleSort(h.getAttribute('data-col'));
                });
            });

            const prevBtn = this.container.querySelector('#soc-table-prev-btn');
            const nextBtn = this.container.querySelector('#soc-table-next-btn');

            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    if (this.currentPage > 1) {
                        this.currentPage--;
                        this.renderTableBody();
                    }
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    const maxPage = Math.ceil(this.filteredEvents.length / this.options.pageSize) || 1;
                    if (this.currentPage < maxPage) {
                        this.currentPage++;
                        this.renderTableBody();
                    }
                });
            }

            this.renderTableBody();
        }

        renderTableBody() {
            const tbody = this.container.querySelector('#soc-log-table-body');
            const pageInfo = this.container.querySelector('#soc-table-pagination-info');
            if (!tbody) return;

            if (this.filteredEvents.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align:center; padding: 2rem; color: var(--soc-text-muted);">
                            <i class="fa-solid fa-folder-open" style="font-size: 1.5rem; margin-bottom: 0.5rem; display:block;"></i>
                            No GestivaSec GES events matched the active filters.
                        </td>
                    </tr>
                `;
                if (pageInfo) pageInfo.textContent = 'Showing 0-0 of 0 logs';
                return;
            }

            const startIdx = (this.currentPage - 1) * this.options.pageSize;
            const endIdx = Math.min(startIdx + this.options.pageSize, this.filteredEvents.length);
            const pageItems = this.filteredEvents.slice(startIdx, endIdx);

            if (pageInfo) {
                pageInfo.textContent = `Showing ${startIdx + 1}-${endIdx} of ${this.filteredEvents.length} logs`;
            }

            tbody.innerHTML = pageItems.map((ev, index) => {
                const sevBadge = ThreatSeverityBadges.render(ev.severity || 'P4_LOW');
                const formattedTime = ev.timestamp ? new Date(ev.timestamp).toLocaleString() : '--';
                return `
                    <tr>
                        <td style="font-family:var(--soc-font-mono); font-size:0.78rem; color:var(--soc-text-muted);">${escapeHtml(formattedTime)}</td>
                        <td>${sevBadge}</td>
                        <td><span class="soc-badge" style="background:rgba(255,255,255,0.05); color:#fff;">${escapeHtml(ev.category || 'GENERAL')}</span></td>
                        <td style="font-weight:600; color:#fff;">${escapeHtml(ev.action || 'EVENT')}</td>
                        <td style="font-family:var(--soc-font-mono); color:var(--soc-cyan);">${escapeHtml(ev.source_ip || 'N/A')}</td>
                        <td style="font-family:var(--soc-font-mono); font-size:0.78rem;">${escapeHtml(ev.destination_asset_uuid || 'N/A')}</td>
                        <td>
                            <button class="soc-btn soc-btn-contain" style="padding:0.25rem 0.6rem; font-size:0.72rem;" onclick="SOCComponents.EventLogViewerTable.openDrawer(${escapeHtml(JSON.stringify(ev))})">
                                <i class="fa-solid fa-code"></i> Inspect JSON
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');
        }
    }

    /* ==========================================================================
       COMPONENT 4: Threat Severity Badges & Incident Response Action Buttons
       (Contain, Quarantine with Confirmation Modal, Dismiss)
       ========================================================================== */
    class ThreatSeverityBadges {
        static render(severity) {
            const sevUpper = (severity || 'P4_LOW').toUpperCase();
            let icon = 'fa-info-circle';
            if (sevUpper.includes('P1') || sevUpper.includes('CRITICAL')) icon = 'fa-triangle-exclamation';
            else if (sevUpper.includes('P2') || sevUpper.includes('HIGH')) icon = 'fa-shield-cat';
            else if (sevUpper.includes('P3') || sevUpper.includes('MEDIUM')) icon = 'fa-triangle-exclamation';

            return `
                <span class="soc-badge soc-badge-${escapeHtml(sevUpper)}">
                    <i class="fa-solid ${icon}"></i> ${escapeHtml(sevUpper)}
                </span>
            `;
        }
    }

    class IncidentResponseActions {
        static renderGroup(targetAssetUuid, callbacks = {}) {
            const uuidEscaped = escapeHtml(targetAssetUuid);
            return `
                <div class="soc-action-btn-group">
                    <button class="soc-btn soc-btn-contain" onclick="SOCComponents.IncidentResponseActions.handleContain('${uuidEscaped}')">
                        <i class="fa-solid fa-shield-halved"></i> Contain
                    </button>
                    <button class="soc-btn soc-btn-quarantine" onclick="SOCComponents.IncidentResponseActions.handleQuarantineModal('${uuidEscaped}')">
                        <i class="fa-solid fa-lock"></i> Quarantine Host
                    </button>
                    <button class="soc-btn soc-btn-dismiss" onclick="SOCComponents.IncidentResponseActions.handleDismiss('${uuidEscaped}')">
                        <i class="fa-solid fa-eye-slash"></i> Dismiss
                    </button>
                </div>
            `;
        }

        static handleContain(assetUuid) {
            alert(`[SOC CONTAINMENT ACTIVATED]\nAsset UUID: ${assetUuid}\nNetwork containment initiated cleanly.`);
        }

        static handleQuarantineModal(assetUuid) {
            // Mandatory Confirmation Modal enforcing AP-NTF-02
            let backdrop = document.getElementById('soc-quarantine-modal-backdrop');
            if (!backdrop) {
                backdrop = document.createElement('div');
                backdrop.id = 'soc-quarantine-modal-backdrop';
                backdrop.className = 'soc-modal-backdrop';
                document.body.appendChild(backdrop);
            }

            backdrop.innerHTML = `
                <div class="soc-modal-dialog">
                    <div class="soc-modal-header">
                        <i class="fa-solid fa-triangle-exclamation" style="font-size:1.4rem;"></i>
                        <div class="soc-modal-title">CONFIRM HOST QUARANTINE</div>
                    </div>
                    <div class="soc-modal-body">
                        Are you sure you want to execute full zero-trust network quarantine on Asset UUID:<br>
                        <strong style="color:var(--soc-cyan); font-family:var(--soc-font-mono); font-size:0.82rem;">${escapeHtml(assetUuid)}</strong>?<br><br>
                        <span style="color:var(--soc-magenta); font-weight:600;">Warning:</span> This operation will sever all active SSH and network traffic channels.
                    </div>
                    <div class="soc-modal-footer">
                        <button class="soc-btn soc-btn-dismiss" onclick="document.getElementById('soc-quarantine-modal-backdrop').classList.remove('active')">Cancel</button>
                        <button class="soc-btn soc-btn-quarantine" onclick="SOCComponents.IncidentResponseActions.executeQuarantine('${escapeHtml(assetUuid)}')">Confirm Quarantine</button>
                    </div>
                </div>
            `;

            backdrop.classList.add('active');
        }

        static executeQuarantine(assetUuid) {
            const backdrop = document.getElementById('soc-quarantine-modal-backdrop');
            if (backdrop) backdrop.classList.remove('active');
            alert(`[HOST ISOLATED SUCCESS]\nAsset UUID ${assetUuid} has been transitioned to ISOLATED state.`);
        }

        static handleDismiss(assetUuid) {
            alert(`[ALERT SUPPRESSED]\nFinding for Asset UUID ${assetUuid} dismissed by analyst.`);
        }
    }

    /* ==========================================================================
       COMPONENT 5: Command Palette / Quick Search Modal
       (Ctrl + K Keyboard Trigger, Instant Search across Assets/IPs/Alerts)
       ========================================================================== */
    class CommandPalette {
        constructor() {
            this.isOpen = false;
            this.selectedIndex = 0;
            this.items = [];
            this.initDOM();
            this.bindGlobalKeyboard();
        }

        initDOM() {
            if (document.getElementById('soc-command-palette-overlay')) return;

            const overlay = document.createElement('div');
            overlay.id = 'soc-command-palette-overlay';
            overlay.className = 'soc-palette-overlay';
            overlay.innerHTML = `
                <div class="soc-palette-modal">
                    <div class="soc-palette-search-box">
                        <i class="fa-solid fa-terminal soc-palette-search-icon"></i>
                        <input type="text" class="soc-palette-input" id="soc-palette-search-input" placeholder="Type a command, asset UUID, or IP address (e.g., 192.168...)" autocomplete="off">
                        <span class="soc-palette-shortcut-badge">ESC to Close</span>
                    </div>
                    <div class="soc-palette-results" id="soc-palette-results-list">
                        <!-- Populated dynamically -->
                    </div>
                    <div class="soc-palette-footer">
                        <div><i class="fa-solid fa-keyboard"></i> Use <strong>↑↓</strong> to navigate, <strong>Enter</strong> to select</div>
                        <div>GESTIVASEC SOC PALETTE v1.0</div>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) this.close();
            });

            const input = document.getElementById('soc-palette-search-input');
            if (input) {
                input.addEventListener('input', (e) => this.onSearch(e.target.value));
                input.addEventListener('keydown', (e) => this.onKeyDown(e));
            }
        }

        bindGlobalKeyboard() {
            document.addEventListener('keydown', (e) => {
                if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
                    e.preventDefault();
                    this.toggle();
                } else if (e.key === 'Escape' && this.isOpen) {
                    this.close();
                }
            });
        }

        toggle() {
            if (this.isOpen) this.close();
            else this.open();
        }

        open() {
            const overlay = document.getElementById('soc-command-palette-overlay');
            const input = document.getElementById('soc-palette-search-input');
            if (overlay && input) {
                overlay.classList.add('active');
                this.isOpen = true;
                input.value = '';
                input.focus();
                this.onSearch('');
            }
        }

        close() {
            const overlay = document.getElementById('soc-command-palette-overlay');
            if (overlay) {
                overlay.classList.remove('active');
                this.isOpen = false;
            }
        }

        onSearch(query) {
            const defaultItems = [
                { title: 'Navigate to Asset Inventory', sub: 'CMDB Master Grid', icon: 'fa-boxes-stacked', action: () => window.location.href = '/inventory' },
                { title: 'View Real-Time Telemetry Stream', sub: 'Operational Dashboard', icon: 'fa-gauge', action: () => window.location.href = '/' },
                { title: 'Inspect Normalized Event Logs (GES)', sub: 'SIEM & Event Pipelines', icon: 'fa-terminal', action: () => window.location.href = '/logs' },
                { title: 'View Active P1/P2 Threat Alerts', sub: 'Incident & Response Console', icon: 'fa-triangle-exclamation', action: () => window.location.href = '/alerts' },
                { title: 'Search Asset UUID ast_8f3a9b12...', sub: 'Digital Asset Intelligence', icon: 'fa-server', action: () => alert('Opening Asset UUID ast_8f3a9b12...') }
            ];

            if (!query.trim()) {
                this.items = defaultItems;
            } else {
                const q = query.toLowerCase();
                this.items = defaultItems.filter(item =>
                    item.title.toLowerCase().includes(q) || item.sub.toLowerCase().includes(q)
                );
                if (this.items.length === 0) {
                    this.items = [
                        { title: `Search logs for "${query}"`, sub: 'Execute Global Query', icon: 'fa-magnifying-glass', action: () => window.location.href = `/logs?search=${encodeURIComponent(query)}` }
                    ];
                }
            }

            this.selectedIndex = 0;
            this.renderResults();
        }

        onKeyDown(e) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.selectedIndex = (this.selectedIndex + 1) % Math.max(1, this.items.length);
                this.renderResults();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.selectedIndex = (this.selectedIndex - 1 + this.items.length) % Math.max(1, this.items.length);
                this.renderResults();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (this.items[this.selectedIndex] && typeof this.items[this.selectedIndex].action === 'function') {
                    this.items[this.selectedIndex].action();
                    this.close();
                }
            }
        }

        renderResults() {
            const listEl = document.getElementById('soc-palette-results-list');
            if (!listEl) return;

            listEl.innerHTML = this.items.map((item, idx) => `
                <div class="soc-palette-item ${idx === this.selectedIndex ? 'selected' : ''}" onclick="SOCComponents.CommandPalette.executeItem(${idx})">
                    <div class="soc-palette-item-left">
                        <div class="soc-palette-item-icon">
                            <i class="fa-solid ${item.icon}"></i>
                        </div>
                        <div>
                            <div class="soc-palette-item-title">${escapeHtml(item.title)}</div>
                            <div class="soc-palette-item-sub">${escapeHtml(item.sub)}</div>
                        </div>
                    </div>
                    <i class="fa-solid fa-chevron-right" style="font-size:0.75rem; color:var(--soc-text-muted);"></i>
                </div>
            `).join('');
        }

        static executeItem(index) {
            if (window.SOCComponentsInstance && window.SOCComponentsInstance.commandPalette) {
                const palette = window.SOCComponentsInstance.commandPalette;
                if (palette.items[index] && typeof palette.items[index].action === 'function') {
                    palette.items[index].action();
                    palette.close();
                }
            }
        }
    }

    // Export namespace
    const SOCComponents = {
        RealTimeTelemetryStreamWidget,
        AssetUUIDIntelligenceCard,
        EventLogViewerTable,
        ThreatSeverityBadges,
        IncidentResponseActions,
        CommandPalette,
        initCommandPalette: function () {
            if (!window.SOCComponentsInstance) window.SOCComponentsInstance = {};
            window.SOCComponentsInstance.commandPalette = new CommandPalette();
            return window.SOCComponentsInstance.commandPalette;
        }
    };

    // Automatically initialize command palette shortcut listener on DOM ready
    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => SOCComponents.initCommandPalette());
        } else {
            SOCComponents.initCommandPalette();
        }
    }

    return SOCComponents;
}));
