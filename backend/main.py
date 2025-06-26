from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend import models, schemas, auth, database, otp_service
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
import uvicorn

app = FastAPI(title="DjibRide Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, session: AsyncSession = Depends(database.get_session)):
    query = await session.execute(select(models.User).filter((models.User.email == user.email) | (models.User.phone == user.phone)))
    existing_user = query.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        phone=user.phone,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(database.get_session)):
    query = await session.execute(select(models.User).filter((models.User.email == form_data.username) | (models.User.phone == form_data.username)))
    user = query.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/otp/request")
async def request_otp(phone: str = Body(..., embed=True)):
    otp = otp_service.generate_otp(phone)
    return {"message": f"OTP sent to {phone}"}

@app.post("/otp/verify")
async def verify_otp(phone: str = Body(...), otp: str = Body(...)):
    if otp_service.verify_otp(phone, otp):
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

from backend.routes import rides
from fastapi import APIRouter

# Additional endpoints for user management, driver profile, rides, payments to be added here

app.include_router(rides.router)
from backend.routes import payments, admin

app.include_router(payments.router)
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
