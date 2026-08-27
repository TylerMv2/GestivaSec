-- GESTIVA SECURITY (GESTIVASEC V1) — DEMO DATA SEED FILE (RELEASE V0.1.0)

-- 1. ORGANIZATIONS SEED (BR-04 MULTI-TENANT ISOLATION)
INSERT INTO organizations (id, name, slug, status)
VALUES 
    ('00000000-0000-0000-0000-000000000001', 'GestivaOne Corporation', 'gestivaone-corp', 'ACTIVE_ORGANIZATION'),
    ('00000000-0000-0000-0000-000000000002', 'Festa Event Systems', 'festa-events', 'ACTIVE_ORGANIZATION')
ON CONFLICT (id) DO NOTHING;

-- 2. USERS SEED (ADMIN & ANALYST)
INSERT INTO users (id, organization_id, email, password_hash, role, is_active)
VALUES 
    ('00000000-0000-0000-0000-000000000099', '00000000-0000-0000-0000-000000000001', 'admin@gestivaone.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'SOC_ADMIN', TRUE),
    ('00000000-0000-0000-0000-000000000098', '00000000-0000-0000-0000-000000000001', 'analyst@gestivaone.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'SOC_ANALYST', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 3. DIGITAL ASSETS SEED (BR-02 OWNER EMAIL REQUIRED)
INSERT INTO assets (id, organization_id, name, target_url, criticality, owner_email, status)
VALUES 
    ('11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000001', 'GestivaOne Core Web Portal', 'https://gestivaone.com', 'P1_CRITICAL', 'ops@gestivaone.com', 'ACTIVE'),
    ('22222222-2222-2222-2222-222222222222', '00000000-0000-0000-0000-000000000001', 'GestivaOne E-Commerce Store', 'https://gestivaone-store.vercel.app', 'P2_HIGH', 'devops@gestivaone.com', 'ACTIVE'),
    ('33333333-3333-3333-3333-333333333333', '00000000-0000-0000-0000-000000000001', 'Festa Event Platform', 'https://festa.gestivaone.com', 'P2_HIGH', 'festa-lead@gestivaone.com', 'ACTIVE')
ON CONFLICT (id) DO NOTHING;
