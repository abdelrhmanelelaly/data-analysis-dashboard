import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ================== تحميل البيانات ==================
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df["المنتج"] = df["المنتج"].astype(str)
    df["المنطقة"] = df["المنطقة"].astype(str)
    df["التاريخ"] = pd.to_datetime(df["التاريخ"])
    return df

df = load_data()

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="لوحة تحليل المبيعات",
    page_icon="📊",
    layout="wide"
)

st.title("📊 لوحة تحليل المبيعات")

# ================== الفلاتر ==================
col1, col2 = st.columns(2)

with col1:
    product_filter = st.multiselect("اختر المنتج:", df["المنتج"].unique(), default=df["المنتج"].unique())

with col2:
    region_filter = st.multiselect("اختر المنطقة:", df["المنطقة"].unique(), default=df["المنطقة"].unique())

# تطبيق الفلاتر
filtered_df = df[(df["المنتج"].isin(product_filter)) & (df["المنطقة"].isin(region_filter))]

# ================== الرسوم البيانية ==================
st.subheader("📈 الإيرادات بمرور الوقت")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x="التاريخ", y="الإيرادات", hue="المنتج", marker="o", ax=ax)
ax.set_title("الإيرادات بمرور الوقت")
st.pyplot(fig)

st.subheader("🏙️ الإيرادات حسب المنطقة")
fig, ax = plt.subplots(figsize=(8,5))
region_data = filtered_df.groupby("المنطقة")["الإيرادات"].sum().reset_index()
sns.barplot(data=region_data, x="المنطقة", y="الإيرادات", hue="المنطقة", dodge=False, ax=ax)
ax.set_title("الإيرادات حسب المنطقة")
st.pyplot(fig)

st.subheader("📦 الإيرادات حسب المنتج")
fig, ax = plt.subplots(figsize=(6,6))
product_data = filtered_df.groupby("المنتج")["الإيرادات"].sum().reset_index()
ax.pie(product_data["الإيرادات"], labels=product_data["المنتج"], autopct="%1.1f%%", startangle=90)
ax.set_title("الإيرادات حسب المنتج")
st.pyplot(fig)

# ================== عرض الجدول ==================
st.subheader("📋 البيانات التفصيلية")
st.dataframe(filtered_df, use_container_width=True)# ================== الرسوم البيانية ==================
st.subheader("📈 الإيرادات بمرور الوقت")
fig_time = px.line(filtered_df, x="التاريخ", y="الإيرادات", color="المنتج", markers=True)
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("🏙️ الإيرادات حسب المنطقة")
fig_region = px.bar(filtered_df.groupby("المنطقة")["الإيرادات"].sum().reset_index(),
                    x="المنطقة", y="الإيرادات", color="المنطقة", text_auto=True)
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("📦 الإيرادات حسب المنتج")
fig_product = px.pie(filtered_df, names="المنتج", values="الإيرادات", hole=0.3)
st.plotly_chart(fig_product, use_container_width=True)

# ================== عرض الجدول ==================
st.subheader("📋 البيانات التفصيلية")
st.dataframe(filtered_df, use_container_width=True)
