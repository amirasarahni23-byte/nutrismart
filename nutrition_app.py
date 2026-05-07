import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="NutriSmart", page_icon="🥗", layout="wide")

# ---------- עיצוב ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4fff7, #eef7ff);
    direction: rtl;
}
.main-box {
    background: white;
    padding: 30px;
    border-radius: 28px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.title {
    font-size: 48px;
    font-weight: 900;
    color: #1b4332;
    text-align: center;
}
.subtitle {
    font-size: 22px;
    color: #52796f;
    text-align: center;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 24px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.07);
}
.metric-card {
    background: linear-gradient(135deg, #d8f3dc, #b7e4c7);
    padding: 25px;
    border-radius: 24px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- זיכרון ----------
if "foods" not in st.session_state:
    st.session_state.foods = []

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# ---------- בחירת שפה ----------
lang = st.sidebar.selectbox("🌐 שפה / اللغة / Language", ["עברית", "العربية", "English"])

TEXT = {
    "עברית": {
        "title": "NutriSmart",
        "subtitle": "אפליקציה חכמה לתזונה בריאה",
        "form": "שאלון אישי",
        "result": "תוצאה",
        "food": "יומן אכילה חכם",
        "camera": "מצלמה",
        "about": "מידע חשוב",
    },
    "العربية": {
        "title": "NutriSmart",
        "subtitle": "تطبيق ذكي للتغذية الصحية",
        "form": "استبيان شخصي",
        "result": "النتيجة",
        "food": "يوميات الأكل الذكية",
        "camera": "الكاميرا",
        "about": "معلومات مهمة",
    },
    "English": {
        "title": "NutriSmart",
        "subtitle": "Smart healthy nutrition app",
        "form": "Questionnaire",
        "result": "Result",
        "food": "Smart Food Diary",
        "camera": "Camera",
        "about": "Important Info",
    }
}

t = TEXT[lang]

page = st.sidebar.radio(
    "Menu",
    [t["form"], t["result"], t["food"], t["camera"], t["about"]]
)

st.markdown(f"<div class='title'>🥗 {t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

# ---------- פונקציות ----------
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 2)

def bmi_status(bmi):
    if bmi < 18.5:
        return "תת משקל", "מומלץ להעלות צריכת קלוריות בצורה בריאה ומאוזנת."
    elif bmi < 25:
        return "משקל תקין", "מצב טוב. כדאי לשמור על תזונה מאוזנת ופעילות קבועה."
    elif bmi < 30:
        return "עודף משקל", "מומלץ להפחית סוכר וחטיפים ולהוסיף תנועה יומית."
    else:
        return "השמנה", "מומלץ להתייעץ עם רופא או תזונאי ולבנות תכנית מסודרת."

def estimate_calories(weight, height, age, gender, activity, goal):
    if gender == "נקבה":
        base = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        base = 10 * weight + 6.25 * height - 5 * age + 5

    factor = {"נמוכה": 1.2, "בינונית": 1.55, "גבוהה": 1.75}
    calories = base * factor.get(activity, 1.2)

    if goal == "תכנית הרזיה":
        calories -= 300
    elif goal == "עלייה במשקל":
        calories += 300

    return int(calories)

# ---------- שאלון ----------
if page == t["form"]:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.header("📝 שאלון אישי")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("שם")
        age = st.number_input("גיל", 8, 100, 14)
        gender = st.selectbox("מין", ["זכר", "נקבה", "אחר"])
        diseases = st.text_area("האם יש מחלות, אלרגיות או מגבלות בריאותיות?")

    with col2:
        height = st.number_input("גובה בס״מ", 100, 230, 160)
        weight = st.number_input("משקל בק״ג", 30, 200, 60)
        goal = st.selectbox("מה המטרה שלך?", ["תכנית הרזיה", "עלייה במשקל", "פעילות גופנית", "שמירה על אורח חיים בריא"])
        activity = st.selectbox("רמת פעילות", ["נמוכה", "בינונית", "גבוהה"])

    if st.button("חשב ושמור"):
        bmi = calculate_bmi(weight, height)
        calories = estimate_calories(weight, height, age, gender, activity, goal)

        st.session_state.user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "goal": goal,
            "activity": activity,
            "diseases": diseases,
            "bmi": bmi,
            "calories": calories
        }

        st.success("הנתונים נשמרו בהצלחה ✅")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- תוצאה ----------
elif page == t["result"]:
    data = st.session_state.user_data

    if not data:
        st.warning("קודם מלאו את השאלון.")
    else:
        status, advice = bmi_status(data["bmi"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='metric-card'>BMI<br>{data['bmi']}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='metric-card'>יעד יומי<br>{data['calories']} קלוריות</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='metric-card'>מצב<br>{status}</div>", unsafe_allow_html=True)

        st.markdown("<div class='main-box'>", unsafe_allow_html=True)
        st.subheader("המלצה כללית")
        st.write(advice)

        if data["diseases"]:
            st.warning("ציינת מצב רפואי. מומלץ להתייעץ עם רופא או תזונאי לפני שינוי משמעותי.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- יומן אכילה חכם ----------
elif page == t["food"]:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.header("🍽️ יומן אכילה חכם עם Gemini AI")

    data = st.session_state.user_data

    if not data:
        st.warning("קודם מלאו את השאלון כדי לחשב יעד קלוריות יומי.")
    else:
        daily_goal = data["calories"]
        eaten_total = sum(item["calories"] for item in st.session_state.foods)
        remaining = daily_goal - eaten_total

        col1, col2, col3 = st.columns(3)
        col1.metric("יעד יומי", f"{daily_goal} קלוריות")
        col2.metric("נאכל עד עכשיו", f"{eaten_total} קלוריות")
        col3.metric("נשאר להיום", f"{remaining} קלוריות")

        st.divider()

        st.subheader("📷 צלמי את הצלחת וכתבי מה אכלת")

        meal_text = st.text_area(
            "פירוט הארוחה",
            placeholder="לדוגמה: אורז, סלט, טחינה, לחם, ביצה, חומוס... אפשר לכתוב גם כמויות בערך."
        )

        meal_image = st.camera_input("צלמי תמונה של הצלחת")

        if st.button("חשב קלוריות בעזרת Gemini AI"):
            if not meal_text and not meal_image:
                st.warning("צריך לכתוב מה אכלת או לצלם תמונה.")
            else:
                try:
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                    prompt = f"""
                    You are a nutrition assistant for a school project.
                    Analyze the meal from the image and the written description.

                    User description:
                    {meal_text}

                    Reply in Hebrew only.

                    Give:
                    1. רשימת מאכלים שזוהו
                    2. הערכת קלוריות לכל פריט
                    3. סך קלוריות משוער
                    4. המלצה קצרה לשיפור הארוחה

                    Important:
                    This is only an estimate and not medical advice.
                    At the end, write the total calories clearly in this format:
                    TOTAL_CALORIES: number
                    """

                    contents = [prompt]

                    if meal_image:
                        image = Image.open(meal_image)
                        contents.append(image)

                    response = client.models.generate_content(
                        model="gemini-3.1-flash-lite-preview",
                        contents=contents
                    )

                    result_text = response.text
                    st.success("הניתוח הושלם ✅")
                    st.write(result_text)

                    # ניסיון לחלץ קלוריות
                    estimated_calories = 0
                    if "TOTAL_CALORIES:" in result_text:
                        try:
                            part = result_text.split("TOTAL_CALORIES:")[1]
                            estimated_calories = int("".join([c for c in part if c.isdigit()][:5]))
                        except:
                            estimated_calories = 0

                    manual_calories = st.number_input(
                        "אפשר לתקן ידנית את מספר הקלוריות אם צריך",
                        min_value=0,
                        value=estimated_calories
                    )

                    if st.button("הוסף את הארוחה ליומן"):
                        st.session_state.foods.append({
                            "description": meal_text if meal_text else "ארוחה מצולמת",
                            "calories": manual_calories
                        })
                        st.success("הארוחה נוספה ליומן ✅")

                except Exception as e:
                    st.error("יש בעיה בחיבור ל־Gemini API.")
                    st.write(e)

        st.divider()
        st.subheader("📋 הארוחות שלי היום")

        if st.session_state.foods:
            for i, item in enumerate(st.session_state.foods, 1):
                st.write(f"{i}. {item['description']} — {item['calories']} קלוריות")

            if st.button("אפס יומן יומי"):
                st.session_state.foods = []
                st.success("היומן אופס ✅")
        else:
            st.info("עדיין לא נוספו ארוחות.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- מצלמה כללית ----------
elif page == t["camera"]:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.header("📷 מצלמה")

    st.info("המצלמה כאן מיועדת לפרויקט לימודי בלבד. היא אינה מאבחנת מצב רפואי.")

    img = st.camera_input("צלם תמונה")

    if img:
        st.image(img, use_container_width=True)
        st.write("אי אפשר לקבוע מצב בריאותי מתמונה בלבד. כדאי להשתמש במדדים כמו גובה, משקל, היקף מותניים והרגלי אכילה.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- מידע ----------
elif page == t["about"]:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.header("ℹ️ מידע חשוב")

    st.write("""
    האפליקציה היא פרויקט לימודי בלבד.
    היא אינה מחליפה רופא, תזונאי או ייעוץ רפואי.
    חישוב הקלוריות בעזרת AI הוא הערכה בלבד ויכול להיות לא מדויק.
    """)

    st.warning("חשוב: אם חשפת API Key בתמונה או בקוד, מומלץ למחוק אותו וליצור מפתח חדש.")
    st.markdown("</div>", unsafe_allow_html=True)
