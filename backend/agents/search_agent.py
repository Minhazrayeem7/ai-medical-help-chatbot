# IMPORTS: Load GenAI, Google Search tools, and environment variables
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# INITIALIZATION: Set up Google GenAI client and tools
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

from langsmith import traceable

# SEARCH AGENT: Uses a search-enabled LLM to answer general web queries
@traceable
def search_agent(query, chat_history=None):

    try:
        # QUERY PREPARATION: Combine chat history and the current user request
        context = ""
        if chat_history:
            context = "Previous Conversation History:\n"
            for msg in chat_history:
                context += f"{msg['role'].capitalize()}: {msg['content']}\n"
            context += "\n"

        system_prompt = """You are a helpful, professional AI medical assistant.
IMPORTANT INSTRUCTION: You MUST ONLY answer questions related to medical topics, health, symptoms, anatomy, treatments, or wellness.
If the user's question is NOT related to a medical or health context, you MUST politely refuse to answer and state: "I am a medical chatbot and can only assist with medical, health, and wellness related questions." Do not answer the non-medical question under any circumstances.

"""
        full_prompt = f"{system_prompt}{context}Current User Query:\n{query}"

        # GENERATION: Invoke the model with search configuration enabled
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=config
        )

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"