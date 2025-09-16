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

st.title("📐 التحويلات الهندسية")
st.markdown("""
<div style='border: 4px solid #1e90ff; border-radius:25px; padding:35px; margin:25px 0; background-color:#121212; box-shadow: 0 0 50px #1e90ff;'>

<h1 style='color:#00bfff; font-size:46px; text-align:center; text-shadow: 3px 3px 12px #000; margin-bottom: 40px;'>
🛠️ التحويلات الهندسية على الصور
</h1>

<p style='font-size:26px; color:#f5f5f5; line-height:2;'>
🖼️ هذا البرنامج التفاعلي باستخدام <b>Streamlit وOpenCV</b> يسمح للمستخدم برفع صورة أو استخدام صورة افتراضية للعرض والمعالجة.
</p>

<p style='font-size:26px; color:#90ee90; line-height:2;'>
🌟 يوفر البرنامج مجموعة من التحويلات الهندسية على الصور، بما في ذلك 
<b>Translation</b> لتحريك الصورة أفقياً وعمودياً، 
<b>Rotation</b> لتدوير الصورة حول مركزها، و
<b>Scaling</b> لتكبير أو تصغير الصورة.
</p>

<p style='font-size:26px; color:#ff6f61; line-height:2;'>
🔹 كما يمكن تطبيق <b>Flipping</b> لعكس الصورة أفقيًا أو رأسيًا، و
<b>Cropping</b> لقص جزء محدد من الصورة حسب إحداثيات يحددها المستخدم.
</p>

<p style='font-size:26px; color:#dda0dd; line-height:2;'>
⚙️ يتم عرض الصورة قبل وبعد التطبيق مباشرة، مع إمكانية تعديل المعلمات مثل الزاوية، نسبة التكبير، الإزاحة، أو حدود القص باستخدام شريط منزلق تفاعلي.
</p>

<p style='font-size:26px; color:#00fa9a; line-height:2;'>
💾 جميع العمليات تفاعلية عبر قوائم وأزرار، ويتيح البرنامج حفظ الصورة الناتجة بعد أي عملية هندسية بسهولة دون الحاجة لكتابة أي كود.
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
    # التحويلات الهندسية (Geometric Transforms)
    # ---------------------------
    st.subheader("التحويلات الهندسية (Geometric Transforms)")

    # اختيار العملية
    geo_type = st.selectbox("اختر نوع التحويل", ["Translation", "Rotation", "Scaling", "Flipping", "Cropping"])

    # نسخة من الصورة للعمل عليها
    geo_img = img.copy()

    if geo_type == "Translation":
        tx = st.slider("الإزاحة الأفقية (X)", -200, 200, 50)
        ty = st.slider("الإزاحة العمودية (Y)", -200, 200, 50)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        result = cv2.warpAffine(geo_img, M, (geo_img.shape[1], geo_img.shape[0]))

    elif geo_type == "Rotation":
        angle = st.slider("زاوية الدوران", -180, 180, 45)
        center = (geo_img.shape[1] // 2, geo_img.shape[0] // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        result = cv2.warpAffine(geo_img, M, (geo_img.shape[1], geo_img.shape[0]))

    elif geo_type == "Scaling":
        scale = st.slider("نسبة التكبير/التصغير", 0.1, 3.0, 1.0)
        result = cv2.resize(geo_img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

    elif geo_type == "Flipping":
        flip_option = st.selectbox("نوع الانعكاس", ["أفقي", "رأسي"])
        if flip_option == "أفقي":
            result = cv2.flip(geo_img, 1)
        else:
            result = cv2.flip(geo_img, 0)

    elif geo_type == "Cropping":
        x_start = st.slider("بداية X", 0, geo_img.shape[1]-1, 50)
        y_start = st.slider("بداية Y", 0, geo_img.shape[0]-1, 50)
        x_end = st.slider("نهاية X", x_start+1, geo_img.shape[1], geo_img.shape[1]//2)
        y_end = st.slider("نهاية Y", y_start+1, geo_img.shape[0], geo_img.shape[0]//2)
        result = geo_img[y_start:y_end, x_start:x_end]

    # عرض الصورة
    st.image(result, caption=f"النتيجة بعد {geo_type}", use_column_width=True)

    # زر حفظ الصورة بعد العملية
    pil_image = Image.fromarray(result)
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label=f"حفظ الصورة بعد {geo_type}",
        data=byte_im,
        file_name=f"{geo_type}_geo.png",
        mime="image/png"
    )


else:
    st.write("لم يتم تحميل الصورة بشكل صحيح.")
