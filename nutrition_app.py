import streamlit as st

st.set_page_config(page_title="NutriSmart", layout="centered")

st.title("🥗 NutriSmart")
st.subheader("אפליקציה חכמה לתזונה בריאה")

# --- שאלון ---
st.header("📝 שאלון אישי")

name = st.text_input("שם")
age = st.number_input("גיל", 8, 100, 14)
height = st.number_input("גובה (ס״מ)", 100, 230, 160)
weight = st.number_input("משקל (ק״ג)", 30, 200, 60)

goal = st.selectbox("מה המטרה שלך?", [
    "תכנית הרזיה",
    "עלייה במשקל",
    "שמירה על אורח חיים בריא"
])

activity = st.selectbox("רמת פעילות", [
    "נמוכה",
    "בינונית",
    "גבוהה"
])

diseases = st.text_area("האם יש מחלות או מגבלות?")

# --- חישוב ---
if st.button("חשב"):
    bmi = weight / ((height / 100) ** 2)
    bmi = round(bmi, 2)

    st.header("📊 תוצאה")

    st.write(f"BMI שלך: **{bmi}**")

    if bmi < 18.5:
        st.success("תת משקל")
        st.write("מומלץ להעלות צריכת קלוריות בצורה בריאה")
    elif bmi < 25:
        st.success("משקל תקין")
        st.write("המשך כך עם תזונה מאוזנת")
    elif bmi < 30:
        st.warning("עודף משקל")
        st.write("מומלץ להפחית סוכר ולהגביר פעילות")
    else:
        st.error("השמנה")
        st.write("מומלץ לפנות לייעוץ מקצועי")

    # --- קלוריות ---
    calories = 10 * weight + 6.25 * height - 5 * age + 5

    if activity == "נמוכה":
        calories *= 1.2
    elif activity == "בינונית":
        calories *= 1.55
    else:
        calories *= 1.75

    if goal == "תכנית הרזיה":
        calories -= 300
    elif goal == "עלייה במשקל":
        calories += 300

    calories = int(calories)

    st.write(f"🍽️ יעד קלוריות יומי: **{calories}**")

    if diseases:
        st.warning("⚠️ מומלץ להתייעץ עם רופא בגלל מצב רפואי")

# --- יומן אכילה ---
st.header("🍽️ יומן אכילה")

food = st.text_input("מה אכלת?")
cal = st.number_input("כמה קלוריות?", 0, 2000)

if st.button("הוסף"):
    st.write(f"✔ נוספו: {food} ({cal} קלוריות)")

# --- מצלמה ---
st.header("📷 מצלמה")

img = st.camera_input("צלם תמונה")

if img:
    st.image(img)
    st.info("המערכת נותנת הערכה כללית בלבד, לא אבחון רפואי")
