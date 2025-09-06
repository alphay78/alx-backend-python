# 0x00. Getting Started with Python Generators

## Project Overview

This project demonstrates the use of **Python generators** to efficiently stream data from a MySQL database. It focuses on:

- Setting up a MySQL database (`ALX_prodev`) with a `user_data` table.
- Populating the table from a CSV file.
- Using a Python generator to stream rows one by one, allowing memory-efficient data processing.

---

## Database Schema

**Table:** `user_data`

| Column   | Type          | Constraints                  |
|----------|---------------|------------------------------|
| user_id  | CHAR(36)      | Primary Key, Indexed, UUID   |
| name     | VARCHAR(255)  | NOT NULL                     |
| email    | VARCHAR(255)  | NOT NULL                     |
| age      | DECIMAL(5,0)  | NOT NULL                     |

---

## Files

- `seed.py` → Python script with functions to:
  - Connect to MySQL
  - Create the database and table
  - Insert CSV data
  - Stream rows using a generator
- `0-main.py` → Example usage script (imports `seed.py` and runs the setup)
- `user_data.csv` → Sample data file with users

---

## Usage

1. Ensure MySQL server is running and credentials in `seed.py` are correct.
2. Run the main script:

```bash
./0-main.py
