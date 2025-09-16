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

st.title("🖌️ العمليات على البكسل")

st.markdown("""
<h1 style='color:#00ffff; font-size:42px; text-align:center; text-shadow: 2px 2px 8px #000; margin-bottom:40px;'>
🖼️ شرح العمليات على البكسل 🎛️
</h1>

<div style='border: 2px solid #00bfff; border-radius:15px; padding:20px; margin-bottom:20px; background-color:#1e1e1e; box-shadow: 0 0 20px #00bfff;'>
<p style='font-size:24px; color:#f5f5f5; line-height:1.8;'>
⚡ هذا البرنامج التفاعلي المبني باستخدام 
<b style='color:#00bfff;'>Streamlit</b> و <b style='color:#ffcc00;'>OpenCV</b>  
يتيح للمستخدم رفع صورة أو استخدام صورة افتراضية للعرض والمعالجة.  
يعرض البرنامج الصورة الأصلية مع معلوماتها مثل 
<b style='color:#90ee90;'>الأبعاد</b> وعدد <b style='color:#ff6f61;'>القنوات</b> 
لتوضيح هيكل الصورة الرقمي.
</p>
</div>

<div style='border: 2px solid #90ee90; border-radius:15px; padding:20px; margin-bottom:20px; background-color:#1e1e1e; box-shadow: 0 0 20px #90ee90;'>
<p style='font-size:24px; color:#90ee90; line-height:1.8;'>
🎨 يمكن للمستخدم تحويل الصورة إلى <b>رمادي</b> والتحكم بالسطوع باستخدام شريط منزلق،  
مع إمكانية <u>حفظ النتيجة مباشرة</u>.  
كما يمكن تطبيق العمليات على البكسل مثل:  
✔️ <b>Brightness</b>  
✔️ <b>Contrast</b>  
✔️ إنشاء الصورة <b>Negative</b>  
✔️ تطبيق <b>Threshold + Otsu</b> لتبسيط الصورة.
</p>
</div>

<div style='border: 2px solid #ff6f61; border-radius:15px; padding:20px; margin-bottom:20px; background-color:#1e1e1e; box-shadow: 0 0 20px #ff6f61;'>
<p style='font-size:24px; color:#ff6f61; line-height:1.8;'>
🚀 جميع العمليات تفاعلية عبر أزرار وقوائم وشريط منزلق،  
مما يتيح تجربة تعليمية <b style='color:#00ffff;'>عملية وشيقة</b> دون الحاجة لكتابة أي كود.  
💾 كما يمكن حفظ الصورة النهائية بعد كل تعديل بسهولة.
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

    # صورة العمل (رمادي أساساً)
    working_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    brightness_px = st.slider("تحكم بالسطوع", -100, 100, 0)
    contrast_px = st.slider("تحكم بالتباين", 0.5, 3.0, 1.0)
    adjusted_img = cv2.convertScaleAbs(working_img, alpha=contrast_px, beta=brightness_px)

    apply_negative = st.checkbox("تطبيق Negative")
    if apply_negative:
        adjusted_img = 255 - adjusted_img

    apply_threshold = st.checkbox("تطبيق Threshold + Otsu")
    if apply_threshold:
        _, adjusted_img = cv2.threshold(adjusted_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    st.image(adjusted_img, caption="الصورة بعد العمليات", use_column_width=True)

    pil_image = Image.fromarray(adjusted_img)
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    st.download_button("حفظ الصورة بعد العمليات", data=buf.getvalue(), file_name="processed_image.png", mime="image/png")

else:
    st.write("لم يتم تحميل الصورة بعد.")

