from pydantic import BaseModel


class Contract(BaseModel):
    contract_id: str
    first_contracted: str
    pricing: float
    service_level_agreements: str
    start_date: str
    end_date: str
    duration_days: int
