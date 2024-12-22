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
import random
from nist_sp800_22.utils.gamma_functions import gammaincc


class NonOverlappingTemplateMatchingTest(TestInterface):
    name = "Non-Overlapping Template Matching Test"

    def _test(self, bitstring: Sequence, verbose: bool = False) -> TestResult:
        # The templates provdided in SP800-22rev1a
        templates = [None for x in range(7)]
        templates[0] = [[0, 1], [1, 0]]
        templates[1] = [[0, 0, 1], [0, 1, 1], [1, 0, 0], [1, 1, 0]]
        templates[2] = [
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 0],
        ]
        templates[3] = [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 1],
            [0, 1, 0, 1, 1],
            [0, 0, 1, 1, 1],
            [0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
        ]
        templates[4] = [
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 1],
            [0, 0, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 1],
            [0, 1, 0, 1, 1, 1],
            [0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [1, 1, 1, 0, 1, 0],
            [1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0],
        ]
        templates[5] = [
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 1, 1],
            [0, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 1, 1],
            [0, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 0],
            [1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 0],
        ]
        templates[6] = [
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 1, 1],
            [0, 0, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 1, 1],
            [0, 1, 0, 0, 1, 1, 1, 1],
            [0, 1, 0, 1, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 1, 0, 1, 1],
            [0, 1, 0, 1, 1, 1, 1, 1],
            [0, 1, 1, 0, 0, 1, 1, 1],
            [0, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 1, 0, 0],
            [1, 1, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 0, 1, 1, 0],
            [1, 1, 1, 0, 1, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 1, 0],
            [1, 1, 1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
        ]

        # n = len(bitstring)

        # Choose the template B
        r = random.SystemRandom()
        template_list = r.choice(templates)
        B = r.choice(template_list)

        m = len(B)

        N = 8
        M = int(math.floor(len(bitstring) / 8))
        # n = M * N

        blocks = list()  # Split into N blocks of M bits
        for i in range(N):
            blocks.append(bitstring[i * M : (i + 1) * M])

        W = list()  # Count the number of matches of the template in each block Wj
        for block in blocks:
            position = 0
            count = 0
            while position < (M - m):
                if block[position : position + m] == B:
                    position += m
                    count += 1
                else:
                    position += 1
            W.append(count)

        mu = float(M - m + 1) / float(2**m)  # Compute mu and sigma
        sigma = M * ((1.0 / float(2**m)) - (float((2 * m) - 1) / float(2 ** (2 * m))))

        chisq = 0.0  # Compute Chi-Square
        for j in range(N):
            chisq += ((W[j] - mu) ** 2) / (sigma**2)

        p = gammaincc(N / 2.0, chisq / 2.0)  # Compute P value
        outcome = TestOutcome.PASSED if (p >= 0.01) else TestOutcome.FAILED
        return TestResult(outcome=outcome, p_value=p, p_list=None)

    def is_eligible(self, bitstring: Sequence) -> bool:
        return True
