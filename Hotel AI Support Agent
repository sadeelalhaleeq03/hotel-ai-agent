🏨 Hotel AI Support Agent
This project is a production-grade AI agent written in Python, designed to demonstrate core concepts in AI engineering:
✅ Tool Use: The agent is equipped with a tool to check real-time restaurant availability.
✅ 3-Tier Reasoning: It follows a structured logic that prioritizes safety, then speed, and finally complex tasks.
✅ Guardrails: It has built-in mechanisms for escalating urgent issues, handling errors, and providing fallback responses.
Architecture
The project's architecture is based on a clear separation of concerns, separating the core logic from the data and configuration. This makes the system easy to maintain and extend.
Key Components
agent.py (Logic Engine):
HotelSupportAgent: The main class that contains the 3-tier reasoning logic and manages the conversation.
RestaurantAvailabilityTool: A specialized tool for querying the restaurant database to check for available seats.
HotelKnowledgeBase: A class responsible for performing fast lookups in the knowledge base to answer frequently asked questions (FAQs).
config.py (Data Hub):
A centralized file containing all configurable data and settings.
This includes hotel information, the restaurant database, escalation keywords, and the knowledge base content.
Logic Flow
The agent follows a deterministic sequence to process every user query:
Plain Text
User Query
    ↓
[Contains Urgent Keywords?]: # "→ (YES) → Escalate to Human Support"
    ↓ (NO)
[Answer in Knowledge Base?]: # "→ (YES) → Provide Instant Response"
    ↓ (NO)
[Is it a Restaurant Query?]: # "→ (YES) → Execute Availability Tool → Return Result"
    ↓ (NO)
[Fallback]: # "→ Offer help from the support team"
Reasoning Approach
The agent is designed to mimic a human decision-making process by using a 3-Tier Reasoning approach, ensuring both efficiency and safety:
Tier 1: Safety First (Escalation Guard):
Before any other processing, the query is scanned for urgent keywords (e.g., complaint, emergency). If a match is found, the conversation is immediately escalated to human support. This ensures critical issues are handled by a person.
Tier 2: Speed & Efficiency (Knowledge Base):
If the query is deemed safe, the agent attempts to find a quick answer in the HotelKnowledgeBase. This path is optimized for common questions (e.g., "What time is check-in?") and provides an instant response without complex analysis.
Tier 3: Complex Tasks (Tool Use):
If no quick answer is available, the agent moves to advanced analysis. If the query is about a restaurant booking, it extracts the necessary details (restaurant name, party size) and executes the RestaurantAvailabilityTool to fetch live data.
Tier 4: Fallback:
If all tiers above fail to handle the query, the agent provides a safe fallback response, offering to connect the user with the support team. It also increments a failed attempts counter to escalate automatically if failure persists.
Design Decisions
Custom Pure Python Build (No Frameworks):
A strategic decision was made to build the agent using only pure Python, without external frameworks like LangChain or CrewAI. This approach results in a faster, lightweight application, reduces dependencies, and provides complete control over the agent's logic.
Separation of Concerns (Logic vs. Config):
All data and settings (e.g., restaurant details, KB content) are stored in a separate config.py file. This principle keeps the main agent.py file clean and focused solely on logic, while making it easy to update data without touching the core code.
Proactive Guardrails:
Instead of treating all queries equally, the agent was designed with proactive guardrails. The "Escalation Guard" as the first step is a key design choice that prevents the automated system from mishandling sensitive customer issues.
No External API Calls:
The agent operates entirely offline without making calls to any external LLMs (like OpenAI). This makes it free to run, ensures data privacy, and eliminates network latency, leading to instant responses.
