import streamlit as st
from pypdf import PdfReader
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

# ---------------------------------------------------------
# 1. Pydantic Schema for Structured Output
# ---------------------------------------------------------
class Topic(BaseModel):
    name: str = Field(description="Name of the main topic")
    sub_topics: list[str] = Field(description="List of sub-topics under this main topic")
    estimated_hours: int = Field(description="Estimated number of hours to study this main topic from scratch")
    suggested_sources: list[str] = Field(description="2-3 specific books, online courses, or YouTube search terms to study this topic")

class Syllabus(BaseModel):
    subject_name: str = Field(description="The overall subject or exam name")
    total_estimated_hours: int = Field(description="Total estimated hours to complete the entire syllabus")
    topics: list[Topic] = Field(description="List of all topics in the syllabus")

# ---------------------------------------------------------
# 2. PDF Extraction Function
# ---------------------------------------------------------
def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ---------------------------------------------------------
# 3. LLM Analysis Function
# ---------------------------------------------------------
def analyze_syllabus(raw_text: str, api_key: str):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2, api_key=api_key)
    structured_llm = llm.with_structured_output(Syllabus)
    
    prompt = f"""You are an expert academic tutor. Analyze the following syllabus text and:
    1. Extract the subject name, main topics, and sub-topics.
    2. Estimate the realistic number of hours a standard student would need to study each main topic.
    3. Suggest 2-3 specific, highly-regarded study sources (e.g., standard textbooks, MIT OCW, specific YouTube channels, or well-known websites) for each main topic.
    4. Calculate the total estimated hours.
    
    Syllabus Text:
    {raw_text}"""
    
    return structured_llm.invoke(prompt)

# ---------------------------------------------------------
# 4. Streamlit UI Setup
# ---------------------------------------------------------
st.set_page_config(page_title="AI Exam Tutor", page_icon="📚", layout="centered")
st.title("📚 AI Exam Syllabus Analyzer")

# Enhanced Sidebar with Step-by-Step Instructions
with st.sidebar:
    st.header("⚙️ Settings")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")
    
    st.divider()
    
    # Instructions Section
    st.markdown("### 🔑 How to get a free Groq API Key:")
    st.markdown(
        """
        1. Go to the [Groq Console](https://console.groq.com/).
        2. Sign up or log in using your Google or GitHub account.
        3. In the left sidebar, click on **API Keys**.
        4. Click the **Create API Key** button.
        5. Name your key (e.g., *Syllabus-Helper*), click **Submit**, and copy the generated key string.
        6. Paste the copied key into the input field above!
        """
    )

uploaded_file = st.file_uploader("Upload Syllabus (PDF format)", type=["pdf"])

# Initialize Session State
if "structured_data" not in st.session_state:
    st.session_state.structured_data = None

# ---------------------------------------------------------
# 5. Execution Logic
# ---------------------------------------------------------
if st.button("Analyze Syllabus & Generate Plan"):
    if not groq_api_key:
        st.error("Please enter your Groq API key in the sidebar first.")
    elif not uploaded_file:
        st.error("Please upload a PDF file.")
    else:
        with st.spinner("Extracting text, estimating study time, and fetching sources via Groq... ⚡"):
            try:
                raw_text = extract_text_from_pdf(uploaded_file)
                st.session_state.structured_data = analyze_syllabus(raw_text, groq_api_key)
                st.success("Study Plan Generated Successfully!")
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# ---------------------------------------------------------
# 6. UI Display
# ---------------------------------------------------------
if st.session_state.structured_data:
    data = st.session_state.structured_data
    
    st.header(f"Subject: {data.subject_name}")
    st.info(f"⏳ **Total Estimated Prep Time:** {data.total_estimated_hours} Hours")
    st.divider()
    
    st.subheader("Your Intelligent Study Roadmap")
    
    for i, topic in enumerate(data.topics):
        with st.expander(f"Module {i+1}: {topic.name} ({topic.estimated_hours} hrs)", expanded=True):
            
            st.markdown("**Recommended Sources:**")
            for source in topic.suggested_sources:
                st.markdown(f"- 📖 *{source}*")
            
            st.markdown("---")
            st.markdown("**Sub-topics to cover:**")
            
            for sub in topic.sub_topics:
                st.checkbox(sub, key=f"{topic.name}_{sub}")