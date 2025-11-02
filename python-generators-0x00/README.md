# Python Generators for Memory-Efficient Data Streaming
This project provides practical examples of how to handle huge database tables without overwhelming your system's memory. By using Python generators, we stream data piece-by-piece (lazy loading), making the application fast, stable.

## Setup: Getting Started
Before running any script, ensure you have the necessary environment set up:

* **MySQL Database:** Have a running MySQL server ready.
* **Python:** Python 3.x is required.
* **Dependencies:** Install the MySQL connector library:
  ``pip install mysql-connector-python``

## Database Initialization
 Run the seed.py file first to prepare your workspace:
* It creates the ALX_prodev database.
* It creates the user_data table.
* It fills the table using the sample data from user_data.csv.

## Project Scripts: The Power of Streaming
* **seed.py** (Database Setup)
  - Foundation (Initializes database and table.)
* **0-stream_users.py** (Row-by-Row Streaming)
  - Prevents high memory usage by yielding one user record at a time (lazy loading).
* **1-batch_processing.py** (Chunking Data)
  - Balances memory use with I/O speed for bulk operations by streaming data in controlled batches.
* **2-lazy_paginate.py** (On-Demand Pages)
  - Ideal for UIs/reports; never loads unnecessary pages, as it fetches the next page only when needed.
* **4-optimized_average_age.py** (Efficient Math)
  - Proves generators are great for calculating aggregates without loading the full dataset into memory.
