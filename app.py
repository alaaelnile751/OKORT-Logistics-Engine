import streamlit as st
import pandas as pd
import random
import string
import io

st.set_page_config(page_title="OKORT Global E-Commerce Hub", layout="wide")

# --- محرك توليد البيانات الضخمة (تحدي أمازون) ---
@st.cache_data
def generate_amazon_scale_data():
    random.seed(101) # بذرة ثابتة لضمان مطابقة البحث 100%
    size = 100000 
    
    # تفاصيل تناسب حجم أعمال أمازون وعلي بابا
    vendors = ['Samsung Official Store', 'Apple Global', 'Nike Middle East', 'Xiaomi China', 'Dell Tech']
    shipping_partners = ['Amazon Shipping', 'DHL Express', 'Aramex International', 'FedEx', 'Bosta']
    warehouses = ['Shenzhen Logistics Hub', 'Dubai Central Warehouse', 'Cairo Fulfillment Center', 'Riyadh Hub']
    
    data = {
        'الرقم السيادي العالمي (Global PID)': ['OK-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=200)) for _ in range(size)],
        'البائع / المورد (Vendor)': [random.choice(vendors) for _ in range(size)],
        'مركز التجميع (Warehouse)': [random.choice(warehouses) for _ in range(size)],
        'شركة التوصيل (Courier Partner)': [random.choice(shipping_partners) for _ in range(size)],
        'سعر المنتج ($)': [round(random.uniform(50, 5000), 2) for _ in range(size)],
        'وقت المعالجة المخطط (ساعة)': [random.randint(2, 12) for _ in range(size)],
        'زمن الشحن المخطط (ساعة)': [random.randint(48, 168) for _ in range(size)],
        'زمن الشحن الفعلي (ساعة)': [random.randint(40, 200) for _ in range(size)],
        'حالة المخزون اللحظية': [random.choice(['متوفر ✅', 'طلب مسبق ⏳', 'آخر قطعة 🔥']) for _ in range(size)],
    }
    
    df = pd.DataFrame(data)
    # المعادلات التجارية المعقدة التي تثبت قوة معالجة OKORT
    df['عمولة المنصة (10%)'] = (df['سعر المنتج ($)'] * 0.10).round(2)
    df['صافي ربح المورد'] = (df['سعر المنتج ($)'] - df['عمولة المنصة (10%)']).round(2)
    df['انحراف كفاءة الشحن'] = df['زمن الشحن الفعلي (ساعة)'] - df['زمن الشحن المخطط (ساعة)']
    return df

# تشغيل المحرك في الخلفية
df = generate_amazon_scale_data()

st.title("🌐 محرك OKORT للتحكم في سلاسل الإمداد العالمية")
st.markdown("---")

# --- لوحة مؤشرات الأداء (Dashboard) ---
st.subheader("📊 لوحة مراقبة العمليات (Global Operations Dashboard)")
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

# --- واجهة البحث الذكي ---
st.subheader("🔍 تتبع دورة حياة الطلب (Cross-Platform Tracking)")
st.info("قم بتحميل ملف الإكسيل من الجانب، انسخ الـ PID المكون من 200 خانة، والقه هنا.")

with st.form("global_search"):
    target_pid = st.text_input("أدخل معرف الطلب السيادي (Global PID):").strip()
    submit = st.form_submit_button("🚀 تحليل المسار والبيانات المالية")

if submit:
    # البحث اللحظي في 100 ألف سجل
    res = df[df['الرقم السيادي العالمي (Global PID)'] == target_pid]
    if not res.empty:
        r = res.iloc[0]
        st.success("🎯 تم الربط السيادي بنجاح بين كافة الأطراف")
        
        col_v, col_l, col_f = st.columns(3)
        with col_v:
            st.markdown("#### 🏭 المورد والمخزون")
            st.write(f"**المورد:** {r['البائع / المورد (Vendor)']}")
            st.write(f"**المخزن الحالى:** {r['مركز التجميع (Warehouse)']}")
            st.write(f"**الحالة:** {r['حالة المخزون اللحظية']}")
        
        with col_l:
            st.markdown("#### 🚚 التحليل اللوجستي")
            st.write(f"**الناقل:** {r['شركة التوصيل (Courier Partner)']}")
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
        st.error("❌ الرقم غير موجود. تأكد من أنك لم تقم بعمل Refresh للمتصفح بعد تحميل ملف الإكسيل.")

# --- مركز تحميل التقارير ---
st.sidebar.header("📥 مخرجات الإدارة العليا")
def to_excel_pro(df_in):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # تصدير أول 5000 سجل للمطابقة والتحقق
        df_in.head(5000).to_excel(writer, index=False, sheet_name='Global_Supply_Chain')
    return output.getvalue()

st.sidebar.download_button(
    "📊 تحميل سجل العمليات العالمي (Excel)", 
    to_excel_pro(df), 
    "OKORT_Global_Trade_Data.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
