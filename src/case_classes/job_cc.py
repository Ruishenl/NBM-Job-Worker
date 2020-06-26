from dataclasses import dataclass


@dataclass(frozen=True)
class JobCC:
    job_id: int
    job_desc: str
    hrs_required: float