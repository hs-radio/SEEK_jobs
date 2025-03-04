Job Data Scraping and Analysis

This repository contains Jupyter notebook files for scraping data engineering job listings from SEEK.com. The relevant data is extracted and stored in a Snowflake database.

By running the cells in the "main" notebook, the following steps are undertaken:
- URLS are found on SEEK.com that link to data engineering jobs in Sydney.
- The relevant data is scraped from these links.
- The data is then formatted to go into the relevant tables.
- These tables are then upload to Snowflake. Duplicates are then removed.
- Two histograms are then created that show: the most in-demand skills from job advertisements and the distribution of annual salaries. These plots are saved as PNG files in the repository.
  
Additionally, a Python file, DAG_file.py, is included, which allows the process to be automated using Apache Airflow.
