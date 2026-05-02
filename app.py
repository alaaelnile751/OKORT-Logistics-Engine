import streamlit as st
import pandas as pd
import random
import string
import io

st.set_page_config(page_title="OKORT Logistics BI", layout="wide")

# --- محرك توليد البيانات الثابت (لضمان مطابقة البحث) ---
@st.cache_data
def generate_fixed_business_data():
    # تثبيت العشوائية لضمان عدم تغير البيانات عند الرفرش
    random.seed(42) 
    
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
        'الموعد الفعلي (ساعة)': [random.randint(20, 80) for _ in range(size)],
    }
    
    df = pd.DataFrame(data)
    df['الضريبة (14%)'] = (df['التكلفة'] * 0.14).round(2)
    df['الإجمالي'] = (df['التكلفة'] + df['الضريبة (14%)']).round(2)
    df['الفارق الزمني'] = df['الموعد الفعلي (ساعة)'] - df['الموعد المخطط (ساعة)']
    df['حالة التوصيل'] = df['الفارق الزمني'].apply(lambda x: 'تأخير ⚠️' if x > 0 else 'في الموعد ✅')
    
    return df

with st.spinner("🚀 جاري مزامنة قاعدة البيانات السيادية..."):
    df = generate_fixed_business_data()

st.title("📊 نظام OKORT للإدارة اللوجستية الذكية")

# --- لوحة التحكم الجانبية ---
st.sidebar.header("📥 مركز التقارير والتحقق")

# دالة تحويل الإكسيل مع ضمان الترميز الصحيح
def to_excel(df_in):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # تصدير أول 1000 سجل للمعاينة السريعة والمطابقة
        df_in.head(1000).to_excel(writer, index=False, sheet_name='Logistics_Report')
    return output.getvalue()

st.sidebar.download_button(
    label="⬇️ تحميل سجل المطابقة (Excel)",
    data=to_excel(df),
    file_name='OKORT_Verification_Sheet.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# --- واجهة البحث ---
st.subheader("🔍 محرك الاستعلام اللحظي")
st.info("قم بنسخ الرقم السيادي من ملف الإكسيل المحمل ولصقه أدناه.")

with st.form("biz_search"):
    # تنظيف النص المدخل من أي مسافات زائدة
    target_input = st.text_input("أدخل الرقم السيادي (200 خانة):").strip()
    submit = st.form_submit_button("🚀 بدء التحليل المالي واللوجستي")

if submit:
    if target_input:
        # البحث الدقيق
        res = df[df['الرقم السيادي (Sovereign ID)'] == target_input]
        
        if not res.empty:
            r = res.iloc[0]
            st.success(f"🎯 تم العثور على شحنة العميل: {r['العميل']}")
            
            # عرض التقارير الاحترافية
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### 💳 التقرير المالي")
                st.metric("الإجمالي المستحق", f"{r['الإجمالي']:,} ج.م")
                st.write(f"**الضريبة:** {r['الضريبة (14%)']:,} ج.م")
                st.write(f"**الحالة:** {r['حالة الدفع']}")
            
            with col_b:
                st.markdown("### ⏱️ تقرير كفاءة التوصيل")
                diff = r['الفارق الزمني']
                status_color = "red" if diff > 0 else "green"
                st.markdown(f"**الوضع الحالي:** <span style='color:{status_color}'>{r['حالة التوصيل']}</span>", unsafe_allow_html=True)
                st.write(f"**المخطط:** {r['الموعد المخطط (ساعة)']} ساعة")
                st.write(f"**الفعلي:** {r['الموعد الفعلي (ساعة)']} ساعة")
        else:
            st.error("⚠️ الرقم غير موجود. تأكد من أنك لم تقم بعمل Refresh للموقع بعد تحميل ملف الإكسيل.")
    else:
        st.warning("يرجى إدخال رقم الشحنة أولاً.")

st.markdown("<br><hr><p style='text-align: center; color: gray;'>تكنولوجيا OKORT © 2026 - رؤية إدارية متكاملة</p>", unsafe_allow_html=True)
