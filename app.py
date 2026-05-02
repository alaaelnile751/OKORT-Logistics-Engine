import streamlit as st
import pandas as pd
import random
import string
import io

st.set_page_config(page_title="OKORT Global Logistics Engine", layout="wide")

# --- دالة توليد البيانات الثابتة (لضمان مطابقة البحث 100%) ---
@st.cache_data
def generate_amazon_data():
    # تثبيت البذرة (Seed) لضمان أن الإكسيل والموقع يقرآن نفس البيانات دائماً
    random.seed(42) 
    size = 100000 
    
    vendors = ['Samsung Official', 'Apple Global', 'Nike ME', 'Xiaomi Store', 'Dell Tech']
    couriers = ['Amazon Shipping', 'DHL Express', 'Aramex', 'FedEx', 'Bosta']
    
    data = {
        'الرقم السيادي العالمي (Global PID)': ['OK-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=200)) for _ in range(size)],
        'البائع (Vendor)': [random.choice(vendors) for _ in range(size)],
        'شركة التوصيل (Courier)': [random.choice(couriers) for _ in range(size)],
        'سعر المنتج ($)': [round(random.uniform(20, 2500), 2) for _ in range(size)],
        'حالة المخزون': [random.choice(['متوفر ✅', 'طلب مسبق ⏳', 'آخر قطعة 🔥']) for _ in range(size)],
        'وقت الشحن المخطط (ساعة)': [random.randint(48, 168) for _ in range(size)],
        'وقت الشحن الفعلي (ساعة)': [random.randint(40, 200) for _ in range(size)],
    }
    
    df = pd.DataFrame(data)
    df['عمولة المنصة (10%)'] = (df['سعر المنتج ($)'] * 0.10).round(2)
    df['صافي المورد'] = (df['سعر المنتج ($)'] - df['عمولة المنصة (10%)']).round(2)
    df['الانحراف الزمني'] = df['وقت الشحن الفعلي (ساعة)'] - df['وقت الشحن المخطط (ساعة)'].astype(int)
    return df

# تشغيل المحرك
df = generate_amazon_data()

st.title("🌐 محرك OKORT لعمالقة التجارة (Amazon/Alibaba Scale)")
st.markdown("---")

# --- القائمة الجانبية للتحميل ---
st.sidebar.header("📥 مركز البيانات السيادية")

def to_excel(df_in):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # تصدير أول 5000 سجل للمطابقة أثناء الديمو
        df_in.head(5000).to_excel(writer, index=False, sheet_name='OKORT_Data')
    return output.getvalue()

st.sidebar.download_button(
    label="📊 تحميل سجل المطابقة (Excel)",
    data=to_excel(df),
    file_name='OKORT_Amazon_Scale_Data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# --- واجهة البحث الذكي ---
st.subheader("🔍 تتبع دورة حياة الطلب والتدفق المالي")
st.info("انسخ رقم الـ PID من ملف الإكسيل والصقه هنا للتحليل اللحظي.")

with st.form("search_form"):
    # تنظيف المدخلات تلقائياً من أي مسافات (Strip)
    user_input = st.text_input("أدخل معرف الطلب السيادي (Global PID):").strip()
    submit_button = st.form_submit_button("🚀 بدء التحليل")

if submit_button:
    if user_input:
        # البحث في قاعدة البيانات الثابتة
        match = df[df['الرقم السيادي العالمي (Global PID)'] == user_input]
        
        if not match.empty:
            r = match.iloc[0]
            st.success(f"🎯 تم الربط السيادي بنجاح: {r['البائع (Vendor)']}")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("#### 🏢 بيانات المورد")
                st.write(f"**البائع:** {r['البائع (Vendor)']}")
                st.write(f"**المخزون:** {r['حالة المخزون']}")
            with c2:
                st.markdown("#### 🚚 الشريك اللوجستي")
                st.write(f"**الناقل:** {r['شركة التوصيل (Courier)']}")
                diff = r['الانحراف الزمني']
                if diff > 0:
                    st.error(f"⚠️ تأخير: {diff} ساعة")
                else:
                    st.success(f"✅ مبكر بـ: {abs(diff)} ساعة")
            with c3:
                st.markdown("#### 💰 التحليل المالي")
                st.write(f"**السعر:** ${r['سعر المنتج ($)']}")
                st.write(f"**عمولة المنصة:** ${r['عمولة المنصة (10%)']}")
                st.markdown(f"**صافي المورد:** `${r['صافي المورد']}`")
        else:
            st.error("❌ الرقم غير موجود! تأكد من أنك قمت بنسخ الرقم كاملاً من ملف الإكسيل الحالي دون تعديل.")
    else:
        st.warning("يرجى إدخال رقم الطلب أولاً.")
