# IMPORTS: Load database, LLM dependencies, and tracing utilities
from backend.rag.retriever import load_db
from backend.llm.model_loader import load_llm
from langsmith import traceable

# RAG AGENT: Answers user queries using context from loaded medical documents
@traceable
def rag_agent(query, chat_history=None):

    # DATA RETRIEVAL: Load database and fetch relevant document chunks
    db=load_db()

    docs=db.similarity_search(query,k=3)

    context="\n\n".join([f"--- Document Chunk {i+1} ---\n{d.page_content}" for i, d in enumerate(docs)])
    
    # CHAT HISTORY: Format previous conversation history if available
    chat_context = ""
    if chat_history:
        chat_context = "Previous Conversation History:\n"
        for msg in chat_history:
            chat_context += f"{msg['role'].capitalize()}: {msg['content']}\n"

    # LLM SETUP: Load the language model and create the prompt
    llm=load_llm()

    prompt=f"""You are a helpful, professional AI medical assistant. 
Your task is to provide a comprehensive, clear, and detailed answer to the user's question based ONLY on the provided patient medical history.
IMPORTANT INSTRUCTION: You are strictly a medical chatbot. If the user's question is not related to medical topics, health, or the provided context, you must politely decline to answer and state: "I am a medical chatbot and can only assist with medical, health, and wellness related questions."
Do not hallucinate or use outside knowledge. If the answer is not contained in the history, say "I don't have enough information to answer that."

Patient Medical History Context:
{context}

{chat_context}

User's Question:
{query}

Provide a complete and well-structured answer:"""

    # GENERATION & FORMATTING: Invoke LLM and append references to the answer
    response=llm.invoke(prompt)

    answer = response.content
    references = "\n\n---\n**References (Chunks used):**\n"
    for i, doc in enumerate(docs, 1):
        references += f"\n**Chunk {i}:**\n{doc.page_content}\n"

    return answer + references