import os
import sqlite3
import json
import secrets
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import List, Optional
from dotenv import load_dotenv

# Env laden
load_dotenv(".env")
SECRET_KEY = os.getenv("SECRET_KEY", "changeme123")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 120
DB_PATH = os.getenv("DB_PATH", "prime_claimer.db")

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- DB INIT ---
def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        hashed_password TEXT,
        is_admin INTEGER DEFAULT 0,
        first_login INTEGER DEFAULT 1,
        email TEXT,
        discord TEXT
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        platform TEXT,
        session_data TEXT,
        last_active TIMESTAMP
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        platform TEXT,
        cover_url TEXT,
        key TEXT,
        claimed INTEGER DEFAULT 0,
        claimed_at TIMESTAMP,
        log TEXT
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        event TEXT,
        detail TEXT,
        created_at TIMESTAMP
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)
    conn.commit()
    conn.close()
init_db()

# --- MODELS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    id: int
    username: str
    is_admin: bool
    email: Optional[str]
    discord: Optional[str]
    first_login: bool

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class Game(BaseModel):
    id: int
    title: str
    platform: str
    cover_url: Optional[str]
    key: Optional[str]
    claimed: bool
    claimed_at: Optional[str]

class LogEntry(BaseModel):
    id: int
    user_id: int
    event: str
    detail: str
    created_at: str

# --- AUTH / UTILS ---
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

def get_user(username: str):
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row

def get_user_by_id(user_id: int):
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

async def get_admin_user(user=Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin privilege required")
    return user

# --- USER MANAGEMENT ---
@app.post("/register", response_model=User)
def register(user: UserCreate):
    conn = db_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, hashed_password, email, is_admin) VALUES (?, ?, ?, ?)",
            (user.username, get_password_hash(user.password), user.email, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    c.execute("SELECT * FROM users WHERE username=?", (user.username,))
    row = c.fetchone()
    conn.close()
    return User(
        id=row["id"], username=row["username"], is_admin=bool(row["is_admin"]),
        email=row["email"], discord=row["discord"], first_login=bool(row["first_login"])
    )

@app.post("/token", response_model=LoginResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"]})
    user_obj = {
        "id": user["id"],
        "username": user["username"],
        "is_admin": bool(user["is_admin"]),
        "email": user["email"],
        "discord": user["discord"],
        "first_login": bool(user["first_login"])
    }
    return {"access_token": token, "token_type": "bearer", "user": user_obj}

@app.get("/me", response_model=User)
def get_me(user=Depends(get_current_user)):
    return User(
        id=user["id"], username=user["username"], is_admin=bool(user["is_admin"]),
        email=user["email"], discord=user["discord"], first_login=bool(user["first_login"])
    )

@app.post("/me/password")
def change_password(new_password: str, user=Depends(get_current_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET hashed_password=?, first_login=0 WHERE id=?",
              (get_password_hash(new_password), user["id"]))
    conn.commit()
    conn.close()
    return {"msg": "Password updated"}

# Mark tutorial as completed for the current user
@app.post("/me/tutorial-complete")
def tutorial_complete(user=Depends(get_current_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET first_login=0 WHERE id=?", (user["id"],))
    conn.commit()
    conn.close()
    return {"msg": "Tutorial completed"}

# --- ADMIN ---
@app.post("/admin/new-user")
def admin_create_user(u: UserCreate, user=Depends(get_admin_user)):
    conn = db_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, hashed_password, email, is_admin) VALUES (?, ?, ?, 0)",
            (u.username, get_password_hash(u.password), u.email))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"msg": "User created"}

# --- PRIME GAMING SESSION (Dummy, für Demo) ---
@app.post("/accounts/amazon/login")
def amazon_login(user=Depends(get_current_user)):
    # Hier würdest du Playwright nutzen und Cookies ablegen
    # Dummy-Daten:
    session = {"logged_in": True, "session_cookies": "DUMMY"}
    conn = db_conn()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO sessions (user_id, platform, session_data, last_active) VALUES (?, 'amazon', ?, ?)",
              (user["id"], json.dumps(session), datetime.utcnow()))
    conn.commit()
    conn.close()
    return {"msg": "Amazon session gespeichert"}

@app.get("/accounts/amazon/status")
def amazon_status(user=Depends(get_current_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM sessions WHERE user_id=? AND platform='amazon'", (user["id"],))
    row = c.fetchone()
    conn.close()
    if not row:
        return {"logged_in": False}
    session = json.loads(row["session_data"])
    return session

@app.delete("/accounts/amazon/logout")
def amazon_logout(user=Depends(get_current_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE user_id=? AND platform='amazon'", (user["id"],))
    conn.commit()
    conn.close()
    return {"msg": "Amazon session gelöscht"}

# --- GAMES / CLAIM ---
@app.get("/games", response_model=List[Game])
def get_games(user=Depends(get_current_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM games WHERE user_id=?", (user["id"],))
    games = [Game(
        id=row["id"], title=row["title"], platform=row["platform"], cover_url=row["cover_url"],
        key=row["key"], claimed=bool(row["claimed"]), claimed_at=row["claimed_at"]
    ) for row in c.fetchall()]
    conn.close()
    return games

@app.post("/games/claim/{game_id}")
def claim_game(game_id: int, user=Depends(get_current_user)):
    # Hier würdest du Playwright für Auto-Claim nutzen und Key speichern
    # Dummy-Implementierung:
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM games WHERE id=? AND user_id=?", (game_id, user["id"]))
    game = c.fetchone()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    # Setze als "eingelöst":
    c.execute("UPDATE games SET claimed=1, claimed_at=? WHERE id=?", (datetime.utcnow(), game_id))
    conn.commit()
    conn.close()
    return {"msg": "Game claimed"}

# --- LOGGING & ADMIN ---
@app.get("/admin/logs", response_model=List[LogEntry])
def get_logs(user=Depends(get_admin_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT 200")
    logs = [LogEntry(
        id=row["id"], user_id=row["user_id"], event=row["event"],
        detail=row["detail"], created_at=row["created_at"]
    ) for row in c.fetchall()]
    conn.close()
    return logs

@app.get("/admin/settings")
def get_settings(user=Depends(get_admin_user)):
    conn = db_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM settings")
    res = {row["key"]: row["value"] for row in c.fetchall()}
    conn.close()
    return res

@app.post("/admin/settings")
def set_settings(settings: dict, user=Depends(get_admin_user)):
    conn = db_conn()
    c = conn.cursor()
    for k, v in settings.items():
        c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (k, v))
    conn.commit()
    conn.close()
    return {"msg": "Settings updated"}

@app.get("/admin/debug")
def admin_debug(user=Depends(get_admin_user)):
    # Dummy-Status: DB, Session, letzte Claims, Bot-Erreichbarkeit etc.
    return {
        "db": "ok",
        "amazon_session": True,
        "last_claim": str(datetime.utcnow()),
        "discord_bot": "reachable (dummy)"
    }
