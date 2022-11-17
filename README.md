<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/7943/7943618.png" alt"" width=256>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3110/"><img src="https://img.shields.io/badge/python-3.11-blue" alt=""></a>
  <a href="https://pypi.org/project/fastapi/0.86.0/"><img src="https://img.shields.io/badge/fastapi-0.86.0-099" alt=""></a>
  <a href="https://github.com/unskvort/FMCG-price-monitoring-FastAPI"><img src="https://img.shields.io/badge/version-0.0.1-lightgrey" alt=""></a>
</p>

<p align="center">
<a href="https://github.com/unskvort/FMCG-price-monitoring-FastAPI/actions/workflows/storeCI.yml"><img src="https://github.com/unskvort/FMCG-price-monitoring-FastAPI/actions/workflows/storeCI.yml/badge.svg" alt=""></a>
</p>

## About
Daily monitoring Fast Moving Consumer Goods prices in Russia

## Settings
`/src/dev.env`

## Setup

##### 1. Clone project
```
git clone https://github.com/unskvort/FMCG-price-monitoring-FastAPI.git
```
##### 2. Install requirements
```
cd FMCG-price-monitoring-FastAPI/ && pip install -r requirements.txt
```
##### 2. Run project
```
cd src && uvicorn main:app --reload
```
## Migrations
##### Autogenerate a new migration
```
alembic revision --autogenerate -m "description"
```
##### Apply the migration
```
alembic upgrade head
```
