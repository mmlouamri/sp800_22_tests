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


class MonobitTest(TestInterface):
    name = "Monobit Test"

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        n = len(bitstring)
        ones = sum(bitstring)
        zeroes = n - ones
        s = abs(ones - zeroes)

        if verbose:
            print("  Ones count   = %d" % ones)
            print("  Zeroes count = %d" % zeroes)

        p = math.erfc(float(s) / (math.sqrt(float(n)) * math.sqrt(2.0)))

        outcome = TestOutcome.PASSED if (p >= 0.01) else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=p, p_list=None)

    def is_eligible(self, bitstring: Sequence) -> bool:
        return True
