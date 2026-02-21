import streamlit as st
from google import genai
from google.genai.types import GenerateContentConfig

# ---------------------------
# Configure API Key
# ---------------------------
client = genai.Client(api_key=st.secrets["API_KEY"])

# ---------------------------
# Streamlit Session Storage
# ---------------------------
if "user_health_data" not in st.session_state:
    st.session_state.user_health_data = {}

# ---------------------------
# Severity Analyzer
# ---------------------------
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

# ---------------------------
# UI
# ---------------------------
st.title("👨‍⚕️ Doctor AI Agent")
st.write("Type your symptoms below to get medical guidance.")

user_input = st.text_area("Enter your symptoms:")

if st.button("Get Diagnosis") and user_input:

    severity = analyze_severity(user_input)

    prompt = f"""
    You are an AI Medical Doctor specializing in Modern Medicine, Ayurveda, Yoga, and Alternative Healing.

    User's Symptoms: {user_input}
    Severity Level: {severity.upper()}

    Provide:
    1. Possible Causes
    2. Treatment (Modern + Ayurveda)
    3. Medications (General Only)
    4. Natural Remedies
    5. Alternative Therapies
    6. Diet Recommendations
    7. Preventive Measures
    8. Health Risk Level
    9. Emergency Alert (if severe)
    10. Next Steps

    Keep it clear and professional.
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

    # Store history
    st.session_state.user_health_data[user_input] = {
        "severity": severity,
        "response": diagnosis
    }

    st.subheader("👨‍⚕️ Doctor's Response:")
    st.write(diagnosis)

    # Smart Reminders
    if "hydration" in user_input.lower():
        st.info("💧 Reminder: Drink 2-3 liters of water daily.")
    if "sleep" in user_input.lower():
        st.info("🛌 Reminder: Aim for 7-9 hours of sleep.")
