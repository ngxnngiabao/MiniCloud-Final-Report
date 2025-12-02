from flask import Flask, jsonify, request
import time, requests, os, json
from jose import jwt
import pymysql

ISSUER = os.getenv("OIDC_ISSUER", "http://authentication-identity-server:8080/realms/master")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "account")

INTERNAL_ISSUER = ISSUER.replace("localhost:8081", "authentication-identity-server:8080")
JWKS_URL = f"{INTERNAL_ISSUER}/protocol/openid-connect/certs"
# ---------------------------------------------

DB_HOST = "relational-database-server"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "studentdb"

_JWKS = None
_TS = 0

def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        try:
            _JWKS = requests.get(JWKS_URL, timeout=5).json()
            _TS = now
        except:
            pass
    return _JWKS

app = Flask(__name__)

@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")

@app.get("/student")
def student_json():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.get("/student/db")
def student_db():
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM students"
            cursor.execute(sql)
            result = cursor.fetchall()
            
            students = []
            for row in result:
                students.append({
                    "id": row[0],
                    "student_id": row[1],
                    "fullname": row[2],
                    "dob": str(row[3]),
                    "major": row[4]
                })
        connection.close()
        return jsonify(message="Data from MariaDB Container", data=students)
    except Exception as e:
        return jsonify(error=f"Database Error: {str(e)}"), 500

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)