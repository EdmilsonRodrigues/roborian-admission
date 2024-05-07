from pydantic import BaseModel


class Contract(BaseModel):
    contract_id: str
    pricing: float
    service_level_agreements: str
    start_date: str
    end_date: str
    duration_days: int
