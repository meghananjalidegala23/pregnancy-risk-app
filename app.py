import streamlit as st
import joblib
import datetime

# Load Model
model = joblib.load('preg_risk_model.pkl')

st.set_page_config(page_title="Maternal Health Companion", layout="wide")

# --- SIDEBAR: WARNING NOTIFICATIONS ---
st.sidebar.header("🚨 Daily Health Alerts")
st.sidebar.warning("📱 Mobile Usage: Limit to < 2 hours to reduce eye strain/radiation.")
st.sidebar.info("💧 Hydration: Drink 10-12 glasses of water today!")

# --- MAIN PAGE TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["Health Update Chat", "Risk Assessment", "Symptoms & Food", "Reminders"])

# 1. CHAT BOX FOR HEALTH UPDATES
with tab1:
    st.header("💬 Health Update Chat")
    user_msg = st.text_input("How are you feeling today? (e.g., 'I feel tired', 'My head hurts')")
    if user_msg:
        if "head" in user_msg.lower() or "blur" in user_msg.lower():
            st.write("🤖 **Assistant:** This could be related to blood pressure. Please check your BP in the Risk tab.")
        elif "tired" in user_msg.lower():
            st.write("🤖 **Assistant:** Fatigue is normal in the 3rd trimester. Ensure you are getting 8 hours of sleep.")
        else:
            st.write("🤖 **Assistant:** Thank you for the update. Keep monitoring your vitals!")

# 2. THIRD TRIMESTER RISK LEVEL
with tab2:
    st.header("📈 3rd Trimester Risk Analysis")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 15, 50, 28)
        sbp = st.number_input("Systolic BP", 70, 200, 115)
    with col2:
        bs = st.number_input("Blood Sugar", 5.0, 20.0, 7.5)
        temp = st.number_input("Body Temp (F)", 95, 105, 98)

    if st.button("Calculate Risk"):
        pred = model.predict([[age, sbp, bs, temp]])
        if pred[0] == 2:
            st.error("HIGH RISK: Please contact your obstetrician immediately.")
        elif pred[0] == 1:
            st.warning("MODERATE RISK: Monitor symptoms closely and rest.")
        else:
            st.success("LOW RISK: Everything looks normal for the third trimester.")

# 3. SYMPTOMS & FOOD SUGGESTIONS
with tab3:
    st.header("🍎 Symptoms & Nutrition")
    symptom = st.selectbox("Select a symptom you are experiencing:", 
                           ["Swollen Feet", "Heartburn", "Back Pain", "Insomnia"])
    
    suggestions = {
        "Swollen Feet": "Reduce salt intake and keep feet elevated above heart level.",
        "Heartburn": "Eat small, frequent meals. Avoid spicy and fried foods.",
        "Back Pain": "Use a pregnancy support belt and practice gentle prenatal yoga.",
        "Insomnia": "Try a warm glass of milk and avoid screens 1 hour before bed."
    }
    st.info(f"**Suggestion:** {suggestions[symptom]}")
    
    st.subheader("🥑 Top Food Suggestions for 3rd Trimester")
    st.write("- **Iron-rich:** Spinach, Lean Meats, Beans (to prevent anemia).")
    st.write("- **Calcium:** Yogurt, Cheese, Tofu (for baby's bone growth).")
    st.write("- **DHA/Omega 3:** Salmon, Walnuts (for baby's brain development).")

# 4. WARNING NOTIFICATIONS
with tab4:
    st.header("⏲️ Activity Tracker")
    screen_time = st.slider("Hours spent on mobile today?", 0, 12, 2)
    if screen_time > 4:
        st.error("🛑 WARNING: High screen time detected. Take a break to reduce stress!")
    
    water_glasses = st.number_input("Glasses of water consumed:", 0, 20, 5)
    if water_glasses < 8:
        st.warning("⚠️ Hydration Alert: You need at least 8-10 glasses of water.")