# IMPORTS & SETUP: Load environment, modify path, and import Streamlit with backend agents
import sys
import os
from dotenv import load_dotenv

load_dotenv(override=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit_geolocation import streamlit_geolocation

from backend.router.router_agent import route_query
from backend.rag.pdf_ingest import ingest_pdf, ingest_text
from backend.tools.ocr_tool import extract_text

# UI INITIALIZATION: Set app title and handle live location tracking
st.title("AI Medical Help Chatbot")

# Add the geolocation button
st.write("📍 **Share your live location for accurate emergency assistance:**")
location = streamlit_geolocation()

lat, lon = None, None
if location and location.get('latitude') is not None and location.get('longitude') is not None:
    st.session_state['lat'] = location['latitude']
    st.session_state['lon'] = location['longitude']

lat = st.session_state.get('lat')
lon = st.session_state.get('lon')

if lat is not None and lon is not None:
    st.success(f"Location captured! (Lat: {lat:.4f}, Lon: {lon:.4f})")

# CHAT INTERFACE: Display history and handle new user messages via the router agent
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask something..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from backend router, passing the chat history
    with st.spinner("Thinking..."):
        response = route_query(prompt, chat_history=st.session_state.messages, lat=lat, lon=lon)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# PDF PROCESSING: Handle document uploads and trigger knowledge base ingestion
st.subheader("Upload Medical PDF")

pdf=st.file_uploader("Upload report",type="pdf")

if pdf is not None:
    if "last_pdf" not in st.session_state or st.session_state.last_pdf != pdf.name:
        st.session_state.last_pdf = pdf.name
        
        # Clear out image cache so we prioritize this new PDF
        if "last_image" in st.session_state:
            del st.session_state["last_image"]
            
        save_path=os.path.join("data",pdf.name)

        with open(save_path,"wb") as f:
            f.write(pdf.getbuffer())

        with st.spinner("Processing PDF..."):
            msg=ingest_pdf(save_path)
            st.session_state.pdf_msg = msg
    
    if "pdf_msg" in st.session_state and "last_pdf" in st.session_state:
        st.success(st.session_state.pdf_msg)

# IMAGE PROCESSING: Handle image uploads for OCR extraction and knowledge ingestion
st.subheader("Upload Image for OCR")

image=st.file_uploader("Upload image",type=["png","jpg","jpeg"])

if image is not None:
    if "last_image" not in st.session_state or st.session_state.last_image != image.name:
        st.session_state.last_image = image.name
        
        # Clear out pdf cache so we prioritize this new Image
        if "last_pdf" in st.session_state:
            del st.session_state["last_pdf"]
            
        with st.spinner("Extracting text and updating knowledge..."):
            # Use getvalue() which doesn't consume the pointer permanently like read() across reruns,
            # or simply run it once and cache the result
            description=extract_text(image.getvalue(), image.type)
            st.session_state.image_desc = description
            
            # Ingest the image description into the knowledge base
            msg = ingest_text(description)
            st.session_state.image_msg = msg
            
    if "image_desc" in st.session_state and "last_image" in st.session_state:
        st.write("Image Description")
        st.write(st.session_state.image_desc)
    
    if "image_msg" in st.session_state and "last_image" in st.session_state:
        st.success(st.session_state.image_msg)