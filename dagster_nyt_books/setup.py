from setuptools import find_packages, setup

setup(
    name="dagster_nyt_books",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "dagster_nyt_books": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-webserver",
        "dagster-dbt",
        "dagster-postgres",
        "dbt-duckdb",
        "dbt-postgres",
        "pandas",
        "python-dotenv",
        "black",
        "mypy",
        "flake8",
        "isort",
    ]
)
