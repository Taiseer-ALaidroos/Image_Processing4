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

st.title("🏁 المشروع الختامي")
st.markdown("""
<div style="background-color:#121212; padding:30px; border-radius:25px; border:3px solid #1e90ff; box-shadow: 0 0 40px #1e90ff;">

<h1 style="color:#00bfff; text-align:center; font-size:48px; text-shadow: 2px 2px 10px #000; margin-bottom:30px;">
🚀 المشروع الختامي - Pipeline
</h1>

<p style="font-size:24px; color:#f5f5f5; line-height:2;">
✨ يتيح لنا رفع صورة والعمل عليها تفاعليًا عبر <b>سلسلة من العمليات</b> بالترتيب الذي تختاره المستخدم.
</p>

<p style="font-size:24px; color:#90ee90; line-height:2;">
🖼️ يمكن تحويل الصورة إلى <b>رمادي (Gray)</b>، تطبيق <b>تمويه (Blur)</b>، كشف <b>الحواف (Edges)</b>، وتنفيذ <b>العمليات المورفولوجية (Morphology)</b.
</p>

<p style="font-size:24px; color:#ff6f61; line-height:2;">
🔹 البرنامج يبدأ بالصورة الأصلية ويطبق كل عملية حسب ترتيبك، مع تحويل الصور الملونة إلى رمادية عند الحاجة.
</p>

<p style="font-size:24px; color:#dda0dd; line-height:2;">
⚙️ يتم عرض النتيجة النهائية مباشرة بعد تنفيذ جميع العمليات، مع إمكانية معاينة كل خطوة قبل الانتقال للخطوة التالية.
</p>

<p style="font-size:24px; color:#00fa9a; line-height:2;">
💾 يوفر البرنامج زر لحفظ الصورة الناتجة بصيغة PNG، سواء كانت ملونة أو رمادية، مما يجعل تجربة المعالجة التعليمية ممتعة وسهلة دون كتابة أي كود.
</p>

</div>
""", unsafe_allow_html=True)



# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])

if uploaded_file is None:
    img = cv2.imread("default_image.jpg")  # ضع صورة افتراضية في نفس المجلد
    if img is not None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
else:
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)

if img is not None:
    st.image(img, caption="الصورة الأصلية", use_column_width=True)
    
    # اختيار سلسلة العمليات بالترتيب
    pipeline_ops = st.multiselect(
        "اختر العمليات التي تريد تطبيقها بالترتيب:",
        ["Gray", "Blur", "Edges", "Morphology", "Filtering", "Geometric Transforms"]
    )

    final_img = img.copy()

    for op in pipeline_ops:
        if op == "Gray":
            final_img = cv2.cvtColor(final_img, cv2.COLOR_RGB2GRAY)
        elif op == "Blur":
            final_img = cv2.GaussianBlur(final_img, (5, 5), 0)
        elif op == "Edges":
            if len(final_img.shape) == 3:
                gray = cv2.cvtColor(final_img, cv2.COLOR_RGB2GRAY)
            else:
                gray = final_img
            final_img = cv2.Canny(gray, 100, 200)
        elif op == "Morphology":
            if len(final_img.shape) == 3:
                gray = cv2.cvtColor(final_img, cv2.COLOR_RGB2GRAY)
            else:
                gray = final_img
            _, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            kernel = np.ones((3, 3), np.uint8)
            final_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
        elif op == "Filtering":
            filter_type = st.selectbox("اختر نوع الفلتر", ["Sharpen", "Blur", "Edge"], key="filter")
            if filter_type == "Sharpen":
                kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
                final_img = cv2.filter2D(final_img, -1, kernel)
            elif filter_type == "Edge":
                kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
                final_img = cv2.filter2D(final_img, -1, kernel)
            else:  # Blur
                final_img = cv2.GaussianBlur(final_img, (5,5), 0)
        elif op == "Geometric Transforms":
            geo_type = st.selectbox("اختر نوع التحويل الهندسي", ["Rotation", "Scaling", "Flipping", "Translation"], key="geo")
            geo_img = final_img.copy()
            if geo_type == "Rotation":
                angle = st.slider("زاوية الدوران", -180, 180, 45, key="angle")
                center = (geo_img.shape[1]//2, geo_img.shape[0]//2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                final_img = cv2.warpAffine(geo_img, M, (geo_img.shape[1], geo_img.shape[0]))
            elif geo_type == "Scaling":
                scale = st.slider("نسبة التكبير/التصغير", 0.1, 3.0, 1.0, key="scale")
                final_img = cv2.resize(geo_img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
            elif geo_type == "Flipping":
                flip_option = st.selectbox("نوع الانعكاس", ["أفقي", "رأسي"], key="flip")
                final_img = cv2.flip(geo_img, 1 if flip_option=="أفقي" else 0)
            elif geo_type == "Translation":
                tx = st.slider("الإزاحة X", -200, 200, 50, key="tx")
                ty = st.slider("الإزاحة Y", -200, 200, 50, key="ty")
                M = np.float32([[1,0,tx],[0,1,ty]])
                final_img = cv2.warpAffine(geo_img, M, (geo_img.shape[1], geo_img.shape[0]))
    
    if len(pipeline_ops) > 0:
        st.image(final_img, caption=f"النتيجة النهائية بعد تنفيذ {pipeline_ops}", use_column_width=True)

        # حفظ الصورة النهائية
        pil_image = Image.fromarray(final_img if len(final_img.shape)==2 else cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="حفظ الصورة النهائية (Pipeline)",
            data=byte_im,
            file_name="final_pipeline.png",
            mime="image/png"
        )
else:
    st.write("لم يتم تحميل الصورة بشكل صحيح.")