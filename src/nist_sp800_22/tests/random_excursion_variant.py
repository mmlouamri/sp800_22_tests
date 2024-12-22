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


class RandomExcursionVariantTest(TestInterface):
    name = "Random Excursion Variant Test"

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        # n = len(bitstring)

        x = list()  # Convert to +1,-1
        for bit in bitstring:
            x.append((bit * 2) - 1)

        # Build the partial sums
        pos = 0
        s = list()
        for e in x:
            pos = pos + e
            s.append(pos)
        sprime = [0] + s + [0]  # Add 0 on each end

        # Count the number of cycles J
        J = 0
        for value in sprime[1:]:
            if value == 0:
                J += 1
        if verbose:
            print("J=", J)
        # Build the counts of offsets
        count = [0 for x in range(-9, 10)]
        for value in sprime:
            if abs(value) < 10:
                count[value] += 1

        # Compute P values
        success = True
        plist = list()
        for x in range(-9, 10):
            if x != 0:
                top = abs(count[x] - J)
                bottom = math.sqrt(2.0 * J * ((4.0 * abs(x)) - 2.0))
                p = math.erfc(top / bottom)
                plist.append(p)
                if p < 0.01:
                    err = " Not Random"
                    success = False
                else:
                    err = ""
                if verbose:
                    print("x = %1.0f\t count=%d\tp = %f %s" % (x, count[x], p, err))

        if J < 500:
            if verbose:
                print("J too small (J=%d < 500) for result to be reliable" % J)
        outcome = TestOutcome.PASSED if success else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=None, p_list=plist)

    def is_eligible(self, bitstring: Sequence) -> bool:
        x = list()  # Convert to +1,-1
        for bit in bitstring:
            x.append((bit * 2) - 1)

        # Build the partial sums
        pos = 0
        s = list()
        for e in x:
            pos = pos + e
            s.append(pos)
        sprime = [0] + s + [0]  # Add 0 on each end

        # Count the number of cycles J
        J = 0
        for value in sprime[1:]:
            if value == 0:
                J += 1
        return J >= 500
