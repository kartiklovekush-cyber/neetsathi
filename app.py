
import streamlit as st
import pdfplumber
import google.generativeai as genai
import os

# Hugging Face के Secrets से API Key उठावल जाई
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NEET Sathi AI", page_icon="🩺")
st.title("🩺 NEET Sathi: Batch Planner")

uploaded_file = st.file_uploader("अपन NEET बैच प्लानर (PDF) अपलोड करीं", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = "".join([page.extract_text() for page in pdf.pages])
    
    prompt = f"Extract only study tasks and homework from this NEET planner: {text[:3000]}"
    response = model.generate_content(prompt)
    tasks = response.text.split('\n')

    for i, t in enumerate(tasks):
        if len(t.strip()) > 5:
            st.checkbox(f"📍 {t.strip()}", key=f"t_{i}")
