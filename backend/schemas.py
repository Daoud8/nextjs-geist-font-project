from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    client = "client"
    driver = "driver"
    admin = "admin"

class ServiceType(str, Enum):
    taxi = "taxi"
    carpool = "carpool"
    parcel_delivery = "parcel_delivery"
    food_delivery = "food_delivery"
    supermarket_delivery = "supermarket_delivery"
    custom_order = "custom_order"

class RideStatus(str, Enum):
    requested = "requested"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class UserBase(BaseModel):
    phone: Optional[constr(min_length=8, max_length=15)]
    email: Optional[EmailStr]
    full_name: Optional[str]

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.client

class UserUpdate(UserBase):
    is_active: Optional[bool]

class UserOut(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        orm_mode = True

class DriverProfileBase(BaseModel):
    cin: Optional[str]
    license: Optional[str]
    vehicle_registration: Optional[str]
    vehicle_photo: Optional[str]
    insurance: Optional[str]
    is_verified: Optional[bool] = False

class DriverProfileCreate(DriverProfileBase):
    pass

class DriverProfileOut(DriverProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class Location(BaseModel):
    lat: float
    lng: float
    address: Optional[str]

class RideBase(BaseModel):
    pickup_location: Location
    dropoff_location: Location
    service_type: ServiceType

class RideCreate(RideBase):
    pass

class RideOut(RideBase):
    id: int
    client_id: int
    driver_id: Optional[int]
    status: RideStatus
    fare: Optional[float]

    class Config:
        orm_mode = True
