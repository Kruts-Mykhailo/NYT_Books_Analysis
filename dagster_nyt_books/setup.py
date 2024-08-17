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
        "dagster-dbt",
        "dbt-duckdb<1.9",
        "dbt-postgres<1.9",
        "pandas",
        "python-dotenv"
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)