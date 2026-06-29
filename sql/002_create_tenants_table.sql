CREATE TABLE IF NOT EXISTS tenants (
    tenant_id VARCHAR(100) PRIMARY KEY,
    max_agents INTEGER NOT NULL DEFAULT 0 CHECK (max_agents >= 0),
    max_running_agents INTEGER NOT NULL DEFAULT 0 CHECK (max_running_agents >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_tenants_tenant_id ON tenants (tenant_id);
