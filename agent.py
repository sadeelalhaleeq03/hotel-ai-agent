"""
Hotel Support AI Agent
Demonstrates: Tool use, Reasoning, Guardrails
"""

import json
from config import (
    HOTEL_KB, RESTAURANTS, ESCALATION_KEYWORDS,
    SUPPORT_PHONE, SUPPORT_EMAIL, MAX_FAILED_ATTEMPTS
)


# ============================================================================
# TOOL 1: Restaurant Availability
# ============================================================================

class RestaurantAvailabilityTool:
    """Check restaurant availability - THE MAIN TOOL"""
    
    @staticmethod
    def check_availability(restaurant_id: str, party_size: int, time_slot: str) -> dict:
        """
        TOOL: Check if restaurant has availability for party size
        
        Args:
            restaurant_id: Restaurant identifier
            party_size: Number of people
            time_slot: Desired time
            
        Returns:
            {available: bool, seats: int, message: str}
        """
        
        # Search restaurant database
        if restaurant_id not in RESTAURANTS:
            return {
                "status": "error",
                "message": f"Restaurant '{restaurant_id}' not found",
                "available": False
            }
        
        restaurant = RESTAURANTS[restaurant_id]
        available_seats = restaurant["max_capacity"] - restaurant["current_reservations"]
        can_accommodate = available_seats >= party_size
        
        return {
            "status": "success",
            "restaurant_name": restaurant["name"],
            "cuisine": restaurant["cuisine"],
            "party_size": party_size,
            "time_slot": time_slot,
            "available": can_accommodate,
            "available_seats": available_seats,
            "message": f"{'✓ Available' if can_accommodate else '✗ Not available'} for {party_size} people at {time_slot}"
        }


# ============================================================================
# KNOWLEDGE BASE - Fast lookup (no API calls)
# ============================================================================

class HotelKnowledgeBase:
    """Quick responses for common questions"""
    
    @staticmethod
    def get_info(query: str) -> str:
        """Get answer from knowledge base"""
        
        q = query.lower()
        
        if "check-in" in q or "arrival" in q:
            return HOTEL_KB["check_in"]
        elif "check-out" in q or "departure" in q:
            return HOTEL_KB["check_out"]
        elif "pet" in q or "dog" in q or "cat" in q:
            return HOTEL_KB["pet_policy"]
        elif "cancel" in q or "refund" in q:
            return HOTEL_KB["cancellation"]
        elif "amenities" in q or "facilities" in q:
            return HOTEL_KB["amenities"]
        elif "room service" in q:
            return HOTEL_KB["room_service"]
        elif "restaurant" in q or "dining" in q:
            return HOTEL_KB["restaurants"]
        
        return None


# ============================================================================
# AI AGENT - 3-TIER REASONING
# ============================================================================

class HotelSupportAgent:
    """
    Hotel Support AI Agent
    
    Tier 1: ESCALATION GUARD (safety first)
    Tier 2: KNOWLEDGE BASE (fast path)
    Tier 3: AI REASONING (complex queries)
    """
    
    def __init__(self):
        self.failed_attempts = 0
        self.conversation_history = []
    
    def _should_escalate(self, query: str) -> bool:
        """GUARD 1: Check if urgent keywords detected"""
        is_urgent = any(kw in query.lower() for kw in ESCALATION_KEYWORDS)
        too_many_failures = self.failed_attempts >= MAX_FAILED_ATTEMPTS
        return is_urgent or too_many_failures
    
    def _check_restaurant_availability(self, query: str) -> dict:
        """TOOL: Extract restaurant info and check availability"""
        
        # Extract restaurant name
        restaurant_map = {
            "sushi": "sushi_palace",
            "grill": "the_grill",
            "bella": "la_bella",
            "italian": "la_bella",
            "spice": "spice_route",
        }
        
        restaurant_id = None
        for keyword, rest_id in restaurant_map.items():
            if keyword in query.lower():
                restaurant_id = rest_id
                break
        
        if not restaurant_id:
            return None
        
        # Extract party size
        import re
        party_match = re.search(r'(\d+)\s*(people|persons|guests)', query)
        party_size = int(party_match.group(1)) if party_match else 2
        
        # Extract time
        time_match = re.search(r'(\d+:\d+\s*(?:am|pm|AM|PM))', query)
        time_slot = time_match.group(1) if time_match else "7:00 PM"
        
        # EXECUTE TOOL
        return RestaurantAvailabilityTool.check_availability(
            restaurant_id, party_size, time_slot
        )
    
    def handle_query(self, user_query: str) -> dict:
        """
        Main query handler - 3-TIER LOGIC
        
        Returns:
            {status, message, escalated, source}
        """
        
        print(f"\n📩 Query: {user_query}")
        
        # ===== TIER 1: ESCALATION GUARD =====
        if self._should_escalate(user_query):
            self.failed_attempts = 0
            return {
                "status": "escalated",
                "message": f"🔴 This requires human support. Contact: {SUPPORT_PHONE}",
                "escalated": True,
                "source": "escalation_guard"
            }
        
        # ===== TIER 2: KNOWLEDGE BASE =====
        kb_answer = HotelKnowledgeBase.get_info(user_query)
        if kb_answer:
            self.failed_attempts = 0
            return {
                "status": "success",
                "message": kb_answer,
                "escalated": False,
                "source": "knowledge_base"
            }
        
        # ===== TIER 3: AI REASONING WITH TOOLS =====
        if "restaurant" in user_query.lower() or "availability" in user_query.lower():
            result = self._check_restaurant_availability(user_query)
            
            if result is None:
                self.failed_attempts += 1
                return {
                    "status": "uncertain",
                    "message": "Which restaurant? We have: Sushi Palace, The Grill House, La Bella Italia, or Spice Route",
                    "escalated": False,
                    "source": "fallback"
                }
            
            if result["status"] == "success":
                self.failed_attempts = 0
                
                if result["available"]:
                    message = f"✓ Great! {result['restaurant_name']} has availability for {result['party_size']} people at {result['time_slot']}. {result['available_seats']} seats available."
                else:
                    message = f"✗ {result['restaurant_name']} doesn't have availability for {result['party_size']} at {result['time_slot']}. Try another time?"
                
                return {
                    "status": "success",
                    "message": message,
                    "escalated": False,
                    "source": "tool_use"
                }
        
        # ===== FALLBACK =====
        self.failed_attempts += 1
        return {
            "status": "uncertain",
            "message": "I'm not sure about that. Would you like to speak with our support team?",
            "escalated": False,
            "source": "fallback"
        }


# ============================================================================
# INTERACTIVE TEST
# ============================================================================

def main():
    """Run interactive agent"""
    
    print("\n" + "="*60)
    print("🏨 HOTEL SUPPORT AI AGENT")
    print("="*60)
    print("\nTry these queries:")
    print("  1. 'What time is check-in?'")
    print("  2. 'Availability at Sushi Palace for 4 at 8 PM?'")
    print("  3. 'I have a complaint!'")
    print("  4. 'What amenities?'")
    print("\nType 'exit' to quit\n")
    
    agent = HotelSupportAgent()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("\nGoodbye! 👋")
            break
        
        if not user_input:
            continue
        
        response = agent.handle_query(user_input)
        
        print(f"\nAgent: {response['message']}")
        print(f"Source: {response['source']} | Escalated: {response['escalated']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
```
