# Statistical Insights Report (Based on Notebook 04)

## Scope
This report summarizes the statistical analysis performed in `notebooks/04_statistical_analysis.ipynb` using the cleaned dataset:
- `data/processed/startups_cleaned.csv`

## Dataset Used for Inference
- Total startups analyzed: **49,437**
- Target event: startup closure (`is_closed`)

## 1) Chi-Square Test: Status vs Series A Progression
### Test
- Chi-square test of independence on `status` x `reached_series_a`

### Result
- `chi2 = 576.41`
- `p-value = 1.31e-124`
- `dof = 3`
- `Cramér's V = 0.108`

### Interpretation
- The association is statistically significant.
- Effect size is **small-to-moderate** (not negligible, not dominant).
- Series A progression is linked with outcome state, but it is not the only failure determinant.

## 2) Mann-Whitney U: Funding Difference (Closed vs Operating)
### Test
- Non-parametric comparison of `funding_total_usd` between `closed` and `operating` startups.

### Result
- `U = 32,474,908`
- `p-value = 1.01e-22`
- Closed sample size: `n = 2,158`
- Operating sample size: `n = 34,424`
- Median funding (closed): **$1,000,000**
- Median funding (operating): **$1,757,977.5**

### Interpretation
- Closed startups show significantly lower funding distribution versus operating startups.
- This supports a financing-depth vulnerability pattern.

## 3) Kruskal-Wallis: Funding Rounds Across Status Groups
### Test
- Kruskal-Wallis on `funding_rounds` across major status groups.

### Result
- `H = 519.52`
- `p-value = 1.54e-113`

### Interpretation
- Median funding-round profiles differ significantly by startup status.
- Lifecycle outcomes are strongly associated with funding trajectory depth.

## 4) Point-Biserial Correlation with Closure
### Variables Tested
- `funding_total_usd`
- `funding_rounds`
- `avg_funding_per_round`
- `days_to_first_funding`

### Result Summary
- `funding_total_usd`: `r = -0.0105`, `p = 0.0355`, `n = 39,800`
- `funding_rounds`: `r = -0.0491`, `p = 4.64e-27`, `n = 48,122`
- `avg_funding_per_round`: `r = -0.0140`, `p = 0.0053`, `n = 39,800`
- `days_to_first_funding`: `r = -0.0509`, `p = 5.10e-23`, `n = 37,628`

### Interpretation
- All relationships are statistically significant, but effect magnitudes are **weak**.
- This implies closure risk is multi-factorial and not well explained by any single numeric predictor alone.

## 5) Logistic Regression: Independent Predictors of Closure
### Model
- Dependent variable: `is_closed`
- Predictors: `funding_rounds`, `log_funding_total_usd`, `reached_series_a`, `days_to_first_funding`, `is_usa`

### Model Fit
- Regression sample size: **31,437**
- Pseudo R²: **0.0313**

### Coefficient Summary
- `funding_rounds`: `coef = -0.2690`, `OR = 0.7642`, `p < 0.001`
- `days_to_first_funding`: `coef = -0.000166`, `OR = 0.999834`, `p < 0.001`
- `log_funding_total_usd`: `coef = -0.0926`, `OR = 0.9116`, `p < 0.001`
- `reached_series_a`: `coef = 0.1880`, `OR = 1.2068`, `p = 0.0096`
- `is_usa`: `coef = 0.0888`, `OR = 1.0928`, `p = 0.0915` (not significant at 5%)

### Interpretation
- More funding rounds and higher total funding are associated with lower closure odds.
- Earlier funding access (lower delay) is associated with lower closure odds.
- `reached_series_a` shows a positive coefficient in the multivariate setting; this likely reflects cohort/selection interactions and should not be interpreted causally in isolation.
- Geographic indicator (`is_usa`) is not a strong standalone predictor at 5% significance.

## Final Statistical Conclusion
- Statistical evidence consistently supports funding-path variables as meaningful failure-risk signals.
- Practical effect sizes are modest, indicating startup failure is driven by combined factors rather than one dominant variable.
- For next-stage predictive work, combine funding features with market, cohort, and operational indicators to improve explanatory power.
