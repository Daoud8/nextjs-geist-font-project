# DjibRide Backend

This is the backend service for DjibRide platform, built with FastAPI and PostgreSQL.

## Features

- Secure authentication (JWT, OTP SMS)
- User management (clients, drivers)
- Ride management APIs
- Payment integrations (Stripe, PayPal, local APIs)
- REST API for mobile and web admin
- OpenAPI documentation

## Setup

1. Create a Python virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables for database and JWT secrets
4. Run the server: `uvicorn main:app --reload`

## Project Structure

- `main.py`: FastAPI app entrypoint
- `models.py`: Database models
- `schemas.py`: Pydantic schemas
- `auth.py`: Authentication utilities
- `routes/`: API route modules
- `services/`: Business logic and integrations
- `database.py`: Database connection and session management

## Next Steps

- Implement authentication endpoints
- Implement user registration and management
- Implement ride management APIs
- Integrate payment gateways
