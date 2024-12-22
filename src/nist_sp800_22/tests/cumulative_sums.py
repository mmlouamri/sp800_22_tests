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


class CumulativeSumsTest(TestInterface):
    name = "Cumulative Sums Test"

    def _normcdf(self, n):
        return 0.5 * math.erfc(-n * math.sqrt(0.5))

    def _p_value(self, n, z):
        sum_a = 0.0
        startk = int(math.floor((((float(-n) / z) + 1.0) / 4.0)))
        endk = int(math.floor((((float(n) / z) - 1.0) / 4.0)))
        for k in range(startk, endk + 1):
            c = (((4.0 * k) + 1.0) * z) / math.sqrt(n)
            # d = scipy.stats.norm.cdf(c)
            d = self._normcdf(c)
            c = (((4.0 * k) - 1.0) * z) / math.sqrt(n)
            # e = scipy.stats.norm.cdf(c)
            e = self._normcdf(c)
            sum_a = sum_a + d - e

        sum_b = 0.0
        startk = int(math.floor((((float(-n) / z) - 3.0) / 4.0)))
        endk = int(math.floor((((float(n) / z) - 1.0) / 4.0)))
        for k in range(startk, endk + 1):
            c = (((4.0 * k) + 3.0) * z) / math.sqrt(n)
            # d = scipy.stats.norm.cdf(c)
            d = self._normcdf(c)
            c = (((4.0 * k) + 1.0) * z) / math.sqrt(n)
            # e = scipy.stats.norm.cdf(c)
            e = self._normcdf(c)
            sum_b = sum_b + d - e

        p = 1.0 - sum_a + sum_b
        return p

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        n = len(bitstring)
        # Step 1
        x = list()  # Convert to +1,-1
        for bit in bitstring:
            # if bit == 0:
            x.append((bit * 2) - 1)

        # Steps 2 and 3 Combined
        # Compute the partial sum and records the largest excursion.
        pos = 0
        forward_max = 0
        for e in x:
            pos = pos + e
            if abs(pos) > forward_max:
                forward_max = abs(pos)
        pos = 0
        backward_max = 0
        for e in reversed(x):
            pos = pos + e
            if abs(pos) > backward_max:
                backward_max = abs(pos)

        # Step 4
        p_forward = self._p_value(n, forward_max)
        p_backward = self._p_value(n, backward_max)

        success = (p_forward >= 0.01) and (p_backward >= 0.01)
        plist = [p_forward, p_backward]
        outcome = TestOutcome.PASSED if success else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=None, p_list=plist)

    def is_eligible(self, bitstring: Sequence) -> bool:
        return True
