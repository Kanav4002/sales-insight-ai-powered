from pydantic import BaseModel, EmailStr


class UploadRequest(BaseModel):
    email: EmailStr


class SalesMetrics(BaseModel):
    total_revenue: float
    top_region: str | None
    top_category: str | None
    cancelled_orders: int

