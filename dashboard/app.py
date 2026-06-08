import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Olist E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ── Data loading ──────────────────────────────────────────────
@st.cache_data
def load_data():
    DATA_PATH = '/Users/egi/Documents/Portfolio/olist-ecommerce-analysis/data/cleaned/'
    RAW_PATH  = '/Users/egi/Documents/Portfolio/olist-ecommerce-analysis/data/'

    master      = pd.read_csv(DATA_PATH + 'master_orders.csv',
                              parse_dates=['order_purchase_timestamp'])
    products    = pd.read_csv(DATA_PATH + 'products_cleaned.csv')
    order_items = pd.read_csv(RAW_PATH  + 'olist_order_items_dataset.csv')
    sellers     = pd.read_csv(RAW_PATH  + 'olist_sellers_dataset.csv')
    payments    = pd.read_csv(RAW_PATH  + 'olist_order_payments_dataset.csv')
    return master, products, order_items, sellers, payments

master, products, order_items, sellers, payments = load_data()
complete = master[master['is_complete']].copy()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("🛒 Olist Dashboard")
st.sidebar.markdown("Brazilian E-Commerce  \nSep 2016 - Aug 2018")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "📈 Revenue Trends",
        "📦 Category Performance",
        "🚚 Delivery & Satisfaction",
        "👥 Customer Segments",
        "🏆 Seller Scorecard",
    ]
)

# ══════════════════════════════════════════════════════════════
# PAGE 1 — Revenue Trends
# ══════════════════════════════════════════════════════════════
if page == "📈 Revenue Trends":
    st.title("📈 Revenue Trends")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue",    f"R${complete['total_revenue'].sum():,.0f}")
    col2.metric("Total Orders",     f"{len(complete):,}")
    col3.metric("Unique Customers", f"{complete['customer_unique_id'].nunique():,}")
    col4.metric("Avg Order Value",  f"R${complete['total_revenue'].mean():,.2f}")

    st.markdown("---")

    complete['year_month'] = (
        complete['order_purchase_timestamp']
        .dt.to_period('M')
        .astype(str)
    )
    monthly = complete.groupby('year_month').agg(
        revenue=('total_revenue', 'sum'),
        orders =('order_id',      'count')
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=monthly['year_month'], y=monthly['revenue'],
               name='Revenue (R$)', marker_color='steelblue'),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=monthly['year_month'], y=monthly['orders'],
                   name='Order Count', line=dict(color='orange', width=2)),
        secondary_y=True
    )
    fig.update_layout(
        title='Monthly Revenue & Order Volume',
        xaxis_tickangle=-45,
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99)
    )
    fig.update_yaxes(title_text="Revenue (R$)", secondary_y=False)
    fig.update_yaxes(title_text="Order Count",  secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Key findings:**
    - Sep 2016 to Nov 2017: explosive growth from R$267 to R$1M per month
    - November 2017 peak — Black Friday effect
    - Dec 2017 to Aug 2018: plateau at R$850k to R$1M per month
    - Sep 2018 sharp drop — incomplete data, dataset ends Oct 2018
    """)

# ══════════════════════════════════════════════════════════════
# PAGE 2 — Category Performance
# ══════════════════════════════════════════════════════════════
elif page == "📦 Category Performance":
    st.title("📦 Category Performance")

    n_cats = st.slider("Number of categories to display", 5, 25, 15)

    items_with_cat = order_items.merge(
        products[['product_id', 'product_category_name']],
        on='product_id', how='left'
    )
    cat_rev = (
        items_with_cat
        .groupby('product_category_name')
        .agg(
            revenue  =('price',    'sum'),
            orders   =('order_id', 'nunique'),
            avg_price=('price',    'mean')
        )
        .reset_index()
        .sort_values('revenue', ascending=False)
        .head(n_cats)
    )

    fig = px.bar(
        cat_rev,
        x='revenue', y='product_category_name',
        orientation='h',
        color='avg_price',
        color_continuous_scale='YlGn',
        labels={
            'revenue':               'Revenue (R$)',
            'product_category_name': 'Category',
            'avg_price':             'Avg Price (R$)'
        },
        title=f'Top {n_cats} Categories by Revenue'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Key findings:**
        - #1 beleza_saude: R$1.26M, 8,836 orders
        - #2 relogios_presentes: R$1.20M, only 5,624 orders
        - relogios wins through high avg price, not volume
        """)
    with col2:
        st.info("""
        - telefonia ranks low despite 4,199 orders
        - avg price only R$77 — accessories not handsets
        - Olist is a lifestyle marketplace, not a gadget store
        """)
        
