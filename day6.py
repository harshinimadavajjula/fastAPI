from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# --------------- SETTINGS -------------------
SECRET_KEY = "mysecretkey123"  # Use a stronger secret key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --------------- PASSWORD HASHING -------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# --------------- TOKEN CREATION -------------------
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --------------- FAKE USER DB -------------------
fake_users_db = {}

# --------------- Pydantic Models -------------------
class User(BaseModel):
    username: str
    full_name: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --------------- SIGNUP -------------------
@app.post("/signup")
def signup(user: OAuth2PasswordRequestForm = Depends()):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = hash_password(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "full_name": user.username,
        "hashed_password": hashed_pwd
    }
    return {"message": "User registered successfully"}

# --------------- LOGIN -------------------
@app.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = fake_users_db.get(user.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")
    
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --------------- GET CURRENT USER -------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_data = fake_users_db[username]
        return User(username=username, full_name=user_data["full_name"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --------------- PROTECTED ROUTE -------------------
@app.get("/profile")
def read_profile(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.full_name}!"}
