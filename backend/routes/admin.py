from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend import models, schemas, database
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

router = APIRouter(prefix="/admin", tags=["admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

async def get_current_admin(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(database.get_session)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role != "admin":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    query = await session.execute(select(models.User).filter(models.User.id == int(user_id)))
    user = query.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/users", response_model=List[schemas.UserOut])
async def list_users(session: AsyncSession = Depends(database.get_session), admin: models.User = Depends(get_current_admin)):
    query = await session.execute(select(models.User))
    users = query.scalars().all()
    return users

@router.post("/verify-driver/{driver_id}")
async def verify_driver(driver_id: int, verified: bool, session: AsyncSession = Depends(database.get_session), admin: models.User = Depends(get_current_admin)):
    query = await session.execute(select(models.DriverProfile).filter(models.DriverProfile.id == driver_id))
    driver_profile = query.scalars().first()
    if not driver_profile:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    driver_profile.is_verified = verified
    session.add(driver_profile)
    await session.commit()
    return {"message": f"Driver verification status updated to {verified}"}

@router.get("/stats")
async def get_stats(session: AsyncSession = Depends(database.get_session), admin: models.User = Depends(get_current_admin)):
    total_clients = await session.execute(select(models.User).filter(models.User.role == models.UserRole.client))
    total_drivers = await session.execute(select(models.User).filter(models.User.role == models.UserRole.driver))
    total_rides = await session.execute(select(models.Ride))
    return {
        "total_clients": total_clients.scalars().count(),
        "total_drivers": total_drivers.scalars().count(),
        "total_rides": total_rides.scalars().count(),
    }
