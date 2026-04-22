# 📘 Data Dictionary — Logarda

This document describes the structure of the core database tables used in the Logarda monitoring system.

---

## TABLE - metrics 

| Column       | Type                | Description                                      | Notes |
|--------------|---------------------|--------------------------------------------------|------|
| metricTime   | TIMESTAMP           | Time when metric was recorded                    | Part of primary key |
| instanceID   | VARCHAR             | Unique instance identifier (e.g., EC2/server)   | Part of primary key |
| cpu          | DOUBLE PRECISION    | CPU usage (%)                                   | Range: 0–100 |
| network      | DOUBLE PRECISION    | Network usage metric                             | Must be consistent unit (e.g., MB/s) |
| memory       | DOUBLE PRECISION    | Memory usage (%)                          | Range: 0–100  |

**Primary Key:** `(metricTime, instanceID)` --composite primary key to prevent double entries at same timestamp for single instance

---

## TABLE - predicted_metrics 

| Column       | Type                | Description                                      | Notes |
|--------------|---------------------|--------------------------------------------------|------|
| metricTime   | TIMESTAMP           | Timestamp being predicted (future time)         | Part of primary key |
| instanceID   | VARCHAR             | Target instance ID                              | Same as metrics |
| cpu          | DOUBLE PRECISION    | Predicted CPU usage                             | ML output |
| network      | DOUBLE PRECISION    | Predicted network usage                         | ML output |
| memory       | DOUBLE PRECISION    | Predicted memory usage                          | ML output |

**Primary Key:** `(metricTime, instanceID)` --composite primary key to prevent double entries at same timestamp for single instance

---

## TABLE - logs

| Column       | Type     | Description                          | Notes |
|--------------|----------|--------------------------------------|------|
| eventTime    | TIMESTAMP | Time when event occurred            | Primary timestamp |
| errorCode    | VARCHAR   | Error category/code                 | e.g. DB_TIMEOUT |
| errorMessage | TEXT      | Detailed error message              | Human-readable |
| serviceName  | VARCHAR   | Service that generated the error    | e.g. EC2, S3 |
| eventName    | VARCHAR   | Operation context                   | e.g. ListResources, DescribeInstance |

**Primary Key:** `(eventTime, errorCode, errorMessage)` --composite primary keys to prevent double entries at same timestamp for same error code + error message
