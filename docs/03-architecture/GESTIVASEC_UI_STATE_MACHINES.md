# GESTIVASEC_UI_STATE_MACHINES.md — UI STATE MACHINES & TRANSITION SPECIFICATION

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `APPROVED & LOCKED INTERACTION SPECIFICATION`  
**Target Audience:** Frontend Engineers, UI/UX Designers, QA Automation Engineers  
**Date:** 2026-07-26  

---

## 1. MANDATORY 12-STATE SCREEN INTERACTION MACHINE

Every screen module across Gestiva Security MUST implement explicit UI behavior for all 12 operational screen states:

```
                  +-------------------+
                  |  UNINITIALIZED    |
                  +-------------------+
                            ↓
                  +-------------------+
                  |     LOADING       |
                  +-------------------+
                   /        |        \
            (Error)      (Success)   (No Data)
             /              |              \
            v               v               v
  +------------------+ +-----------+ +------------+
  |  ERROR / RETRY   | |  LOADED   | |   EMPTY    |
  +------------------+ +-----------+ +------------+
                            |
                     (Live Update)
                            |
                            v
            +--------------------------------+
            |      REALTIME_CONNECTED        |
            +--------------------------------+
             /                              \
     (Network Loss)                    (Auth Loss)
           /                                  \
          v                                    v
+------------------------+          +--------------------+
| REALTIME_RECONNECTING  |          | PERMISSION_DENIED  |
+------------------------+          +--------------------+
```

### 1.1 Screen State Descriptions & UI Requirements
1. **`UNINITIALIZED`:** State before component mount. Zero DOM rendering.
2. **`LOADING`:** Skeleton loaders active across metric containers and table rows.
3. **`LOADED`:** Data successfully populated in view components.
4. **`REFRESHING`:** Background polling update in progress (subtle spinner in topbar; primary grid untouched).
5. **`PARTIAL_FAILURE`:** Secondary widget failed to load; primary grid remains operational with warning badge.
6. **`OFFLINE / DISCONNECTED`:** Backend unreachable; display top-right warning badge, preserve current screen state.
7. **`ERROR / RETRY`:** Full API failure; render clean error container with manual `[ Retry Query ]` button.
8. **`EMPTY`:** Query returned 0 records; render custom domain empty state illustration with action button.
9. **`READ_ONLY`:** User has view-only permissions; hide all mutation buttons and edit controls.
10. **`PERMISSION_DENIED`:** User lacks RBAC role; display access denied message with request access option.
11. **`REALTIME_CONNECTED`:** Polling active every 3s; green connectivity indicator in footer.
12. **`REALTIME_RECONNECTING`:** Network reconnect loop active; orange reconnecting badge in footer.

---

## 2. DOMAIN ENTITY STATE MACHINES & UI BEHAVIOR

### 2.1 Digital Asset (`DigitalAsset`) State Machine
$$\text{DISCOVERED} \longrightarrow \text{REGISTERED} \longrightarrow \text{ACTIVE} \rightleftharpoons \text{UNDER\_MAINTENANCE} \longrightarrow \text{ISOLATED} \longrightarrow \text{DECOMMISSIONED}$$

- **`DISCOVERED`:** Unpromoted host discovered by network scan. UI presents `[ Promote to Asset ]` button.
- **`REGISTERED`:** Asset registered with owner email (*BR-02*). UI displays `[ Activate Monitoring ]` button.
- **`ACTIVE`:** Normal operational monitoring. All action buttons active.
- **`UNDER_MAINTENANCE`:** Asset in maintenance window. Suppress non-critical alert popups.
- **`ISOLATED`:** Asset network-isolated via SOAR playbook. Render red `ISOLATED` warning banner in Inspector Drawer.
- **`DECOMMISSIONED`:** Asset retired. View-only mode in historical records.

### 2.2 Incident (`Incident`) State Machine
$$\text{DECLARED} \longrightarrow \text{ASSIGNED} \longrightarrow \text{IN\_DIAGNOSIS} \longrightarrow \text{REMEDIATED} \longrightarrow \text{CLOSED\_WITH\_RCA}$$

- **`DECLARED`:** Incident created from correlated alerts. UI prompts for responder assignment.
- **`ASSIGNED`:** Assigned to SOC Tier 2 analyst. SOAR playbooks unlocked.
- **`IN_DIAGNOSIS`:** Active investigation in progress. Evidence timeline enabled.
- **`REMEDIATED`:** Threat contained. Requires Root Cause Analysis (RCA) text before closing.
- **`CLOSED_WITH_RCA`:** Incident officially resolved. Inmutable archive state.
