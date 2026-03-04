from fastapi import APIRouter, HTTPException, Request
from schemas.user import UserRegister, UserLogin
from services.auth_service import hash_password, verify_password, create_access_token
from repos.user_repo import create_user, get_user_by_email

router = APIRouter(prefix="/api")

@router.post("/register")
async def register(user_data: UserRegister):
    hashed_pw = hash_password(user_data.password)
    success = create_user(user_data.name, user_data.email, hashed_pw)
    if success:
        return {"status": "success", "message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="Username or Email already exists")

@router.post("/login")
async def login(login_data: UserLogin):
    user = get_user_by_email(login_data.email)
    if user and verify_password(login_data.password, user['password_hash']):
        token = create_access_token({"sub": user['username'], "email": user['email'], "id": user['id']})
        return {"status": "success", "access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")
