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
# ---------- باقي الصفحات ----------

st.title("🧩 الفلاتر")
st.markdown("""
<div style='border: 4px solid #00ffcc; border-radius:25px; padding:35px; margin:25px 0; background-color:#1b1b1b; box-shadow: 0 0 50px #00ffcc;'>

<h1 style='color:#00ffff; font-size:46px; text-align:center; text-shadow: 3px 3px 12px #000; margin-bottom: 40px;'>
✨ شرح الفلاتر على الصور 🎨
</h1>

<p style='font-size:26px; color:#f5f5f5; line-height:2;'>
🖼️ يعرض هذا البرنامج التفاعلي الصور باستخدام <b>Streamlit وOpenCV</b> ويتيح للمستخدم رفع صورة أو استخدام صورة افتراضية للمعالجة.
</p>

<p style='font-size:26px; color:#90ee90; line-height:2;'>
🌟 يستطيع المستخدم تحويل الصورة إلى <b>رمادي</b> أولاً لتسهيل تطبيق الفلاتر، ثم اختيار نوع الفلتر مثل <b>Sharpen</b> لتوضيح التفاصيل، 
<b>Edge</b> لاكتشاف الحواف، أو <b>Blur</b> لتنعيم الصورة باستخدام <b>Gaussian Blur</b>.
</p>

<p style='font-size:26px; color:#ff6f61; line-height:2;'>
🔧 يمكن التحكم بحجم <b>Kernel</b> عند استخدام Blur لتغيير درجة التنعيم، ويعرض البرنامج الصورة الأصلية والصورة بعد تطبيق الفلتر للمقارنة.
</p>

<p style='font-size:26px; color:#dda0dd; line-height:2;'>
💾 جميع العمليات تفاعلية عبر القوائم والشريط المنزلق، مع إمكانية حفظ الصورة النهائية بعد التعديلات بسهولة، دون الحاجة لكتابة أي كود.
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

    # اختيار الفلتر
    filter_type = st.selectbox("اختر نوع الفلتر", ["Sharpen", "Blur", "Edge"])
    kernel_size = st.slider("حجم Kernel (لـ Blur فقط)", 1, 31, 3, step=2)

    filtered_img = adjusted_img.copy()
    if filter_type == "Sharpen":
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        filtered_img = cv2.filter2D(filtered_img, -1, kernel)
    elif filter_type == "Edge":
        kernel = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])
        filtered_img = cv2.filter2D(filtered_img, -1, kernel)
    elif filter_type == "Blur":
        filtered_img = cv2.GaussianBlur(filtered_img, (kernel_size, kernel_size), 0)

    st.image(filtered_img, caption=f"الصورة بعد تطبيق {filter_type}", use_column_width=True)

    # حفظ الصورة بعد الفلتر
    pil_image = Image.fromarray(filtered_img)
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    st.download_button(
        label=f"حفظ الصورة بعد {filter_type}",
        data=buf.getvalue(),
        file_name=f"{filter_type}_filtered.png",
        mime="image/png"
    )

else:
    st.write("لم يتم تحميل الصورة بعد.")