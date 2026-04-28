"""Generate submission PDFs for the Why Startups Fail project.

This script builds two lightweight but real deliverables:
- reports/project_report.pdf
- reports/presentation.pdf

They are derived from the current processed dataset and screenshot exports so
the repo no longer ships empty placeholder PDFs.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
SCREENSHOTS = ROOT / "tableau" / "screenshots"
REPORTS = ROOT / "reports"

REPORTS.mkdir(parents=True, exist_ok=True)

DF = pd.read_csv(PROCESSED / "startups_cleaned.csv")
KPI = pd.read_csv(PROCESSED / "kpi_summary.csv")
SECTOR = pd.read_csv(PROCESSED / "sector_level_summary.csv")
COUNTRY = pd.read_csv(PROCESSED / "country_level_summary.csv")


def wrap(text: str, width: int = 92) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def make_text_page(pdf: PdfPages, title: str, body_lines: list[str], footer: str = "") -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    fig.text(0.08, 0.94, title, fontsize=22, fontweight="bold", va="top")

    y = 0.88
    for line in body_lines:
        fig.text(0.08, y, wrap(line), fontsize=11.5, va="top")
        y -= 0.07 if len(line) < 90 else 0.095

    if footer:
        fig.text(0.08, 0.04, footer, fontsize=9, color="#666666")

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def make_table_page(pdf: PdfPages, title: str, df: pd.DataFrame, subtitle: str = "") -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0.06, 0.08, 0.88, 0.78])
    ax.axis("off")
    fig.text(0.06, 0.94, title, fontsize=22, fontweight="bold", va="top")
    if subtitle:
        fig.text(0.06, 0.89, wrap(subtitle), fontsize=11, va="top")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="left",
        colLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 1.6)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#DDDDDD")
        if row == 0:
            cell.set_facecolor("#F3F6FA")
            cell.set_text_props(weight="bold")

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def make_image_page(pdf: PdfPages, title: str, image_paths: list[Path], captions: list[str]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(8.27, 11.69))
    fig.suptitle(title, fontsize=22, fontweight="bold", y=0.98)

    for ax, image_path, caption in zip(axes, image_paths, captions):
        ax.axis("off")
        ax.imshow(mpimg.imread(image_path))
        ax.set_title(caption, fontsize=11, pad=10)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def build_report() -> Path:
    report_path = REPORTS / "project_report.pdf"
    failure_rate = DF["is_closed"].mean() * 100
    status_counts = DF["status"].value_counts()

    with PdfPages(report_path) as pdf:
        make_text_page(
            pdf,
            "Why Startups Fail\nVC Investment Pattern Analysis",
            [
                "Newton School of Technology | Data Visualization & Analytics | Capstone 2",
                f"Final cleaned dataset: {len(DF):,} rows x {DF.shape[1]} columns | Failure rate: {failure_rate:.2f}%",
                "This report summarises the end-to-end Python ETL, exploratory analysis, statistical testing, and Tableau export workflow committed in the repository.",
                "Objective: identify funding, timing, sector, and geography signals that meaningfully separate startup survival from closure.",
            ],
            footer="Generated from the committed repository state.",
        )

        make_text_page(
            pdf,
            "Executive Summary",
            [
                "The project studies Crunchbase startup investment records to answer one business question: which measurable startup characteristics are associated with failure?",
                f"The cleaned sample contains {status_counts.get('operating', 0):,} operating firms, {status_counts.get('acquired', 0):,} acquired firms, and {status_counts.get('closed', 0):,} closed firms.",
                "Across the analysis, startups with fewer funding rounds and lower total capital show consistently worse outcomes. Sector and cohort effects also matter, which means failure cannot be reduced to one universal rule.",
                "The final repository now includes portable notebooks, corrected processed outputs, ETL logs, Tableau-ready CSVs, and report artifacts.",
            ],
        )

        make_text_page(
            pdf,
            "Dataset And ETL",
            [
                "Source: Crunchbase startup investments via Kaggle.",
                "The production ETL script normalises column names, converts funding values, parses dates, removes invalid temporal records, filters the analytical year range to 1990–2014, removes duplicates, handles extreme funding outliers, and engineers derived features such as is_closed, reached_series_a, funding_tier, and funding_duration_days.",
                "The notebook pipeline now calls the same ETL helpers as the standalone script, which removes notebook-versus-script drift and makes local Jupyter and Colab runs consistent.",
            ],
        )

        make_table_page(
            pdf,
            "Quick KPI Snapshot",
            KPI.head(10),
            "Top dashboard metrics exported to data/processed/kpi_summary.csv.",
        )

        make_image_page(
            pdf,
            "EDA Highlights I",
            [
                SCREENSHOTS / "eda_01_status_distribution.png",
                SCREENSHOTS / "eda_02_failure_by_rounds.png",
            ],
            [
                "Status mix in the cleaned sample",
                "Failure rate is highest among startups with only one funding round",
            ],
        )

        make_image_page(
            pdf,
            "EDA Highlights II",
            [
                SCREENSHOTS / "eda_03_failure_by_market.png",
                SCREENSHOTS / "eda_06_failure_by_country.png",
            ],
            [
                "Sector-level failure patterns differ materially",
                "Geographic ecosystems show different base failure rates",
            ],
        )

        make_image_page(
            pdf,
            "EDA Highlights III",
            [
                SCREENSHOTS / "eda_04_funding_distribution.png",
                SCREENSHOTS / "eda_05_failure_trend.png",
            ],
            [
                "Funding distributions shift left for closed firms",
                "Failure risk varies across founding cohorts",
            ],
        )

        make_text_page(
            pdf,
            "Statistical Findings",
            [
                "Chi-square testing shows a statistically significant relationship between startup outcome and Series A attainment.",
                "The Mann-Whitney U test shows that closed startups raised significantly less capital than operating firms.",
                "Kruskal-Wallis tests indicate that both funding rounds and sector membership differ significantly across outcome groups.",
                "Logistic regression shows funding rounds and total capital are strong protective predictors after controls, while other variables need careful interpretation because of overlap and feature dependence.",
            ],
        )

        make_table_page(
            pdf,
            "High-Risk Segments",
            SECTOR.head(12)[["market", "Total_Startups", "Failure_Rate_Pct", "Series_A_Rate_Pct"]],
            "Selected sector summary extracted from the Tableau-ready outputs.",
        )

        make_table_page(
            pdf,
            "Country Summary",
            COUNTRY.head(12)[["country_code", "Total_Startups", "Failure_Rate_Pct", "Avg_Rounds"]],
            "Leading country-level aggregates used for dashboard filters and maps.",
        )

        make_text_page(
            pdf,
            "Recommendations And Limitations",
            [
                "1. Flag one-round startups for enhanced diligence or post-investment review.",
                "2. Treat underfunding as an explicit risk factor when assessing startup runway.",
                "3. Use sector-adjusted hurdle rates instead of one common benchmark across all markets.",
                "4. Interpret recent founding cohorts carefully because startup outcomes take time to mature.",
                "Limitations: class imbalance remains substantial, Crunchbase coverage is not universal, and some status labels may lag real-world outcomes.",
            ],
            footer="See notebooks/03_eda.ipynb and notebooks/04_statistical_analysis.ipynb for the full analytical narrative.",
        )

    return report_path


def build_presentation() -> Path:
    deck_path = REPORTS / "presentation.pdf"
    failure_rate = DF["is_closed"].mean() * 100

    slides: list[tuple[str, list[str]]] = [
        (
            "Why Startups Fail",
            [
                "VC Investment Pattern Analysis",
                "Newton School of Technology | DVA Capstone 2",
                f"Final cleaned data: {len(DF):,} startups | Failure rate: {failure_rate:.2f}%",
            ],
        ),
        (
            "Business Problem",
            [
                "Most VC-backed startups fail, but investors need clearer signals about which companies are most at risk and when those risks become visible.",
                "Goal: convert raw startup investment data into a decision-ready failure analysis workflow.",
            ],
        ),
        (
            "Data And Pipeline",
            [
                "Raw Crunchbase investment records were cleaned through a reproducible ETL pipeline.",
                "Final outputs include a cleaned analytical dataset, ETL log, Tableau summary tables, and exported visuals.",
            ],
        ),
        (
            "Key EDA Insight",
            [
                "Single-round startups fail at higher rates than firms that continue attracting follow-on capital.",
                "Funding persistence looks like a stronger risk signal than one large cheque.",
            ],
        ),
        (
            "Capital Matters",
            [
                "Closed startups show materially lower median funding than operating startups.",
                "The full funding distribution also shifts lower for failed firms.",
            ],
        ),
        (
            "Sector And Geography",
            [
                "Failure rates vary by market and country, which means startup risk is partly structural.",
                "Investors should evaluate opportunities against sector-adjusted and ecosystem-aware benchmarks.",
            ],
        ),
        (
            "Statistical Validation",
            [
                "Chi-square, Mann-Whitney U, Kruskal-Wallis, and logistic regression all support the idea that funding behavior and market context are linked to closure risk.",
                "Effect sizes are often modest, so the right framing is risk scoring rather than deterministic prediction.",
            ],
        ),
        (
            "Dashboard Outputs",
            [
                "The repo now exports Tableau-ready CSVs for KPI, sector, country, yearly trend, and master-record views.",
                "These files support executive tiles, drill-downs, and cohort trend analysis in the dashboard layer.",
            ],
        ),
        (
            "Recommendations",
            [
                "Review one-round startups more aggressively.",
                "Use minimum-runway thresholds in funding decisions.",
                "Apply higher hurdle rates in structurally high-risk sectors.",
                "Track cohort risk across macro cycles.",
            ],
        ),
        (
            "Submission Ready State",
            [
                "Portable notebooks, corrected output filenames, ETL run log, dashboard link stub, data dictionary updates, and real PDF deliverables are now in place.",
                "Remaining manual fields, if any, are the human-owned items such as final mentor names or published Tableau URLs.",
            ],
        ),
    ]

    with PdfPages(deck_path) as pdf:
        for title, bullets in slides:
            make_text_page(pdf, title, bullets)

    return deck_path


def main() -> None:
    report = build_report()
    deck = build_presentation()
    print(f"Generated {report}")
    print(f"Generated {deck}")


if __name__ == "__main__":
    main()
