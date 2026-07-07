import streamlit as st
from pypdf import PdfReader
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

# 1. Pydantic Schema
class Topic(BaseModel):
    name: str = Field(description="Name of the main topic")
    sub_topics: list[str] = Field(description="List of sub-topics under this main topic")

class Syllabus(BaseModel):
    subject_name: str = Field(description="The overall subject or exam name")
    topics: list[Topic] = Field(description="List of all topics in the syllabus")

# 2. PDF Extraction Function
def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# 3. LLM Analysis Function
def analyze_syllabus(raw_text: str, api_key: str):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)
    structured_llm = llm.with_structured_output(Syllabus)
    prompt = f"Analyze the following syllabus text and extract the subject name, main topics, and sub-topics.\n\nSyllabus Text:\n{raw_text}"
    return structured_llm.invoke(prompt)

# --- UI Setup ---
st.set_page_config(page_title="AI Exam Tutor", page_icon="📚", layout="centered")
st.title("📚 AI Exam Syllabus Analyzer")

with st.sidebar:
    st.header("⚙️ Settings")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")

uploaded_file = st.file_uploader("Upload Syllabus (PDF format)", type=["pdf"])

# ---------------------------------------------------------
# NEW: 4. Initialize Session State
# ---------------------------------------------------------
# We create a safe place to store our data so it survives page reloads
if "structured_data" not in st.session_state:
    st.session_state.structured_data = None

# Only run the heavy processing when the button is explicitly clicked
if st.button("Analyze Syllabus"):
    if not groq_api_key:
        st.error("Please enter your Groq API key in the sidebar first.")
    elif not uploaded_file:
        st.error("Please upload a PDF file.")
    else:
        with st.spinner("Extracting text and analyzing via Groq... ⚡"):
            try:
                raw_text = extract_text_from_pdf(uploaded_file)
                # Save the result DIRECTLY into session_state!
                st.session_state.structured_data = analyze_syllabus(raw_text, groq_api_key)
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# ---------------------------------------------------------
# NEW: 5. Display the Data from Memory
# ---------------------------------------------------------
# Now we draw the UI completely outside of the button click!
if st.session_state.structured_data:
    data = st.session_state.structured_data
    
    st.header(f"Subject: {data.subject_name}")
    st.divider()
    
    st.subheader("Your Study Roadmap")
    
    for i, topic in enumerate(data.topics):
        with st.expander(f"Module {i+1}: {topic.name}", expanded=True):
            for sub in topic.sub_topics:
                # The checkboxes will now work perfectly without resetting the app
                st.checkbox(sub, key=f"{topic.name}_{sub}")