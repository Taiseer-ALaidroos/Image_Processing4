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



# ---------------------------
# رفع الصورة
# ---------------------------
st.title("✂️ كشف الحواف")
st.markdown("""
<div style='border: 4px solid #ff4500; border-radius:25px; padding:35px; margin:25px 0; background-color:#1b1b1b; box-shadow: 0 0 50px #ff4500;'>

<h1 style='color:#ffa500; font-size:46px; text-align:center; text-shadow: 3px 3px 12px #000; margin-bottom: 40px;'>
✂️ كشف الحواف على الصور
</h1>

<p style='font-size:26px; color:#f5f5f5; line-height:2;'>
🖼️ هذا البرنامج التفاعلي باستخدام <b>Streamlit وOpenCV</b> يسمح للمستخدم برفع صورة أو استخدام صورة افتراضية للعرض والمعالجة.
</p>

<p style='font-size:26px; color:#90ee90; line-height:2;'>
🌟 يمكن تحويل الصورة أولاً إلى <b>رمادي</b> لتسهيل معالجة الحواف، ثم اختيار طريقة كشف الحافة مثل <b>Sobel</b> لاكتشاف التغيرات الأفقية والعمودية، 
<b>Laplacian</b> لاكتشاف التغيرات الكلية، أو <b>Canny</b> الذي يعتمد على العتبات لتحديد الحواف الدقيقة.
</p>

<p style='font-size:26px; color:#ff6f61; line-height:2;'>
🔧 يمكن التحكم بالعتبات العليا والدنيا في طريقة <b>Canny</b> لتحديد حساسية الكشف، ويعرض البرنامج الصورة الأصلية والصورة بعد تطبيق الكشف للمقارنة.
</p>

<p style='font-size:26px; color:#dda0dd; line-height:2;'>
💾 البرنامج يتيح حفظ الصورة بعد كشف الحواف، وجميع العمليات تفاعلية عبر قوائم وشريط منزلق دون الحاجة لكتابة أي كود، مما يجعل التجربة تعليمية وعملية في نفس الوقت.
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

    # تحويل الصورة للعمل عليها
    working_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # تعديل السطوع والتباين
    brightness = st.slider("تحكم بالسطوع", -100, 100, 0)
    contrast = st.slider("تحكم بالتباين", 0.5, 3.0, 1.0)
    adjusted_img = cv2.convertScaleAbs(working_img, alpha=contrast, beta=brightness)

    st.image(adjusted_img, caption="الصورة بعد السطوع والتباين", use_column_width=True)

    # اختيار طريقة كشف الحواف
    edge_type = st.selectbox("اختر نوع كشف الحافة", ["Sobel", "Laplacian", "Canny"])
    filtered_img = adjusted_img.copy()

    if edge_type == "Sobel":
        grad_x = cv2.Sobel(filtered_img, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(filtered_img, cv2.CV_64F, 0, 1, ksize=3)
        filtered_img = cv2.magnitude(grad_x, grad_y)
        filtered_img = np.uint8(np.clip(filtered_img, 0, 255))
    elif edge_type == "Laplacian":
        filtered_img = cv2.Laplacian(filtered_img, cv2.CV_64F)
        filtered_img = np.uint8(np.clip(filtered_img, 0, 255))
    elif edge_type == "Canny":
        lower = st.slider("Lower Threshold", 0, 255, 50)
        upper = st.slider("Upper Threshold", 0, 255, 150)
        filtered_img = cv2.Canny(filtered_img, lower, upper)

    st.image(filtered_img, caption=f"الصورة بعد كشف الحواف ({edge_type})", use_column_width=True)

    # حفظ الصورة بعد كشف الحواف
    pil_image = Image.fromarray(filtered_img)
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    st.download_button(
        label=f"حفظ الصورة بعد كشف الحواف ({edge_type})",
        data=buf.getvalue(),
        file_name=f"{edge_type}_edges.png",
        mime="image/png"
    )

else:
    st.write("لم يتم تحميل الصورة بعد.")