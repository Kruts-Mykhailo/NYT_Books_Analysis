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

Extract data from an api -> load raw data in postgres

## Prerequisities

## Run the project

## Warehouse schema
Source tables:

1. Books + Lists
---------------
DWH:

BestSellerFact  
BooksDim  
AuthorDim  
AgeGroupDim  
PublisherDim  
DateDim  
CategoryDim  

Source table books_published:

id: STRING
age_group: STRING
author: STRING
book_uri: STRING
contributor: STRING
contributor_note: STRING
created_date: DATE
description: STRING
updated_date: DATE
updated_rate: STRING
price: INT
publisher: STRING
published_date: DATE
primary_isbn13: STRING
list_id: INT
list_name: STRING
rank: INT
rank_last_week: INT
weeks_on_list: INT






