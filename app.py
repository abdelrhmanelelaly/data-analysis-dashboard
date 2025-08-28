import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# نظام الألوان المحسن (ألوان فاتحة واحترافية)
COLOR_PALETTE = {
    "primary": "#4A90E2",       # أزرق متوسط (رئيسي)
    "primary_light": "#74B9F5", # أزرق فاتح
    "secondary": "#50C878",     # أخضر نضرة
    "background": "#F8FAFE",   # خلفية فاتحة جدا
    "surface": "#FFFFFF",       # سطح أبيض
    "text": "#2B2D42",          # نص داكن
    "text_light": "#8D99AE",    # نص فاتح
    "error": "#FF6B6B",         # أحمر للخطأ
    "warning": "#FFD166",       # أصفر للتحذير
    "success": "#06D6A0",       # أخضر للنجاح
    "info": "#118AB2",          # أزرق للمعلومات
    "gradient1": "#4A90E2",     # تدرج 1
    "gradient2": "#7B68EE"      # تدرج 2
}

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

# تهيئة الصفحة مع خلفية مخصصة وإعدادات محسنة
st.set_page_config(
    page_title="لوحة تحليل المبيعات | داشبورد احترافي",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إضافة CSS مخصص لتحسين المظهر
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

    :root {{
        --primary-color: {COLOR_PALETTE["primary"]};
        --primary-light: {COLOR_PALETTE["primary_light"]};
        --secondary-color: {COLOR_PALETTE["secondary"]};
        --background-color: {COLOR_PALETTE["background"]};
        --surface-color: {COLOR_PALETTE["surface"]};
        --text-color: {COLOR_PALETTE["text"]};
        --text-light: {COLOR_PALETTE["text_light"]};
        --error-color: {COLOR_PALETTE["error"]};
        --warning-color: {COLOR_PALETTE["warning"]};
        --success-color: {COLOR_PALETTE["success"]};
        --info-color: {COLOR_PALETTE["info"]};
    }}

    .stApp {{
        background-color: var(--background-color);
        font-family: 'Cairo', sans-serif;
    }}

    /* تحسين العنوان الرئيسي */
    .main-title {{
        color: var(--text-color);
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }}

    /* تحسين الفلاتر */
    .filter-container {{
        background-color: var(--surface-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }}

    .filter-title {{
        color: var(--primary-color);
        font-weight: 600;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }}

    /* تحسين بطاقات KPI */
    .metric-card {{
        background-color: var(--surface-color);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid var(--primary-color);
        transition: all 0.3s ease;
    }}

    .metric-card:hover {{
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}

    .metric-title {{
        color: var(--text-light);
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }}

    .metric-value {{
        color: var(--text-color);
        font-size: 1.8rem;
        font-weight: 700;
    }}

    /* تحسين التابز */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        margin-bottom: 1rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: var(--surface-color);
        border-radius: 8px 8px 0 0;
        padding: 0.8rem 1.5rem;
        border: none;
        color: var(--text-light);
        transition: all 0.2s ease;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: var(--surface-color);
        color: var(--primary-color);
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}

    /* تحسين الجدول */
    .stDataFrame {{
        background-color: var(--surface-color);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}

    /* تحسين زر التحميل */
    .stDownloadButton {{
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }}

    .stDownloadButton:hover {{
        background-color: var(--primary-light);
        transform: translateY(-1px);
    }}

    /* تحسين الفاصل */
    .stDivider {{
        background: linear-gradient(to right, transparent, rgba(0,0,0,0.1), transparent);
        height: 1px;
        margin: 2rem 0;
    }}

    /* تحسين بطاقة التحليل */
    .analysis-card {{
        background: linear-gradient(135deg, {COLOR_PALETTE["gradient1"]}, {COLOR_PALETTE["gradient2"]});
        border-radius: 12px;
        padding: 2rem;
        color: white;
        margin-bottom: 2rem;
    }}

    .analysis-title {{
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}

    /* تحسين الفوتر */
    .footer {{
        text-align: center;
        color: var(--text-light);
        font-size: 0.9rem;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }}

    /* تحسين الشريط الجانبي */
    .st-emotion-cache-1v0mbdj {{
        background-color: var(--surface-color);
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05);
    }}

    /* تحسين عناوين الأقسام */
    .section-header {{
        color: var(--text-color);
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .section-icon {{
        color: var(--primary-color);
    }}

    /* تحسين الرسوم البيانية */
    .stPlotlyChart {{
        background-color: var(--surface-color);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي مع أيقونة
st.markdown('<h1 class="main-title">📊 لوحة تحليل المبيعات الاحترافية</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:var(--text-light); margin-bottom:2rem;">منصة تحليل بيانات متقدمة لأداء المبيعات مع واجهة مستخدم عصرية وتفاعلية</p>', unsafe_allow_html=True)

# الشريط الجانبي للفلاتر
with st.sidebar:
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="filter-title">🔍 فلاتر البيانات</h3>', unsafe_allow_html=True)

    st.markdown('<p style="color:var(--text-light); font-size:0.9rem; margin-bottom:1rem;">اختر المعايير لفلترة البيانات:</p>', unsafe_allow_html=True)

    product_filter = st.multiselect(
        "المنتجات:",
        options=df["المنتج"].unique(),
        default=df["المنتج"].unique(),
        placeholder="اختر منتج..."
    )

    region_filter = st.multiselect(
        "المناطق:",
        options=df["المنطقة"].unique(),
        default=df["المنطقة"].unique(),
        placeholder="اختر منطقة..."
    )

    min_date, max_date = df["التاريخ"].min(), df["التاريخ"].max()
    date_filter = st.date_input(
        "الفترة الزمنية:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown('<div style="margin-top:1.5rem;">')
    if st.button("✅ تطبيق الفلاتر", use_container_width=True):
        st.rerun()
    st.markdown('</div>')

    st.markdown('</div>', unsafe_allow_html=True)

# تصفية البيانات
filtered_df = df[
    (df["المنتج"].isin(product_filter)) &
    (df["المنطقة"].isin(region_filter)) &
    (df["التاريخ"] >= pd.to_datetime(date_filter[0])) &
    (df["التاريخ"] <= pd.to_datetime(date_filter[1]))
]

# قسم لمحة سريعة مع بطاقات KPI محسنة
st.markdown('<div class="section-header">📌 <span>لمحة سريعة عن الأداء</span></div>', unsafe_allow_html=True)
st.markdown('<p style="color:var(--text-light); margin-bottom:1.5rem;">نظرة عامة على المؤشرات الرئيسية بناءً على الفلاتر المختارة</p>', unsafe_allow_html=True)

kpi_cols = st.columns(4)
with kpi_cols[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">إجمالي الإيرادات</div>
        <div class="metric-value">{filtered_df['الإيرادات'].sum():,.0f} ريال</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    top_day_series = filtered_df.groupby("يوم_الأسبوع")["الإيرادات"].sum()
    if not top_day_series.empty:
        top_day_name = top_day_series.idxmax()
        top_day_value = top_day_series.max()
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid var(--success-color);">
            <div class="metric-title">اليوم الأعلى مبيعًا</div>
            <div class="metric-value">{top_day_name}</div>
            <div style="color:var(--text-light); font-size:0.9rem; margin-top:0.5rem;">{top_day_value:,.0f} ريال</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">اليوم الأعلى مبيعًا</div>
            <div class="metric-value">-</div>
        </div>
        """, unsafe_allow_html=True)

with kpi_cols[2]:
    top_product_series = filtered_df.groupby("المنتج")["الإيرادات"].sum()
    if not top_product_series.empty:
        top_prod_name = top_product_series.idxmax()
        top_prod_value = top_product_series.max()
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid var(--secondary-color);">
            <div class="metric-title">المنتج الأعلى مبيعًا</div>
            <div class="metric-value">{top_prod_name}</div>
            <div style="color:var(--text-light); font-size:0.9rem; margin-top:0.5rem;">{top_prod_value:,.0f} ريال</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">المنتج الأعلى مبيعًا</div>
            <div class="metric-value">-</div>
        </div>
        """, unsafe_allow_html=True)

with kpi_cols[3]:
    low_product_series = filtered_df.groupby("المنتج")["الإيرادات"].sum()
    if not low_product_series.empty:
        low_prod_name = low_product_series.idxmin()
        low_prod_value = low_product_series.min()
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid var(--error-color);">
            <div class="metric-title">المنتج الأقل مبيعًا</div>
            <div class="metric-value">{low_prod_name}</div>
            <div style="color:var(--text-light); font-size:0.9rem; margin-top:0.5rem;">{low_prod_value:,.0f} ريال</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">المنتج الأقل مبيعًا</div>
            <div class="metric-value">-</div>
        </div>
        """, unsafe_allow_html=True)

# قسم الرسوم البيانية الرئيسية
st.divider()

# رسم بياني للإيرادات بمرور الوقت مع تحسينات بصرية
st.markdown('<div class="section-header">📈 <span>اتجاهات الإيرادات بمرور الوقت</span></div>', unsafe_allow_html=True)

fig_time = make_subplots(specs=[[{"secondary_y": False}]])
for product in filtered_df["المنتج"].unique():
    product_data = filtered_df[filtered_df["المنتج"] == product]
    fig_time.add_trace(
        go.Scatter(
            x=product_data["التاريخ"],
            y=product_data["الإيرادات"],
            name=product,
            mode='lines+markers',
            line=dict(width=3, color=px.colors.qualitative.Set2[filtered_df["المنتج"].unique().tolist().index(product)]),
            marker=dict(size=6),
            hovertemplate="<b>%{x|%Y-%m-%d}</b><br>إيرادات: %{y:,.0f} ريال<br>المنتج: " + product + "<extra></extra>"
        )
    )

fig_time.update_layout(
    title={
        'text': "الإيرادات اليومية حسب المنتج",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=18, family="Cairo")
    },
    xaxis_title="التاريخ",
    yaxis_title="الإيرادات (ريال)",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Cairo"
    ),
    margin=dict(l=20, r=20, t=60, b=20),
    height=500
)

fig_time.update_yaxes(
    showgrid=True,
    gridcolor='rgba(0,0,0,0.05)',
    zeroline=True,
    zerolinecolor='rgba(0,0,0,0.1)'
)

fig_time.update_xaxes(
    showgrid=True,
    gridcolor='rgba(0,0,0,0.05)',
    rangeslider_visible=True
)

st.plotly_chart(fig_time, use_container_width=True, config={"displayModeBar": False})

# قسم مقارنات تفصيلية مع تبويبات محسنة
st.divider()
st.markdown('<div class="section-header">🔍 <span>مقارنات تفصيلية</span></div>', unsafe_allow_html=True)

tabs = st.tabs([
    "📦 مقارنة المنتجات حسب المناطق",
    "🏙️ مقارنة المناطق حسب المنتجات",
    "📅 مقارنة المنتجات حسب الأيام",
    "🗓️ مقارنة المناطق حسب الأيام"
])

with tabs[0]:
    prod_region_data = filtered_df.groupby(["المنتج", "المنطقة"])["الإيرادات"].sum().reset_index()
    fig_prod_region = px.bar(
        prod_region_data,
        x="المنتج",
        y="الإيرادات",
        color="المنطقة",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="مبيعات كل منتج موزعة على المناطق",
        template='plotly_white'
    )
    fig_prod_region.update_traces(
        hovertemplate="<b>%{{x}}</b><br>المنطقة: %{{customdata[0]}}<br>الإيرادات: %{{y:,.0f}} ريال<extra></extra>",
        customdata=prod_region_data[["المنطقة"]],
        texttemplate='%{y:,.0f}',
        textposition='auto',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )
    fig_prod_region.update_layout(
        title={
            'text': "مبيعات المنتجات حسب المناطق",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="المنتج",
        yaxis_title="الإيرادات (ريال)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend_title_text="المنطقة",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Cairo"
        )
    )
    st.plotly_chart(fig_prod_region, use_container_width=True, config={"displayModeBar": False})

with tabs[1]:
    region_prod_data = filtered_df.groupby(["المنطقة", "المنتج"])["الإيرادات"].sum().reset_index()
    fig_region_prod = px.bar(
        region_prod_data,
        x="المنطقة",
        y="الإيرادات",
        color="المنتج",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="مبيعات كل منطقة موزعة على المنتجات",
        template='plotly_white'
    )
    fig_region_prod.update_traces(
        hovertemplate="<b>%{{x}}</b><br>المنتج: %{{customdata[0]}}<br>الإيرادات: %{{y:,.0f}} ريال<extra></extra>",
        customdata=region_prod_data[["المنتج"]],
        texttemplate='%{y:,.0f}',
        textposition='auto',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )
    fig_region_prod.update_layout(
        title={
            'text': "مبيعات المناطق حسب المنتجات",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="المنطقة",
        yaxis_title="الإيرادات (ريال)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend_title_text="المنتج",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Cairo"
        )
    )
    st.plotly_chart(fig_region_prod, use_container_width=True, config={"displayModeBar": False})

with tabs[2]:
    day_order = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
    prod_day_data = filtered_df.groupby(["المنتج", "يوم_الأسبوع"])["الإيرادات"].sum().reset_index()
    prod_day_data['يوم_الأسبوع'] = pd.Categorical(prod_day_data['يوم_الأسبوع'], categories=day_order, ordered=True)
    prod_day_data = prod_day_data.sort_values(by=["المنتج", "يوم_الأسبوع"])

    fig_prod_day = px.bar(
        prod_day_data,
        x="المنتج",
        y="الإيرادات",
        color="يوم_الأسبوع",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="مبيعات المنتجات حسب أيام الأسبوع",
        template='plotly_white'
    )
    fig_prod_day.update_traces(
        hovertemplate="<b>%{{x}}</b><br>يوم الأسبوع: %{{customdata[0]}}<br>الإيرادات: %{{y:,.0f}} ريال<extra></extra>",
        customdata=prod_day_data[["يوم_الأسبوع"]],
        texttemplate='%{y:,.0f}',
        textposition='auto',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )
    fig_prod_day.update_layout(
        title={
            'text': "مبيعات المنتجات حسب أيام الأسبوع",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="المنتج",
        yaxis_title="الإيرادات (ريال)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend_title_text="يوم الأسبوع",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Cairo"
        )
    )
    st.plotly_chart(fig_prod_day, use_container_width=True, config={"displayModeBar": False})

with tabs[3]:
    region_day_data = filtered_df.groupby(["المنطقة", "يوم_الأسبوع"])["الإيرادات"].sum().reset_index()
    region_day_data['يوم_الأسبوع'] = pd.Categorical(region_day_data['يوم_الأسبوع'], categories=day_order, ordered=True)
    region_day_data = region_day_data.sort_values(by=["المنطقة", "يوم_الأسبوع"])

    fig_region_day = px.bar(
        region_day_data,
        x="المنطقة",
        y="الإيرادات",
        color="يوم_الأسبوع",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="مبيعات المناطق حسب أيام الأسبوع",
        template='plotly_white'
    )
    fig_region_day.update_traces(
        hovertemplate="<b>%{{x}}</b><br>يوم الأسبوع: %{{customdata[0]}}<br>الإيرادات: %{{y:,.0f}} ريال<extra></extra>",
        customdata=region_day_data[["يوم_الأسبوع"]],
        texttemplate='%{y:,.0f}',
        textposition='auto',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )
    fig_region_day.update_layout(
        title={
            'text': "مبيعات المناطق حسب أيام الأسبوع",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="المنطقة",
        yaxis_title="الإيرادات (ريال)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend_title_text="يوم الأسبوع",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Cairo"
        )
    )
    st.plotly_chart(fig_region_day, use_container_width=True, config={"displayModeBar": False})

# قسم تحليل تأثير الأيام على المبيعات
st.divider()
st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
st.markdown('<div class="analysis-title">🔮 تحليل تأثير أيام الأسبوع على المبيعات</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    selected_product = st.selectbox(
        "اختر المنتج:",
        options=filtered_df["المنتج"].unique(),
        key="analysis_product",
        label_visibility="collapsed"
    )
with col2:
    selected_region = st.selectbox(
        "اختر المنطقة:",
        options=filtered_df["المنطقة"].unique(),
        key="analysis_region",
        label_visibility="collapsed"
    )

analysis_df = filtered_df[
    (filtered_df["المنتج"] == selected_product) &
    (filtered_df["المنطقة"] == selected_region)
].groupby("يوم_الأسبوع")["الإيرادات"].sum().reset_index()

analysis_df['يوم_الأسبوع'] = pd.Categorical(analysis_df['يوم_الأسبوع'], categories=day_order, ordered=True)
analysis_df = analysis_df.sort_values(by="يوم_الأسبوع")

if not analysis_df.empty:
    avg_sales = analysis_df["الإيرادات"].mean()
    max_day = analysis_df.loc[analysis_df["الإيرادات"].idxmax()]
    min_day = analysis_df.loc[analysis_df["الإيرادات"].idxmin()]
    max_percentage = ((max_day["الإيرادات"] - avg_sales) / avg_sales * 100) if avg_sales > 0 else 0
    min_percentage = ((avg_sales - min_day["الإيرادات"]) / avg_sales * 100) if avg_sales > 0 else 0

    fig_analysis = go.Figure()
    fig_analysis.add_trace(go.Bar(
        x=analysis_df["يوم_الأسبوع"],
        y=analysis_df["الإيرادات"],
        marker_color=px.colors.qualitative.Pastel,
        hovertemplate="<b>%{x}</b><br>الإيرادات: %{y:,.0f} ريال<extra></extra>",
        text=analysis_df["الإيرادات"].apply(lambda x: f"{x:,.0f}"),
        textposition='auto'
    ))

    fig_analysis.add_hline(
        y=avg_sales,
        line_dash="dot",
        line_color="rgba(255, 107, 107, 0.7)",
        annotation_text=f"المتوسط: {avg_sales:,.0f} ريال",
        annotation_position="top right",
        annotation_font_size=14,
        annotation_font_color="rgba(255, 107, 107, 0.8)"
    )

    fig_analysis.update_layout(
        title={
            'text': f"مبيعات {selected_product} في {selected_region} حسب أيام الأسبوع",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=16, family="Cairo")
        },
        xaxis_title="يوم الأسبوع",
        yaxis_title="الإيرادات (ريال)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Cairo"
        ),
        font=dict(family="Cairo", size=12)
    )

    st.plotly_chart(fig_analysis, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div style="display:flex; justify-content:space-around; margin-top:1.5rem; background-color:rgba(255,255,255,0.2); padding:1rem; border-radius:8px;">
        <div style="text-align:center;">
            <div style="font-size:1.2rem; font-weight:600;">{avg_sales:,.0f}</div>
            <div style="font-size:0.9rem; opacity:0.9;">متوسط المبيعات اليومي</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:1.2rem; font-weight:600; color:#06D6A0;">{max_day['يوم_الأسبوع']}</div>
            <div style="font-size:0.9rem; opacity:0.9;">اليوم الأعلى (+{max_percentage:.1f}%)</div>
            <div style="font-size:0.9rem; font-weight:600;">{max_day['الإيرادات']:,.0f} ريال</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:1.2rem; font-weight:600; color:#FF6B6B;">{min_day['يوم_الأسبوع']}</div>
            <div style="font-size:0.9rem; opacity:0.9;">اليوم الأقل (-{min_percentage:.1f}%)</div>
            <div style="font-size:0.9rem; font-weight:600;">{min_day['الإيرادات']:,.0f} ريال</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("لا توجد بيانات كافية للتحليل بناءً على الاختيارات الحالية.")

st.markdown('</div>', unsafe_allow_html=True)

# قسم البيانات التفصيلية
st.divider()
st.markdown('<div class="section-header">📋 <span>البيانات التفصيلية</span></div>', unsafe_allow_html=True)

# عرض البيانات في جدول تفاعلي مع تحسينات
st.dataframe(
    filtered_df.style
    .format("{:,.0f}", subset=["الإيرادات"])
    .applymap(lambda x: f"color: {COLOR_PALETTE['text']}; background-color: {COLOR_PALETTE['surface']};", subset=pd.IndexSlice[:, :])
    .applymap(lambda x: f"font-weight: bold; color: {COLOR_PALETTE['primary']};", subset=pd.IndexSlice[:, ["المنتج", "المنطقة"]])
    .set_properties(**{
        'border': f'1px solid {COLOR_PALETTE["background"]}',
        'text-align': 'center'
    })
    .set_table_styles([{
        'selector': 'th',
        'props': [
            ('background-color', COLOR_PALETTE["primary"]),
            ('color', 'white'),
            ('font-weight', 'bold'),
            ('text-align', 'center')
        ]
    }]),
    use_container_width=True,
    height=400
)

# زر تحميل البيانات
st.download_button(
    label="⬇️ تحميل البيانات المفلترة (CSV)",
    data=filtered_df.to_csv(index=False, encoding='utf-8-sig'),
    file_name=f"مبيعات_{pd.to_datetime('today').strftime('%Y%m%d')}.csv",
    mime="text/csv",
    key="download_button"
)

# الفوتر
st.divider()
st.markdown('''
<div class="footer">
    <p>© 2025 لوحة تحليل المبيعات الاحترافية | جميع الحقوق محفوظة</p>
    <p style="margin-top:0.5rem; font-size:0.8rem;">
        للاتصال: team@salesanalytics.com | الدعم الفني: +966 11 123 4567
    </p>
</div>
''', unsafe_allow_html=True)
