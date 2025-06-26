import random
import time

# Simple in-memory OTP store for demonstration purposes
otp_store = {}

def generate_otp(phone: str) -> str:
    otp = f"{random.randint(100000, 999999)}"
    otp_store[phone] = {"otp": otp, "timestamp": time.time()}
    # In real implementation, send OTP via SMS gateway here
    print(f"Sending OTP {otp} to phone {phone}")
    return otp

def verify_otp(phone: str, otp: str) -> bool:
    record = otp_store.get(phone)
    if not record:
        return False
    if record["otp"] == otp and (time.time() - record["timestamp"]) < 300:  # 5 minutes expiry
        del otp_store[phone]
        return True
    return False
