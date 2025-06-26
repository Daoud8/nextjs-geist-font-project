from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend import models, schemas, database, services
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

router = APIRouter(prefix="/rides", tags=["rides"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(database.get_session)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    query = await session.execute(select(models.User).filter(models.User.id == int(user_id)))
    user = query.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/", response_model=schemas.RideOut)
async def create_ride(ride: schemas.RideCreate, current_user: models.User = Depends(get_current_user), session: AsyncSession = Depends(database.get_session)):
    if current_user.role != models.UserRole.client:
        raise HTTPException(status_code=403, detail="Only clients can create rides")
    # Calculate distance and fare here (distance calculation to be implemented)
    # For now, assume distance is passed in ride data or calculate externally
    distance_km = 5.0  # Placeholder value, replace with real calculation
    fare = services.fare_calculation.calculate_fare(distance_km)
    db_ride = models.Ride(
        client_id=current_user.id,
        pickup_location=ride.pickup_location.dict(),
        dropoff_location=ride.dropoff_location.dict(),
        service_type=ride.service_type,
        status="requested",
        fare=fare
    )
    session.add(db_ride)
    await session.commit()
    await session.refresh(db_ride)
    return db_ride

@router.get("/", response_model=List[schemas.RideOut])
async def list_rides(current_user: models.User = Depends(get_current_user), session: AsyncSession = Depends(database.get_session)):
    if current_user.role == models.UserRole.client:
        query = await session.execute(select(models.Ride).filter(models.Ride.client_id == current_user.id))
    elif current_user.role == models.UserRole.driver:
        query = await session.execute(select(models.Ride).filter(models.Ride.driver_id == current_user.id))
    else:
        query = await session.execute(select(models.Ride))
    rides = query.scalars().all()
    return rides
