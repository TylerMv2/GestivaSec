# GESTIVASEC_UI_ANTI_PATTERNS.md — FORBIDDEN UI/UX ANTI-PATTERNS MANUAL

**Platform:** Gestiva Security (GestivaSec V1 Enterprise SOC Platform)  
**Document Status:** `APPROVED & STRICTLY ENFORCED GOVERNANCE MANUAL`  
**Target Audience:** UI/UX Designers, Frontend Engineers, QA Engineers, Product Managers  
**Date:** 2026-07-26  

---

## 1. EXECUTIVE MANDATE

This manual documents every forbidden UI and UX anti-pattern in **Gestiva Security**. Any component or layout violating these rules will be automatically rejected during Architecture Review Board (ARB) reviews.

---

## 2. FORBIDDEN ANTI-PATTERNS BY CATEGORY

### 2.1 Navigation Anti-Patterns
- ❌ **AP-NAV-01: Page Redirection Context Destruction:** Redirecting users to a new page to view entity details during active triage.
  - *Danger:* Destroys search state, scroll position, and analyst focus.
  - *Correction:* Use slide-over **Inspector Drawers** over the active grid.
- ❌ **AP-NAV-02: Deep Navigation Hierarchies (> 2 Clics):** Hiding critical actions or entities deeper than 2 clicks.
  - *Correction:* Maintain shallow 2-click max navigation paths.

### 2.2 Table & Data Anti-Patterns
- ❌ **AP-TBL-01: Unpaginated Data Dumps:** Rendering thousands of log records directly in the DOM without pagination.
  - *Danger:* Browser freezing and memory leaks.
  - *Correction:* Server-side pagination with virtualized table rendering.
- ❌ **AP-TBL-02: Ephemeral IP as Asset Primary Key:** Displaying IP addresses as the main asset identity.
  - *Correction:* Render **Asset UUID** with historical IP popovers.

### 2.3 Notification & Alerting Anti-Patterns
- ❌ **AP-NTF-01: Toast Notification Flooding:** Emitting toast popups for routine background operations.
  - *Correction:* Use silent activity logs; reserve toasts for critical error feedback.
- ❌ **AP-NTF-02: Unconfirmed Destructive Actions:** Executing host isolations or credential revocations without confirmation.
  - *Correction:* Mandatory confirmation modals for destructive operations.

### 2.4 Multi-Tenancy Anti-Patterns (BR-0004)
- ❌ **AP-MT-01: Client-Side Tenant Filtering:** Filtering tenant data in Javascript instead of passing `X-Organization-ID` header.
  - *Danger:* Critical multi-tenant security vulnerability (*BR-0004*).
  - *Correction:* Inject `X-Organization-ID` header into every HTTP request.

### 2.5 Visual & Cognitive Anti-Patterns
- ❌ **AP-VIS-01: Decorative Non-Semantic Color Usage:** Using red, amber, or green for purely aesthetic purposes.
  - *Correction:* Color accents must strictly represent severity (`P1_CRITICAL`, `P2_HIGH`, `P3_MEDIUM`, `P4_LOW`).
- ❌ **AP-VIS-02: Blank Screen Failure States:** Showing white/empty screens when backend APIs fail.
  - *Correction:* Explicit `ERROR` state containers with actionable retry buttons.
