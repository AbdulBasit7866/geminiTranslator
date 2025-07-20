import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# Streamlit UI config
st.set_page_config(page_title="🌐 AI Language Translator", layout="centered")
st.title("🌐 Language Translator with Gemini")
st.markdown("Translate text between any two languages using AI.")

# Language options
language_list = [
    "English", "Urdu", "Spanish", "French", "German", "Chinese", "Arabic", 
    "Hindi", "Russian", "Japanese", "Korean", "Portuguese", "Italian"
]

# Input UI
source_lang = st.selectbox("Select Source Language", language_list, index=0)
target_lang = st.selectbox("Select Target Language", language_list, index=1)
text_to_translate = st.text_area("Enter text to translate", height=150)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator AI."),
    ("human", "Translate the following text from {source_language} to {target_language}:\n\n{text}")
])

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Translate
if st.button("Translate"):
    if text_to_translate.strip():
        with st.spinner("Translating..."):
            response = chain.invoke({
                "source_language": source_lang,
                "target_language": target_lang,
                "text": text_to_translate.strip()
            })
            st.success("Translation Complete!")
            st.markdown("### 📝 Translated Text")
            st.text_area("", response, height=150)
    else:
        st.warning("Please enter some text to translate.")
