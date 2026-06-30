from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import uuid
from datetime import datetime, timedelta

app = FastAPI()

conn = sqlite3.connect("licenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS licenses (
    license_key TEXT PRIMARY KEY,
    hwid TEXT,
    expires TEXT,
    token TEXT
)
""")

conn.commit()

class LicenseRequest(BaseModel):
    key: str
    hwid: str

def create_token():
    return str(uuid.uuid4())

@app.post("/check")
def check_license(req: LicenseRequest):

    cursor.execute("SELECT * FROM licenses WHERE license_key=?", (req.key,))
    row = cursor.fetchone()

    if not row:
        return {"status": "error", "message": "Invalid key"}

    license_key, hwid, expires, token = row

    expire_date = datetime.strptime(expires, "%Y-%m-%d")

    if datetime.now() > expire_date:
        return {"status": "error", "message": "Subscription expired"}

    if hwid is None:
        cursor.execute("UPDATE licenses SET hwid=? WHERE license_key=?", (req.hwid, req.key))
        conn.commit()

    elif hwid != req.hwid:
        return {"status": "error", "message": "Key already used"}

    token = create_token()

    cursor.execute("UPDATE licenses SET token=? WHERE license_key=?", (token, req.key))
    conn.commit()

    return {"status": "ok", "token": token}


@app.get("/create/{days}")
def create_key(days: int):

    key = str(uuid.uuid4()).split("-")[0].upper()
    expire = datetime.now() + timedelta(days=days)

    cursor.execute("""
        INSERT INTO licenses (license_key, hwid, expires, token)
        VALUES (?, ?, ?, ?)
    """, (key, None, expire.strftime("%Y-%m-%d"), None))

    conn.commit()

    return {"key": key, "expires": expire.strftime("%Y-%m-%d")}


@app.get("/")
def root():
    return {"status": "online"}