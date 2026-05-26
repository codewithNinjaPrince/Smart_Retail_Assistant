# 🛒 AI-Powered Smart Retail Multi-Agent Platform with Demand Forecasting & Anomaly Detection

An intelligent retail analytics platform that combines Machine Learning, Multi-Agent AI systems, and Data Engineering to generate demand forecasts, detect anomalies, and provide actionable business insights.

This project integrates data pipelines, predictive analytics, anomaly detection, FastAPI services, and agent-based intelligence into a unified retail decision-making system.

---

## 📌 Project Overview

Retail businesses generate huge amounts of sales data daily. Manual analysis is difficult and often misses patterns that affect business decisions.

This platform solves that problem by:

- Forecasting future demand using Machine Learning
- Detecting abnormal sales behavior
- Generating intelligent insights using AI agents
- Providing visual analytics dashboards
- Exposing predictions through APIs

---

## 🚀 Features

### Demand Forecasting
- XGBoost-based sales prediction
- Future demand trend analysis

### Anomaly Detection
- Isolation Forest model
- Detect unusual sales activity
- Inventory and business risk alerts

### Multi-Agent Intelligence System
Agents included:

**1. Data Analyst Agent**
- Summarizes datasets
- Generates trends and statistics

**2. Document Assistant (RAG)**
- Retrieves contextual information
- Answers retail-related questions

**3. ML Insight Agent**
- Interprets prediction outputs
- Provides actionable recommendations

---

## 🏗 Architecture

Retail Dataset
↓
Data Cleaning
↓
Feature Engineering
↓
ML Models
├── XGBoost (Demand Forecasting)
└── Isolation Forest (Anomaly Detection)
↓
FastAPI APIs
↓
Multi-Agent System
↓
Power BI Dashboard
↓
Azure Deployment

---

## 🛠 Tech Stack

### Languages
- Python

### Data Processing
- Pandas
- NumPy

### Machine Learning
- Scikit-Learn
- XGBoost
- Isolation Forest

### Backend
- FastAPI
- Uvicorn

### AI / Agent Components
- Azure OpenAI
- Azure AI Search
- RAG Architecture
- Data Foundary 
- Crew-AI

### Visualization
- Power BI

### Cloud
- Azure

---

## 📂 Project Structure

```bash
project/
│
├── data/
│   ├── raw/
│   ├── curated/
│   └── processed/
│
├── saved_models/
│   ├── demand_model.pkl
│   ├── anomaly_model.pkl
│   └── scaler.pkl
│   └── encoders.pkl
│
├── agents/
│   ├── anomaly_agent.py
│   ├── sentiment_agent.py
│
├── api/
│   └──anomaly_api.py
│   └──demand_api.py
│   └──rag_api.py
│   └──crew_routes.py
│   └──document_routes.py
│   └──sentiment_routes.py
│ 
├── crew/
│   └──retail_crew.py
│
├── tests/test.py
│ 
├── pipelines/
│   └──clean_data.py
│   └──feature_engineering.py
│  
├── ml/
│   └──anomaly_detection.py
│   └──demand_forecast.py
│ 
├── schemas/
│   └──anomaly_schema.py
│   └──demand_schema.py
│   └──crew_schema.py
│   └──document_schema.py
│   └──rag_schema.py
│ 
├── myenv
│ 
├── rag/
│   └──chat.py
│   └──retriever.py
│   
├── document_agent/
│   └──sample_docs
│   └──document_service.py
│   └──extract_invoice.py
│  
├── uploads/
│   └──INV004.pdf
│   └──INV005.pdf
│  
├── .env
├── gitignore
├── database.py
├── main.py
├── README.md
├── requirements.txt

```

## 🔌 API Endpoints

The platform exposes REST APIs through FastAPI for demand forecasting, anomaly detection, document intelligence, sentiment analysis, and multi-agent insights.

### Core Prediction APIs

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/predict-demand` | Predict future product demand using ML models |
| POST | `/predict-anomaly` | Detect unusual sales behavior using Isolation Forest |

---

### Document Agent APIs

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/document-agent/extract` | Extract and process document content |
| GET | `/document-agent/history` | Retrieve previous document analysis history |

---

### Sentiment Agent APIs

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/sentiment-agent/analyze` | Analyze customer sentiment and feedback |
| GET | `/sentiment-agent/history` | View sentiment analysis history |

---

### Crew AI / Multi-Agent APIs

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/crew/analyze` | Generate AI-powered business insights |
| GET | `/crew/history` | Retrieve previous agent interactions |

---

### RAG AI Agent APIs

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/data-analyst-and-query-agent/ask` | Ask sales and retail insight questions |
| GET | `/data-analyst-and-query-agent/history` | Retrieve insight query history |



## Future Improvements

- Real-time streaming data
- Reinforcement learning optimization
- Advanced recommendation engine
- Full Azure deployment
- Multi-user authentication

---

## Results

The platform helps businesses:

✔ Forecast future demand

✔ Detect unusual patterns

✔ Improve inventory planning

✔ Reduce operational risk

✔ Generate AI-driven insights and query 

---

## Author

Prince Dixit

B.Tech CSE | AI & Data Engineering
