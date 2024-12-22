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
from nist_sp800_22.utils.gamma_functions import gammaincc, gamma


class OverlappingTemplateMatchingTest(TestInterface):
    name = "Overlapping Template Matching Test"

    def lgamma(self, x):
        return math.log(gamma(x))

    def Pr(self, u, eta):
        if u == 0:
            p = math.exp(-eta)
        else:
            sum = 0.0
            for lll in range(1, u + 1):
                sum += math.exp(
                    -eta
                    - u * math.log(2)
                    + lll * math.log(eta)
                    - self.lgamma(lll + 1)
                    + self.lgamma(u)
                    - self.lgamma(lll)
                    - self.lgamma(u - lll + 1)
                )
            p = sum
        return p

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        # n = len(bitstring)

        m = 10
        # Build the template B as a random list of bits
        B = [1 for x in range(m)]

        N = 968
        K = 5
        M = 1062
        if len(bitstring) < (M * N):
            print(
                "Insufficient data. %d bit provided. 1,028,016 bits required"
                % len(bitstring)
            )
            return False, 0.0, None

        blocks = list()  # Split into N blocks of M bits
        for i in range(N):
            blocks.append(bitstring[i * M : (i + 1) * M])

        # Count the distribution of matches of the template across blocks: Vj
        v = [0 for x in range(K + 1)]
        for block in blocks:
            count = 0
            for position in range(M - m):
                if block[position : position + m] == B:
                    count += 1

            if count >= (K):
                v[K] += 1
            else:
                v[count] += 1

        # lamd = float(M-m+1)/float(2**m) # Compute lambda and nu
        # nu = lamd/2.0

        chisq = 0.0  # Compute Chi-Square
        # pi = [0.324652,0.182617,0.142670,0.106645,0.077147,0.166269] # From spec
        pi = [0.364091, 0.185659, 0.139381, 0.100571, 0.0704323, 0.139865]  # From STS
        piqty = [int(x * N) for x in pi]

        lambd = (M - m + 1.0) / (2.0**m)
        eta = lambd / 2.0
        sum = 0.0
        for i in range(K):  #  Compute Probabilities
            pi[i] = self.Pr(i, eta)
            sum += pi[i]

        pi[K] = 1 - sum
        # for block in blocks:
        #    count = 0
        #    for j in xrange(M-m+1):
        #        if B == block[j:j+m]:
        #            count += 1
        #    if ( count <= 4 ):
        #        v[count]+= 1
        #    else:
        #        v[K]+=1

        sum = 0
        chisq = 0.0
        for i in range(K + 1):
            chisq += ((v[i] - (N * pi[i])) ** 2) / (N * pi[i])
            sum += v[i]

        p = gammaincc(5.0 / 2.0, chisq / 2.0)  # Compute P value

        if verbose:
            print("  B = ", B)
            print("  m = ", m)
            print("  M = ", M)
            print("  N = ", N)
            print("  K = ", K)
            print("  model = ", piqty)
            print("  v[j] =  ", v)
            print("  chisq = ", chisq)

        outcome = TestOutcome.PASSED if (p >= 0.01) else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=p, p_list=None)

    def is_eligible(self, bitstring: Sequence) -> bool:
        N = 968
        M = 1062
        return len(bitstring) >= (M * N)
