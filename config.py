# HOTEL AI AGENT - CONFIGURATION

# Hotel Information
HOTEL_NAME = "Sunrise Luxury Hotel"
CHECK_IN_TIME = "6:00 PM"
CHECK_OUT_TIME = "11:00 AM"

# Knowledge Base Topics
HOTEL_KB = {
    "check_in": "Check-in time is 6:00 PM",
    "check_out": "Check-out time is 11:00 AM",
    "pet_policy": "Pets allowed with $50 per night fee",
    "cancellation": "Free cancellation up to 48 hours before arrival",
    "amenities": "Amenities: Pool, Spa, WiFi, Gym, Fine dining, Business center",
    "room_service": "Room service available 24/7",
    "restaurants": "We have 4 restaurants: Sushi Palace (Japanese), The Grill House (Steakhouse), La Bella Italia (Italian), and Spice Route (Indian)"
}

# Restaurant Database
RESTAURANTS = {
    "sushi_palace": {
        "name": "Sushi Palace",
        "cuisine": "Japanese",
        "max_capacity": 30,
        "current_reservations": 8,
    },
    "the_grill": {
        "name": "The Grill House",
        "cuisine": "Steakhouse",
        "max_capacity": 50,
        "current_reservations": 45,
    },
    "la_bella": {
        "name": "La Bella Italia",
        "cuisine": "Italian",
        "max_capacity": 40,
        "current_reservations": 38,
    },
    "spice_route": {
        "name": "Spice Route",
        "cuisine": "Indian",
        "max_capacity": 60,
        "current_reservations": 25,
    },
}

# Escalation Keywords
ESCALATION_KEYWORDS = [
    "complaint",
    "dispute",
    "emergency",
    "urgent",
    "refund",
    "accident",
    "incident",
]

# Support Contact
SUPPORT_PHONE = "+1-800-SUNRISE"
SUPPORT_EMAIL = "support@hotel.com"

# Agent Settings
MAX_FAILED_ATTEMPTS = 2
MODEL = "claude-opus-4-20250805"
MAX_TOKENS = 1024


