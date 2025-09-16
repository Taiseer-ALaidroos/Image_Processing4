import io
from PIL import Image
import streamlit as st
import cv2
import numpy as np


# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="محاضرات معالجة الصور", layout="wide")


# ---------- session_state ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------- CSS ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(to right, #0f0f0f, #1a1a1a); color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
h1 { color: #bb86fc; text-align: center; font-size: 48px; margin-bottom: 10px; }
h2 { color: #03dac6; font-size: 32px; }
p { color: #e0e0e0; font-size: 18px; line-height: 1.5; }
.stButton>button { background-color: #6200ee; color: white; border-radius: 8px; padding: 8px 16px; font-weight: bold; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)



st.title("🎨 التحويلات اللونية")
st.markdown("""
<div style='border: 4px solid #00ffff; border-radius:20px; padding:30px; margin:20px 0; background-color:#1e1e1e; box-shadow: 0 0 40px #00ffff;'>

<h1 style='color:#00ffff; font-size:48px; text-align:center; text-shadow: 2px 2px 12px #000; margin-bottom: 40px;'>
🌍 شرح تحويل الصور بين أنظمة الألوان 🎨
</h1>

<p style='font-size:26px; color:#f5f5f5; line-height:2;'>
✨ يتيح هذا القسم للمستخدم اختيار أي نظام ألوان يرغب به للصورة: 
<b style='color:#00bfff;'>RGB</b> (الألوان الأصلية)، 
<b style='color:#dcdcdc;'>Gray</b> (رمادي)، 
<b style='color:#90ee90;'>HSV</b> (Hue, Saturation, Value).
</p>

<p style='font-size:26px; color:#90ee90; line-height:2;'>
🌟 عند اختيار النظام الرمادي، يمكن تعديل <b>السطوع</b> باستخدام شريط منزلق، 
ومشاهدة تأثيره مباشرة على الصورة، مع إمكانية <u>حفظها</u>.
</p>

<p style='font-size:26px; color:#ff6f61; line-height:2;'>
🔴 إذا تم اختيار <b>RGB</b>، يتم عرض كل قناة لونية على حدة (<b>R</b>, <b>G</b>, <b>B</b>)، 
مما يسمح للمستخدم بفهم توزيع الألوان داخل الصورة بشكل بصري.
</p>

<p style='font-size:26px; color:#dda0dd; line-height:2;'>
💾 كما يمكن حفظ الصورة بعد التحويل إلى أي نظام ألوان، لتكون جاهزة للاستخدام أو المعالجة في خطوات لاحقة، 
مع المحافظة على التفاعل السهل عبر القوائم والأزرار.
</p>

</div>
""", unsafe_allow_html=True)





uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])

if uploaded_file is None:
    img = None
else:
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)

if img is not None:
    st.image(img, caption="الصورة المختارة", use_column_width=True)
    st.write("أبعاد الصورة:", img.shape)

    convert_gray = st.checkbox("تحويل إلى رمادي")
    if convert_gray:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        st.image(gray, caption="الصورة الرمادية", use_column_width=True)

        brightness = st.slider("تحكم بالسطوع", 0, 200, 100)
        adjusted = cv2.convertScaleAbs(gray, alpha=brightness/100, beta=0)
        st.image(adjusted, caption=f"الصورة بعد تعديل السطوع ({brightness}%)", use_column_width=True)

        pil_image = Image.fromarray(adjusted)
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        st.download_button("حفظ الصورة الرمادية", data=buf.getvalue(), file_name="gray_image.png", mime="image/png")

    convert_to = st.selectbox("اختر نظام الألوان للتحويل", ["RGB", "Gray", "HSV"])
    if convert_to == "Gray":
        converted = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    elif convert_to == "HSV":
        converted = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    else:
        converted = img

    st.image(converted, caption=f"الصورة بعد التحويل إلى {convert_to}", use_column_width=True)

    if convert_to == "RGB":
        r, g, b = cv2.split(img)
        st.image(r, caption="القناة R", use_column_width=True)
        st.image(g, caption="القناة G", use_column_width=True)
        st.image(b, caption="القناة B", use_column_width=True)

    if len(converted.shape) == 2:
        pil_image = Image.fromarray(converted)
    else:
        pil_image = Image.fromarray(cv2.cvtColor(converted, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    st.download_button(f"حفظ الصورة بعد التحويل إلى {convert_to}", data=buf.getvalue(), file_name=f"{convert_to}_image.png", mime="image/png")

else:
    st.write("لم يتم تحميل الصورة بعد.")


