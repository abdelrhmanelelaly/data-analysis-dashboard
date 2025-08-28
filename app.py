import streamlit as st
import pandas as pd
import plotly.express as px

# ================== تحميل البيانات (مع الكاش) ==================
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

# ================== عنوان ووصف أعلى الصفحة ==================
st.title("📊 لوحة تحليل المبيعات")
st.markdown("> منصة تفاعلية لتحليل أداء المنتجات والمناطق خلال فترات زمنية مختلفة")

st.divider()

# ================== الفلاتر ==================
col1, col2 = st.columns(2)

with col1:
    product_filter = st.multiselect(
        "اختر المنتج:", df["المنتج"].unique(), default=df["المنتج"].unique()
    )

with col2:
    region_filter = st.multiselect(
        "اختر المنطقة:", df["المنطقة"].unique(), default=df["المنطقة"].unique()
    )

# فلتر التاريخ
min_date, max_date = df["التاريخ"].min(), df["التاريخ"].max()
date_filter = st.date_input(
    "الفترة الزمنية:", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

# ================== تطبيق الفلاتر ==================
filtered_df = df[
    (df["المنتج"].isin(product_filter)) &
    (df["المنطقة"].isin(region_filter)) &
    (df["التاريخ"] >= pd.to_datetime(date_filter[0])) &
    (df["التاريخ"] <= pd.to_datetime(date_filter[1]))
]

st.divider()

# ================== كروت الملخص ==================
st.subheader("📌 لمحة سريعة")

# صف أول
kpi_row1 = st.columns(3)
with kpi_row1[0]:
    st.metric("إجمالي الإيرادات", f"{filtered_df['الإيرادات'].sum():,.0f}")
with kpi_row1[1]:
    st.metric("متوسط الإيرادات", f"{filtered_df['الإيرادات'].mean():,.0f}")
with kpi_row1[2]:
    st.metric("عدد المنتجات", filtered_df['المنتج'].nunique())

# صف ثاني
kpi_row2 = st.columns(3)
with kpi_row2[0]:
    st.metric("عدد المناطق", filtered_df['المنطقة'].nunique())
with kpi_row2[1]:
    top_product_series = filtered_df.groupby("المنتج")["الإيرادات"].sum()
    if not top_product_series.empty:
        top_prod_name = top_product_series.idxmax()
        top_prod_value = top_product_series.max()
        st.metric("المنتج الأعلى إيرادًا", f"{top_prod_name} ({top_prod_value:,.0f})")
    else:
        st.metric("المنتج الأعلى إيرادًا", "-")
with kpi_row2[2]:
    top_region_series = filtered_df.groupby("المنطقة")["الإيرادات"].sum()
    if not top_region_series.empty:
        top_region_name = top_region_series.idxmax()
        top_region_value = top_region_series.max()
        st.metric("المنطقة الأعلى إيرادًا", f"{top_region_name} ({top_region_value:,.0f})")
    else:
        st.metric("المنطقة الأعلى إيرادًا", "-")

st.divider()

# ================== الرسوم البيانية ==================
color_palette = px.colors.qualitative.Set2

# الإيرادات بمرور الوقت
st.subheader("📈 الإيرادات بمرور الوقت")
fig_time = px.line(
    filtered_df, x="التاريخ", y="الإيرادات", color="المنتج", markers=True,
    color_discrete_sequence=color_palette, title="الإيرادات اليومية حسب المنتج",
    template='plotly_white'
)
fig_time.update_traces(line=dict(width=3))
fig_time.update_layout(
    title_x=0.5,
    xaxis_title="التاريخ",
    yaxis_title="الإيرادات",
    plot_bgcolor="white",
    paper_bgcolor="white",
    yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1, zeroline=True, zerolinecolor="gray"),
    xaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
    legend_title_text="المنتج",
    hovermode="x unified",
    font=dict(family="Cairo", size=12, color="black")
)
st.plotly_chart(fig_time, use_container_width=True, config={"staticPlot": True})

# الإيرادات حسب المنتج
st.subheader("📦 الإيرادات حسب المنتج")
fig_product = px.pie(
    filtered_df, names="المنتج", values="الإيرادات", hole=0.3,
    color_discrete_sequence=color_palette, title="نسبة الإيرادات حسب المنتج",
    template='plotly_white'
)
fig_product.update_traces(
    hovertemplate="المنتج: %{label}<br>الإيرادات: %{value:,.0f}<br>النسبة: %{percent}",
    pull=[0.05]*len(filtered_df['المنتج'].unique()),
    textinfo='percent+label'
)
fig_product.update_layout(title_x=0.5, legend_title_text="المنتج",
                          font=dict(family="Cairo", size=12, color="black"))
st.plotly_chart(fig_product, use_container_width=True, config={"staticPlot": True})

