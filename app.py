import streamlit as st
import google.generativeai as genai
import json
import os
import requests

# Initialize API
Authorization=st.secrets["API_KEY"]
genai.configure(api_key=Authorization)

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# Health Report Storage
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

# Streamlit UI
st.title("👨‍⚕️ AI Doctor Chatbot")
st.write("Type your symptoms below to get medical guidance.")

user_input = st.text_area("Enter your symptoms:")

if st.button("Get Diagnosis") and user_input:
    severity = analyze_severity(user_input)
    
    prompt = f"""
    You are an AI Medical Doctor specializing in **Modern Medicine, Ayurveda, Yoga, and Alternative Healing**.

    **User's Symptoms:** "{user_input}"
    **Severity Level:** {severity.upper()}

    Provide a structured response including:
    1️⃣ **Possible Causes**
    2️⃣ **Treatment (Modern + Ayurveda + Alternative)**
    3️⃣ **Medications (General Guidance Only)**
    4️⃣ **Natural Remedies (Ayurveda, Homeopathy, Herbal)**
    5️⃣ **Alternative Therapies (Yoga, Meditation, Acupressure, Naturopathy)**
    6️⃣ **Diet & Fitness Recommendations**
    7️⃣ **Preventive Measures**
    8️⃣ **Health Risk Level (High/Medium/Low)**
    9️⃣ **Emergency Alert (if symptoms are severe, suggest emergency contacts)**
    🔟 **Health Tracking & Next Steps**

    Ensure the response is **clear, professional, and easy to understand**.
    """
    
    response = model.generate_content(prompt)
    diagnosis = response.text
    
    st.session_state.user_health_data[user_input] = {
        "severity": severity,
        "response": diagnosis
    }
    
    st.subheader("👨‍⚕️ Doctor's Response:")
    st.write(diagnosis)
    
    # Smart Reminders
    if "hydration" in user_input.lower():
        st.info("💧 Reminder: Drink 2-3 liters of water daily for proper hydration!")
    elif "sleep" in user_input.lower():
        st.info("🛌 Reminder: Aim for 7-9 hours of sleep for good health!")

