from pydantic import BaseModel
from .test_outcome_enum import TestOutcome


class TestResult(BaseModel):
    outcome: TestOutcome
    p_value: float | None
    p_list: list[float] | None
