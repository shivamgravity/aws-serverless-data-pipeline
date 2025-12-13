import streamlit as st
import boto3
import json
import pandas as pd
from io import BytesIO

# --- Configuration ---
BUCKET_NAME = 'blackcoffer-task-10-data-shivam'
AWS_REGION = 'ap-southeast-2'

# --- AWS Connection ---
@st.cache_resource
def get_s3_client():
    return boto3.client('s3', region_name=AWS_REGION)

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
        st.subheader("Recent Transactions")
        # Data Table
        st.dataframe(df[['order_id', 'product', 'price', 'date']].sort_values(by='date', ascending=False), use_container_width=True)

else:
    st.warning("No data found in the bucket. Run your Lambda function to generate data!")
    st.info("💡 Tip: Go to AWS Console > Lambda > GenerateSalesData > Test")