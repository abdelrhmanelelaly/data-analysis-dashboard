# في بداية الكود بعد تحميل المكتبات
import base64
from io import BytesIO

# إضافة CSS مخصصة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
    }

    .st-bf {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .st-df {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stMetric {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }

    .stPlotlyChart {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)    .metric-container:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-family: 'Cairo', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    .metric-label {
        font-family: 'Cairo', sans-serif;
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }
    
    .section-header {
        font-family: 'Cairo', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea, #764ba2);
        background-size: 100% 3px;
        background-repeat: no-repeat;
        background-position: bottom;
        border-radius: 10px 10px 0 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Cairo', sans-serif;
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .filter-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ================== تحميل البيانات ==================
@st.cache_data
def load_data():
    # إنشاء بيانات تجريبية إذا لم يكن الملف موجوداً
    try:
        df = pd.read_csv("Dataset.csv")
    except FileNotFoundError:
        # إنشاء بيانات تجريبية
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        products = ['هواتف ذكية', 'أجهزة لوحية', 'حاسوب محمول', 'سماعات', 'إكسسوارات']
        regions = ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة']
        
        np.random.seed(42)
        data = []
        for date in dates[:100]:  # أول 100 يوم
            for _ in range(np.random.randint(1, 4)):
                data.append({
                    'التاريخ': date,
                    'المنتج': np.random.choice(products),
                    'المنطقة': np.random.choice(regions),
                    'الإيرادات': np.random.randint(1000, 50000)
                })
        df = pd.DataFrame(data)
    
    df["المنتج"] = df["المنتج"].astype(str)
    df["المنطقة"] = df["المنطقة"].astype(str)
    df["التاريخ"] = pd.to_datetime(df["التاريخ"])
    return df

df = load_data()

# ================== العنوان الرئيسي ==================
st.markdown("""
<div class="main-header">
    <h1 class="main-title">📊 لوحة تحليل المبيعات الذكية</h1>
    <p class="subtitle">نظام تحليل متقدم لبيانات المبيعات والإيرادات</p>
</div>
""", unsafe_allow_html=True)

# ================== الفلاتر ==================
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    product_filter = st.multiselect(
        "🎯 اختر المنتج:", 
        df["المنتج"].unique(), 
        default=df["المنتج"].unique()
    )

with col2:
    region_filter = st.multiselect(
        "🏙️ اختر المنطقة:", 
        df["المنطقة"].unique(), 
        default=df["المنطقة"].unique()
    )

with col3:
    date_range = st.date_input(
        "📅 فترة التحليل:",
        value=(df["التاريخ"].min(), df["التاريخ"].max()),
        min_value=df["التاريخ"].min(),
        max_value=df["التاريخ"].max()
    )

st.markdown('</div>', unsafe_allow_html=True)

# تطبيق الفلاتر
filtered_df = df[
    (df["المنتج"].isin(product_filter)) & 
    (df["المنطقة"].isin(region_filter))
]

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["التاريخ"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["التاريخ"] <= pd.to_datetime(date_range[1]))
    ]

# ================== كروت الملخص ==================
st.markdown('<h2 class="section-header">📌 المؤشرات الرئيسية</h2>', unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

metrics_data = [
    ("إجمالي الإيرادات", f"{filtered_df['الإيرادات'].sum():,.0f} ريال"),
    ("متوسط الإيرادات", f"{filtered_df['الإيرادات'].mean():,.0f} ريال"),
    ("عدد المنتجات", f"{filtered_df['المنتج'].nunique()} منتج"),
    ("عدد المناطق", f"{filtered_df['المنطقة'].nunique()} منطقة")
]

for col, (label, value) in zip([kpi1, kpi2, kpi3, kpi4], metrics_data):
    with col:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{value.split()[0]}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ================== الرسوم البيانية ثلاثية الأبعاد ==================

# إعدادات الألوان المتقدمة
colors_3d = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

st.markdown('<h2 class="section-header">📈 الإيرادات بمرور الوقت (ثلاثي الأبعاد)</h2>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# رسم ثلاثي الأبعاد للإيرادات عبر الزمن
fig_3d_time = go.Figure()

for i, product in enumerate(filtered_df['المنتج'].unique()):
    product_data = filtered_df[filtered_df['المنتج'] == product]
    daily_data = product_data.groupby('التاريخ')['الإيرادات'].sum().reset_index()
    
    fig_3d_time.add_trace(go.Scatter3d(
        x=daily_data['التاريخ'],
        y=[product] * len(daily_data),
        z=daily_data['الإيرادات'],
        mode='markers+lines',
        marker=dict(
            size=8,
            color=colors_3d[i % len(colors_3d)],
            symbol='circle',
            opacity=0.8
        ),
        line=dict(
            color=colors_3d[i % len(colors_3d)],
            width=4
        ),
        name=product,
        text=[f'{product}<br>التاريخ: {date}<br>الإيرادات: {revenue:,}' 
              for date, revenue in zip(daily_data['التاريخ'], daily_data['الإيرادات'])],
        hovertemplate='%{text}<extra></extra>'
    ))

fig_3d_time.update_layout(
    scene=dict(
        xaxis_title='التاريخ',
        yaxis_title='المنتج',
        zaxis_title='الإيرادات (ريال)',
        bgcolor='rgb(240,240,240)',
        camera=dict(eye=dict(x=1.25, y=1.25, z=1.25))
    ),
    title={
        'text': 'تطور الإيرادات عبر الزمن والمنتجات',
        'x': 0.5,
        'font': {'family': 'Cairo', 'size': 20, 'color': '#2c3e50'}
    },
    font=dict(family='Cairo'),
    height=600,
    margin=dict(l=0, r=0, t=60, b=0)
)

st.plotly_chart(fig_3d_time, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================== رسم ثلاثي الأبعاد للمناطق والمنتجات ==================
st.markdown('<h2 class="section-header">🏙️ تحليل المناطق والمنتجات (ثلاثي الأبعاد)</h2>', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# إعداد البيانات للرسم ثلاثي الأبعاد
pivot_data = filtered_df.groupby(['المنطقة', 'المنتج'])['الإيرادات'].sum().reset_index()

fig_3d_surface = go.Figure()

# إنشاء surface plot
regions = pivot_data['المنطقة'].unique()
products = pivot_data['المنتج'].unique()

z_matrix = []
for region in regions:
    row = []
    for product in products:
        revenue = pivot_data[
            (pivot_data['المنطقة'] == region) & 
            (pivot_data['المنتج'] == product)
        ]['الإيرادات'].sum()
        row.append(revenue)
    z_matrix.append(row)

fig_3d_surface.add_trace(go.Surface(
    z=z_matrix,
    x=list(range(len(products))),
    y=list(range(len(regions))),
    colorscale='Viridis',
    opacity=0.8,
    contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True)
))

fig_3d_surface.update_layout(
    scene=dict(
        xaxis=dict(
            title='المنتجات',
            tickmode='array',
            tickvals=list(range(len(products))),
            ticktext=products
        ),
        yaxis=dict(
            title='المناطق',
            tickmode='array',
            tickvals=list(range(len(regions))),
            ticktext=regions
        ),
        zaxis_title='الإيرادات (ريال)',
        bgcolor='rgb(240,240,240)',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    ),
    title={
        'text': 'خريطة الإيرادات ثلاثية الأبعاد',
        'x': 0.5,
        'font': {'family': 'Cairo', 'size': 20, 'color': '#2c3e50'}
    },
    font=dict(family='Cairo'),
    height=600
)

st.plotly_chart(fig_3d_surface, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================== رسوم بيانية متقدمة أخرى ==================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="section-header">📊 توزيع الإيرادات حسب المنطقة</h2>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    region_data = filtered_df.groupby("المنطقة")["الإيرادات"].sum().reset_index()
    fig_donut = go.Figure(data=[go.Pie(
        labels=region_data["المنطقة"], 
        values=region_data["الإيرادات"],
        hole=0.6,
        marker_colors=colors_3d,
        textinfo='label+percent',
        textfont=dict(family='Cairo', size=12),
        hovertemplate='<b>%{label}</b><br>الإيرادات: %{value:,}<br>النسبة: %{percent}<extra></extra>'
    )])
    
    fig_donut.update_layout(
        title={'text': 'نسبة الإيرادات لكل منطقة', 'x': 0.5, 'font': {'family': 'Cairo'}},
        font=dict(family='Cairo'),
        height=400
    )
  
