import streamlit as st

# ---------- הגדרות ----------
st.set_page_config(page_title="NutriSmart", layout="centered")

# ---------- שפות ----------
languages = {
    "עברית": {
        "title": "NutriSmart",
        "subtitle": "אפליקציה חכמה לתזונה בריאה",
        "name": "שם",
        "age": "גיל",
        "height": "גובה (ס״מ)",
        "weight": "משקל (ק״ג)",
        "goal": "מה המטרה שלך?",
        "activity": "רמת פעילות",
        "diseases": "האם יש מחלות?",
        "button": "חשב תוצאה",
        "result": "התוצאה שלך",
        "food": "מה אכלת?",
        "cal": "כמה קלוריות?",
        "camera": "צלם תמונה",
    },
    "English": {
        "title": "NutriSmart",
        "subtitle": "Smart Healthy Nutrition App",
        "name": "Name",
        "age": "Age",
        "height": "Height",
        "weight": "Weight",
        "goal": "Your goal",
        "activity": "Activity level",
        "diseases": "Any diseases?",
        "button": "Calculate",
        "result": "Your Result",
        "food": "What did you eat?",
        "cal": "Calories",
        "camera": "Take photo",
    },
    "العربية": {
        "title": "NutriSmart",
        "subtitle": "تطبيق ذكي للتغذية الصحية",
        "name": "الاسم",
        "age": "العمر",
        "height": "الطول",
        "weight": "الوزن",
        "goal": "ما هدفك؟",
        "activity": "مستوى النشاط",
        "diseases": "هل لديك أمراض؟",
        "button": "احسب",
        "result": "النتيجة",
        "food": "ماذا أكلت؟",
        "cal": "كم سعر حراري؟",
        "camera": "التقاط صورة",
    }
}

# ---------- בחירת שפה ----------
lang = st.selectbox("🌐 Language / שפה / اللغة", list(languages.keys()))
t = languages[lang]

# ---------- עיצוב ----------
st.markdown("""
<style>
body {
    direction: rtl;
}
.main-title {
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    color: #2d6a4f;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    color: gray;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- כותרת ----------
st.markdown(f"<div class='main-title'>🥗 {t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

# ---------- שאלון ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

name = st.text_input(t["name"])
age = st.number_input(t["age"], 8, 100, 14)
height = st.number_input(t["height"], 100, 230, 160)
weight = st.number_input(t["weight"], 30, 200, 60)

goal = st.selectbox(t["goal"], ["הרזיה", "עלייה במשקל", "שמירה"])
activity = st.selectbox(t["activity"], ["נמוכה", "בינונית", "גבוהה"])
diseases = st.text_area(t["diseases"])

if st.button(t["button"]):
    bmi = round(weight / ((height / 100) ** 2), 2)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(t["result"])
    st.write(f"BMI: {bmi}")

    if bmi < 18.5:
        st.success("תת משקל")
    elif bmi < 25:
        st.success("תקין")
    elif bmi < 30:
        st.warning("עודף משקל")
    else:
        st.error("השמנה")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- יומן אכילה ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("🍽️ יומן אכילה")

food = st.text_input(t["food"])
cal = st.number_input(t["cal"], 0, 2000)

if st.button("➕ הוסף"):
    st.write(f"{food} - {cal} קלוריות")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- מצלמה ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.subheader("📷 מצלמה")

img = st.camera_input(t["camera"])

if img:
    st.image(img)
    st.info("הערכה כללית בלבד")

st.markdown("</div>", unsafe_allow_html=True)
