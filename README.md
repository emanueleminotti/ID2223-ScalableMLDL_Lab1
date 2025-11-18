# Air Quality Prediction Service
**ID2223 – Lab 1 (HT2025)**  
*Predictive Air Quality Modeling with Feature Stores and Serverless Pipelines*

---

## Overview

This project implements a **serverless machine learning system** that predicts **PM2.5 air quality levels** for two air quality sensors in **Malmö, Sweden**:

- **Rådhuset**
- **Dalaplan**

The goal of the lab is to build a complete end-to-end pipeline that ingests weather and air-quality data, creates features, trains a predictive model, runs batch inference, and exposes predictions through a simple dashboard.  

This project is part of the course **ID2223: Scalable Machine Learning Systems**, following the workflow from the book *Building ML Systems with a Feature Store*.

---

## Features

### ✅ Air Quality Forecasting  
We forecast PM2.5 values for the next **7–10 days** using a model trained on:

- Historical PM2.5 measurements  
- Historical and forecasted weather data  
- Sensor-specific contextual features  

### ✅ Two Malmö Sensors Implemented  
We implemented the full pipeline for two AQI sensors:

- **Malmö – Rådhuset**
- **Malmö – Dalaplan**

These sensors were selected because they provide **high-quality historical data** on https://aqicn.org.

### ✅ Reproducible Serverless ML Pipelines  
Using **Hopsworks**, **GitHub Actions**, and **Jupyter notebooks**, we implemented:

1. **Backfill feature pipeline**  
   Loads >1 year of historical weather and air-quality data and writes them to feature groups.

2. **Daily feature pipeline**  
   Updates the Feature Store with yesterday’s observations and next-week forecasts.

3. **Training pipeline**  
   Creates a Feature View, trains an XGBoost regression model, and registers it in Hopsworks.

4. **Batch inference pipeline**  
   Downloads the latest model, generates predictions, and creates the dashboard PNG.

### ✅ Dashboard Visualization  
We provide a dashboard that visualizes:

- 7-day PM2.5 forecast  
- Historical data (hindcast)  
- Comparison of predicted vs real measurements  

The dashboard is publicly accessible as required.

---

## How to Run the Project

### 1. Create Accounts
- **Hopsworks.ai** (Feature Store)
- **GitHub** (GitHub Actions for serverless scheduling)

### 2. Add Secrets
Store `HOPSWORKS_API_KEY` in:

- GitHub → Settings → Secrets → Actions

### 3. Run the Pipelines
You can run all pipelines locally from Jupyter, or schedule them using GitHub Actions.

### 4. View Dashboard
The batch inference pipeline generates a forecast PNG for both Rådhuset and Dalaplan.

---

## Deliverables

✔ Source code in GitHub repository  
✔ README.md (this document)  
✔ Public dashboard URL  
✔ Implementation of forecasting for **Rådhuset** and **Dalaplan** sensors  
✔ All pipelines completed as per lab requirements  

---

## References

- *Building ML Systems with a Feature Store*  
  https://github.com/featurestorebook/mlfs-book  

- AQI Sensor Data  
  https://aqicn.org  

- Weather Forecast Data  
  https://open-meteo.com  

---

## Authors

Emanuele Minotti - minotti@kth.se
Stefano Romano - sromano@kth.se

Group project for ID2223 – HT2025  
KTH Royal Institute of Technology  

