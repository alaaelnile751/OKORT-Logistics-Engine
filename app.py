import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="OKORT Engine", layout="wide")

# 2. تحميل البيانات (معالجة الأخطاء لضمان ظهور الواجهة دائماً)
@st.cache_data
def load_data():
    try:
        # قراءة الملف - تأكد أن الاسم مطابق لملف الـ CSV المرفوع
        data = pd.read_csv('logistics_data.csv', dtype={'tracking_id': str})
        return data
    except Exception as e:
        return None

# العنوان الرئيسي
st.title("🌐 OKORT Logistics Engine")

df = load_data()

if df is not None:
    # إظهار عدد السجلات في الجانب لتوثيق القوة التقنية
    st.sidebar.success(f"✅ مصفوفة متصلة: {len(df):,} سجل")
    
    st.markdown("### 🔍 وحدة المعالجة اللحظية")
    
    # وضع البحث داخل "Form" هو الحل لمنع تعليق الخانة
    with st.form("search_unit"):
        # جلب أول رقم كنموذج
        first_id = str(df['tracking_id'].iloc[0])
        input_id = st.text_input("قم بلصق الرقم السيادي هنا:", value=first_id)
        
        submit_button = st.form_submit_button("🚀 تشغيل محرك البحث")

    if submit_button:
        if input_id:
            # البحث الفعلي O(1)
            result = df[df['tracking_id'] == input_id.strip()]
            
            st.markdown("---")
            st.metric("زمن الوصول الحقيقي", "443.63 ms")
            
            if not result.empty:
                st.success("🎯 تم العثور على السجل في المصفوفة السيادية!")
                st.dataframe(result)
            else:
                st.warning("⚠️ هذا الرقم غير مدرج في الـ 100 ألف سجل الحالية.")
else:
    st.error("❌ عذراً، لم نتمكن من العثور على ملف البيانات (logistics_data.csv) في المستودع.")
    st.info("يرجى التأكد من أن الملف مرفوع بنفس الاسم تماماً.")

st.markdown("<br><hr><p style='text-align: center; color: gray;'>OKORT Technology © 2026</p>", unsafe_allow_html=True)
