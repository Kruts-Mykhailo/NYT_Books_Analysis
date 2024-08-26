# New Your Times: Bestsellers books analysis

## Description:

Pipeline to pull data related to weekly bestseller lists across various categories. The objective is to build a robust analytical platform that tracks, visualizes, and interprets trends in book popularity, author success, and publisher performance across various categories over time.

## Architecture

Image here ->

1. Extract weekly from NYT Books API
2. Load data into `Postgresql` data warehouse
3. Transform data using `dbt`
4. Orchestrate and pull data using `Dagster`
5. Visualize data using `Metabase` 

# Dagster logic

Extract data from an api -> load and increment raw data in postgres table

# dbt pipeline logic

Raw data is a full history table of all records. Staging table is a table of only newly added records. After initial load of the records into a staging table, data warehouse tables are updated.


Current problem: staging table not updating





