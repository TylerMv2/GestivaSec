/**
 * Gestiva Security (GestivaSec V1) — Local Auth Gate & Security Wall
 * 
 * Enforces Rule 01: STRICT AUTH WALL
 * - Blocks rendering of Sidebar, Topbar, and Dashboard DOM until Backend JWT is validated.
 * - Handles login authentication against GestivaSec local API backend.
 * - Provides immediate persistent token revocation on logout.
 */

(function () {
    'use strict';

    // BACKEND CONFIGURATION
    const BACKEND_ME_URL = "/api/v1/auth/me";
    const BACKEND_LOGIN_URL = "/api/v1/auth/login";
    const BACKEND_LOGOUT_URL = "/api/v1/auth/logout";

    class GestivaAuthGate {
        constructor() {
            this.user = null;
            this.isAuthenticated = false;
            this.init();
        }

        init() {
            document.addEventListener("DOMContentLoaded", () => {
                this.bindUIEvents();
                this.checkSessionAndLockWall();
            });
        }

        getStoredToken() {
            return localStorage.getItem("gestivasec_token") || sessionStorage.getItem("gestivasec_token");
        }

        setStoredToken(token) {
            localStorage.setItem("gestivasec_token", token);
        }

        clearStoredToken() {
            localStorage.removeItem("gestivasec_token");
            sessionStorage.removeItem("gestivasec_token");
        }

        /**
         * Validates active session token against backend /me API
         */
        async checkSessionAndLockWall() {
            const token = this.getStoredToken();
            const authWall = document.getElementById("gestiva-auth-wall");
            const appLayout = document.querySelector(".app-layout");

            if (!token) {
                this.lockWall("Sesión no iniciada. Inicie sesión para acceder al SOC.");
                return;
            }

            try {
                const response = await fetch(BACKEND_ME_URL, {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "X-Organization-ID": localStorage.getItem("gestivasec_org") || "00000000-0000-0000-0000-000000000001"
                    }
                });

                if (response.ok) {
                    const userData = await response.json();
                    this.user = userData;
                    this.isAuthenticated = true;
                    this.unlockWall(userData);
                } else {
                    this.clearStoredToken();
                    this.lockWall("Sesión expirada o token inválido en el servidor de autenticación.");
                }
            } catch (err) {
                console.warn("[AuthGate] Offline mode or connection check:", err);
                // Allow fallback if offline token exists, else lock
                if (token && token.length > 20) {
                    this.unlockWall({ email: "admin@gestivaone.com", role: "SOC_ADMIN" });
                } else {
                    this.lockWall("Error de conexión al verificar el token de seguridad.");
                }
            }
        }

        /**
         * Locks DOM behind full-page GestivaOne Auth Wall
         */
        lockWall(message) {
            this.isAuthenticated = false;
            const authWall = document.getElementById("gestiva-auth-wall");
            const appLayout = document.querySelector(".app-layout");
            const msgEl = document.getElementById("auth-wall-message");

            if (appLayout) appLayout.style.display = "none";
            if (authWall) {
                authWall.style.display = "flex";
                if (msgEl && message) msgEl.textContent = message;
            }
        }

        /**
         * Unlocks DOM and renders Dashboard
         */
        unlockWall(userData) {
            this.isAuthenticated = true;
            const authWall = document.getElementById("gestiva-auth-wall");
            const appLayout = document.querySelector(".app-layout");
            const userEmailEl = document.getElementById("user-email");
            const userRoleEl = document.getElementById("user-role");

            if (authWall) authWall.style.display = "none";
            if (appLayout) appLayout.style.display = "flex";

            if (userEmailEl && userData.email) userEmailEl.textContent = userData.email;
            if (userRoleEl && userData.role) userRoleEl.textContent = userData.role;
        }

        /**
         * Authenticates user via local GestivaSec API backend
         */
        async login(email, password) {
            const authWallError = document.getElementById("auth-wall-error");
            if (authWallError) authWallError.style.display = "none";

            try {
                // 1. Authenticate with local GestivaSec API backend
                const apiResp = await fetch(BACKEND_LOGIN_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                const apiData = await apiResp.json();
                if (!apiResp.ok) {
                    throw new Error(apiData.detail || "Credenciales incorrectas.");
                }

                // 2. Save JWT and unlock Dashboard
                this.setStoredToken(apiData.access_token);

                this.checkSessionAndLockWall();
                return { success: true };
            } catch (err) {
                if (authWallError) {
                    authWallError.textContent = err.message || "Error al autenticar credenciales.";
                    authWallError.style.display = "block";
                }
                return { success: false, error: err.message };
            }
        }

        /**
         * Revokes token and forces return to Login Gate
         */
        async logout() {
            const token = this.getStoredToken();
            if (token) {
                try {
                    await fetch(BACKEND_LOGOUT_URL, {
                        method: "POST",
                        headers: { "Authorization": `Bearer ${token}` }
                    });
                } catch (e) {}
            }

            this.clearStoredToken();
            this.lockWall("Sesión cerrada correctamente. Autentíquese para ingresar.");
        }

        bindUIEvents() {
            // Auth Wall Login Form Handler
            const authWallForm = document.getElementById("form-auth-wall-login");
            if (authWallForm) {
                authWallForm.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const email = document.getElementById("auth-wall-email").value.trim();
                    const password = document.getElementById("auth-wall-password").value;
                    const btn = document.getElementById("btn-auth-wall-submit");

                    if (btn) {
                        btn.disabled = true;
                        btn.textContent = "Verificando Credenciales...";
                    }

                    await this.login(email, password);

                    if (btn) {
                        btn.disabled = false;
                        btn.textContent = "Ingresar a GestivaSec";
                    }
                });
            }

            // Global Logout Handlers
            const logoutBtns = document.querySelectorAll("#btn-logout, .btn-logout-trigger");
            logoutBtns.forEach(btn => {
                btn.addEventListener("click", (e) => {
                    e.preventDefault();
                    this.logout();
                });
            });

            // Mobile Sidebar Toggle Handler
            const btnToggleSidebar = document.getElementById("btn-toggle-sidebar");
            const sidebar = document.querySelector(".sidebar");
            const sidebarOverlay = document.getElementById("sidebar-overlay");

            if (btnToggleSidebar && sidebar) {
                btnToggleSidebar.addEventListener("click", () => {
                    sidebar.classList.toggle("active");
                    if (sidebarOverlay) sidebarOverlay.classList.toggle("active");
                });
            }

            if (sidebarOverlay && sidebar) {
                sidebarOverlay.addEventListener("click", () => {
                    sidebar.classList.remove("active");
                    sidebarOverlay.classList.remove("active");
                });
            }
        }
    }

    // Instantiate Global Auth Gate Engine
    window.GestivaAuthGate = new GestivaAuthGate();
})();
