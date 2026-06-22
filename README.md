<div align="center">
    <h1>Full-Stack YFinance Analysis Platform</h1>
    <img src="https://img.shields.io/badge/Project_Status-In_Development-red" height=25 />
    <p>
        <img src="https://img.shields.io/badge/React-%2320232a.svg?logo=react&logoColor=%2361DAFB" height=25/>
        <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=fff" height=25/>
        <img src="https://img.shields.io/badge/Python 3.14.4-3776AB?logo=python&logoColor=fff" height=25/>
        <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff" height=25/>
        <img src="https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white" height=25/>
    </p>
</div>
 

## Overview
YTrend is a personal full-stack project for financial analytics that ingests real-time & historical data. The data is fed into a medallion ETL pipeline that produces ML predicted buy/sell signals with confidence scores to a React dashboard. 

Built with: 
- **Backend** - Python & FastAPI
- **Storage** - PostgreSQL
- **Deep Learning Layer** - PyTorch & Scikit-Learn
- **Containerization** - Docker

> **Active Development Note:** This project is currently in development. Built concurrently with learning React/TypeScript & FastAPI as well as ML Fundamentals

--- 

## Intended Functionality
<h3>Ingestion</h3>

- Adjust ticker watchlist to house primary tickers selected by the user
- From watchlist, ingest yfinance dataframes for each ticker in json format within the bronze layer
- Store and repeat ingestion in incremented bits daily
- Storage pattern: Extract historical data from bronze layer -> Combine data with new dataframe -> Clean data -> Re-integrate with bronze layer

<h3>Transformation</h3>

- Extract data from the bronze layer as a pandas dataframe
- Run through tranformation architecture to
    - Calculate rolling SMA 20/50/100
    - Calculate rsi on 14 day period
    - Calculate Volatility on 30 day period
    - Calculate Bollinger Band (2 std away from SMA 30) range
- Push back into silver medallian architecture 
- Update silver layer with on-conflict-do-update

<h3>Prediction</h3>

<h3>Visualization</h3>

- TBC

## Architecture

**Medallian Data Architecture:** Used for ETL to refine data into predictions. 

```
yFinance Library
        |
        |
        ▼
 _______________
|               |
|     BRONZE    |   Raw Data ingestion - Unprocessed OHLCV JSON directly stored
|_______________|
        |
        |
        ▼
 _______________
|               |
|     SILVER    |   Feature Engineering - RSI, MA, Volatility, Bollinger Band Range
|_______________|
        |
        |
        ▼
 _______________
|               |
|      GOLD     |   Predictions - LSTM price forecast + buy/sell signal from classification
|_______________|

Additional Database Tables

 _______________
|               |
|    PullLog    | Stores intake information - Tickers Pulled, ingestion date, ingestion success, and error messages
|_______________|

 _______________
|               |
|   WatchList   | Stores ticker information - Tickers watched, tickers active, & date added
|_______________|

```

## Tech
| Tech Layer | Technology |
|---|---|
| **Frontend** | React, Typescript, Tailwind CSS, Vite
| **Backend**  | Python, FastAPI, SQLAlchemy
| **Database** | PostgreSQL
| **ML/Data**  | PyTorch, Scikit-Learn, yFinance, Pandas
| **Infrastructure** | Docker, Docker Compose
| **Visualization** | Matplotlib, Seaborn, Tableau (tbd)

## Features

### Working/Built
- Containerized environment with Docker Compose (except tableau)
- PostgreSQL Database with SQLAlchemy Mapping
- Medallian Schema
- yFinance Data Backfill & Data Ingestion
- Pull logging schema for ingestion tracking

### Next Steps
- Silver Layer: Feature Engineering (RSI, MA, Volatility)
- FastAPI Endpoings
- React/TypeScript Dashboard
- LSTM model training & integration (PyTorch)
- Classification Model with confidence scores (scikit-learn)

## Roadmap

- [X] Complete Silver Layer
- [ ] FastAPI endpoint implementation for all layers
- [ ] React Dashboard with charts & Data display
- [ ] Buy/Sell Classifier & LSTM Model Training Pipelines
- [ ] Complete Gold ETL Layer
- [ ] Automate Ingestion
- [ ] TBA

## Lessons Learned
- Project development should closely model the agile framework. Incremental steps for database features include a roadmap from SQLite Files -> Localized Postgres -> Dockerized Postgres Imaging to produce consistent deliverables without wasting time on environment creation. 
- FastAPI routers are built like React components in their architecture, allowing main app to run complex delegated tasks with just headers and reducing overhead. 
- Models require vast amounts of data. Models like LSTMs especially require lots of information in order to both create weights and reinforce those weights. For this system, the model has to both learn the weights and the patterns based on several tickers, which have similar instances of ups/downs, especially for stocks that have survived market collapse and have sustained themselves over the years.
- Software often expands much further than anticipated. Although this is seemingly intuitive, the realization hits when building full-stack applications with dysfunctional features requiring an increase in the amounts of features. 

## Model Performance
The LSTM model was trained across 10 large-cap and mega-cap tickers on max historical data. The data was split 70/15/15. The model achieves ~90% directional accuracy on held-out testing data , predicting the monthly price direction and estimated price percentage change from a 42 look back window. 

## Progress Images

<div align="center">
  <img src="./images/Screenshot 2026-06-19 192736.png" width="70%" alt="ML Model Loss Over Epochs">
  <p><em>Figure 1: Training and validation loss over epochs. Shows model convergence without overfitting</em></p>
</div>

<div align="center">
    <img src="./images/Screenshot%202026-06-19%20192743.png">
    <p><em>Figure 2: Prediction data overlayed atop true values. Shows model directional accuracy. </em></p>
</div>

<div align="center">
    <img src="./images/Screenshot%202026-06-21%20163932.png">
    <p><em>Figure 3: Frontend Dashboard UI. Shows interactive graph, and sidebar with real data and dummy stats </em></p>
</div>

<div align="center">
    <img src="./images/Screenshot 2026-06-21 165920.png">
    <p><em>Figure 4: Confusion matrix comparing counts of prediction data vs true data. Shows model is more conservative with guesswork </em></p>
</div>