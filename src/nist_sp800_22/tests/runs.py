# Copyright (C) 2017 David Johnston
# This program is distributed under the terms of the GNU General Public License.
#
# This file is part of sp800_22_tests.
#
# sp800_22_tests is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sp800_22_tests is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sp800_22_tests.  If not, see <http://www.gnu.org/licenses/>.


from typing import Sequence
from .test_result import TestResult

from .test_outcome_enum import TestOutcome
from .test_interface import TestInterface
import math


class RunsTest(TestInterface):
    name = "Runs Test"

    def count_ones_zeroes(self, bits):
        ones = 0
        zeroes = 0
        for bit in bits:
            if bit == 1:
                ones += 1
            else:
                zeroes += 1
        return (zeroes, ones)

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        n = len(bitstring)
        zeroes, ones = self.count_ones_zeroes(bitstring)

        prop = float(ones) / float(n)
        if verbose:
            print("  prop ", prop)

        tau = 2.0 / math.sqrt(n)
        if verbose:
            print("  tau ", tau)

        if abs(prop - 0.5) > tau:
            return TestResult(TestOutcome.FAILED, 0.0, None)

        vobs = 1.0
        for i in range(n - 1):
            if bitstring[i] != bitstring[i + 1]:
                vobs += 1.0

        if verbose:
            print("  vobs ", vobs)

        p = math.erfc(
            abs(vobs - (2.0 * n * prop * (1.0 - prop)))
            / (2.0 * math.sqrt(2.0 * n) * prop * (1 - prop))
        )

        outcome = TestOutcome.PASSED if (p >= 0.01) else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=p, p_list=None)

    def is_eligible(self, bitstring: Sequence) -> bool:
        return True
