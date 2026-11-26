
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
app = FastAPI(
    title="Advanced LMS API",
    description="Learning Management System Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router)
@app.get("/")
def home():
    return {
        "message": "Advanced LMS Backend Running Successfully!"
    }

@app.get("/health")
def health():
    return {"status": "OK"}