# الإيرادات حسب المنطقة
st.subheader("🏙️ الإيرادات حسب المنطقة")
region_data = filtered_df.groupby("المنطقة")["الإيرادات"].sum().reset_index()
fig_region = px.bar(
    region_data, x="المنطقة", y="الإيرادات", color="المنطقة",
    color_discrete_sequence=color_palette, title="إجمالي الإيرادات لكل منطقة",
    template='plotly_white'
)
fig_region.update_layout(
    title_x=0.5,
    xaxis_title="المنطقة",
    yaxis_title="الإيرادات",
    plot_bgcolor="white",
    paper_bgcolor="white",
    yaxis=dict(range=[0, region_data["الإيرادات"].max()*1.1], showgrid=True, gridcolor='lightgray'),
    showlegend=False,
    font=dict(family="Cairo", size=12, color="black")
)
st.plotly_chart(fig_region, use_container_width=True, config={"staticPlot": True})

st.divider()

# ================== علامات التبويب للمقارنات ==================
st.subheader("📊 مقارنات تفصيلية")
tab1, tab2, tab3 = st.tabs([
    "مقارنة المنتجات حسب المناطق",
    "مقارنة المناطق حسب المنتجات",
    "تحليل متقدم"
])

# Tab 1
with tab1:
    prod_region_data = filtered_df.groupby(["المنتج","المنطقة"])["الإيرادات"].sum().reset_index()
    fig_prod_region = px.bar(
        prod_region_data, x="المنتج", y="الإيرادات", color="المنطقة",
        barmode="group", color_discrete_sequence=color_palette,
        title="مبيعات كل منتج موزعة على المناطق",
        template='plotly_white'
    )
    st.plotly_chart(fig_prod_region, use_container_width=True, config={"staticPlot": True})

# Tab 2
with tab2:
    region_prod_data = filtered_df.groupby(["المنطقة","المنتج"])["الإيرادات"].sum().reset_index()
    fig_region_prod = px.bar(
        region_prod_data, x="المنطقة", y="الإيرادات", color="المنتج",
        barmode="group", color_discrete_sequence=color_palette,
        title="مبيعات كل منطقة موزعة على المنتجات",
        template='plotly_white'
    )
    st.plotly_chart(fig_region_prod, use_container_width=True, config={"staticPlot": True})

# Tab 3: تحليل متقدم
with tab3:
    st.markdown("### 📅 الإيرادات الشهرية لكل منتج")
    monthly_data = filtered_df.copy()
    monthly_data['الشهر'] = monthly_data['التاريخ'].dt.to_period('M')
    monthly_prod = monthly_data.groupby(['الشهر','المنتج'])['الإيرادات'].sum().reset_index()
    fig_monthly = px.line(
        monthly_prod, x='الشهر', y='الإيرادات', color='المنتج',
        markers=True, color_discrete_sequence=color_palette,
        title="تطور الإيرادات الشهري لكل منتج", template='plotly_white'
    )
    st.plotly_chart(fig_monthly, use_container_width=True, config={"staticPlot": True})

    st.markdown("### 📈 نسبة النمو الشهري للإيرادات لكل منتج")
    monthly_prod['إيرادات_سابق'] = monthly_prod.groupby('المنتج')['الإيرادات'].shift(1)
    monthly_prod['نسبة_النمو'] = ((monthly_prod['الإيرادات'] - monthly_prod['إيرادات_سابق']) / monthly_prod['إيرادات_سابق']) * 100
    fig_growth = px.line(
        monthly_prod, x='الشهر', y='نسبة_النمو', color='المنتج',
        markers=True, color_discrete_sequence=color_palette,
        title="نسبة النمو الشهري للإيرادات (%) لكل منتج", template='plotly_white'
    )
    st.plotly_chart(fig_growth, use_container_width=True, config={"staticPlot": True})

    st.markdown("### 🔥 Heatmap للإيرادات بين المنتجات والمناطق")
    heat_data = filtered_df.pivot_table(index='المنتج', columns='المنطقة', values='الإيرادات', aggfunc='sum').fillna(0)
    fig_heat = px.imshow(
        heat_data, text_auto=True, color_continuous_scale='Viridis',
        title="مقارنة الإيرادات بين المنتجات والمناطق"
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"staticPlot": True})

    st.markdown("### 🏆 أعلى وأقل 5 منتجات من حيث الإيرادات")
    top5 = filtered_df.groupby('المنتج')['الإيرادات'].sum().sort_values(ascending=False).head(5)
    bottom5 = filtered_df.groupby('المنتج')['الإيرادات'].sum().sort_values(ascending=True).head(5)
    col_top, col_bottom = st.columns(2)
    with col_top:
        st.bar_chart(top5, use_container_width=True)
        st.caption("أعلى 5 منتجات")
    with col_bottom:
        st.bar_chart(bottom5, use_container_width=True)
        st.caption("أقل 5 منتجات")

st.divider()

# ================== عرض الجدول + زر تحميل ==================
st.subheader("📋 البيانات التفصيلية")
st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    label="⬇️ تحميل البيانات المفلترة (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="المبيعات_المفلترة.csv",
    mime="text/csv"
)

st.divider()
st.caption("""
برنامج التحليل مقدم بواسطة فريق المبيعات. للاستفسارات يرجى التواصل عبر فريق التحليل أو البريد الإلكتروني.
""")
