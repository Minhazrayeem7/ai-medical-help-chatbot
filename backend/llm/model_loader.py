# IMPORTS: Load required libraries and environment variables
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# INITIALIZATION: Load environment variables
load_dotenv()

# LLM LOADER: Function to configure and return the Gemini language model
def load_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1
    )
    return llm