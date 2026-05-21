# 🏥 Healthcare Data Warehouse  End-to-End Data Engineering Project

## Overview

A production-grade, end-to-end data engineering pipeline built on Microsoft Azure. This project demonstrates a complete **Medallion Architecture** (Bronze → Silver → Gold) using Azure Data Factory for orchestration, Databricks for transformation, and ADLS Gen2 as the Delta Lake storage layer.

---

## 🏗️ Architecture

```
CSV Files (9 datasets)
        │
        ▼
ADLS Gen2 (landing container)
        │
        ▼
Azure Data Factory (Orchestration)
   pl_master_full_refresh
   ├── pl_master_bronze_load ──► Databricks: 01_bronze_ingestion
   ├── pl_master_silver_load ──► Databricks: 02_silver_transformation
   └── pl_master_gold_load   ──► Databricks: 03_gold_aggregations
        │
        ▼
ADLS Gen2 — Delta Lake Storage
   ├── /bronze  (raw + audit columns)
   ├── /silver  (cleaned + typed + deduplicated)
   └── /gold    (Star Schema: dims + facts)
        │
        ▼
Power BI Dashboards (in progress)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | Azure Data Factory |
| Compute | Azure Databricks (PySpark + SQL) |
| Storage | ADLS Gen2 (Delta Lake) |
| Authentication | Service Principal (OAuth 2.0) |
| File Format | Delta Lake |
| Reporting | Power BI (in progress) |
| Version Control | GitHub |

---

## 📊 Datasets

9 healthcare domain datasets (~550K total rows):

| Dataset | Rows | Description |
|---------|------|-------------|
| patients | 60,000 | Patient demographics + location |
| encounters | 70,000 | Hospital visits and admissions |
| diagnoses | 70,000 | Diagnosis codes and descriptions |
| claims_and_billing | 70,000 | Insurance claims and payments |
| denials | 5,998 | Claim denials and appeals |
| procedures | 126,021 | Medical procedures performed |
| medications | 94,498 | Prescribed medications |
| providers | 1,491 | Healthcare providers |
| lab_tests | 54,537 | Lab test results |

---

## 🥉 Bronze Layer — Raw Ingestion

**Notebook:** `01_bronze_ingestion`

- Reads 9 CSVs from ADLS Gen2 `landing` container
- Adds audit columns: `_ingested_at`, `_source_file`, `_layer`
- Writes Delta tables to `bronze` container
- No transformations — raw data preserved as-is

---

## 🥈 Silver Layer — Transformation

**Notebook:** `02_silver_transformation`

Transformations applied per table:

- **Date casting** — string dates → proper date types
- **String standardization** — `TRIM()` + `UPPER()` for consistency
- **Numeric rounding** — financial columns rounded to 2 decimal places
- **Deduplication** — two strategies:
  - By ID column for tables with unique IDs (`patients`, `encounters`, `claims`, `denials`, `providers`)
  - Full row dedup for tables with non-unique IDs (`diagnoses`, `procedures`, `medications`, `lab_tests`)

**Key Finding:** Source data ID columns are not always reliable unique keys — deduplication strategy validated per table.

---

## 🥇 Gold Layer — Star Schema

**Notebook:** `03_gold_aggregations`

Built a Star Schema optimized for Power BI analytics:

### Dimension Tables

| Table | Rows | Columns | Description |
|-------|------|---------|-------------|
| dim_patient | 60,000 | 14 | Demographics + city/state/zip for maps |
| dim_provider | 1,491 | 8 | Provider details and specialty |
| dim_date | 90 | 8 | Date dimension from encounter dates |

### Fact Tables

| Table | Rows | Columns | Description |
|-------|------|---------|-------------|
| fact_encounters | 70,000 | 23 | Visit trends + readmissions + demographics |
| fact_claims | 70,000 | 22 | Claims KPIs + billing + demographics |
| fact_denials | 5,998 | 24 | Denial root cause + appeal outcomes |

### Business Questions Answered

1. **Patient Health & Demographics** — disease distribution by age, gender, ethnicity, location
2. **Claims & Billing KPIs** — total billed vs paid, approval rates, claims by insurance provider
3. **Denial Analysis** — top denial reasons, appeal success rates, denials by demographics

---

## ⚙️ ADF Orchestration

4 pipelines in Azure Data Factory:

| Pipeline | Description |
|----------|-------------|
| `01_bronze_master_pipeline` | Triggers Databricks bronze notebook |
| `02_silver_master_pipeline` | Triggers Databricks silver notebook |
| `03_gold_master_pipeline` | Triggers Databricks gold notebook |
| `pl_master_full_refresh` | Chains all 3 in sequence |

**Scheduling:** Daily trigger at 2:00 AM UTC

---

## 🔐 Security

- **Service Principal** authentication (OAuth 2.0) for Databricks → ADLS Gen2 access
- **App Registration:** `adf-databricks-sp` in Microsoft Entra ID
- **Role Assignment:** `Storage Blob Data Contributor` on ADLS Gen2
- **Credentials:** Never hardcoded — stored as Databricks secrets

---

## ☁️ Azure Infrastructure

| Resource | Name |
|----------|------|
| Resource Group | `rg_hospital_dwh` |
| ADLS Gen2 Storage | `adlshospitaldwh` |
| Databricks Workspace | `hospital-Databricls` |
| Databricks Cluster | `Hospital-Cluster2026` |
| Azure Data Factory | `adf-hospital-2026` |
| App Registration | `adf-databricks-sp` |

---

## 📁 Project Structure

```
Healthcare-Data-Engineering/
├── notebooks/
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_transformation.py
│   └── 03_gold_aggregations.py
├── architecture/
│   ├── medallion_architecture.drawio
│   └── healthcare_data_model.drawio
├── docs/
│   └── README.md
└── adf/
    └── pipeline_definitions/
```

---

## 🔜 In Progress

- [ ] Fix Unity Catalog external location for Power BI connectivity
- [ ] Connect Power BI to Gold Delta tables via Databricks SQL Warehouse
- [ ] Build Power BI dashboards:
  - Claims & Billing KPIs
  - Denial Root Cause Analysis
  - Patient Demographics
  - Geographic Map visuals
- [ ] Add audit logging (`audit.pipeline_runs` table)
- [ ] Add retry logic on ADF pipeline failures

---

## 💡 Key Learnings

- **Service Principal + ADLS Gen2** is the enterprise standard for secure storage access
- **Medallion Architecture** separates concerns cleanly: raw → clean → business-ready
- **Source data ID columns are not always unique** — always validate deduplication strategy per table
- **Unity Catalog** requires careful IAM role configuration for external storage access
- **ADF + Databricks** is a powerful orchestration + compute combination used widely in enterprise

---

## 👤 Author

**Linda Sylvie**
Data Analyst → Data Engineer
Indianapolis, IN
[GitHub](https://github.com) | [LinkedIn](https://linkedin.com)
