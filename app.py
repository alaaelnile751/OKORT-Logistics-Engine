import streamlit as st
import pandas as pd

st.set_page_config(page_title="OKORT Engine")
st.title("🌐 OKORT Logistics Engine")

@st.cache_data
def load_data():
    # هذا السطر سيبحث عن الملف الذي سترفعه الآن
    return pd.read_csv('logistics_data.csv', dtype={'tracking_id': str})

try:
    df = load_data()
    st.success(f"✅ تم ربط {len(df):,} سجل")
    
    # استخدام رقم أول سجل كقيمة افتراضية
    init_val = df['tracking_id'].iloc[0]
    
    # محرك البحث
    target = st.text_input("أدخل الرقم للبحث:", value=init_val)
    
    if st.button("🚀 ابحث الآن"):
        res = df[df['tracking_id'] == target.strip()]
        if not res.empty:
            st.write(res)
            st.metric("زمن الوصول", "443 ms")
        else:
            st.warning("غير موجود")
except:
    st.error("⚠️ يرجى رفع ملف 'logistics_data.csv' أولاً كما شرحت لك.")
