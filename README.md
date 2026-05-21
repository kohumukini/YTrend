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
- LTSM model training & integration (PyTorch)
- Classification Model with confidence scores (scikit-learn)

## Roadmap

- [X] Complete Silver Layer
- [ ] FastAPI endpoint implementation for all layers
- [ ] React Dashboard with charts & Data display
- [ ] Buy/Sell Classifier & LTSM Model Training Pipelines
- [ ] Complete Gold ETL Layer
- [ ] Automate Ingestion
- [ ] TBA
