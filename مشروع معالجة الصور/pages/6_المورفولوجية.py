import io
from PIL import Image
import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="محاضرات معالجة الصور", layout="wide")
st.title("سلسلة محاضرات معالجة الصور")

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

st.title("🔬 العمليات المورفولوجية")
st.markdown("""
<div style='border: 4px solid #ff8c00; border-radius:25px; padding:35px; margin:25px 0; background-color:#121212; box-shadow: 0 0 50px #ff8c00;'>

<h1 style='color:#ffa500; font-size:46px; text-align:center; text-shadow: 3px 3px 12px #000; margin-bottom: 40px;'>
🔧 العمليات المورفولوجية على الصور
</h1>

<p style='font-size:26px; color:#f5f5f5; line-height:2;'>
🖼️ هذا البرنامج التفاعلي باستخدام <b>Streamlit وOpenCV</b> يتيح للمستخدم رفع صورة أو استخدام صورة افتراضية للعرض والمعالجة.
</p>

<p style='font-size:26px; color:#90ee90; line-height:2;'>
🌟 يمكن تحويل الصورة أولاً إلى <b>رمادي</b> ثم إلى <b>ثنائية Binary</b> باستخدام Threshold لتسهيل تطبيق العمليات المورفولوجية على الصورة.
</p>

<p style='font-size:26px; color:#ff6f61; line-height:2;'>
🔹 يوفر البرنامج أربع عمليات مورفولوجية أساسية: 
<b>Erosion</b> لتقليص الكائنات، 
<b>Dilation</b> لتوسيعها، 
<b>Opening</b> لإزالة الضوضاء الصغيرة، و
<b>Closing</b> لملء الفراغات.
</p>

<p style='font-size:26px; color:#dda0dd; line-height:2;'>
⚙️ يمكن التحكم بحجم العنصر البنائي <b>Kernel</b> لتغيير تأثير العملية، ويعرض البرنامج الصورة الثنائية قبل وبعد التطبيق للمقارنة.
</p>

<p style='font-size:26px; color:#00fa9a; line-height:2;'>
💾 جميع العمليات تفاعلية عبر القوائم وشريط المنزلق، مع إمكانية حفظ الصورة النهائية بعد المعالجة بسهولة دون الحاجة لكتابة أي كود.
</p>

</div>
""", unsafe_allow_html=True)



# ---------------------------
# رفع الصورة
# ---------------------------
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])

if uploaded_file is None:
    img = cv2.imread("default_image.jpg")  # ضع صورة افتراضية في نفس المجلد
    if img is not None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
else:
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)



# ---------------------------
# عرض الصورة الأصلية ومعلوماتها
# ---------------------------
if img is not None:
    st.image(img, caption="الصورة المختارة", use_column_width=True)
    st.write("أبعاد الصورة:", img.shape)

    # ---------------------------
    # تحويل الصورة إلى رمادي باستخدام checkbox
    # ---------------------------
    convert_gray = st.checkbox("تحويل إلى رمادي")
    if convert_gray:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        st.image(gray, caption="الصورة الرمادية", use_column_width=True)

        # شريط منزلق لتعديل السطوع
        brightness = st.slider("تحكم بالسطوع", 0, 200, 100)  # 100% افتراضي
        adjusted = cv2.convertScaleAbs(gray, alpha=brightness/100, beta=0)
        st.image(adjusted, caption=f"الصورة بعد تعديل السطوع ({brightness}%)", use_column_width=True)

        # زر حفظ الصورة الرمادية
        pil_image = Image.fromarray(adjusted)
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="حفظ الصورة الرمادية",
            data=byte_im,
            file_name="gray_image.png",
            mime="image/png"
        )



        # ---------------------------
    # العمليات المورفولوجية (Morphological Ops)
    # ---------------------------
    st.subheader("العمليات المورفولوجية (Morphological Operations)")

    # تحويل إلى Gray لو مش محول
    if convert_gray and 'adjusted' in locals():
        morph_img = adjusted.copy()
    else:
        morph_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # تحويل إلى Binary (Threshold)
    _, binary_img = cv2.threshold(morph_img, 127, 255, cv2.THRESH_BINARY)

    # اختيار العملية
    morph_type = st.selectbox("اختر العملية المورفولوجية", ["Erosion", "Dilation", "Opening", "Closing"])

    # التحكم بحجم العنصر البنائي
    k_size = st.slider("حجم الـ Kernel", 1, 15, 3)
    kernel = np.ones((k_size, k_size), np.uint8)

    # تطبيق العملية المختارة
    if morph_type == "Erosion":
        result = cv2.erode(binary_img, kernel, iterations=1)
    elif morph_type == "Dilation":
        result = cv2.dilate(binary_img, kernel, iterations=1)
    elif morph_type == "Opening":
        result = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
    elif morph_type == "Closing":
        result = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    # عرض قبل/بعد
    st.image(binary_img, caption="الصورة الثنائية (Binary)", use_column_width=True)
    st.image(result, caption=f"النتيجة بعد {morph_type}", use_column_width=True)

    # زر حفظ الصورة بعد العملية
    pil_image = Image.fromarray(result)
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label=f"حفظ الصورة بعد {morph_type}",
        data=byte_im,
        file_name=f"{morph_type}_morph.png",
        mime="image/png"
    )


else:
    st.write("لم يتم تحميل الصورة بشكل صحيح.")