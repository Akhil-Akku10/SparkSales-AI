import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor
import matplotlib.pyplot as plt
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
CHART_DIR = os.path.join(REPORT_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_sales_trend_chart(dates, sales):
    path = os.path.join(CHART_DIR, "sales_trend.png")
    plt.figure(figsize=(7, 3.5), dpi=120)

    plt.plot(dates, sales, marker="o", linewidth=2)
    plt.title("Monthly Sales Trend", fontsize=12)
    plt.xlabel("Month")
    plt.ylabel("Sales")

    # FIX: readable x-axis
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(alpha=0.3)

    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path


def generate_growth_chart(dates, growth):
    path = os.path.join(CHART_DIR, "growth_trend.png")
    plt.figure(figsize=(8, 4), dpi=140)

    plt.bar(dates, growth)
    plt.title("Sales Growth (%)", fontsize=12)
    plt.xlabel("Month")
    plt.ylabel("Growth %")

    plt.xticks(range(0, len(dates), 3), rotation=45, fontsize=8)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
def generate_performance_delta(avg_sales, latest_sales):
    path = os.path.join(CHART_DIR, "performance_delta.png")
    plt.figure(figsize=(5, 3), dpi=140)

    plt.bar(
        ["Average Sales", "Latest Sales"],
        [avg_sales, latest_sales],
        color=["#1f77b4", "#ff7f0e"]
    )

    plt.title("Performance Delta", fontsize=12)
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
def generate_risk_donut(volatility_level):
    path = os.path.join(CHART_DIR, "risk_donut.png")

    risk = 75 if volatility_level == "High" else 30
    values = [risk, 100 - risk]
    labels = ["Risk", "Stability"]
    colors = ["#d62728", "#dddddd"]

    plt.figure(figsize=(4, 4), dpi=140)
    plt.pie(
        values,
        labels=labels,
        colors=colors,
        startangle=90,
        wedgeprops={"width": 0.4}
    )
    plt.title("Demand Risk Level", fontsize=12)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def generate_pdf_report(data):
    file_path = os.path.join(REPORT_DIR, "SparkSales_Report.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # ================= PAGE 1 =================
    # HEADER
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "SparkSales AI – Business Intelligence Report")

    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#666666"))
    c.drawString(
        50, height - 75,
        f"Generated on: {datetime.datetime.now().strftime('%d %B %Y, %H:%M')}"
    )

    c.setFillColor(HexColor("#000000"))
    y = height - 120

    # EXECUTIVE SUMMARY
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Executive Summary")
    y -= 22

    c.setFont("Helvetica", 11)
    summary = data.get(
        "summary",
        "This report presents AI-driven sales forecasts, KPIs, demand patterns, and risk indicators derived from historical data."
    )
    c.drawString(50, y, summary)
    y -= 40

    # KPI SUMMARY (TEXT ONLY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Key Performance Indicators")
    y -= 22

    c.setFont("Helvetica", 11)
    kpis = data.get("kpis", {})
    for key, value in kpis.items():
        c.drawString(60, y, f"• {key.replace('_',' ').title()}: {value}")
        y -= 18

    y -= 20

    # INSIGHTS
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Actionable Business Insights")
    y -= 22

    c.setFont("Helvetica", 11)
    insights = data.get("insights", [])
    if insights:
        for insight in insights:
            c.drawString(60, y, f"• {insight}")
            y -= 16
    else:
        c.drawString(60, y, "• No critical risks detected. Business performance remains stable.")

    # DISCLAIMER (BOTTOM)
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(HexColor("#888888"))
    c.drawString(
        50, 40,
        "Disclaimer: Predictions are based on historical data and statistical models. Actual results may vary."
    )

    # ================= PAGE 2 =================
    c.showPage()
    c.setFillColor(HexColor("#000000"))

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Visual Analytics Dashboard")

    trend = data.get("trend", {})
    kpis = data.get("kpis", {})

    y_top = height - 100

    # SALES TREND
    if trend:
        sales_chart = generate_sales_trend_chart(trend["dates"], trend["sales"])
        c.drawImage(
            sales_chart,
            50, y_top - 220,
            width=6.5 * inch,
            height=2.8 * inch,
            preserveAspectRatio=True
        )

    # GROWTH CHART
    if trend:
        growth_chart = generate_growth_chart(trend["dates"], trend["growth"])
        c.drawImage(
            growth_chart,
            50, y_top - 480,
            width=6.5 * inch,
            height=2.8 * inch
        )

    # PERFORMANCE DELTA
    if "avg_sales" in kpis and "latest_sales" in kpis:
        perf_chart = generate_performance_delta(
            kpis["avg_sales"],
            kpis["latest_sales"]
        )
        c.drawImage(
            perf_chart,
            50, y_top - 720,
            width=3 * inch,
            height=3 * inch
        )

    # RISK DONUT
    if "volatility_level" in kpis:
        risk_chart = generate_risk_donut(kpis["volatility_level"])
        c.drawImage(
            risk_chart,
            330, y_top - 720,
            width=3 * inch,
            height=3 * inch
        )

    c.save()
    return file_path