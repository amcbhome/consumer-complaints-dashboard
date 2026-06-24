import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config for a wide layout
st.set_page_config(page_title="Consumer Complaints Dashboard", layout="wide")

st.title("📊 Consumer Complaints Executive Dashboard")
st.markdown("An interactive overview of the most critical consumer metrics and trends.")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Reads the Excel file from the same directory
    df = pd.read_excel("Consumer_Complaints.xlsx", sheet_name="Data")
    df['Date submitted'] = pd.to_datetime(df['Date submitted'])
    df['Year-Month'] = df['Date submitted'].dt.to_period('M').astype(str)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load 'Consumer_Complaints.xlsx'. Make sure it's in the same repository folder. Error: {e}")
    st.stop()

# --- KPI METRICS ---
total_complaints = len(df)
timely_yes = (df['Timely response?'] == 'Yes').sum()
timely_pct = (timely_yes / total_complaints) * 100

top_product_name = df['Product'].value_counts().idxmax()
top_channel = df['Submitted via'].value_counts().idxmax()

# Display Metrics side-by-side
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Total Complaints", value=f"{total_complaints:,}")
with kpi2:
    st.metric(label="Timely Response Rate", value=f"{timely_pct:.1f}%")
with kpi3:
    st.metric(label="Top Product Category", value=top_product_name, help="Highest volume of complaints")
with kpi4:
    st.metric(label="Primary Channel", value=top_channel)

st.markdown("---")

# --- VISUALIZATIONS ---
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2 = st.columns(2)

# 1. Top 10 Products
with row1_col1:
    st.subheader("Top 10 Products by Complaint Volume")
    top_products = df['Product'].value_counts().head(10).reset_index()
    top_products.columns = ['Product', 'Complaints']
    fig_prod = px.bar(top_products, x='Complaints', y='Product', orientation='h', color='Complaints', color_continuous_scale='viridis')
    fig_prod.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig_prod, use_container_width=True)

# 2. Top 10 Issues
with row1_col2:
    st.subheader("Top 10 Complaint Issues")
    top_issues = df['Issue'].value_counts().head(10).reset_index()
    top_issues.columns = ['Issue', 'Complaints']
    fig_issue = px.bar(top_issues, x='Complaints', y='Issue', orientation='h', color='Complaints', color_continuous_scale='magma')
    fig_issue.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig_issue, use_container_width=True)

# 3. Submission Methods
with row2_col1:
    st.subheader("Submission Methods")
    sub_via = df['Submitted via'].value_counts().reset_index()
    sub_via.columns = ['Method', 'Count']
    # FIXED: Corrected path to qualitative.Pastel
    fig_pie = px.pie(sub_via, values='Count', names='Method', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

# 4. Top Company Responses
with row2_col2:
    st.subheader("Top Company Responses to Consumers")
    comp_resp = df['Company response to consumer'].value_counts().head(5).reset_index()
    comp_resp.columns = ['Response', 'Count']
    # FIXED: Changed 'Rocket' to lowercase 'rocket'
    fig_resp = px.bar(comp_resp, x='Count', y='Response', orientation='h', color='Count', color_continuous_scale='rocket')
    fig_resp.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig_resp, use_container_width=True)

# 5. Trend Over Time
with row3_col1:
    st.subheader("Complaint Volume Trend Over Time")
    trend = df.groupby('Year-Month').size().reset_index(name='Count')
    fig_trend = px.line(trend, x='Year-Month', y='Count', markers=True)
    fig_trend.update_xaxes(tickangle=45)
    st.plotly_chart(fig_trend, use_container_width=True)

# 6. Timely Response Rate Breakdown
with row3_col2:
    st.subheader("Timely Response Distribution")
    timely = df['Timely response?'].fillna('No Response Recorded').value_counts().reset_index()
    timely.columns = ['Timely Status', 'Count']
    # FIXED: Safely using color_continuous_scale for sequential mapping instead of passing a continuous array directly to standard sequences
    fig_timely = px.bar(timely, x='Timely Status', y='Count', color='Count', color_continuous_scale='crest')
    fig_timely.update_layout(showlegend=False)
    st.plotly_chart(fig_timely, use_container_width=True)
