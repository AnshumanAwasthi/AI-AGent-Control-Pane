
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'agent_status_type') THEN
        CREATE TYPE agent_status_type AS ENUM ('stopped', 'running', 'paused', 'created');
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS agents (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    tenant_id VARCHAR(100) NOT NULL,
    runtime VARCHAR(100) NOT NULL DEFAULT 'python',
    status agent_status_type NOT NULL DEFAULT 'created',
    config JSON NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_agents_user_id ON agents (user_id);
