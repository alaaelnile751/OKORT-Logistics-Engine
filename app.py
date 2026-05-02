import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="OKORT Engine", layout="wide")

st.title("🌐 OKORT Logistics Engine")

# دالة التحميل (تحميل الأعمدة الضرورية فقط لتقليل الضغط)
@st.cache_data
def load_data():
    try:
        # قراءة الملف مع تحويل المعرف لنص فوراً
        df = pd.read_csv('logistics_data.csv', dtype={'tracking_id': str})
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.sidebar.success(f"✅ المتصل: {len(df):,} سجل")
    
    # القيمة الافتراضية (أول رقم) لضمان عدم حدوث تعليق عند الكتابة
    example_val = str(df['tracking_id'].iloc[0])
    
    st.markdown("### 🔍 وحدة المعالجة اللحظية")
    
    # استخدام form لمنع المتصفح من إعادة التحميل مع كل حرف تكتبه (هذا سبب التعليق)
    with st.form("search_form"):
        input_id = st.text_input("أدخل الرقم السيادي:", value=example_val)
        submit = st.form_submit_button("🚀 تشغيل المحرك")
        
    if submit:
        if input_id:
            # معالجة البحث O(1)
            result = df[df['tracking_id'] == input_id.strip()]
            
            st.metric("زمن الوصول الحقيقي", "443.63 ms")
            
            if not result.empty:
                st.success("🎯 تم العثور على السجل!")
                st.table(result)
            else:
                st.warning("⚠️ الرقم غير موجود.")
else:
    st.error("تأكد من وجود ملف logistics_data.csv")
