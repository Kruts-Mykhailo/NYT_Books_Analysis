# New Your Times: Bestsellers books analysis

## Description:

Pipeline to pull data related to weekly bestseller lists across various categories. The objective is to build a robust analytical platform that tracks, visualizes, and interprets trends in book popularity, author success, and publisher performance across various categories over time.

## Architecture

Image here ->

1. Extract weekly or monthly from NYT Books API
2. Load data into `Postgresql` data warehouse
3. Transform data using `dbt`
4. Orchestrate and pull data using `Dagster`
5. Visualize data using `Metabase` 

## Prerequisities

## Run the project

## Warehouse schema
Source tables:

1. Lists
2. Books
---------------
DWH:

BestSellerFact
BooksDim
AuthorDim
AgeGroupDim
PublisherDim
DateDim
CategoryDim



