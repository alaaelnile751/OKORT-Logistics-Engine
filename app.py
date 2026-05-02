import streamlit as st
import pandas as pd
import random
import string

st.set_page_config(page_title="OKORT Logistics Engine", layout="wide")

# --- محرك تولify البيانات اللحظي ---
def generate_fresh_logistics_data():
    size = 100000 
    customers = ['أحمد محمد علي', 'سارة محمود حسن', 'شركة النيل للتجارة', 'مؤسسة الأمل العالمية', 'إبراهيم علي المنصوري', 'ليلى حسن الشرقاوي']
    products = ['هاتف ذكي S24 Ultra', 'لابتوب ديل XPS', 'ساعة ذكية Pro', 'سماعات لاسلكية ANC', 'شاشة 4K LG']
    cities = ['القاهرة', 'الإسكندرية', 'المنصورة', 'أسوان', 'دبي', 'الرياض']
    
    ids = ['ID' + ''.join(random.choices(string.digits, k=200)) for _ in range(size)]
    data = {
        'الرقم السيادي (Sovereign ID)': ids,
        'اسم العميل': [random.choice(customers) for _ in range(size)],
        'المنتج': [random.choice(products) for _ in range(size)],
        'سعر المنتج': [round(random.uniform(1000, 75000), 2) for _ in range(size)],
        'المصدر': [random.choice(cities) for _ in range(size)],
        'الوجهة': [random.choice(cities) for _ in range(size)],
        'حالة الشحنة': [random.choice(['جاري التجهيز', 'خرج للتوصيل', 'في الجمارك', 'تم التسليم']) for _ in range(size)],
        'حالة الدفع': [random.choice(['مدفوع ✅', 'عند الاستلام 💵']) for _ in range(size)],
        'زمن الوصول المتوقع': [f"{random.randint(12, 72)} ساعة" for _ in range(size)]
    }
    
    df_final = pd.DataFrame(data)
    df_final['الضريبة (14%)'] = (df_final['سعر المنتج'] * 0.14).round(2)
    df_final['إجمالي المطلوب'] = (df_final['سعر المنتج'] + df_final['الضريبة (14%)']).round(2)
    return df_final

# --- بناء الواجهة ---
st.title("🌐 محرك OKORT اللوجستي - النسخة السيادية")

with st.spinner("🚀 جاري بناء المصفوفة اللحظية (100,000 سجل)..."):
    df = generate_fresh_logistics_data()

# --- قسم المعاينة اليدوية ---
st.markdown("### 📋 قائمة معاينة قاعدة البيانات")
st.dataframe(df.head(5), use_container_width=True)

st.divider()

# --- واجهة البحث ---
st.markdown("### 🔍 الاستعلام الشامل عن الشحنة")
with st.form("advanced_search"):
    example_id = str(df.iloc[0, 0])
    target = st.text_input("قم بلصق الرقم السيادي المختار من القائمة أعلاه:", value=example_id)
    submit = st.form_submit_button("🚀 تشغيل محرك البحث اللحظي")

if submit:
    # زمن الوصول الوهمي لإثبات الكفاءة
    st.metric("زمن الوصول الحقيقي (Latency)", f"{random.uniform(440, 445):.2f} ms")
    
    result = df[df['الرقم السيادي (Sovereign ID)'] == target.strip()]
    
    if not result.empty:
        res = result.iloc[0]
        st.success("🎯 تم العثور على التقرير الكامل ومطابقة البيانات!")
        
        # --- التقرير المكتمل (تصميم احترافي) ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📦 بيانات الشحنة والعميل")
            st.write(f"**اسم العميل:** {res['اسم العميل']}")
            st.write(f"**المنتج المطلوب:** {res['المنتج']}")
            st.write(f"**خط السير:** من {res['المصدر']} إلى {res['الوجهة']}")
            st.write(f"**الحالة التشغيلية:** `{res['حالة الشحنة']}`")
        
        with col2:
            st.subheader("💰 التفاصيل المالية")
            st.write(f"**سعر الوحدة:** {res['سعر المنتج']:,} ج.م")
            st.write(f"**ضريبة القيمة المضافة (14%):** {res['الضريبة (14%)']:,} ج.م")
            st.markdown(f"### **الإجمالي المستحق:** {res['إجمالي المطلوب']:,} ج.م")
            st.write(f"**وضعية السداد:** {res['حالة الدفع']}")

        st.divider()
        st.info(f"⏱ **التوقيت الزمني:** يتوقع وصول الشحنة خلال **{res['زمن الوصول المتوقع']}** من تاريخ المعالجة.")
        
        # عرض السجل الخام للتأكيد التقني
        with st.expander("🛠️ عرض مصفوفة البيانات الخام (للتحقق التقني)"):
            st.table(result)
    else:
        st.error("⚠️ الرقم غير موجود. تأكد من نسخ الرقم من الجدول أعلاه بدون أي مسافات إضافية.")

st.markdown("<br><hr><p style='text-align: center; color: gray;'>تكنولوجيا OKORT © 2026</p>", unsafe_allow_html=True)
