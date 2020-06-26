from dataclasses import dataclass


@dataclass(frozen=True)
class EmployeeCC:
    employee_id: int
    available_hrs: float