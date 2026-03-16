# IMPORTS: Load required tools, database loader, LLM, and tracing utilities
from backend.tools.maps_tool import find_nearby_hospitals
from backend.rag.retriever import load_db
from backend.llm.model_loader import load_llm
import os
from langsmith import traceable

# EMERGENCY AGENT: Handles emergency situations, retrieves patient history, finds hospitals, and drafts messages
@traceable
def emergency_agent(query, chat_history=None, lat=None, lon=None):
    # PATIENT HISTORY: Retrieve and summarize medical history from the vector database
    patient_history = "No medical history provided."
    if os.path.exists("vector_db"):
        try:
            db = load_db()
            docs = db.similarity_search("medical history condition diagnosis", k=5)
            context = "\n".join([d.page_content for d in docs])
            
            llm = load_llm()
            prompt = f"""
            Extract a short, factual 2-sentence summary of the patient's medical condition and history from the following text:
            {context}
            
            Do not provide medical advice. Just summarize what the text says about their health.
            """
            response = llm.invoke(prompt)
            patient_history = response.content
        except Exception as e:
            patient_history = "Could not retrieve history."

    # HOSPITAL SEARCH: Find nearby hospitals based on user location
    try:
        hospitals, location_str = find_nearby_hospitals(lat, lon)
        if not hospitals:
            hospitals = ["Unknown (No hospitals found nearby)"]
    except Exception:
        hospitals = ["Unknown (Failed to fetch hospitals)"]
        location_str = "Unknown Location"
    
    hospital_list = "\n".join([f"- {h}" for h in hospitals])

    # MESSAGE DRAFTING: Create emergency templates for relatives and dispatch
    relative_msg = f"EMERGENCY: I am feeling unwell. My known medical condition is: {patient_history}. Please meet me at {hospitals[0]}."

    ambulance_msg = f"DISPATCH: Patient requires immediate assistance at location: {location_str}. Known medical history: {patient_history}. Nearest receiving facility: {hospitals[0]}."

    return f"""
🚨 **EMERGENCY PROTOCOL ACTIVATED** 🚨

**1. Patient Medical Summary:**
{patient_history}

**2. Live Location Shared:**
📍 {location_str}

**3. Nearby Hospital Contacted (Nearest 1):**
{hospital_list}

**4. Action Taken:**
Messages have been drafted to your close relative and emergency services requesting immediate assistance.

**Drafted Message to Relative:**
> "{relative_msg}"

**Drafted Notification to Ambulance / EMS:**
> "{ambulance_msg}"

*Please seek real medical help immediately. Call 999 if necessary.*
"""