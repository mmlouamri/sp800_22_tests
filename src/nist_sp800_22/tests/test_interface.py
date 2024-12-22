from abc import ABC, abstractmethod
from typing import Sequence

from .test_result import TestResult

from .test_outcome_enum import TestOutcome


class TestInterface(ABC):
    name: str

    @abstractmethod
    def is_eligible(self, bitstring: Sequence) -> bool:
        pass

    @abstractmethod
    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        pass

    def test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        if not self.is_eligible(bitstring):
            return TestResult(outcome=TestOutcome.UNELIGIBLE, p_value=None, p_list=None)
        return self._test(bitstring, verbose)
