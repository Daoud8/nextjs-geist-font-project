from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime

Base = declarative_base()

class UserRole(enum.Enum):
    client = "client"
    driver = "driver"
    admin = "admin"

class ServiceType(enum.Enum):
    taxi = "taxi"
    carpool = "carpool"
    parcel_delivery = "parcel_delivery"
    food_delivery = "food_delivery"
    supermarket_delivery = "supermarket_delivery"
    custom_order = "custom_order"

class RideStatus(enum.Enum):
    requested = "requested"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.client)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False)
    rides_as_client = relationship("Ride", back_populates="client", foreign_keys="Ride.client_id")
    rides_as_driver = relationship("Ride", back_populates="driver", foreign_keys="Ride.driver_id")

class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cin = Column(String, nullable=True)
    license = Column(String, nullable=True)
    vehicle_registration = Column(String, nullable=True)
    vehicle_photo = Column(String, nullable=True)
    insurance = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="driver_profile")

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    pickup_location = Column(JSON, nullable=False)  # e.g. {"lat": ..., "lng": ..., "address": ...}
    dropoff_location = Column(JSON, nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    status = Column(Enum(RideStatus), default=RideStatus.requested)
    fare = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    client = relationship("User", back_populates="rides_as_client", foreign_keys=[client_id])
    driver = relationship("User", back_populates="rides_as_driver", foreign_keys=[driver_id])
