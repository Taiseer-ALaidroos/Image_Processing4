import streamlit as st
import io
from PIL import Image
import cv2
import numpy as np

# ---------- إعداد الصفحة ----------
st.set_page_config(page_title="مشروع معالجة الصور", layout="wide", page_icon="📷")

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

# ---------- زر الرجوع ----------
def back_to_home():
    if st.session_state.page != "home":
        st.markdown("""
            <style>
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(10px); }
                100% { transform: translateY(0px); }
            }

            .back-button {
                display: inline-block;
                background-color: #1e1e1e;
                color: #00ffff;
                font-size: 22px;
                font-weight: bold;
                padding: 15px 40px;
                border-radius: 20px;
                border: 2px solid #00bfff;
                box-shadow: 2px 2px 15px #000;
                cursor: pointer;
                text-align: center;
                margin-top: 60px;
                animation: float 2s ease-in-out infinite;
                text-decoration: none;
            }

            .back-button:hover {
                background-color: #00bfff;
                color: #1e1e1e;
                transform: scale(1.1);
                box-shadow: 4px 4px 20px #00ffff;
            }

            .button-container {
                display: flex;
                justify-content: flex-start;  /* << زر اليسار */
            }
            </style>

            <div class="button-container">
                <form action="">
                    <button class="back-button" type="submit" name="back">⬅️ الرجوع للصفحة الرئيسية</button>
                </form>
            </div>
        """, unsafe_allow_html=True)


        # التعامل مع الضغط على الزر
        # if st.button("⬅️ الرجوع للصفحة الرئيسية", key="back_btn"):
        #     st.session_state.page = "home"
        #     st.experimental_rerun()






