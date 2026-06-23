#!/usr/bin/env python3
"""Database migration for ping_log table and RPC function."""

import psycopg2
import os
import sys

DB_CONFIG = {
    'host': 'db.ujxmftvftcbjrdmzhlrw.supabase.co',
    'port': 5432,
    'dbname': 'postgres',
    'user': 'postgres',
    'password': os.environ.get('SUPABASE_DB_PASSWORD'),
    'sslmode': 'require'
}

MIGRATIONS = [
    "DROP TABLE IF EXISTS ping_log CASCADE;",
    """CREATE TABLE ping_log (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        pinged_at TIMESTAMPTZ DEFAULT now()
    );""",
    "ALTER TABLE ping_log ENABLE ROW LEVEL SECURITY;",
    """CREATE POLICY "Public access" ON ping_log FOR ALL TO anon USING (true) WITH CHECK (true);""",
    """CREATE OR REPLACE FUNCTION ping_keep_alive()
       RETURNS JSON AS $$
       BEGIN
           INSERT INTO ping_log (pinged_at) VALUES (now());
           RETURN json_build_object('status', 'pong', 'timestamp', now());
       END;
       $$ LANGUAGE plpgsql;"""
]

def run_migrations():
    if not DB_CONFIG['password']:
        print("Error: SUPABASE_DB_PASSWORD environment variable not set")
        sys.exit(1)

    print("Running database migrations...\n")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()

        for sql in MIGRATIONS:
            try:
                cur.execute(sql)
                summary = sql.split('\n')[0][:60]
                print(f"✓ {summary}...")
            except Exception as e:
                print(f"✗ Failed: {sql.split(chr(10))[0]}")
                print(f"  {str(e)}")
                sys.exit(1)

        cur.close()
        conn.close()
        print("\n✓ All migrations complete!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_migrations()
