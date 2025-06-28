import streamlit as st
import re

# 💬 English Responses
responses_en = {
    "fever": (
        "🩺 You might have a fever.\n\n"
        "**💡 Recommendations:**\n"
        "- Stay hydrated with water or ORS.\n"
        "- Take rest in a cool room.\n"
        "- Use a wet cloth on your forehead.\n\n"
        "**🏠 Home Remedies:**\n"
        "- Drink tulsi tea or herbal decoction.\n"
        "- Avoid spicy food.\n"
        "- Take paracetamol if needed."
    ),
    "cough": (
        "🗣️ You might have a cough.\n\n"
        "**💡 Recommendations:**\n"
        "- Drink warm water.\n"
        "- Avoid cold drinks.\n"
        "- Rest your voice.\n\n"
        "**🏠 Home Remedies:**\n"
        "- Mix honey + ginger juice + pepper.\n"
        "- Try turmeric milk.\n"
        "- Do steam inhalation."
    ),
    "stomach pain": (
        "🤕 You may have stomach pain.\n\n"
        "**💡 Recommendations:**\n"
        "- Eat light food like curd rice.\n"
        "- Avoid outside food.\n"
        "- Drink enough water.\n\n"
        "**🏠 Home Remedies:**\n"
        "- Drink ajwain or cumin water.\n"
        "- Use a warm compress.\n"
        "- Try hing in warm water."
    ),
    "headache": "Headaches are often due to stress or dehydration. Drink water and rest.",
    "cold": "It may be a common cold. Rest and drink warm fluids.",
    "vomiting": "Avoid food for a few hours. Drink water slowly.",
    "diarrhea": "Drink ORS. Consult a doctor if it continues.",
    "rash": "Could be allergy or infection. Avoid scratching.",
    "chest pain": "⚠️ Chest pain can be serious. Seek medical help immediately!",
    "dizziness": "Might be due to dehydration or low BP. Sit down and rest.",
    "sore throat": "Try warm salt water gargles and warm fluids.",
}

# 🗣️ Tamil Responses
responses_ta = {
    "fever": (
        "🩺 உங்களுக்கு காய்ச்சல் இருக்கலாம்.\n\n"
        "**💡 பரிந்துரை:**\n"
        "- அதிகமாக தண்ணீர் குடிக்கவும்.\n"
        "- தூங்கவும், ஓய்வெடுக்கவும்.\n"
        "- தலையில் ஈர துணி வைத்து குளிர்விக்கவும்.\n\n"
        "**🏠 வீட்டு வைத்தியம்:**\n"
        "- துளசி டீ அல்லது கஷாயம் குடிக்கவும்.\n"
        "- காரமான உணவை தவிர்க்கவும்.\n"
        "- தேவையானால் பராசிடமால் எடுத்துக்கொள்ளவும்."
    ),
    "cough": (
        "🗣️ உங்களுக்கு இருமல் இருக்கலாம்.\n\n"
        "**💡 பரிந்துரை:**\n"
        "- வெந்நீர் குடிக்கவும்.\n"
        "- குளிர் உணவை தவிர்க்கவும்.\n"
        "- குரலுக்கு ஓய்வளிக்கவும்.\n\n"
        "**🏠 வீட்டு வைத்தியம்:**\n"
        "- தேன் + இஞ்சி சாறு + மிளகு சேர்த்து குடிக்கவும்.\n"
        "- மஞ்சள் பால் பருகவும்.\n"
        "- நீராவி வாங்கவும்."
    ),
    "stomach pain": (
        "🤕 வயிற்று வலி இருக்கலாம்.\n\n"
        "**💡 பரிந்துரை:**\n"
        "- சாதம், தயிர் போன்ற மெதுவான உணவு சாப்பிடவும்.\n"
        "- வெளி உணவு தவிர்க்கவும்.\n"
        "- அதிகம் தண்ணீர் குடிக்கவும்.\n\n"
        "**🏠 வீட்டு வைத்தியம்:**\n"
        "- ஓமம்/சீரகம் நீர் குடிக்கவும்.\n"
        "- வெப்ப ஒத்தடம் செய்யவும்.\n"
        "- பெருங்காயம் கலந்த வெந்நீர் பருகவும்."
    ),
    "headache": "தலையழுத்தம் காரணமாக தலைவலி இருக்கலாம். ஓய்வெடுக்கவும், தண்ணீர் குடிக்கவும்.",
    "cold": "சாதாரண சளி இருக்கலாம். ஓய்வெடுக்கவும், வெந்நீர் குடிக்கவும்.",
    "vomiting": "சிறிது நேரம் உணவு தவிர்க்கவும். தண்ணீர் குடிக்கவும்.",
    "diarrhea": "ORS குடிக்கவும். நீண்ட நேரம் இருந்தால் டாக்டர் பார்க்கவும்.",
    "rash": "அலர்ஜி அல்லது தோல் தொற்று இருக்கலாம். தேய்த்தல் தவிர்க்கவும்.",
    "chest pain": "⚠️ மார்புவலி இருந்தால் உடனடியாக மருத்துவ உதவி பெறவும்.",
    "dizziness": "நீரிழைப்பு அல்லது குறைந்த இரத்த அழுத்தம் காரணமாக இருக்கலாம்.",
    "sore throat": "வெந்நீர் கருக்கல் மற்றும் சூடான சாறு பருகவும்.",
}

# 💬 Function to get response based on language
def get_medical_response(user_input, lang="English"):
    user_input = user_input.lower()
    responses = responses_en if lang == "English" else responses_ta
    for keyword, reply in responses.items():
        if keyword in user_input:
            return reply
    return {
        "English": "I'm not sure about that symptom. Please consult a medical professional.",
        "Tamil": "இந்த அறிகுறி பற்றி எனக்குத் தெரியவில்லை. தயவுசெய்து ஒரு மருத்துவ நிபுணரை அணுகவும்."
    }[lang]

# UI
st.set_page_config(page_title="MedBot - AI Medical Chat", layout="centered")
st.title("🤖 MedBot - Offline Medical Chat Assistant")

# Language Switcher
lang = st.selectbox("🌐 Choose Language / மொழியை தேர்ந்தெடுக்கவும்:", ["English", "Tamil"])

st.write("💬 Ask me about common symptoms (e.g., fever, cough, stomach pain).")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
user_input = st.text_input("Your message:" if lang == "English" else "உங்கள் செய்தி:")

# On new input, respond
if user_input and (len(st.session_state.chat_history) == 0 or user_input != st.session_state.chat_history[-2][1]):
    response = get_medical_response(user_input, lang)
    st.session_state.chat_history.append(("You" if lang == "English" else "நீங்கள்", user_input))
    st.session_state.chat_history.append(("MedBot", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender in ["You", "நீங்கள்"]:
        st.markdown(f"**🧑‍💬 {sender}:** {message}")
    else:
        st.markdown(f"**🤖 {sender}:** {message}")
