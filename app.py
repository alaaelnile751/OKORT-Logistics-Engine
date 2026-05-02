import streamlit as st
import pandas as pd
import random
import string
import io
from datetime import datetime, timedelta

st.set_page_config(page_title="OKORT Global Logistics Engine", layout="wide")

@st.cache_data
def generate_pro_data():
    random.seed(777) # بذرة ثابتة لضمان مطابقة البحث
    size = 100000 
    
    vendors = ['Samsung Global', 'Apple Inc', 'Nike HQ', 'Xiaomi Store', 'Dell Technologies']
    couriers = ['Amazon Shipping', 'DHL Express', 'Aramex', 'FedEx', 'Bosta']
    factory_countries = ['China (PRC)', 'Vietnam', 'Germany', 'USA', 'India']
    dest_countries = ['Egypt', 'Saudi Arabia', 'UAE', 'Kuwait', 'Jordan']
    
    # توليد تواريخ عشوائية احترافية
    base_date = datetime(2026, 1, 1)
    
    data = {
        'الرقم السيادي العالمي (Global PID)': ['OK-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=200)) for _ in range(size)],
        'البائع (Vendor)': [random.choice(vendors) for _ in range(size)],
        'بلد المصنع (Origin)': [random.choice(factory_countries) for _ in range(size)],
        'بلد الاستلام (Destination)': [random.choice(dest_countries) for _ in range(size)],
        'شركة الشحن (Courier)': [random.choice(couriers) for _ in range(size)],
        'تكلفة المنتج ($)': [round(random.uniform(100, 3000), 2) for _ in range(size)],
        'تكلفة الشحن ($)': [round(random.uniform(10, 200), 2) for _ in range(size)],
        # توليد الوقت والتاريخ
        'تاريخ الشحن': [base_date + timedelta(days=random.randint(0, 90), hours=random.randint(0, 23)) for _ in range(size)],
    }
    
    df = pd.DataFrame(data)
    # حساب تاريخ الاستلام (بعد 3 لـ 10 أيام من الشحن)
    df['تاريخ الاستلام'] = df['تاريخ الشحن'] + df.apply(lambda x: timedelta(days=random.randint(3, 10), hours=random.randint(0, 23)), axis=1)
    
    # المعادلات المالية والربحية (Business Intelligence)
    df['عمولة المنصة (15%)'] = (df['تكلفة المنتج ($)'] * 0.15).round(2)
    df['إجمالي التكاليف ($)'] = df['تكلفة المنتج ($)'] + df['تكلفة الشحن ($)']
    df['صافي الربح ($)'] = (df['عمولة المنصة (15%)'] - (df['تكلفة الشحن ($)'] * 0.1)).round(2) # مثال لربح المنصة بعد خصم مصاريف إدارية
    
    return df

df = generate_pro_data()

st.title("🌐 نظام OKORT للتحكم في سلاسل الإمداد الدولية")
st.markdown("---")

# --- لوحة مؤشرات الأرباح (Executive Dashboard) ---
st.subheader("📊 تحليل الربحية والتدفق المالي العالمي")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("إجمالي قيمة البضائع", f"${df['تكلفة المنتج ($)'].sum():,.0f}")
with c2:
    st.metric("صافي أرباح المحرك", f"${df['صافي الربح ($)'].sum():,.0f}")
with c3:
    st.metric("متوسط تكلفة الشحن", f"${df['تكلفة الشحن ($)'].mean():,.1f}")
with c4:
    st.metric("عمليات نشطة (100k)", f"{len(df):,}")

st.divider()

# --- محرك البحث الاستراتيجي ---
st.subheader("🔍 استعلام دورة حياة المنتج والربحية")
with st.form("search_form"):
    user_input = st.text_input("أدخل معرف الطلب السيادي (200 خانة):").strip()
    submit = st.form_submit_button("🚀 تحليل البيانات اللحظي")

if submit:
    res = df[df['الرقم السيادي العالمي (Global PID)'] == user_input]
    if not res.empty:
        r = res.iloc[0]
        st.success("🎯 تم استدعاء البيانات المالية والزمنية بنجاح")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### 🌍 الجغرافيا والمورد")
            st.write(f"**المورد:** {r['البائع (Vendor)']}")
            st.write(f"**بلد المنشأ:** {r['بلد المصنع (Origin)']}")
            st.write(f"**وجهة الاستلام:** {r['بلد الاستلام (Destination)']}")
        
        with col2:
            st.markdown("#### ⏱️ السجل الزمني")
            st.write(f"**تاريخ الشحن:** {r['تاريخ الشحن'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**تاريخ الاستلام:** {r['تاريخ الاستلام'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**الناقل:** {r['شركة الشحن (Courier)']}")
            
        with col3:
            st.markdown("#### 💰 تحليل الربح ($)")
            st.write(f"**تكلفة المنتج:** ${r['تكلفة المنتج ($)']}")
            st.write(f"**تكلفة الشحن:** ${r['تكلفة الشحن ($)']}")
            st.info(f"**صافي الربح من العملية:** ${r['صافي الربح ($)']}")
    else:
        st.error("❌ الرقم غير موجود في قاعدة بيانات هذه الجلسة.")

# --- تحميل ملف البيانات المعدل ---
st.sidebar.header("📥 مركز التقارير")
def to_excel(df_in):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_in.head(5000).to_excel(writer, index=False)
    return output.getvalue()

st.sidebar.download_button("📊 تحميل سجل الأرباح والعمليات", to_excel(df), "OKORT_Global_Profit_Report.xlsx")
