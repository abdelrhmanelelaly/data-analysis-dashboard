import streamlit as st
import pandas as pd
import plotly.express as px

# تخصيص الألوان والأنماط
PRIMARY_COLOR = "#1E90FF"  # أزرق متوسط
BACKGROUND_COLOR = "#F0F8FF"  # أزرق فاتح كخلفية
TEXT_COLOR = "#333333"  # لون نص داكن

@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df["المنتج"] = df["المنتج"].astype(str)
    df["المنطقة"] = df["المنطقة"].astype(str)
    df["التاريخ"] = pd.to_datetime(df["التاريخ"])
    days_map = {
        'Monday': 'الإثنين',
        'Tuesday': 'الثلاثاء',
        'Wednesday': 'الأربعاء',
        'Thursday': 'الخميس',
        'Friday': 'الجمعة',
        'Saturday': 'السبت',
        'Sunday': 'الأحد'
    }
    df['يوم_الأسبوع'] = df['التاريخ'].dt.day_name().map(days_map)
    return df

df = load_data()

# تهيئة الصفحة مع خلفية مخصصة
st.set_page_config(
    page_title="لوحة تحليل المبيعات",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}
    .stHeader {{
        background-color: {PRIMARY_COLOR};
        color: white;
        padding: 10px;
        border-radius: 5px;
    }}
    .stMetric > div {{
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 لوحة تحليل المبيعات")
st.markdown("> منصة تفاعلية لتحليل أداء المنتجات والمناطق خلال فترات زمنية مختلفة", unsafe_allow_html=True)

st.divider()

# فلاتر بتصميم محسّن
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="stHeader">اختر المنتج:</div>', unsafe_allow_html=True)
    product_filter = st.multiselect("", df["المنتج"].unique(), default=df["المنتج"].unique(), key="product_filter")

with col2:
    st.markdown('<div class="stHeader">اختر المنطقة:</div>', unsafe_allow_html=True)
    region_filter = st.multiselect("", df["المنطقة"].unique(), default=df["المنطقة"].unique(), key="region_filter")

min_date, max_date = df["التاريخ"].min(), df["التاريخ"].max()
date_col = st.columns(1)
with date_col[0]:
    st.markdown('<div class="stHeader">الفترة الزمنية:</div>', unsafe_allow_html=True)
    date_filter = st.date_input("", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="date_filter")

filtered_df = df[
    (df["المنتج"].isin(product_filter)) &
    (df["المنطقة"].isin(region_filter)) &
    (df["التاريخ"] >= pd.to_datetime(date_filter[0])) &
    (df["التاريخ"] <= pd.to_datetime(date_filter[1]))
]

st.divider()

st.subheader("📌 لمحة سريعة")
st.caption("نظرة عامة على الأداء الرئيسي بناءً على الفلاتر المختارة")

kpi_row1 = st.columns(3)
with kpi_row1[0]:
    st.metric("إجمالي الإيرادات", f"{filtered_df['الإيرادات'].sum():,.0f}")
with kpi_row1[1]:
    top_day_series = filtered_df.groupby("يوم_الأسبوع")["الإيرادات"].sum()
    if not top_day_series.empty:
        top_day_name = top_day_series.idxmax()
        top_day_value = top_day_series.max()
        st.metric("اليوم الأعلى مبيعًا", f"{top_day_name} ({top_day_value:,.0f})")
    else:
        st.metric("اليوم الأعلى مبيعًا", "-")
with kpi_row1[2]:
    top_product_series = filtered_df.groupby("المنتج")["الإيرادات"].sum()
    if not top_product_series.empty:
        top_prod_name = top_product_series.idxmax()
        top_prod_value = top_product_series.max()
        st.metric("المنتج الأعلى مبيعًا", f"{top_prod_name} ({top_prod_value:,.0f})")
    else:
        st.metric("المنتج الأعلى مبيعًا", "-")

kpi_row2 = st.columns(3)
with kpi_row2[0]:
    low_product_series = filtered_df.groupby("المنتج")["الإيرادات"].sum()
    if not low_product_series.empty:
        low_prod_name = low_product_series.idxmin()
        low_prod_value = low_product_series.min()
        st.metric("المنتج الأقل مبيعًا", f"{low_prod_name} ({low_prod_value:,.0f})")
    else:
        st.metric("المنتج الأقل مبيعًا", "-")
with kpi_row2[1]:
    top_region_series = filtered_df.groupby("المنطقة")["الإيرادات"].sum()
    if not top_region_series.empty:
        top_region_name = top_region_series.idxmax()
        top_region_value = top_region_series.max()
        st.metric("المنطقة الأعلى إيرادًا", f"{top_region_name} ({top_region_value:,.0f})")
    else:
        st.metric("المنطقة الأعلى إيرادًا", "-")
with kpi_row2[2]:
    low_region_series = filtered_df.groupby("المنطقة")["الإيرادات"].sum()
    if not low_region_series.empty:
        low_region_name = low_region_series.idxmin()
        low_region_value = low_region_series.min()
        st.metric("المنطقة الأقل مبيعًا", f"{low_region_name} ({low_region_value:,.0f})")
    else:
        st.metric("المنطقة الأقل مبيعًا", "-")

st.divider()

color_palette = px.colors.qualitative.Set2

st.subheader("📈 الإيرادات بمرور الوقت")
fig_time = px.line(
    filtered_df, x="التاريخ", y="الإيرادات", color="المنتج", markers=True,
    color_discrete_sequence=color_palette, title="الإيرادات اليومية حسب المنتج",
    template='plotly_white'
)
fig_time.update_traces(
    line=dict(width=3, dash="solid"),  # إضافة نمط خط
    hovertemplate="التاريخ: %{x|%Y-%m-%d}<br>الإيرادات: %{y:,.0f}<br>المنتج: %{customdata}",
    customdata=filtered_df["المنتج"]
)
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
    font=dict(family="Cairo", size=14, color=TEXT_COLOR),  # زيادة حجم الخط
    width=1200,
    height=500  # إضافة ارتفاع محدد
)
st.plotly_chart(fig_time, use_container_width=True, config={"staticPlot": True})

st.subheader("📦 الإيرادات حسب المنتج")
fig_product = px.pie(
    filtered_df, names="المنتج", values="الإيرادات", hole=0.3,
    color_discrete_sequence=color_palette, title="نسبة الإيرادات حسب المنتج",
    template='plotly_white'
)
fig_product.update_traces(
    hovertemplate="المنتج: %{label}<br>الإيرادات: %{value:,.0f}<br>النسبة: %{percent}",
    pull=[0.05] * len(filtered_df['المنتج'].unique()),
    textinfo='percent+label'
)
fig_product.update_layout(
    title_x=0.5,
    legend_title_text="المنتج",
    font=dict(family="Cairo", size=14, color=TEXT_COLOR),
    width=1200,
    height=500
)
st.plotly_chart(fig_product, use_container_width=True, config={"staticPlot": True})

st.subheader("🏙️ الإيرادات حسب المنطقة")
region_data = filtered_df.groupby("المنطقة")["الإيرادات"].sum().reset_index()
region_data = region_data.sort_values(by="الإيرادات")  # ترتيب من الصغير إلى الكبير
fig_region = px.bar(
    region_data, x="المنطقة", y="الإيرادات", color="المنطقة",
    color_discrete_sequence=color_palette, title="إجمالي الإيرادات لكل منطقة",
    template='plotly_white'
)
fig_region.update_traces(
    hovertemplate="المنطقة: %{x}<br>الإيرادات: %{y:,.0f}",
    texttemplate='%{y:,.0f}',
    textposition='auto'
)
fig_region.update_layout(
    title_x=0.5,
    xaxis_title="المنطقة",
    yaxis_title="الإيرادات",
    plot_bgcolor="white",
    paper_bgcolor="white",
    yaxis=dict(range=[0, region_data["الإيرادات"].max() * 1.1], showgrid=True, gridcolor='lightgray'),
    showlegend=False,
    font=dict(family="Cairo", size=14, color=TEXT_COLOR),
    width=1200,
    height=500
)
st.plotly_chart(fig_region, use_container_width=True, config={"staticPlot": True})

st.divider()

st.subheader("📊 مقارنات تفصيلية")
tabs = st.tabs(["مقارنة المنتجات حسب المناطق", "مقارنة المناطق حسب المنتجات", "مقارنة المنتجات حسب الأيام", "مقارنة المناطق حسب الأيام"])

with tabs[0]:
    prod_region_data = filtered_df.groupby(["المنتج", "المنطقة"])["الإيرادات"].sum().reset_index()
    fig_prod_region = px.bar(
        prod_region_data, x="المنتج", y="الإيرادات", color="المنطقة",
        barmode="group", color_discrete_sequence=color_palette,
        title="مبيعات كل منتج موزعة على المناطق",
        template='plotly_white'
    )
    fig_prod_region.update_traces(
        hovertemplate="المنتج: %{x}<br>المنطقة: %{customdata}<br>الإيرادات: %{y:,.0f}",
        customdata=prod_region_data["المنطقة"],
        texttemplate='%{y:,.0f}',
        textposition='auto'
    )
    fig_prod_region.update_layout(
        title_x=0.5,
        xaxis_title="المنتج",
        yaxis_title="الإيرادات",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(range=[0, prod_region_data["الإيرادات"].max() * 1.1], showgrid=True, gridcolor='lightgray'),
        legend_title_text="المنطقة",
        font=dict(family="Cairo", size=14, color=TEXT_COLOR),
        width=1200,
        height=500
    )
    st.plotly_chart(fig_prod_region, use_container_width=True, config={"staticPlot": True})

with tabs[1]:
    region_prod_data = filtered_df.groupby(["المنطقة", "المنتج"])["الإيرادات"].sum().reset_index()
    region_prod_data = region_prod_data.sort_values(by="الإيرادات")  # ترتيب من الصغير إلى الكبير
    fig_region_prod = px.bar(
        region_prod_data, x="المنطقة", y="الإيرادات", color="المنتج",
        barmode="group", color_discrete_sequence=color_palette,
        title="مبيعات كل منطقة موزعة على المنتجات",
        template='plotly_white'
    )
    fig_region_prod.update_traces(
        hovertemplate="المنطقة: %{x}<br>المنتج: %{customdata}<br>الإيرادات: %{y:,.0f}",
        customdata=region_prod_data["المنتج"],
        texttemplate='%{y:,.0f}',
        textposition='auto'
    )
    fig_region_prod.update_layout(
        title_x=0.5,
        xaxis_title="المنطقة",
        yaxis_title="الإيرادات",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(range=[0, region_prod_data["الإيرادات"].max() * 1.1], showgrid=True, gridcolor='lightgray'),
        legend_title_text="المنتج",
        font=dict(family="Cairo", size=14, color=TEXT_COLOR),
        width=1200,
        height=500
    )
    st.plotly_chart(fig_region_prod, use_container_width=True, config={"staticPlot": True})

with tabs[2]:
    prod_day_data = filtered_df.groupby(["المنتج", "يوم_الأسبوع"])["الإيرادات"].sum().reset_index()
    # ترتيب الأيام حسب ترتيب الأسبوع
    day_order = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
    prod_day_data['يوم_الأسبوع'] = pd.Categorical(prod_day_data['يوم_الأسبوع'], categories=day_order, ordered=True)
    prod_day_data = prod_day_data.sort_values(by=["المنتج", "يوم_الأسبوع"])
    fig_prod_day = px.bar(
        prod_day_data, x="المنتج", y="الإيرادات", color="يوم_الأسبوع",
        barmode="group", color_discrete_sequence=color_palette,
        title="مبيعات كل منتج موزعة على الأيام",
        template='plotly_white'
    )
    fig_prod_day.update_traces(
        hovertemplate="المنتج: %{x}<br>يوم الأسبوع: %{customdata}<br>الإيرادات: %{y:,.0f}",
        customdata=prod_day_data["يوم_الأسبوع"],
        texttemplate='%{y:,.0f}',
        textposition='auto'
    )
    fig_prod_day.update_layout(
        title_x=0.5,
        xaxis_title="المنتج",
        yaxis_title="الإيرادات",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(range=[0, prod_day_data["الإيرادات"].max() * 1.1], showgrid=True, gridcolor='lightgray'),
        legend_title_text="يوم الأسبوع",
        font=dict(family="Cairo", size=14, color=TEXT_COLOR),
        width=1200,
        height=500
    )
    st.plotly_chart(fig_prod_day, use_container_width=True, config={"staticPlot": True})

with tabs[3]:
    region_day_data = filtered_df.groupby(["المنطقة", "يوم_الأسبوع"])["الإيرادات"].sum().reset_index()
    # ترتيب الأيام حسب ترتيب الأسبوع
    region_day_data['يوم_الأسبوع'] = pd.Categorical(region_day_data['يوم_الأسبوع'], categories=day_order, ordered=True)
    region_day_data = region_day_data.sort_values(by=["المنطقة", "يوم_الأسبوع"])
    fig_region_day = px.bar(
        region_day_data, x="المنطقة", y="الإيرادات", color="يوم_الأسبوع",
        barmode="group", color_discrete_sequence=color_palette,
        title="مبيعات كل منطقة موزعة على الأيام",
        template='plotly_white'
    )
    fig_region_day.update_traces(
        hovertemplate="المنطقة: %{x}<br>يوم الأسبوع: %{customdata}<br>الإيرادات: %{y:,.0f}",
        customdata=region_day_data["يوم_الأسبوع"],
        texttemplate='%{y:,.0f}',
        textposition='auto'
    )
    fig_region_day.update_layout(
        title_x=0.5,
        xaxis_title="المنطقة",
        yaxis_title="الإيرادات",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(range=[0, region_day_data["الإيرادات"].max() * 1.1], showgrid=True, gridcolor='lightgray'),
        legend_title_text="يوم الأسبوع",
        font=dict(family="Cairo", size=14, color=TEXT_COLOR),
        width=1200,
        height=500
    )
    st.plotly_chart(fig_region_day, use_container_width=True, config={"staticPlot": True})

st.divider()

# قسم جديد: تحليل تأثير الأيام على المبيعات
st.subheader("📊 تحليل تأثير الأيام على المبيعات")
st.caption("تحليل كيفية تأثير أيام الأسبوع على مبيعات منتج معين في منطقة معينة")

# فلاتر لاختيار المنتج والمنطقة
col1, col2 = st.columns(2)
with col1:
    selected_product = st.selectbox("اختر المنتج:", filtered_df["المنتج"].unique(), key="analysis_product")
with col2:
    selected_region = st.selectbox("اختر المنطقة:", filtered_df["المنطقة"].unique(), key="analysis_region")

# تصفية البيانات بناءً على المنتج والمنطقة المختارة
analysis_df = filtered_df[
    (filtered_df["المنتج"] == selected_product) &
    (filtered_df["المنطقة"] == selected_region)
].groupby("يوم_الأسبوع")["الإيرادات"].sum().reset_index()

# ترتيب الأيام حسب ترتيب الأسبوع
analysis_df['يوم_الأسبوع'] = pd.Categorical(analysis_df['يوم_الأسبوع'], categories=day_order, ordered=True)
analysis_df = analysis_df.sort_values(by="يوم_الأسبوع")

# حساب المتوسط واليوم الأعلى والأقل
if not analysis_df.empty:
    avg_sales = analysis_df["الإيرادات"].mean()
    max_day = analysis_df.loc[analysis_df["الإيرادات"].idxmax()]
    min_day = analysis_df.loc[analysis_df["الإيرادات"].idxmin()]
    max_percentage = ((max_day["الإيرادات"] - avg_sales) / avg_sales * 100) if avg_sales > 0 else 0
    min_percentage = ((avg_sales - min_day["الإيرادات"]) / avg_sales * 100) if avg_sales > 0 else 0

    # رسم بياني للمبيعات حسب الأيام
    fig_analysis = px.bar(
        analysis_df,
        x="يوم_الأسبوع",
        y="الإيرادات",
        title=f"مبيعات {selected_product} في {selected_region} حسب الأيام",
        color="يوم_الأسبوع",
        color_discrete_sequence=px.colors.qualitative.Set3,
        template='plotly_white'
    )
    fig_analysis.update_traces(
        hovertemplate="اليوم: %{x}<br>الإيرادات: %{y:,.0f}",
        texttemplate='%{y:,.0f}',
        textposition='auto'
    )
    fig_analysis.update_layout(
        title_x=0.5,
        xaxis_title="يوم الأسبوع",
        yaxis_title="الإيرادات",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
        showlegend=False,
        font=dict(family="Cairo", size=14, color=TEXT_COLOR),
        width=1200,
        height=500
    )
    st.plotly_chart(fig_analysis, use_container_width=True, config={"staticPlot": True})

    # عرض الإحصائيات
    st.markdown(f"**المتوسط اليومي للمبيعات:** {avg_sales:,.0f}")
    st.markdown(f"**اليوم الأعلى مبيعًا:** {max_day['يوم_الأسبوع']} ({max_day['الإيرادات']:,.0f}, +{max_percentage:.1f}%)")
    st.markdown(f"**اليوم الأقل مبيعًا:** {min_day['يوم_الأسبوع']} ({min_day['الإيرادات']:,.0f}, -{min_percentage:.1f}%)")
else:
    st.write("لا توجد بيانات كافية للتحليل بناءً على الاختيارات الحالية.")

st.divider()

st.subheader("📋 البيانات التفصيلية")
st.caption("عرض جميع البيانات المفلترة في جدول تفاعلي")
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
