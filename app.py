import streamlit as st
from google import genai

# Configure API Key
client = genai.Client(api_key=st.secrets["API_KEY"])

# Severity Analyzer
def analyze_severity(symptoms):
    severity_keywords = {
        "mild": ["slight", "mild", "occasional", "light"],
        "moderate": ["frequent", "persistent", "disruptive"],
        "severe": ["severe", "intense", "chronic", "crippling"]
    }
    for level, keywords in severity_keywords.items():
        if any(word in symptoms.lower() for word in keywords):
            return level
    return "unknown"

# UI
st.title("👨‍⚕️ Doctor AI Agent")
st.write("Describe your symptoms below.")

user_input = st.text_area("Enter your symptoms:")

if st.button("Get Diagnosis") and user_input:

    severity = analyze_severity(user_input)

    prompt = f"""
    You are a professional AI medical assistant.

    Symptoms: {user_input}
    Severity: {severity}

    Provide:
    - Possible causes
    - Suggested treatments
    - General medications
    - Diet advice
    - Risk level
    - When to see a doctor
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",  # changed to pro
            contents=prompt
        )

        diagnosis = response.text

    except Exception as e:
        diagnosis = f"Error: {str(e)}"

    st.subheader("Doctor's Response")
    st.write(diagnosis)
