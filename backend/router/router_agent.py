# IMPORTS: Load specialized agents, LLM, and tracing utilities
from backend.agents.rag_agent import rag_agent
from backend.agents.search_agent import search_agent
from backend.agents.emergency_agent import emergency_agent
from backend.llm.model_loader import load_llm
from langsmith import traceable

# ROUTER AGENT: Analyzes user query and context to select the most appropriate agent
@traceable
def route_query(query, chat_history=None, lat=None, lon=None):

    query_lower = query.lower()
    
    # Use LLM for intelligent routing
    context = ""
    if chat_history:
        context = "Recent conversation context:\n"
        for msg in chat_history[-3:]: # Last 3 messages for context
            context += f"{msg['role'].capitalize()}: {msg['content']}\n"

    # LLM CLASSIFICATION: Use the language model to determine the query intent
    try:
        llm = load_llm()
        prompt = f"""
Choose the right agent for the user's current query based on the context.
Options:
- 'emergency': Use ONLY if the user is actively experiencing symptoms, saying they feel sick/unwell right now, or asking for immediate medical help/advice for themselves (e.g., "I'm having a heart attack," "I'm bleeding," "I need an ambulance"). DO NOT classify as 'emergency' just because the user uses words like "help", "pain", or "sick" in a normal context (e.g., "Can you help me understand this?", "What is sickness?"). 
- 'rag': Use if the user asks about a specific patient, test result, uploaded medical report/pdf/prescription, personal data, or refers to "the patient", "they", "name", "age", etc.
- 'search': Use for general knowledge, general medical facts, normal chatting, greetings, wide topics, or asking for assistance with non-emergency tasks.

{context}
Current User Query: "{query}"

Output exactly one word: 'emergency', 'rag', or 'search'.
"""
        response = llm.invoke(prompt)
        intent = response.content.strip().lower()
    except Exception as e:
        intent = "search"

    if "emergency" in intent:
        # AGENT ROUTING: Execute the selected agent based on the classified intent
        return emergency_agent(query, chat_history, lat, lon)
    elif "rag" in intent:
        import os
        if os.path.exists("vector_db"):
            return rag_agent(query, chat_history)
        else:
            return search_agent(query, chat_history)

    return search_agent(query, chat_history)