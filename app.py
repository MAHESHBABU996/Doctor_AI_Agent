import streamlit as st
from google import genai
from google.genai.types import GenerateContentConfig

# Configure API
client = genai.Client(api_key=st.secrets["API_KEY"])

if "user_health_data" not in st.session_state:
    st.session_state.user_health_data = {}

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

st.title("👨‍⚕️ Doctor AI Agent")
st.write("Type your symptoms below to get medical guidance.")

user_input = st.text_area("Enter your symptoms:")

if st.button("Get Diagnosis") and user_input:

    severity = analyze_severity(user_input)

    prompt = f"""
    You are an AI Medical Doctor.

    Symptoms: {user_input}
    Severity: {severity}

    Provide:
    1. Possible Causes
    2. Treatment
    3. Medications (general only)
    4. Natural remedies
    5. Diet advice
    6. Risk level
    7. When to see a doctor
    """

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1024,
            ),
        )

        diagnosis = response.text

    except Exception as e:
        diagnosis = f"⚠️ Error: {str(e)}"

    st.subheader("👨‍⚕️ Doctor's Response:")
    st.write(diagnosis)
