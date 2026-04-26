"""
scripts — reusable ETL utilities for SectionC_G17_WhyStartupsFail.

Public API
----------
normalize_columns   Standardise a DataFrame's column names to snake_case.
basic_clean         Apply safe, default cleaning steps (dedup, strip, types).
build_clean_dataset Load a raw CSV and return a fully cleaned DataFrame.
save_processed      Write a DataFrame to disk, creating parent dirs as needed.

Usage example
-------------
>>> from scripts import build_clean_dataset, save_processed
>>> df = build_clean_dataset(Path("data/raw/investments_VC.csv"))
>>> save_processed(df, Path("data/processed/startups_cleaned.csv"))

All transformation logic lives in ``etl_pipeline.py``.  Import from here so
that notebooks and external callers share a single, stable import path.
"""

from scripts.etl_pipeline import (
    normalize_columns,
    basic_clean,
    build_clean_dataset,
    save_processed,
)

__all__ = [
    "normalize_columns",
    "basic_clean",
    "build_clean_dataset",
    "save_processed",
]