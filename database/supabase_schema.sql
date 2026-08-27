-- ================================================================================
-- GESTIVASEC V1 — SUPABASE POSTGRESQL SCHEMA SPECIFICATION
-- Platform: Gestiva Security (GestivaSec V1 Enterprise SOC Platform)
-- Governance: Compatible with Supabase Auth, Audit Trail (BR-0005) & Multi-Tenant RBAC
-- ================================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. ORGANIZATIONS TABLE (TENANTS)
CREATE TABLE IF NOT EXISTS public.organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Default GestivaOne Tenant
INSERT INTO public.organizations (id, name, slug)
VALUES ('00000000-0000-0000-0000-000000000001', 'GestivaOne Corporation', 'gestivaone-corp')
ON CONFLICT (slug) DO NOTHING;

-- 2. USERS PROFILE & RBAC TABLE (LINKED TO SUPABASE AUTH.USERS)
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES public.organizations(id),
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'SOC_ANALYST',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. DIGITAL ASSET INVENTORY TABLE
CREATE TABLE IF NOT EXISTS public.assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES public.organizations(id),
    name VARCHAR(255) NOT NULL,
    target_url TEXT NOT NULL,
    criticality VARCHAR(50) NOT NULL DEFAULT 'P3_MEDIUM',
    owner_email VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    ip_history JSONB DEFAULT '[]'::jsonb,
    os_fingerprint VARCHAR(100) DEFAULT 'Linux x86_64',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. ACTIONABLE ALERTS TABLE
CREATE TABLE IF NOT EXISTS public.actionable_alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES public.organizations(id),
    asset_id UUID REFERENCES public.assets(id),
    rule_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'NEW',
    source_ip VARCHAR(100),
    mitre_attack_id VARCHAR(50),
    finding_count INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. INCIDENT CASES LIFECYCLE TABLE
CREATE TABLE IF NOT EXISTS public.incident_cases (
    case_id VARCHAR(50) PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES public.organizations(id),
    title VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'NEW',
    assigned_analyst VARCHAR(255),
    root_cause_analysis TEXT,
    evidence_timeline JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. IMMUTABLE AUDIT TRAIL LOG TABLE (BR-0005)
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES public.organizations(id),
    action VARCHAR(100) NOT NULL,
    actor_email VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255) NOT NULL,
    ip_address VARCHAR(100) NOT NULL,
    details JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.actionable_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.incident_cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Allow authenticated users to view resources in their tenant
CREATE POLICY tenant_isolation_assets ON public.assets
    FOR ALL USING (auth.uid() IN (
        SELECT id FROM public.user_profiles WHERE organization_id = assets.organization_id
    ));

CREATE POLICY tenant_isolation_audit ON public.audit_logs
    FOR SELECT USING (auth.uid() IN (
        SELECT id FROM public.user_profiles WHERE organization_id = audit_logs.organization_id
    ));

-- INITIAL SEED DATA FOR SECURITY.GESTIVAONE.COM
INSERT INTO public.assets (id, organization_id, name, target_url, criticality, owner_email, status, ip_history, os_fingerprint)
VALUES 
    ('11111111-1111-1111-1111-111111111111', '00000000-0000-0000-0000-000000000001', 'GestivaOne Portal Principal', 'https://gestivaone.com', 'P1_CRITICAL', 'propietario@gestivaone.com', 'ACTIVE', '["192.168.1.10", "10.0.0.1"]'::jsonb, 'Linux Ubuntu 24.04 LTS'),
    ('22222222-2222-2222-2222-222222222222', '00000000-0000-0000-0000-000000000001', 'Gestiva Security Subdomain', 'https://security.gestivaone.com', 'P1_CRITICAL', 'admin@gestivaone.com', 'ACTIVE', '["192.168.1.15"]'::jsonb, 'Linux Ubuntu 24.04 LTS'),
    ('33333333-3333-3333-3333-333333333333', '00000000-0000-0000-0000-000000000001', 'Festa Event Systems Portal', 'https://festa.gestivaone.com', 'P2_HIGH', 'festa-admin@gestivaone.com', 'ACTIVE', '["192.168.1.20"]'::jsonb, 'Linux Alpine 3.19')
ON CONFLICT (id) DO NOTHING;
