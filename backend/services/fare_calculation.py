# Fare calculation service for DjibRide

BASE_FARE = 50  # DJF once passenger is onboard
PER_KM_FARE = 150  # DJF per kilometer

def calculate_fare(distance_km: float) -> float:
    """
    Calculate the fare based on distance in kilometers.
    """
    if distance_km <= 0:
        return 0
    return BASE_FARE + (PER_KM_FARE * distance_km)
