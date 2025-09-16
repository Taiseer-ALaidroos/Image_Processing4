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

st.title("🔇 إزالة الضوضاء")
st.markdown("""
<div style='border: 4px solid #1e90ff; border-radius:25px; padding:35px; margin:25px 0; background-color:#121212; box-shadow: 0 0 50px #1e90ff;'>

<h1 style='color:#00ffff; font-size:46px; text-align:center; text-shadow: 3px 3px 12px #000; margin-bottom: 40px;'>
🔇 إزالة الضوضاء على الصور
</h1>

<p style='font-size:26px; color:#f5f5f5; line-height:2;'>
🖼️ هذا البرنامج التفاعلي باستخدام <b>Streamlit وOpenCV</b> يتيح للمستخدم رفع صورة أو استخدام صورة افتراضية للعرض والمعالجة.
</p>

<p style='font-size:26px; color:#90ee90; line-height:2;'>
🌟 يمكن تحويل الصورة أولاً إلى <b>رمادي</b> لتسهيل تطبيق إزالة الضوضاء، ويمكن إضافة ضوضاء صناعية مثل <b>Salt & Pepper</b> أو <b>Gaussian</b> لتجربة الفلاتر المختلفة.
</p>

<p style='font-size:26px; color:#ff6f61; line-height:2;'>
🔧 يمكن للمستخدم اختيار نوع فلتر لإزالة الضوضاء مثل <b>Median Filter</b> لتقليل التشويش النقطي أو <b>Bilateral Filter</b> للحفاظ على حواف الصورة أثناء إزالة الضوضاء.
</p>

<p style='font-size:26px; color:#dda0dd; line-height:2;'>
💾 يعرض البرنامج الصورة قبل وبعد إزالة الضوضاء، مع إمكانية التحكم بحجم <b>Kernel</b> أو معلمات الفلتر، ويتيح حفظ الصورة النهائية بسهولة.
</p>

<p style='font-size:26px; color:#00fa9a; line-height:2;'>
⚡ كل العمليات تفاعلية عبر قوائم وأزرار وشريط منزلق دون الحاجة لكتابة أي كود، مما يجعل التجربة تعليمية وعملية في الوقت نفسه.
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

    # إضافة ضوضاء إذا رغب المستخدم
    add_noise = st.checkbox("إضافة ضوضاء للصورة")
    denoise_img = adjusted_img.copy()

    if add_noise:
        noise_type = st.selectbox("اختر نوع الضوضاء", ["Salt & Pepper", "Gaussian"])
        if noise_type == "Salt & Pepper":
            s_vs_p = 0.5
            amount = 0.02
            noisy = denoise_img.copy()
            num_salt = np.ceil(amount * noisy.size * s_vs_p)
            coords = [np.random.randint(0, i-1, int(num_salt)) for i in noisy.shape]
            noisy[coords[0], coords[1]] = 255
            num_pepper = np.ceil(amount * noisy.size * (1. - s_vs_p))
            coords = [np.random.randint(0, i-1, int(num_pepper)) for i in noisy.shape]
            noisy[coords[0], coords[1]] = 0
            denoise_img = noisy
        elif noise_type == "Gaussian":
            mean = 0
            var = 10
            sigma = var**0.5
            gauss = np.random.normal(mean, sigma, denoise_img.shape).reshape(denoise_img.shape)
            denoise_img = denoise_img + gauss
            denoise_img = np.clip(denoise_img, 0, 255).astype(np.uint8)

    # اختيار فلتر إزالة الضوضاء
    filter_choice = st.selectbox("اختر فلتر لإزالة الضوضاء", ["Median Filter", "Bilateral Filter"])
    if filter_choice == "Median Filter":
        ksize = st.slider("حجم Kernel للـ Median Filter", 3, 15, 3, step=2)
        filtered_denoise = cv2.medianBlur(denoise_img, ksize)
    elif filter_choice == "Bilateral Filter":
        d = st.slider("Diameter (d) للـ Bilateral Filter", 5, 15, 9)
        sigmaColor = st.slider("SigmaColor", 25, 150, 75)
        sigmaSpace = st.slider("SigmaSpace", 25, 150, 75)
        filtered_denoise = cv2.bilateralFilter(denoise_img, d, sigmaColor, sigmaSpace)

    st.image(denoise_img, caption="الصورة قبل إزالة الضوضاء", use_column_width=True)
    st.image(filtered_denoise, caption=f"الصورة بعد تطبيق {filter_choice}", use_column_width=True)

    # حفظ الصورة بعد إزالة الضوضاء
    pil_image = Image.fromarray(filtered_denoise)
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    st.download_button(
        label=f"حفظ الصورة بعد إزالة الضوضاء",
        data=buf.getvalue(),
        file_name="denoised_image.png",
        mime="image/png"
    )

else:
    st.write("لم يتم تحميل الصورة بعد.")