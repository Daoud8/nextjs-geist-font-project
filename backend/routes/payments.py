from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend import database, schemas, services, models
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

router = APIRouter(prefix="/payments", tags=["payments"])

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

@router.post("/stripe")
async def stripe_payment(payment_data: dict, current_user: models.User = Depends(get_current_user)):
    result = await services.payment_service.process_stripe_payment(payment_data)
    return result

@router.post("/paypal")
async def paypal_payment(payment_data: dict, current_user: models.User = Depends(get_current_user)):
    result = await services.payment_service.process_paypal_payment(payment_data)
    return result

@router.post("/waafi")
async def waafi_payment(payment_data: dict, current_user: models.User = Depends(get_current_user)):
    result = await services.payment_service.process_waafi_pay(payment_data)
    return result

@router.post("/edahab")
async def edahab_payment(payment_data: dict, current_user: models.User = Depends(get_current_user)):
    result = await services.payment_service.process_e_dahab(payment_data)
    return result

@router.post("/cacpay")
async def cacpay_payment(payment_data: dict, current_user: models.User = Depends(get_current_user)):
    result = await services.payment_service.process_cac_pay(payment_data)
    return result

@router.post("/sabapay")
async def sabapay_payment(payment_data: dict, current_user: models.User = Depends(get_current_user)):
    result = await services.payment_service.process_saba_pay(payment_data)
    return result
