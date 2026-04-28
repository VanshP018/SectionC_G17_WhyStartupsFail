# Cleaning Insights Report

## Scope
This report documents exactly what was done from `data/raw/investments_VC.csv` to `data/processed/startups_cleaned.csv` and verifies whether missing-value handling, outlier handling, and final cleaning quality checks were completed.

## Input and Output Snapshot
- Raw dataset: `data/raw/investments_VC.csv`
- Cleaned dataset: `data/processed/startups_cleaned.csv`
- ETL log: `data/processed/etl_run_log.csv`

### Shape Comparison
- Raw shape: **54,294 rows x 39 columns**
- Cleaned shape: **49,437 rows x 42 columns**
- Net row reduction: **4,857 rows removed**
- Net column increase: **+3 columns** (derived analytical features)

## Exact Cleaning Steps Performed
The pipeline logs 7 transformation steps in `etl_run_log.csv`.

1. `load_raw_data`
- Action: Loaded raw file using `latin1` encoding.
- Why: Raw contains non-UTF-8 characters; this prevents decode failures.
- Impact: no row/column change.

2. `standardize_column_names`
- Action: Trimmed spaces, lowercased, converted special characters/spaces to `_`.
- Why: Standardized schema avoids reference errors and inconsistent naming.
- Exact impact: **10 column names changed**.
- Example normalization: `' market '` -> `market`, `' funding_total_usd '` -> `funding_total_usd`.

3. `clean_text_and_missing_tokens`
- Action:
  - Stripped whitespace in text columns.
  - Replaced placeholders (`''`, `'nan'`, `'None'`, `'NULL'`, `'N/A'`) with real nulls.
  - Normalized selected fields (`status`, `market`, `country_code`, etc.), lowercased `status`.
- Why: unify text quality and missing-value semantics.
- Exact impact from ETL log: **94,909 cell-level text/placeholder standardizations**.

4. `remove_duplicates`
- Action:
  - Removed exact duplicate rows.
  - Removed duplicate entities by `permalink` (keeping first).
- Why: prevent inflated counts and biased analysis.
- Exact impact:
  - **4,855 exact duplicate rows removed**
  - **2 permalink-duplicate rows removed**
  - **Total removed: 4,857 rows**

5. `parse_validate_dates`
- Action:
  - Parsed `founded_at`, `first_funding_at`, `last_funding_at` as datetimes.
  - Validated `founded_year` to range `[1900, current_year]`, invalid -> null.
- Why: ensure valid temporal analytics.
- Exact impact in log: no net row/column changes; type normalization applied.

6. `standardize_numeric_funding`
- Action:
  - Parsed mixed numeric/currency formats to numeric across funding columns.
  - Converted invalid/negative funding values to null.
  - Filled missing stage-level funding columns with `0.0` (except `funding_total_usd` and `funding_rounds`).
- Why: produce mathematically reliable numeric features.
- Exact impact from ETL log: **40,905 numeric-cell standardizations**.
- Validation result: **0 negative numeric values remain** in cleaned numeric columns.

7. `derive_analysis_features`
- Action:
  - Added `status_group` (`active`/`terminal`/`other`)
  - Added `is_closed` flag
  - Added `funding_duration_days`
- Why: make EDA/statistical workflows cleaner and reproducible.
- Exact impact: **3 new columns added**.

## Missing Values Handling Check
### Was missing-value handling done?
**Yes.**

### Evidence
- Placeholder tokens were normalized to nulls.
- Missing values were intentionally retained where business meaning requires uncertainty preservation (e.g., unknown `state_code`, `city`, `founded_at`).
- Stage-level funding columns were imputed to `0.0` where missing likely means “no amount disclosed/raised for that stage”.

### Missingness Summary (Raw vs Clean)
- Total missing cells in raw: **281,768**
- Total missing cells in cleaned: **102,273**
- Reduction: **179,495 fewer missing cells**

Top missing columns after cleaning (expected in real-world startup data):
- `state_code`: 19,278
- `founded_year`: 10,957
- `founded_month`: 10,957
- `founded_quarter`: 10,957
- `founded_at`: 10,886

## Outlier Handling Check
### Was outlier handling done?
**Partially, with domain-safe handling.**

### What was done
- Invalid negative numeric values were treated as data quality errors and coerced to null.
- No aggressive row deletion or winsorization/capping was applied, to avoid removing true high-funding startups (which are common legitimate right-tail observations in VC data).

### Current outlier profile (IQR diagnostic on cleaned numeric fields)
Top fields with high right-tail outlier counts:
- `seed`: 10,465
- `venture`: 7,029
- `funding_duration_days`: 6,096
- `funding_total_usd`: 5,231
- `funding_rounds`: 4,154

Interpretation:
- These are mostly expected distributional outliers in VC datasets (heavy-tailed funding behavior), not necessarily bad data.
- Dataset is cleaned for analysis, but if a downstream model is sensitive to outliers, robust scaling/log transforms should be applied at modeling stage.

## Final Quality Check: Is the dataset cleaned?
**Yes, the dataset is cleaned and analysis-ready for EDA/statistical workflows.**

### Final validation points passed
- Raw file remained untouched in `data/raw/`.
- Column schema standardized.
- Duplicate records removed with exact counts.
- Numeric/currency fields parsed and validated.
- Date fields parsed and validated.
- Missing-value treatment applied with clear strategy.
- Invalid negative numeric values removed.
- Process traceability captured in `etl_run_log.csv`.
- Cleaned outputs saved in `data/processed/`.

## Output Files Produced
- `data/processed/startups_cleaned.csv`
- `data/processed/startups_cleaned.parquet`
- `data/processed/etl_run_log.csv`