# ---------- الصفحة الرئيسية ----------
def home_page():
    # st.title("📷 مشروع معالجة الصور")
    # st.markdown("<h1>واجهة تفاعلية لجميع العمليات</h1>", unsafe_allow_html=True)
    # st.markdown("<p>استكشف كل عملية بصرياً ونصياً مع إمكانية الانتقال للتنفيذ مباشرة.</p>", unsafe_allow_html=True)

    # operations = [
    #     {"title": "التحويلات اللونية", "description": "تحويل الصورة من RGB إلى Gray أو HSV، عرض كل قناة على حدة، التحكم بالسطوع والتباين.", "image": "https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg", "key": "color_conversion"},
    #     {"title": "العمليات على البكسل", "description": "تعديل قيم البكسل مباشرة، التحكم بالسطوع والتباين، إنشاء Negative، وتطبيق Threshold.", "image": "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg", "key": "pixel_ops"},
    #     {"title": "الفلاتر", "description": "تطبيق الفلاتر المختلفة مثل Gaussian, Median, Box لتنعيم الصورة أو إبراز التفاصيل.", "image": "https://images.pexels.com/photos/207983/pexels-photo-207983.jpeg", "key": "filters"},
    #     {"title": "كشف الحواف", "description": "استخراج الحواف باستخدام Canny, Sobel, Laplacian، لمعرفة ملامح الصورة بدقة.", "image": "https://images.pexels.com/photos/34950/pexels-photo.jpg", "key": "edge_detection"},
    #     {"title": "إزالة الضوضاء", "description": "تنقية الصورة من الضوضاء باستخدام أساليب مثل Gaussian Blur أو Median Filter.", "image": "https://images.pexels.com/photos/459225/pexels-photo-459225.jpeg", "key": "denoising"},
    #     {"title": "العمليات المورفولوجية", "description": "Erosion, Dilation, Opening, Closing لتعديل الشكل الهندسي للبنية داخل الصورة.", "image": "https://images.pexels.com/photos/256381/pexels-photo-256381.jpeg", "key": "morphology"},
    #     {"title": "التحويلات الهندسية", "description": "Translation, Rotation, Scaling, Flipping, Cropping للتحكم بموقع وحجم الصورة.", "image": "https://images.pexels.com/photos/19670/pexels-photo-19670.jpeg", "key": "geometric"},
    #     {"title": "المشروع الختامي", "description": "تطبيق سلسلة العمليات في Pipeline واحد متكامل لتجربة شاملة لمعالجة الصور.", "image": "https://images.pexels.com/photos/267614/pexels-photo-267614.jpeg", "key": "final_project"},
    # ]


    # العنوان الرئيسي
    st.markdown(
        """
        <h1 style='font-size:52px; color:#00bfff; text-align:center; font-weight:bold; 
        text-shadow: 2px 2px 8px rgba(0,0,0,0.6); margin-bottom:20px;'>
            📷 مشروع معالجة الصور المتكامل
        </h1>
        """, 
        unsafe_allow_html=True
    )

    # العنوان الثانوي
    st.markdown(
        """
        <h2 style='font-size:34px; color:#f1f1f1; text-align:center; font-weight:500;
        margin-top:0; margin-bottom:20px;'>
            واجهة ضخمة وتفاعلية لجميع عمليات معالجة الصور
        </h2>
        """, 
        unsafe_allow_html=True
    )

    # الوصف
    st.markdown(
        """
        <p style='font-size:22px; color:#dcdcdc; text-align:center; line-height:1.8;
        background-color:#1e1e1e; padding:15px 25px; border-radius:12px;
        border: 1px solid #00bfff; max-width:900px; margin:auto;'>
            استكشف كل عملية <strong style="color:#ffd700;">بصرياً</strong> و<strong style="color:#90ee90;">نصياً</strong>،  
            مع إمكانية مشاهدة الفيديو وتنفيذ العملية مباشرة من خلال الواجهة
        </p>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style='background-color:#1e1e1e; border-left:6px solid #00bfff; padding:15px; border-radius:10px;'>
        <h3 style='color:#00bfff; margin-top:0;'>💡 ملاحظة هامة</h3>
        <p style='font-size:18px; color:#f1f1f1; line-height:1.6;'>
        في جميع العمليات يتم أولاً <strong style='color:#ffd700;'> تحويل الصورة إلى تدرج رمادي </strong>،
        وبعد ذلك تتم المعالجة المطلوبة.  
        إذا كنت ترغب في إجراء المعالجة على <strong style='color:#90ee90;'>الصورة الأصلية الملونة</strong>،
        فعليك الدخول إلى <strong style='color:#ff7f50;'>المشروع الختامي الضخم</strong>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


    # ---------- العمليات ----------
    operations = [
        {
            
            "title": "التحويلات اللونية المتقدمة",
            "description": """
                <h2 style='color:#00bfff;'>التحويلات اللونية المتقدمة</h2>
                <h1 style='color:#00ffff; font-size:28px;'>
                تحكم كامل في ألوان الصورة: تحويل RGB إلى Gray أو HSV، عرض كل قناة على حدة، تعديل السطوع والتباين بطريقة احترافية.
                </h1>
                <h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>
                🔹 انقر مرتين للانتقال إلى العملية التالية 🔹
                </h2>
            """,
            "image": "https://images.pexels.com/photos/207983/pexels-photo-207983.jpeg",
            "video": "https://www.youtube.com/embed/example1",
            "key": "color_conversion"


        },
        {
            
    "title": "العمليات على البكسل",
    "description": """
        <h2 style='color:#1e90ff;'>العمليات على البكسل</h2>
        <h1 style='color:#00ffff; font-size:28px;'>
        تحكم كامل في كل بكسل: تعديل قيم البكسل مباشرة، إنشاء Negative، تطبيق Threshold، وتعديل السطوع والتباين بدقة.
        </h1>
        <h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>
        🔹 انقر مرتين للانتقال إلى العملية التالية 🔹
        </h2>
    """,
    "image": "https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg",
    "video": "https://www.youtube.com/embed/example2",
    "key": "pixel_ops"


        },
       {
    "title": "الفلاتر الاحترافية",
    "description": """
        <h2 style='color:#1e90ff;'>الفلاتر الاحترافية</h2>
        <h1 style='color:#00ffff; font-size:28px;'>
        تطبيق فلاتر Gaussian, Median, Box لتنعيم الصورة أو إبراز التفاصيل الدقيقة بطريقة احترافية.
        </h1>
        <h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>
        🔹 انقر مرتين للانتقال إلى العملية التالية 🔹
        </h2>
    """,
    "image": "https://images.pexels.com/photos/2698519/pexels-photo-2698519.jpeg",
    "video": "https://www.youtube.com/embed/example3",
    "key": "filters"
}
,
        {
            
            "title": "كشف الحواف بدقة عالية",
            "description": "<h2></h2>"
            "<p>استخدام Canny, Sobel, Laplacian لاستخراج الحواف ومعرفة ملامح الصورة بوضوح ودقة متناهية.</p>"
            "<p>هذه العملية تساعد على تحديد <strong>الحدود والفواصل بين الكائنات داخل الصورة</strong>، مما يسهل تحليلها ومعالجتها لاحقًا.</p>"

            "<h3>Canny</h3>"
            "<p>يقلل الضوضاء أولاً ثم يحدد التغيرات الكبيرة في شدة البكسل للحصول على حواف دقيقة.</p>"

            "<h3>Sobel</h3>"
            "<p>يركز على التغيرات الرأسية والأفقية لتحديد اتجاهات الحواف المختلفة داخل الصورة.</p>"

            "<h3>Laplacian</h3>"
            "<p>يستخدم التغيرات الثانية في شدة الصورة لاستخراج التفاصيل الدقيقة والحواف الصغيرة جدًا.</p>"

            "<p>الهدف من هذه العملية هو <strong>إبراز ملامح الصورة بدقة عالية</strong>، مما يجعلها مفيدة لتطبيقات التعرف على الأشياء، الرؤية الحاسوبية، وتحسين نتائج المعالجة الأخرى مثل الفلاتر والتحويلات الهندسية.</p>"
            "<p><h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>        🔹 انقر مرتين للانتقال إلى العملية التالية 🔹    </h2> </p>"
            , 
            "image": "https://images.pexels.com/photos/8090298/pexels-photo-8090298.jpeg",  # صورة مناسبة لخطوط وحواف الصور
            "video": "https://www.youtube.com/embed/example4",
            "key": "edge_detection"
        

        },
        {
            "title": "إزالة الضوضاء والفلترة المتقدمة",
            "description":
            "<h1> تنقية الصورة من الضوضاء باستخدام Gaussian Blur وMedian Filter مع الحفاظ على التفاصيل المهمة.</h1>"
           "<p><h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>        🔹 انقر مرتين للانتقال إلى العملية التالية 🔹    </h2> </p>" ,
            "image": "https://images.pexels.com/photos/459225/pexels-photo-459225.jpeg",  # صورة توضح إزالة الضوضاء
            "video": "https://www.youtube.com/embed/example5",
            "key": "denoising"
        },
        {
            "title": "العمليات المورفولوجية",
            "description": "<h2>"
            "</h2>"
            "<h1>تحكم في الشكل الهندسي للبنية داخل الصورة باستخدام Erosion, Dilation, Opening, Closing بطريقة احترافية.</h1>"
           "<p><h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>        🔹 انقر مرتين للانتقال إلى العملية التالية 🔹    </h2> </p>",
            "image": "https://images.pexels.com/photos/256381/pexels-photo-256381.jpeg",  # صورة توضح التغير الهندسي للبنية
            "video": "https://www.youtube.com/embed/example6",
            "key": "morphology"
        },
        {
            "title": "التحويلات الهندسية",
            "description":"<h1>تحكم كامل في موقع وحجم الصورة: Translation, Rotation, Scaling, Flipping, Cropping بطريقة سهلة ومرنة.</h1>"
            "<p><h2 style='color:#ffd700; font-size:24px; margin-top:20px;'> 🔹 انقر مرتين للانتقال إلى العملية التالية 🔹</h2> </p>",
            "image": "https://images.pexels.com/photos/356830/pexels-photo-356830.jpeg",
            "video": "https://www.youtube.com/embed/example7",
            "key": "geometric"
        },
        {
            "title": "المشروع الختامي الضخم",
            "description":  "<h2>"
            "</h2>"
          "<h1>تطبيق جميع العمليات في Pipeline واحد متكامل لتجربة شاملة وواقعية لمعالجة الصور بطريقة احترافية.</h1>"
           "<p><h2 style='color:#ffd700; font-size:24px; margin-top:20px;'>        🔹 انقر مرتين للانتقال إلى العملية التالية 🔹    </h2> </p>",
            "image": "https://images.pexels.com/photos/267614/pexels-photo-267614.jpeg",  # صورة مناسبة للمشروع النهائي
            "video": "https://www.youtube.com/embed/example8",
            "key": "final_project"
        },
    ]


    # ---------- عرض العمليات مع الأعمدة ----------
    for op in operations:
        st.markdown(f"## {op['title']}")
        col1, col2 = st.columns(2)
        
        # العمود الأول: الصورة
        with col1:
            st.image(op['image'], caption=op['title'], use_container_width=True)

        # العمود الثاني: الفيديو + الوصف + زر الانتقال
        with col2:
            st.markdown(f"<p style='font-size:30px;'>{op['description']}</p>", unsafe_allow_html=True)
            st.video(op['video'])
            
            # زر الانتقال بدون استخدام experimental_rerun
            if st.button(f"اذهب إلى {op['title']}", key=op['key']):
                st.session_state['page'] = op['key']  # حفظ الصفحة المطلوبة
                st.stop()  # إيقاف التنفيذ لإعادة تحميل الصفحة تلقائيًا
        
        st.markdown("---")

    # for op in operations:
    #     st.markdown(f"<h2>{op['title']}</h2>", unsafe_allow_html=True)
    #     col1, col2 = st.columns([1,1])
    #     with col1:
    #         st.image(op["image"], use_column_width=True)
    #     with col2:
    #         st.markdown(f"<p>{op['description']}</p>", unsafe_allow_html=True)
    #         if st.button(f"اذهب لـ {op['title']}", key=op["key"]):
    #             st.session_state.page = op["key"]
    #     st.markdown("---")

# ---------- صفحة التحويلات اللونية ----------
def color_conversion_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
        st.write("أبعاد الصورة:", img.shape)

        convert_gray = st.checkbox("تحويل إلى رمادي")
        if convert_gray:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            st.image(gray, caption="الصورة الرمادية", use_container_width=True)

            brightness = st.slider("تحكم بالسطوع", 0, 200, 100)
            adjusted = cv2.convertScaleAbs(gray, alpha=brightness/100, beta=0)
            st.image(adjusted, caption=f"الصورة بعد تعديل السطوع ({brightness}%)", use_container_width=True)

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

        st.image(converted, caption=f"الصورة بعد التحويل إلى {convert_to}", use_container_width=True)

        if convert_to == "RGB":
            r, g, b = cv2.split(img)
            st.image(r, caption="القناة R", use_container_width=True)
            st.image(g, caption="القناة G", use_container_width=True)
            st.image(b, caption="القناة B", use_container_width=True)

        if len(converted.shape) == 2:
            pil_image = Image.fromarray(converted)
        else:
            pil_image = Image.fromarray(cv2.cvtColor(converted, cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        st.download_button(f"حفظ الصورة بعد التحويل إلى {convert_to}", data=buf.getvalue(), file_name=f"{convert_to}_image.png", mime="image/png")

    else:
        st.write("لم يتم تحميل الصورة بعد.")

# ---------- صفحة العمليات على البكسل ----------
def pixel_ops_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
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

        st.image(adjusted_img, caption="الصورة بعد العمليات", use_container_width=True)

        pil_image = Image.fromarray(adjusted_img)
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        st.download_button("حفظ الصورة بعد العمليات", data=buf.getvalue(), file_name="processed_image.png", mime="image/png")

    else:
        st.write("لم يتم تحميل الصورة بعد.")

# ---------- باقي الصفحات ----------
def filters_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
        st.write("أبعاد الصورة:", img.shape)

        # تحويل الصورة للعمل عليها
        working_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # تعديل السطوع والتباين
        brightness = st.slider("تحكم بالسطوع", -100, 100, 0)
        contrast = st.slider("تحكم بالتباين", 0.5, 3.0, 1.0)
        adjusted_img = cv2.convertScaleAbs(working_img, alpha=contrast, beta=brightness)

        st.image(adjusted_img, caption="الصورة بعد السطوع والتباين", use_container_width=True)

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

        st.image(filtered_img, caption=f"الصورة بعد تطبيق {filter_type}", use_container_width=True)

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


def edge_detection_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
        st.write("أبعاد الصورة:", img.shape)

        # تحويل الصورة للعمل عليها
        working_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # تعديل السطوع والتباين
        brightness = st.slider("تحكم بالسطوع", -100, 100, 0)
        contrast = st.slider("تحكم بالتباين", 0.5, 3.0, 1.0)
        adjusted_img = cv2.convertScaleAbs(working_img, alpha=contrast, beta=brightness)

        st.image(adjusted_img, caption="الصورة بعد السطوع والتباين", use_container_width=True)

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

        st.image(filtered_img, caption=f"الصورة بعد كشف الحواف ({edge_type})", use_container_width=True)

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

def denoising_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
        st.write("أبعاد الصورة:", img.shape)

        # تحويل الصورة للعمل عليها
        working_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # تعديل السطوع والتباين
        brightness = st.slider("تحكم بالسطوع", -100, 100, 0)
        contrast = st.slider("تحكم بالتباين", 0.5, 3.0, 1.0)
        adjusted_img = cv2.convertScaleAbs(working_img, alpha=contrast, beta=brightness)

        st.image(adjusted_img, caption="الصورة بعد السطوع والتباين", use_container_width=True)

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

        st.image(denoise_img, caption="الصورة قبل إزالة الضوضاء", use_container_width=True)
        st.image(filtered_denoise, caption=f"الصورة بعد تطبيق {filter_choice}", use_container_width=True)

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




def morphology_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
        st.write("أبعاد الصورة:", img.shape)

        # ---------------------------
        # تحويل الصورة إلى رمادي باستخدام checkbox
        # ---------------------------
        convert_gray = st.checkbox("تحويل إلى رمادي")
        if convert_gray:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            st.image(gray, caption="الصورة الرمادية", use_container_width=True)

            # شريط منزلق لتعديل السطوع
            brightness = st.slider("تحكم بالسطوع", 0, 200, 100)  # 100% افتراضي
            adjusted = cv2.convertScaleAbs(gray, alpha=brightness/100, beta=0)
            st.image(adjusted, caption=f"الصورة بعد تعديل السطوع ({brightness}%)", use_container_width=True)

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
        st.image(binary_img, caption="الصورة الثنائية (Binary)", use_container_width=True)
        st.image(result, caption=f"النتيجة بعد {morph_type}", use_container_width=True)

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


def geometric_page():
    back_to_home()
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
        st.image(img, caption="الصورة المختارة", use_container_width=True)
        st.write("أبعاد الصورة:", img.shape)

        # ---------------------------
        # تحويل الصورة إلى رمادي باستخدام checkbox
        # ---------------------------
        convert_gray = st.checkbox("تحويل إلى رمادي")
        if convert_gray:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            st.image(gray, caption="الصورة الرمادية", use_container_width=True)

            # شريط منزلق لتعديل السطوع
            brightness = st.slider("تحكم بالسطوع", 0, 200, 100)  # 100% افتراضي
            adjusted = cv2.convertScaleAbs(gray, alpha=brightness/100, beta=0)
            st.image(adjusted, caption=f"الصورة بعد تعديل السطوع ({brightness}%)", use_container_width=True)

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
        st.image(result, caption=f"النتيجة بعد {geo_type}", use_container_width=True)

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



def final_project_page():
    back_to_home()
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
        st.image(img, caption="الصورة الأصلية", use_container_width=True)
        
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
            st.image(final_img, caption=f"النتيجة النهائية بعد تنفيذ {pipeline_ops}", use_container_width=True)

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


# ---------- التوجيه ----------
pages = {
    "home": home_page,
    "color_conversion": color_conversion_page,
    "pixel_ops": pixel_ops_page,
    "filters": filters_page,
    "edge_detection": edge_detection_page,
    "denoising": denoising_page,
    "morphology": morphology_page,
    "geometric": geometric_page,
    "final_project": final_project_page
}

# عرض الصفحة الحالية
pages[st.session_state.page]()
# ----------- طباعة النص في أسفل الصفحة -----------
import streamlit as st

# باقي كود المشروع ...

# ----------- طباعة النص في أسفل الصفحة -----------
st.markdown(
    """
    <div style='
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 36px; 
        font-weight: bold;
        color: #FFD700;  /* لون ذهبي ليتباين مع الخلفية الداكنة */
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7); /* ظل للنص لزيادة وضوحه */
        background-color: rgba(0, 0, 0, 0.5); /* خلفية نصف شفافة */
        padding: 15px 0;
        z-index: 1000;
    '>
        إعداد المهندسين: تيسير العيدروس و أيهم ال قاسم
    </div>
    """,
    unsafe_allow_html=True
)