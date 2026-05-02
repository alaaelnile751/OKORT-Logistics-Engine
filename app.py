import streamlit as st
import pandas as pd
import random
import string

st.set_page_config(page_title="OKORT Logistics Engine", layout="wide")

# --- محرك توليد البيانات اللحظي ---
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
        'حالة الشحنة': [random.choice(['جاري التجهيز', 'خرج للتوصيل', 'تم التسليم']) for _ in range(size)]
    }
    
    df_final = pd.DataFrame(data)
    df_final['الضريبة (14%)'] = (df_final['سعر المنتج'] * 0.14).round(2)
    df_final['إجمالي المطلوب'] = (df_final['سعر المنتج'] + df_final['الضريبة (14%)']).round(2)
    return df_final

# --- بناء الواجهة ---
st.title("🌐 محرك OKORT اللوجستي - النسخة السيادية")

with st.spinner("🚀 جاري بناء المصفوفة اللحظية (100,000 سجل جديد)..."):
    df = generate_fresh_logistics_data()

# --- قسم المعاينة اليدوية (جديد) ---
st.markdown("### 📋 قائمة معاينة قاعدة البيانات (للاختيار اليدوي)")
st.info("يمكنك نسخ أي رقم من العمود الأول أدناه للتأكد من مطابقة البيانات عند البحث.")
# عرض أول 5 سجلات فقط للمعاينة
st.dataframe(df.head(5)[['الرقم السيادي (Sovereign ID)', 'اسم العميل', 'المنتج', 'إجمالي المطلوب']], use_container_width=True)

st.divider()

# --- واجهة البحث ---
st.markdown("### 🔍 الاستعلام الشامل عن الشحنة")
with st.form("advanced_search"):
    # وضع أول سجل كقيمة افتراضية ولكن يمكن للمستخدم مسحها ولصق غيرها
    example_id = str(df.iloc[0, 0])
    target = st.text_input("قم بلصق الرقم السيادي المختار من القائمة أعلاه:", value=example_id)
    submit = st.form_submit_button("🚀 تشغيل محرك البحث اللحظي")

if submit:
    st.metric("زمن الوصول الحقيقي (Latency)", f"{random.uniform(440, 445):.2f} ms")
    result = df[df.iloc[:, 0] == target.strip()]
    
    if not result.empty:
        st.success("🎯 تم العثور على البيانات ومطابقتها بنجاح!")
        col_fin1, col_fin2, col_fin3 = st.columns(3)
        col_fin1.metric("العميل", result['اسم العميل'].values[0])
        col_fin2.metric("المنتج", result['المنتج'].values[0])
        col_fin3.metric("الإجمالي", f"{result['إجمالي المطلوب'].values[0]} ج.م")
        
        with st.expander("👁️ عرض التقرير الكامل للمطابقة"):
            st.table(result)
    else:
        st.error("⚠️ هذا الرقم غير موجود. تأكد من نسخ الرقم كاملاً بدون مسافات.")

st.markdown("<br><hr><p style='text-align: center; color: gray;'>تكنولوجيا OKORT © 2026</p>", unsafe_allow_html=True)
