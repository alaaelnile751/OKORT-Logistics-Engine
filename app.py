import streamlit as st
import pandas as pd
import random
import string
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="OKORT Logistics BI", layout="wide")

# --- محرك توليد البيانات التجاري ---
@st.cache_data
def generate_business_data():
    size = 100000 
    customers = ['أحمد محمد علي', 'سارة محمود حسن', 'شركة النيل للتجارة', 'مؤسسة الأمل', 'إبراهيم علي', 'ليلى حسن']
    products = ['هاتف ذكي S24', 'لابتوب ديل XPS', 'ساعة ذكية Pro', 'سماعات لاسلكية', 'شاشة 4K LG']
    cities = ['القاهرة', 'الإسكندرية', 'المنصورة', 'أسوان', 'دبي', 'الرياض']
    
    data = {
        'الرقم السيادي (Sovereign ID)': ['ID' + ''.join(random.choices(string.digits, k=200)) for _ in range(size)],
        'العميل': [random.choice(customers) for _ in range(size)],
        'المنتج': [random.choice(products) for _ in range(size)],
        'التكلفة': [random.uniform(1000, 50000) for _ in range(size)],
        'المصدر': [random.choice(cities) for _ in range(size)],
        'الوجهة': [random.choice(cities) for _ in range(size)],
        'حالة الدفع': [random.choice(['مدفوع ✅', 'عند الاستلام 💵']) for _ in range(size)],
        'الموعد المخطط (ساعة)': [random.randint(24, 72) for _ in range(size)],
        'الموعد الفعلي (ساعة)': [random.randint(20, 80) for _ in range(size)], # لتوليد تأخيرات عشوائية
    }
    
    df = pd.DataFrame(data)
    df['الضريبة (14%)'] = (df['التكلفة'] * 0.14).round(2)
    df['الإجمالي'] = (df['التكلفة'] + df['الضريبة (14%)']).round(2)
    # حساب الفارق (Performance Gap)
    df['الفارق الزمني'] = df['الموعد الفعلي (ساعة)'] - df['الموعد المخطط (ساعة)']
    df['حالة التوصيل'] = df['الفارق الزمني'].apply(lambda x: 'تأخير ⚠️' if x > 0 else 'في الموعد ✅')
    
    return df

with st.spinner("🚀 جاري معالجة البيانات التجارية..."):
    df = generate_business_data()

st.title("📊 نظام OKORT للإدارة اللوجستية الذكية")
st.markdown("---")

# --- 1. لوحة تقارير الإدارة (Executive Insights) ---
st.subheader("📈 تقارير الأداء العام (نظرة إدارية)")
c1, c2, c3, c4 = st.columns(4)

with c1:
    total_rev = df['الإجمالي'].sum()
    st.metric("إجمالي التدفق المالي", f"{total_rev:,.0f} ج.م")
with c2:
    total_tax = df['الضريبة (14%)'].sum()
    st.metric("إجمالي الضرائب المستحقة", f"{total_tax:,.0f} ج.م")
with c3:
    on_time_rate = (len(df[df['حالة التوصيل'] == 'في الموعد ✅']) / len(df)) * 100
    st.metric("كفاءة التوصيل (KPI)", f"{on_time_rate:.1f}%")
with c4:
    st.metric("إجمالي العمليات", f"{len(df):,}")

st.divider()

# --- 2. محرك البحث والتحقق من الشحنة ---
st.subheader("🔍 الاستعلام التفصيلي ومطابقة الأداء")
with st.form("biz_search"):
    target = st.text_input("أدخل الرقم السيادي للشحنة للتحليل:")
    submit = st.form_submit_button("🚀 تحليل البيانات اللحظي")

if submit:
    res = df[df['الرقم السيادي (Sovereign ID)'] == target.strip()]
    if not res.empty:
        r = res.iloc[0]
        st.success("🎯 تم استدعاء السجل ومطابقته بنجاح")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 📦 تفاصيل الشحنة")
            st.write(f"**العميل:** {r['العميل']}")
            st.write(f"**المنتج:** {r['المنتج']}")
            st.write(f"**المسار:** من {r['المصدر']} إلى {r['الوجهة']}")
            st.info(f"💰 **الإجمالي المالي:** {r['الإجمالي']:,} ج.م ({r['حالة الدفع']})")
            
        with col_b:
            st.markdown("#### ⏱️ تحليل الأداء (مخطط vs فعلي)")
            st.write(f"**الموعد المخطط:** {r['الموعد المخطط (ساعة)']} ساعة")
            st.write(f"**الموعد الفعلي:** {r['الموعد الفعلي (ساعة)']} ساعة")
            
            diff = r['الفارق الزمني']
            if diff > 0:
                st.error(f"⚠️ هناك تأخير قدره {diff} ساعة عن المخطط")
            else:
                st.success(f"✅ تم التسليم قبل الموعد بـ {abs(diff)} ساعة")
    else:
        st.error("⚠️ الرقم غير موجود.")

# --- 3. تصدير التقارير ---
st.sidebar.header("📥 مركز التقارير")
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.head(5000).to_excel(writer, index=False, sheet_name='Logistics_Report')
    return output.getvalue()

st.sidebar.download_button(
    label="📊 تحميل تقرير الأداء (Excel)",
    data=to_excel(df),
    file_name='OKORT_Business_Report.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
