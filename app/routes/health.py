
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to PolicyGuard AI",
        "status": "running",
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "PolicyGuard AI",
    }
