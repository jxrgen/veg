import requests
import psycopg2
import base64
import json

SUPABASE_URL = "https://ujxmftvftcbjrdmzhlrw.supabase.co"
ANON_KEY = "sb_publishable_EeimAI1x6_X1KxT-Clw5Bg_zIveRDYb"
ADMIN_EMAIL = "jxrgen@gmail.com"
ADMIN_PASSWORD = "aihmarkadmin"
DB_HOST = "db.ujxmftvftcbjrdmzhlrw.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "upmarkningsapp3000safeashell"

print("=" * 60)
print("TEST 1: POST /auth/v1/token?grant_type=password")
print("=" * 60)

auth_url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
auth_headers = {
    "apikey": ANON_KEY,
    "Content-Type": "application/json"
}
auth_body = {
    "email": ADMIN_EMAIL,
    "password": ADMIN_PASSWORD
}

resp = requests.post(auth_url, headers=auth_headers, json=auth_body)
print(f"HTTP Status: {resp.status_code}")
print(f"Full response body (raw): {resp.text}")
print()
try:
    resp_json = resp.json()
    print("Parsed JSON keys:", list(resp_json.keys()))
    print("Full parsed JSON:")
    for k, v in resp_json.items():
        if k in ("access_token", "refresh_token"):
            print(f"  {k}: {str(v)[:60]}...")
        else:
            print(f"  {k}: {v}")
    jwt = resp_json.get("access_token")
except Exception as e:
    print(f"Error parsing response: {e}")
    jwt = None

print()
print("=" * 60)
print("TEST 2: GET /rest/v1/members?select=*")
print("=" * 60)

if jwt:
    members_url = f"{SUPABASE_URL}/rest/v1/members?select=*"
    members_headers = {
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    resp2 = requests.get(members_url, headers=members_headers)
    print(f"HTTP Status: {resp2.status_code}")
    try:
        data = resp2.json()
        if isinstance(data, list):
            print(f"Total rows returned: {len(data)}")
            print(f"First 3 rows:")
            for i, row in enumerate(data[:3]):
                print(f"  Row {i+1}: {row}")
        else:
            print(f"Response (not a list): {data}")
    except Exception as e:
        print(f"Error parsing members response: {e}")
        print(f"Raw: {resp2.text[:500]}")
else:
    print("No JWT available, skipping Test 2")

print()
print("=" * 60)
print("TEST 3: RLS policies on members table (via psycopg2)")
print("=" * 60)

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT policyname, cmd, qual, with_check
        FROM pg_policies
        WHERE tablename = 'members';
    """)
    rows = cur.fetchall()
    print(f"Number of RLS policies: {len(rows)}")
    for row in rows:
        print(f"  policyname: {row[0]}")
        print(f"  cmd: {row[1]}")
        print(f"  qual: {row[2]}")
        print(f"  with_check: {row[3]}")
        print()
    cur.close()
    conn.close()
except Exception as e:
    print(f"psycopg2 connection error: {e}")

print()
print("=" * 60)
print("TEST 4: Decode JWT claims")
print("=" * 60)

if jwt:
    try:
        parts = jwt.split('.')
        # Add padding
        payload_b64 = parts[1] + '=='
        # Fix base64url to base64
        payload_b64 = payload_b64.replace('-', '+').replace('_', '/')
        payload = json.loads(base64.b64decode(payload_b64))
        print("JWT Payload:")
        for k, v in payload.items():
            print(f"  {k}: {v}")
        print()
        role_claim = payload.get("role")
        print(f"'role' claim value: {role_claim!r}")
        print(f"Is role == 'authenticated'? {role_claim == 'authenticated'}")
    except Exception as e:
        print(f"Error decoding JWT: {e}")
else:
    print("No JWT available, skipping Test 4")

print()
print("=" * 60)
print("TEST 5: Fetch members WITHOUT apikey header (only Authorization)")
print("=" * 60)

if jwt:
    members_url = f"{SUPABASE_URL}/rest/v1/members?select=*"
    headers_no_apikey = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }
    resp5 = requests.get(members_url, headers=headers_no_apikey)
    print(f"HTTP Status: {resp5.status_code}")
    try:
        data5 = resp5.json()
        if isinstance(data5, list):
            print(f"Total rows returned: {len(data5)}")
            print(f"First 3 rows:")
            for i, row in enumerate(data5[:3]):
                print(f"  Row {i+1}: {row}")
        else:
            print(f"Response (not a list): {data5}")
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw: {resp5.text[:500]}")
else:
    print("No JWT available, skipping Test 5")

print()
print("=" * 60)
print("TEST 6: Direct row count via psycopg2")
print("=" * 60)

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), MIN(luge_gruppe), MAX(luge_gruppe) FROM members;")
    row = cur.fetchone()
    print(f"COUNT(*): {row[0]}")
    print(f"MIN(luge_gruppe): {row[1]}")
    print(f"MAX(luge_gruppe): {row[2]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"psycopg2 error in Test 6: {e}")

print()
print("=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
