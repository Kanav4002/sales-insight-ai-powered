import io
import logging
from typing import IO

import pandas as pd

from ..models.request_models import SalesMetrics

logger = logging.getLogger(__name__)


def parse_sales_file(buffer: IO[bytes], filename: str) -> pd.DataFrame:
    suffix = filename.lower().rsplit(".", 1)[-1]

    try:
        if suffix == "csv":
            df = pd.read_csv(buffer)
        else:
            df = pd.read_excel(buffer)
    except Exception as exc:
        logger.exception("Failed to parse sales file %s: %s", filename, exc)
        raise

    df.columns = [str(c).strip() for c in df.columns]
    return df


def calculate_sales_metrics(df: pd.DataFrame) -> SalesMetrics:
    working_df = df.copy()

    working_df["Revenue"] = pd.to_numeric(working_df.get("Revenue"), errors="coerce").fillna(0.0)

    total_revenue = float(working_df["Revenue"].sum())

    top_region = None
    if "Region" in working_df.columns:
        top_region_series = (
            working_df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
        )
        top_region = str(top_region_series.index[0]) if not top_region_series.empty else None

    top_category = None
    if "Product_Category" in working_df.columns:
        top_category_series = (
            working_df.groupby("Product_Category")["Revenue"].sum().sort_values(ascending=False)
        )
        top_category = (
            str(top_category_series.index[0]) if not top_category_series.empty else None
        )

    cancelled_orders = 0
    if "Status" in working_df.columns:
        cancelled_orders = int(
            (working_df["Status"].astype(str).str.lower() == "cancelled").sum()
        )

    metrics = SalesMetrics(
        total_revenue=total_revenue,
        top_region=top_region,
        top_category=top_category,
        cancelled_orders=cancelled_orders,
    )
    logger.debug("Calculated sales metrics: %s", metrics.json())
    return metrics