# ══════════════════════════════════════════════════════════════
# PAGE 3 - Delivery & Satifaction
# ══════════════════════════════════════════════════════════════
elif page == "🚚 Delivery & Satisfaction":
    st.title("🚚 Delivery & Satisfaction")
    
    delivered = complete[
        complete['delivery_days'].notnull() &
        complete['review_score'].notnull()
    ].copy()
    delivered['review_score_int'] = delivered['review_score'].round().astype('Int64')
    
    delay_by_score = delivered.groupby('review_score_int').agg(
        avg_delay=('delivery_delay_days', 'mean'),
        avg_delivery=('delivery_days', 'mean'),
        order_count=('order_id', 'count')
    ).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            delay_by_score,
            x='review_score_int', y='avg_delay',
            color='avg_delay', 
            color_continuous_scale='RdYlGn_r',
            labels={
                'review_score_int': 'Review Score',
                'avg_delivery': 'Avg Delivery Days'
            },
            title='Average Delivery Delay by Review Score'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = px.bar(
            delay_by_score,
            x='review_score_int', y='avg_delay',
            color='avg_delay',
            color_continuous_scale='RdYlGn',
            labels={
                'review_score_int': 'Review Score',
                'avg_delay': 'Avg Delay vs Estimate (days)'
            },
            title='Average Delay vs Estimated Date by Review Score'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    st.info("""
    **Key findings:**
    - Perfect monotonic relationship across all 5 score levels
    - 1-star customers waited TWICE as long as 5-star customers (20.9 vs 10.2 days)
    - Even 1-star orders arrived early on average — slow delivery kills satisfaction
    """)

    st.markdown("### Review Score Distribution")
    score_counts = (
        complete['review_score']
        .round()
        .astype('Int64')
        .value_counts()
        .sort_index()
    )
    score_counts = score_counts[score_counts.index.isin([1, 2, 3, 4, 5])]
    score_df = score_counts.reset_index()
    score_df.columns = ['score', 'count']

    fig3 = px.bar(
        score_df,
        x='score', y='count',
        color='score',
        color_continuous_scale='RdYlGn',
        labels={
            'score': 'Review Score',
            'count': 'Number of Orders'
        },
        title='Review Score Distribution'
    )
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4 — Customer Segments
# ══════════════════════════════════════════════════════════════
elif page == "👥 Customer Segments":
    st.title("👥 Customer Segments (RFM)")

    reference_date = complete['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    rfm = complete.groupby('customer_unique_id').agg(
        recency  =('order_purchase_timestamp', lambda x: (reference_date - x.max()).days),
        frequency=('order_id',                 'count'),
        monetary =('total_revenue',            'sum')
    ).reset_index()

    rfm['r_score'] = pd.qcut(rfm['recency'],
                              q=5, labels=[5,4,3,2,1])
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'),
                              q=5, labels=[1,2,3,4,5])
    rfm['m_score'] = pd.qcut(rfm['monetary'],
                              q=5, labels=[1,2,3,4,5])

    rfm['rfm_score'] = (rfm['r_score'].astype(int) +
                        rfm['f_score'].astype(int) +
                        rfm['m_score'].astype(int)
                    )

    def segment(score):
        if score >= 13: return 'Champions'
        elif score >= 10: return 'Loyal Customers'
        elif score >= 7: return 'Potential Loyalists'
        elif score >= 5: return 'At Risk'
        else: return 'Lost'

    rfm['segment'] = rfm['rfm_score'].apply(segment)

    seg_summary = rfm.groupby('segment').agg(
        customers   =('customer_unique_id', 'count'),
        avg_monetary=('monetary',           'mean'),
        avg_recency =('recency',            'mean')
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.treemap(
            seg_summary,
            path=['segment'],
            values='customers',
            color='avg_monetary',
            color_continuous_scale='YlGn',
            title='Segments by Size & Avg Spend'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            seg_summary.sort_values('customers', ascending=False),
            x='segment', y='customers',
            color='avg_monetary',
            color_continuous_scale='YlGn',
            labels={'customers':    'Customer Count',
                    'segment':      'Segment',
                    'avg_monetary': 'Avg Revenue (R$)'},
            title='Customer Count by Segment'
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(
        seg_summary.sort_values('customers', ascending=False),
        use_container_width=True
    )

    st.info("""
    **Key findings:**
    - 41.2% are Potential Loyalists — one good experience away from loyalty
    - Champions (8.5%) generate disproportionate revenue — protect this segment
    - 96.9% overall churn rate — growth was entirely acquisition-driven
    """)
    
# ══════════════════════════════════════════════════════════════
# PAGE 5 — Seller Scorecard
# ══════════════════════════════════════════════════════════════
elif page == "🏆 Seller Scorecard":
    st.title("🏆 Seller Scorecard")
    
    min_orders = st.slider("Minimum orders per seller", 5, 50, 10)
    
    items_master = order_items.merge(
        master[['order_id', 'review_score', 'delivery_days','is_complete']],
        on='order_id', how='left'
    )
    items_master = items_master[items_master['is_complete']]
    
    seller_scores = items_master.groupby('seller_id').agg(
        total_revenue=('price', 'sum'),
        total_orders  =('order_id', 'nunique'),
        avg_review_score=('review_score', 'mean'),
        avg_delivery_days=('delivery_days', 'mean')
    ).reset_index()
    
    seller_scores = seller_scores[seller_scores['total_orders'] >= min_orders]
    
    fig = px.scatter(
        seller_scores,
        x='avg_delivery_days', 
        y='avg_review_score',
        size='total_orders',
        color='total_revenue',
        color_continuous_scale='YlGn',
        hover_data=['seller_id', 'total_orders', 'total_revenue'],
        labels={
            'avg_delivery_days': 'Avg Delivery Days',
            'avg_review_score': 'Avg Review Score',
            'total_revenue': 'Total Revenue (R$)',
            'total_orders': 'Total Orders'
        },
        title=f'Seller Performance - {len(seller_scores):,} sellers with ≥ {min_orders} orders'   
    )
    
    med_delivery = seller_scores['avg_delivery_days'].median()
    med_review = seller_scores['avg_review_score'].median()
    fig.add_hline(
        y=med_review,
        line_dash="dash",
        line_color="grey",
        opacity=0.5,
    )
    fig.add_vline(
        x=med_delivery,
        line_dash="dash",
        line_color="grey",
        opacity=0.5,
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **Key findings:**
    - Top-left = Fast & Loved (ideal)
    - Top-right = Slow but Liked
    - Bottom-left = Fast but Disliked
    - Bottom-right = Slow & Disliked (red flag)
    - Bubble size = order volume  |  Colour = revenue
    - Dashed lines = median delivery days and median review score
    """)