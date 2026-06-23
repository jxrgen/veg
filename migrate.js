#!/usr/bin/env node
const https = require('https');

const SUPABASE_URL = 'https://ujxmftvftcbjrdmzhlrw.supabase.co';
const SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;

if (!SERVICE_KEY) {
  console.error('Error: SUPABASE_SERVICE_KEY environment variable not set');
  process.exit(1);
}

const SQL_MIGRATIONS = [
  `DROP TABLE IF EXISTS ping_log CASCADE;`,
  `CREATE TABLE ping_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    pinged_at TIMESTAMPTZ DEFAULT now()
  );`,
  `ALTER TABLE ping_log ENABLE ROW LEVEL SECURITY;`,
  `CREATE POLICY "Public access" ON ping_log FOR ALL TO anon USING (true) WITH CHECK (true);`,
  `CREATE OR REPLACE FUNCTION ping_keep_alive()
   RETURNS JSON AS $$
   BEGIN
     INSERT INTO ping_log (pinged_at) VALUES (now());
     RETURN json_build_object('status', 'pong', 'timestamp', now());
   END;
   $$ LANGUAGE plpgsql;`
];

async function runMigrations() {
  console.log('Running database migrations...\n');

  for (const sql of SQL_MIGRATIONS) {
    try {
      const result = await executeSQL(sql);
      console.log(`✓ ${sql.split('\n')[0].substring(0, 60)}...`);
    } catch (error) {
      console.error(`✗ Failed: ${sql.split('\n')[0]}`);
      console.error(`  ${error.message}`);
      process.exit(1);
    }
  }

  console.log('\n✓ All migrations complete!');
}

function executeSQL(sql) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ query: sql });

    const options = {
      hostname: 'ujxmftvftcbjrdmzhlrw.supabase.co',
      port: 443,
      path: '/rest/v1/rpc/exec_sql',
      method: 'POST',
      headers: {
        'apikey': SERVICE_KEY,
        'Authorization': `Bearer ${SERVICE_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': payload.length
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 400) {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        } else {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

runMigrations().catch(err => {
  console.error('Migration failed:', err);
  process.exit(1);
});
