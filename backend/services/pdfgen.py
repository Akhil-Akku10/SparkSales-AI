import os
import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    Image,
    PageBreak
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
CHART_DIR = os.path.join(REPORT_DIR, "charts")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)

styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "Title",
    fontSize=20,
    fontName="Helvetica-Bold",
    spaceAfter=16
)

SUBTEXT = ParagraphStyle(
    "Subtext",
    fontSize=10,
    textColor=HexColor("#666666"),
    spaceAfter=20
)

SECTION = ParagraphStyle(
    "Section",
    fontSize=14,
    fontName="Helvetica-Bold",
    spaceBefore=14,
    spaceAfter=10
)

BODY = ParagraphStyle(
    "Body",
    fontSize=11,
    leading=15,
    spaceAfter=8
)

#graphs,charts
def generate_sales_trend_chart(dates, sales):
    path = os.path.join(CHART_DIR, "sales_trend.png")
    plt.figure(figsize=(7, 3.5), dpi=120)
    plt.plot(dates, sales, linewidth=2)
    plt.title("Sales Trend")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def generate_rolling_avg_chart(dates, sales):
    path = os.path.join(CHART_DIR, "sales_vs_rolling_avg.png")

    df = pd.DataFrame({"date": dates, "sales": sales})
    df["rolling_avg"] = df["sales"].rolling(window=3, min_periods=1).mean()

    plt.figure(figsize=(7, 3.5), dpi=120)
    plt.plot(df["date"], df["sales"], label="Actual Sales", alpha=0.6, linewidth=2)
    plt.plot(df["date"], df["rolling_avg"], label="Rolling Average (3)", linewidth=3)
    plt.title("Sales vs Rolling Average")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def generate_monthly_growth_chart(dates, growth):
    path = os.path.join(CHART_DIR, "monthly_growth.png")
    plt.figure(figsize=(7, 3.5), dpi=120)
    plt.bar(dates, growth, color="#2ca02c")
    plt.title("Monthly Growth Analysis")
    plt.xlabel("Month")
    plt.ylabel("Growth (%)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def generate_performance_delta(avg_sales, latest_sales):
    path = os.path.join(CHART_DIR, "performance_delta.png")
    plt.figure(figsize=(4, 3), dpi=120)
    plt.bar(
        ["Average Sales", "Latest Sales"],
        [avg_sales, latest_sales],
        color=["#1f77b4", "#ff7f0e"]
    )
    plt.title("Performance Delta")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

#footer
def add_footer(canvas, doc):
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(HexColor("#888888"))
    canvas.drawString(
        50,
        30,
        "Disclaimer: Predictions are AI-generated and based on historical data. Actual results may vary."
    )

#pdf generator function
def generate_pdf_report(data):
    file_path = os.path.join(REPORT_DIR, "SparkSales_Report.pdf")

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    story = []

    story.append(Paragraph(
        "SparkSales AI – Business Intelligence Report",
        TITLE
    ))

    story.append(Paragraph(
        f"Generated on: {datetime.datetime.now().strftime('%d %B %Y, %H:%M')}",
        SUBTEXT
    ))

    kpis = data.get("kpis", {})
    avg_sales = float(kpis.get("avg_sales", 0))
    latest_sales = float(kpis.get("latest_sales", 0))
    growth_pct = kpis.get("growth_pct", 0)

    story.append(Paragraph("Executive Summary", SECTION))
    story.append(Paragraph(
        f"This Business Intelligence report presents a comprehensive, AI-driven evaluation of historical sales "
        f"performance and short-term demand dynamics. Advanced time-series analysis and machine learning models "
        f"are applied to uncover underlying trends, seasonal behavior, and demand variability across time periods.<br/><br/>"

        f"The analysis reveals an average sales volume of <b>{round(avg_sales,2)}</b> units, while the most recent "
        f"period recorded <b>{round(latest_sales,2)}</b> units. Monthly aggregation highlights directional growth "
        f"patterns, and rolling average analysis smooths short-term fluctuations to expose the true demand signal "
        f"beneath market noise.<br/><br/>"

        f"These insights enable data-driven decision-making across inventory planning, revenue forecasting, and "
        f"operational strategy. By combining historical evidence with predictive intelligence, the system supports "
        f"proactive demand management, reduced forecasting risk, and improved alignment between supply and market needs.",
        BODY
        ))

    story.append(Paragraph("Key Performance Indicators", SECTION))
    story.append(ListFlowable(
        [
            Paragraph(f"Average Sales: <b>{round(avg_sales,2)}</b>", BODY),
            Paragraph(f"Latest Sales: <b>{round(latest_sales,2)}</b>", BODY),
            Paragraph(f"Sales Growth: <b>{growth_pct}%</b>", BODY),
        ],
        bulletType="bullet"
    ))

    story.append(Paragraph("Actionable Business Insights", SECTION))
    insights = data.get("insights", [])
    story.append(ListFlowable(
        [Paragraph(i, BODY) for i in insights],
        bulletType="bullet"
    ))

    story.append(PageBreak())
    story.append(Paragraph("Visual Analytics Dashboard", SECTION))
    story.append(Spacer(1, 12))

    trend = data.get("trend", {})
    dates = trend.get("dates", [])
    sales = trend.get("sales", [])
    growth = trend.get("growth", [])

    if len(dates) > 1:
        story.append(Image(
            generate_sales_trend_chart(dates, sales),
            width=6.5 * inch,
            height=3 * inch
        ))

        story.append(Spacer(1, 14))

        story.append(Image(
            generate_rolling_avg_chart(dates, sales),
            width=6.5 * inch,
            height=3 * inch
        ))

        story.append(Spacer(1, 14))

        story.append(Image(
            generate_monthly_growth_chart(dates, growth),
            width=6.5 * inch,
            height=3 * inch
        ))
        
    story.append(PageBreak())
    story.append(Paragraph("Performance Analysis", SECTION))
    story.append(Spacer(1, 12))

    story.append(Image(
        generate_performance_delta(avg_sales, latest_sales),
        width=3.5 * inch,
        height=3 * inch
    ))

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return file_path