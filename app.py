import streamlit as st  # هذا السطر يحل مشكلة الخطأ في صورتك
import pandas as pd
import random
import string
import io

# إعداد الصفحة لتكون احترافية وواسعة
st.set_page_config(page_title="OKORT Global E-Commerce Hub", layout="wide")

# --- محرك توليد بيانات التجارة العالمية (Scale: 100k) ---
@st.cache_data
def generate_amazon_scale_data():
    random.seed(101) # لضمان ثبات الأرقام والمطابقة في البحث
    size = 100000 
    
    # تصنيفات تحاكي بيئة أمازون وعلي بابا
    vendors = ['Samsung Official', 'Apple Global Store', 'Nike Middle East', 'Xiaomi China', 'Dell Tech']
    shipping_partners = ['Amazon Shipping', 'DHL Express', 'Aramex', 'FedEx', 'Bosta']
    hubs = ['Shenzhen Hub (China)', 'Jebel Ali Center (UAE)', 'Cairo Central Warehouse', 'Alexandria Port']
    
    data = {
        'الرقم السيادي العالمي (Global PID)': ['OK-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=200)) for _ in range(size)],
        'البائع / المورد (Vendor)': [random.choice(vendors) for _ in range(size)],
        'مركز التوزيع (Hub)': [random.choice(hubs) for _ in range(size)],
        'شركة التوصيل (Courier Partner)': [random.choice(shipping_partners) for _ in range(size)],
        'سعر المنتج ($)': [round(random.uniform(20, 2500), 2) for _ in range(size)],
        'حالة المخزون اللحظية': [random.choice(['متوفر ✅', 'طلب مسبق ⏳', 'آخر قطعة 🔥']) for _ in range(size)],
        'وقت المعالجة في المخزن (ساعة)': [random.randint(2, 12) for _ in range(size)],
        'زمن الشحن المخطط (ساعة)': [random.randint(48, 168) for _ in range(size)],
        'زمن الشحن الفعلي (ساعة)': [random.randint(40, 200) for _ in range(size)],
    }
    
    df = pd.DataFrame(data)
    # منطق البيزنس (الانتفاع والربحية)
    df['عمولة المنصة (10%)'] = (df['سعر المنتج ($)'] * 0.10).round(2)
    df['صافي ربح المورد'] = (df['سعر المنتج ($)'] - df['عمولة المنصة (10%)']).round(2)
    df['انحراف كفاءة الشحن'] = df['زمن الشحن الفعلي (ساعة)'] - df['زمن الشحن المخطط (ساعة)']
    return df

with st.spinner("🚀 جاري محاكاة بيئة البيانات الضخمة لـ OKORT..."):
    df = generate_amazon_scale_data()

st.title("🌐 محرك OKORT للتحكم في سلاسل الإمداد العالمية")
st.markdown("---")

# --- لوحة مؤشرات الأداء (Dashboard) ---
st.subheader("📊 لوحة مراقبة العمليات المركزية")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("حجم التجارة (GMV)", f"${df['سعر المنتج ($)'].sum():,.0f}")
with c2:
    st.metric("أرباح المنصة المتوقعة", f"${df['عمولة المنصة (10%)'].sum():,.0f}")
with c3:
    shipping_efficiency = (len(df[df['انحراف كفاءة الشحن'] <= 0]) / len(df)) * 100
    st.metric("دقة مواعيد التوصيل", f"{shipping_efficiency:.1f}%")
with c4:
    st.metric("إجمالي العمليات النشطة", f"{len(df):,}")

st.divider()

# --- محرك البحث والربط السيادي ---
st.subheader("🔍 تتبع دورة حياة الطلب (Cross-Platform Tracking)")
with st.form("global_search"):
    target = st.text_input("أدخل معرف الطلب السيادي (200 خانة):").strip()
    submit = st.form_submit_button("🚀 تحليل رحلة المنتج والبيانات المالية")

if submit:
    res = df[df['الرقم السيادي العالمي (Global PID)'] == target]
    if not res.empty:
        r = res.iloc[0]
        st.success("🎯 تم الربط السيادي بنجاح بين المورد والمخزن وشركة الشحن")
        
        col_v, col_l, col_f = st.columns(3)
        with col_v:
            st.markdown("#### 🏭 المورد والمخزون")
            st.write(f"**المورد:** {r['البائع / المورد (Vendor)']}")
            st.write(f"**نقطة الانطلاق:** {r['مركز التوزيع (Hub)']}")
            st.write(f"**الحالة:** {r['حالة المخزون اللحظية']}")
        
        with col_l:
            st.markdown("#### 🚚 التحليل اللوجستي")
            st.write(f"**الناقل:** {r['شركة التوصيل (Courier Partner)']}")
            st.write(f"**المخطط:** {r['زمن الشحن المخطط (ساعة)']} ساعة")
            diff = r['انحراف كفاءة الشحن']
            if diff > 0:
                st.error(f"**تأخير:** {diff} ساعة")
            else:
                st.success(f"**مبكر بـ:** {abs(diff)} ساعة")
        
        with col_f:
            st.markdown("#### 💰 التدفق المالي")
            st.write(f"**سعر البيع:** ${r['سعر المنتج ($)']}")
            st.write(f"**عمولة المنصة:** ${r['عمولة المنصة (10%)']}")
            st.markdown(f"**صافي المورد:** `${r['صافي ربح المورد']}`")
    else:
        st.error("رقم الطلب غير موجود. يرجى التأكد من نسخة الإكسيل.")

# --- مركز تحميل التقارير ---
st.sidebar.header("📥 مركز تقارير الإدارة")
def to_excel_global(df_in):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_in.head(5000).to_excel(writer, index=False)
    return output.getvalue()

st.sidebar.download_button(
    "📊 تحميل سجل العمليات الموحد", 
    to_excel_global(df), 
    "OKORT_Global_Trade_Report.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
