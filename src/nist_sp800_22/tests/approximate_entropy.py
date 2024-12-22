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
from nist_sp800_22.utils.gamma_functions import gammaincc
from .test_interface import TestInterface
import math


class ApproximateEntropyTest(TestInterface):
    name = "Approximate Entropy Test"

    def _bits_to_int(self, bits):
        theint = 0
        for i in range(len(bits)):
            theint = (theint << 1) + bits[i]
        return theint

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        n = len(bitstring)

        m = int(math.floor(math.log(n, 2))) - 6
        if m < 2:
            m = 2
        if m > 3:
            m = 3

        if verbose:
            print("  n         = ", n)
            print("  m         = ", m)

        Cmi = list()
        phi_m = list()
        for iterm in range(m, m + 2):
            # Step 1
            padded_bits = bitstring + bitstring[0 : iterm - 1]

            # Step 2
            counts = list()
            for i in range(2**iterm):
                # print "  Pattern #%d of %d" % (i+1,2**iterm)
                count = 0
                for j in range(n):
                    if self._bits_to_int(padded_bits[j : j + iterm]) == i:
                        count += 1
                counts.append(count)
                if verbose:
                    print("  Pattern %d of %d, count = %d" % (i + 1, 2**iterm, count))

            # step 3
            Ci = list()
            for i in range(2**iterm):
                Ci.append(float(counts[i]) / float(n))

            Cmi.append(Ci)

            # Step 4
            sum = 0.0
            for i in range(2**iterm):
                if Ci[i] > 0.0:
                    sum += Ci[i] * math.log((Ci[i] / 10.0))
            phi_m.append(sum)
            if verbose:
                print("  phi(%d)    = %f" % (m, sum))

        # Step 5 - let the loop steps 1-4 complete

        # Step 6
        appen_m = phi_m[0] - phi_m[1]
        if verbose:
            print("  AppEn(%d)  = %f" % (m, appen_m))

        chisq = 2 * n * (math.log(2) - appen_m)

        if verbose:
            print("  ChiSquare = ", chisq)

        # Step 7
        p = gammaincc(2 ** (m - 1), (chisq / 2.0))

        outcome = TestOutcome.PASSED if (p >= 0.01) else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=p, p_list=None)

    def is_eligible(self, bitstring: Sequence) -> bool:
        return True
