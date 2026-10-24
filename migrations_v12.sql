-- ============================================================
-- Mailair v12 Migrations — Run in Supabase SQL Editor
-- ============================================================

-- Demo requests from the "Book a demo" form on the landing page.
-- Written only by the backend (service key); RLS on with no policies
-- keeps the table unreadable from the browser.
CREATE TABLE IF NOT EXISTS demo_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    company TEXT NOT NULL DEFAULT '',
    team_size TEXT NOT NULL DEFAULT '',
    interests TEXT[] NOT NULL DEFAULT '{}',  -- campaigns | inbox | workspace | integrations
    message TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'new',      -- new | contacted | scheduled | done
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_demo_requests_created_at ON demo_requests(created_at DESC);

ALTER TABLE demo_requests ENABLE ROW LEVEL SECURITY;
