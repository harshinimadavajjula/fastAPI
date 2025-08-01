from fastapi import FastAPI, Request, Header, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

# ✅ 1. API Key verification dependency
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "mysecretkey123":
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return x_api_key

# ✅ 2. Logging Middleware for request time
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        print(f"{request.method} {request.url} completed in {duration:.2f}s")
        return response

# Add middleware to the app
app.add_middleware(LoggingMiddleware)

# ✅ A secured route using the API key
@app.get("/secure-data")
def get_secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "You accessed secure data!"}

# ✅ A normal route with no key check
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
