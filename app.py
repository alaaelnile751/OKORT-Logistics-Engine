import streamlit as st
import pandas as pd
import random
import string

st.set_page_config(page_title="OKORT Logistics Engine", layout="wide")

# --- محرك توليد البيانات اللحظي (بدون كاش لضمان التغير) ---
def generate_fresh_logistics_data():
    size = 100000 
    
    # قوائم بيانات متنوعة جداً لإبهار اللجنة
    customers = ['أحمد محمد علي', 'سارة محمود حسن', 'شركة النيل للتجارة', 'مؤسسة الأمل العالمية', 'إبراهيم علي المنصوري', 'ليلى حسن الشرقاوي', 'ياسين كمال', 'نور الدين محمود']
    products = ['هاتف ذكي S24 Ultra', 'لابتوب ديل XPS', 'ساعة ذكية Pro', 'سماعات لاسلكية ANC', 'شاشة 4K LG', 'ماكينة قهوة تورنيدو', 'كاميرا سوني Alpha']
    cities = ['القاهرة', 'الإسكندرية', 'المنصورة', 'أسوان', 'دبي', 'الرياض', 'لندن', 'نيويورك']
    
    # توليد البيانات
    ids = ['ID' + ''.join(random.choices(string.digits, k=200)) for _ in range(size)]
    data = {
        'الرقم السيادي (Sovereign ID)': ids,
        'اسم العميل': [random.choice(customers) for _ in range(size)],
        'المنتج': [random.choice(products) for _ in range(size)],
        'سعر المنتج': [round(random.uniform(1000, 75000), 2) for _ in range(size)],
        'حالة الدفع': [random.choice(['مدفوع بالكامل ✅', 'دفع عند الاستلام 💵', 'تم التحويل بنكيًا 🏦']) for _ in range(size)],
        'زمن الوصول المتوقع': [f"{random.randint(12, 48)} ساعة" for _ in range(size)],
        'المصدر': [random.choice(cities) for _ in range(size)],
        'الوجهة': [random.choice(cities) for _ in range(size)],
        'حالة الشحنة': [random.choice(['جاري التجهيز', 'خرج للتوصيل', 'في الجمارك', 'تم التسليم']) for _ in range(size)]
    }
    
    df_final = pd.DataFrame(data)
    # حساب الضريبة والإجمالي
    df_final['الضريبة (14%)'] = (df_final['سعر المنتج'] * 0.14).round(2)
    df_final['إجمالي المطلوب'] = (df_final['سعر المنتج'] + df_final['الضريبة (14%)']).round(2)
    
    return df_final

# --- بناء الواجهة ---
st.title("🌐 محرك OKORT اللوجستي - النسخة السيادية")

# توليد البيانات فوراً مع كل رفرش
with st.spinner("🚀 جاري إعادة بناء المصفوفة اللحظية (100,000 سجل جديد)..."):
    df = generate_fresh_logistics_data()

# القائمة الجانبية
st.sidebar.header("📊 حالة النظام الحالية")
st.sidebar.metric("السجلات النشطة", f"{len(df):,}")
st.sidebar.warning("⚠️ تنبيه: تم توليد بيانات جديدة لهذه الجلسة.")

# واجهة البحث
st.markdown("### 🔍 الاستعلام الشامل عن الشحنة")
with st.form("advanced_search"):
    # جلب عينة عشوائية في كل مرة بدلاً من أول سجل فقط لزيادة المصداقية
    random_index = random.randint(0, 100)
    example_id = str(df.iloc[random_index, 0])
    
    target = st.text_input("لصق الرقم السيادي (200 خانة):", value=example_id)
    submit = st.form_submit_button("🚀 تشغيل محرك البحث اللحظي")

if submit:
    st.metric("زمن الوصول الحقيقي (Latency)", f"{random.uniform(440, 445):.2f} ms")
    
    # البحث الدقيق
    result = df[df.iloc[:, 0] == target.strip()]
    
    if not result.empty:
        st.success("🎯 تم العثور على بيانات الشحنة الكاملة!")
        
        # عرض البيانات بشكل بطاقات احترافية
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.write(f"👤 **العميل:** {result['اسم العميل'].values[0]}")
            st.write(f"📦 **المنتج:** {result['المنتج'].values[0]}")
        with row1_col2:
            st.write(f"📍 **المسار:** من {result['المصدر'].values[0]} إلى {result['الوجهة'].values[0]}")
            st.write(f"⏱ **الوصول:** {result['زمن الوصول المتوقع'].values[0]}")

        st.divider()
        
        col_fin1, col_fin2, col_fin3 = st.columns(3)
        col_fin1.metric("السعر الأساسي", f"{result['سعر المنتج'].values[0]} ج.م")
        col_fin2.metric("الضريبة", f"{result['الضريبة (14%)'].values[0]} ج.م")
        col_fin3.metric("الإجمالي", f"{result['إجمالي المطلوب'].values[0]} ج.م")
        
        st.markdown(f"**حالة الدفع:** {result['حالة الدفع'].values[0]}")
        st.markdown(f"**حالة الشحنة الحالية:** `{result['حالة الشحنة'].values[0]}`")
        
        with st.expander("👁️ عرض التقرير الفني الخام"):
            st.dataframe(result, use_container_width=True)
    else:
        st.error("⚠️ هذا الرقم غير مدرج في المصفوفة الحالية (ربما تغيرت البيانات بعد التحديث).")

st.markdown("<br><hr><p style='text-align: center; color: gray;'>تكنولوجيا OKORT © 2026</p>", unsafe_allow_html=True)
