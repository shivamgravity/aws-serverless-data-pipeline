import streamlit as st
import boto3
import json
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

# --- AWS Connection ---
@st.cache_resource
def get_s3_client():
    return boto3.client(
        's3',
        region_name=os.getenv('AWS_DEFAULT_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

# --- Fetch Data Logic ---
def load_data():
    s3 = get_s3_client()
    data = []
    
    try:
        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' not in response:
            return []

        # Iterate through files and read JSON
        for obj in response['Contents']:
            file_key = obj['Key']
            if file_key.endswith('.json'):
                file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
                file_content = file_obj['Body'].read().decode('utf-8')
                json_content = json.loads(file_content)
                data.append(json_content)
                
    except Exception as e:
        st.error(f"Error fetching data from S3: {e}")
        return []

    return data

# --- The Dashboard UI ---
st.set_page_config(page_title="Serverless Sales Dashboard", layout="wide")

st.title("☁️ Serverless Data Pipeline Dashboard")
st.markdown(f"**Data Source:** AWS S3 Bucket (`{BUCKET_NAME}`)")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()

# Load Data
raw_data = load_data()

if raw_data:
    df = pd.DataFrame(raw_data)
    
    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", len(df))
    col2.metric("Total Revenue", f"${df['price'].sum():,.2f}")
    col3.metric("Avg Order Value", f"${df['price'].mean():,.2f}")

    st.divider()

    # Charts Layout
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Sales by Product")
        # Bar Chart: Product vs Revenue
        product_sales = df.groupby("product")["price"].sum().sort_values(ascending=False)
        st.bar_chart(product_sales)

    with c2:
        st.subheader("Product Distribution")
        # Pie Chart using Matplotlib
        fig1, ax1 = plt.subplots()
        product_counts = df['product'].value_counts()
        ax1.pie(product_counts, labels=product_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  
        st.pyplot(fig1)

    st.divider()

    # Line Chart
    st.subheader("Revenue Trends")
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        # Group by minute or hour to show trends if all data is from today
        daily_revenue = df.groupby(df['date'].dt.strftime('%H:%M:%S'))['price'].sum()
        st.line_chart(daily_revenue)
    else:
        st.warning("Date column missing for trend analysis.")

    st.divider()

    # Data Table
    st.subheader("Recent Transactions")
    st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)

else:
    st.warning("No data found in the bucket. Run your Lambda function to generate data!")
    st.info("💡 Tip: Go to AWS Console > Lambda > GenerateSalesData > Test")