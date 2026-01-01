import pandas as pd

def load_base_csv(file):
    df = pd.read_csv(file)

    # Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Required columns for ALL pipelines
    required = ["order_date", "sales"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Parse dates safely
    df["order_date"] = pd.to_datetime(
        df["order_date"], dayfirst=True, errors="coerce"
    )

    # Drop invalid dates
    df = df.dropna(subset=["order_date"])

    return df


def load_dashboard_view(df):
    """
    Used for:
    - Analytics dashboard
    - SARIMA
    """
    return (
        df.groupby("order_date", as_index=False)["sales"]
        .sum()
        .sort_values("order_date")
    )


def load_segmented_view(df, region=None, category=None, sub_category=None):
    """
    Used ONLY for product-wise / segmented analysis
    """

    required_cols = ["region", "category", "sub_category"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required segmentation column: {col}")

    df_seg = df.copy()

    if region:
        df_seg = df_seg[df_seg["region"] == region]
    if category:
        df_seg = df_seg[df_seg["category"] == category]
    if sub_category:
        df_seg = df_seg[df_seg["sub_category"] == sub_category]

    return df_seg