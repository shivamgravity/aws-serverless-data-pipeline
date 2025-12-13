# AWS Serverless Data Pipeline & Analytics Dashboard

This project demonstrates a cloud-native data engineering pipeline built on **Amazon Web Services (AWS)**. It automates the generation, ingestion, and visualization of sales data using a serverless architecture.

## 🚀 Project Overview

The objective of this project was to architect a scalable data pipeline that simulates real-time transaction processing. The system automatically generates synthetic sales records, stores them in a data lake, and provides immediate business intelligence insights through a custom dashboard.

### Key Features
* **Serverless Ingestion:** Uses AWS Lambda to generate and process data without provisioning servers.
* **Scalable Storage:** Leverages Amazon S3 as a durable Data Lake for JSON documents.
* **Custom Visualization:** Features a purpose-built **Streamlit** dashboard for real-time analytics (chosen as a flexible, code-first alternative to AWS QuickSight).
* **Infrastructure as Code:** Python `boto3` is used for programmatic interaction with AWS services.

---

## 🏗️ Architecture

1.  **Data Generator (AWS Lambda):** A Python function (`GenerateSalesData`) creates simulated e-commerce transactions (Product, Price, Timestamp) and creates a JSON object.
2.  **Data Lake (Amazon S3):** These objects are stored in a dedicated S3 bucket (`blackcoffer-task-10-data-shivam`) for persistence.
3.  **Analytics Engine (Streamlit):** A local Python application connects to S3 via the `boto3` SDK, ingests the raw JSON files, processes them into a Pandas DataFrame, and renders interactive charts.

---

## 🛠️ Prerequisites

Before running this project, ensure you have the following:

* **AWS Account:** Access to the AWS Console (Free Tier is sufficient).
* **Python 3.10+:** Installed on your local machine.
* **AWS CLI:** Installed and configured with valid IAM credentials.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
    ```bash
    git clone https://github.com/shivamgravity/aws-serverless-data-pipeline
    cd aws-serverless-data-pipeline
    ```
### 2. Setup Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

    ``` bash
    # Create venv
    python -m venv venv

    # Activate venv (Windows)
    venv\Scripts\activate

    # Activate venv (Mac/Linux)
    source venv/bin/activate
    ```
### 3. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```
*(Dependencies include: streamlit, boto3, pandas, matplotlib, seaborn, python-dotenv)*

### 4. Configure AWS Credentials

To allow the local dashboard to read from S3, you must configure your AWS credentials.
Create a `.env` file in the root directory:

    ```bash
    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    AWS_DEFAULT_REGION=your_s3_bucket_region
    AWS_S3_BUCKET_NAME=your_s3_bucket_name
    ```

## How to Run

### Step 1: Generate Data (Cloud Side)

* Log in to the **AWS Console.**
* Navigate to **Lambda** > Functions > `GenerateSalesData`.
* Click the **Test** button multiple times.
* *Verification:* Go to your **S3 Bucket** and confirm that new `.json` files have appeared.

### Step 2: Launch Dashboard (Local Side)

Run the streamlit application from your terminal:

    ```bash
    streamlit run dashboard.py
    ```

### Step 3: View Analytics

* The dashboard will open automatically in your browser at `http://localhost:8501`.
* Click the **"🔄 Refresh Data"** button to pull the latest records from S3.
* Explore the **KPI Cards, Sales Charts,** and **Transaction Tables.**

## Source Code Guide

* `lambda_function.py`: The logic deployed to AWS Lambda. It uses the `random` library to simulate sales and `boto3` to write to S3.
* `dashboard.py`: The main application file. It handles the S3 connection, data parsing, and UI rendering using Streamlit and Matplotlib.
* `requirements.txt`: List of Python libraries required to run the dashboard.

## Troubleshooting

* **"No Data Found":** Ensure you have run the Lambda function at least once. Check your S3 bucket permissions.
* **"Access Denied" Error:** This usually means your local AWS credentials are missing or incorrect. Re-run `aws configure` or check your `.env` file.
* **"Module Not Found":** Ensure you activated your virtual environment before running `streamlit run`.

## Future Improvements

* **Automation:** Set up an Amazon EventBridge (CloudWatch Events) rule to trigger the Lambda function automatically every minute.
* **Database:** For higher scale, write data to Amazon DynamoDB instead of raw S3 files.
* **Hosting:** Deploy the Streamlit dashboard to AWS EC2 or Fargate so it runs permanently in the cloud.