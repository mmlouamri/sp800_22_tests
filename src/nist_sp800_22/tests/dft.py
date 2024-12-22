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
import numpy as np


class DiscreteFourierTransformTest(TestInterface):
    name = "Discrete Fourier Transform Test"

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        n = len(bitstring)
        if (n % 2) == 1:  # Make it an even number
            bitstring = bitstring[:-1]

        ts = list()  # Convert to +1,-1
        for bit in bitstring:
            ts.append((bit * 2) - 1)

        ts_np = np.array(ts)
        fs = np.fft.fft(ts_np)  # Compute DFT

        mags = abs(fs)[: n // 2]  # Compute magnitudes of first half of sequence

        T = math.sqrt(math.log(1.0 / 0.05) * n)  # Compute upper threshold
        N0 = 0.95 * n / 2.0
        if verbose:
            print("  N0 = %f" % N0)

        N1 = 0.0  # Count the peaks above the upper theshold
        for mag in mags:
            if mag < T:
                N1 += 1.0
        if verbose:
            print("  N1 = %f" % N1)
        d = (N1 - N0) / math.sqrt((n * 0.95 * 0.05) / 4)  # Compute the P value
        p = math.erfc(abs(d) / math.sqrt(2))

        outcome = TestOutcome.PASSED if (p >= 0.01) else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=p, p_list=None)

    def is_eligible(self, bitstring: Sequence) -> bool:
        return True
