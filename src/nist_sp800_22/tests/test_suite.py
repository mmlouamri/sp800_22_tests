from typing import Sequence

from .test_outcome_enum import TestOutcome
from .approximate_entropy import ApproximateEntropyTest
from .monobit import MonobitTest
from .binary_matrix_rank import BinaryMatrixRankTest
from .cumulative_sums import CumulativeSumsTest
from .dft import DiscreteFourierTransformTest
from .frequency_within_block import FrequencyWithinBlockTest
from .longest_run_ones_in_a_block import LongestRunOnesInABlockTest
from .overlapping_template_matching import OverlappingTemplateMatchingTest
from .random_excursion import RandomExcursionTest
from .random_excursion_variant import RandomExcursionVariantTest
from .runs import RunsTest
from .serial import SerialTest
from .maurers_universal import MaurersUniversalTest
from .non_overlapping_template_matching import NonOverlappingTemplateMatchingTest
from .linear_complexity import LinearComplexityTest


class NistSP80022r1Tests:
    tests = [
        MonobitTest(),
        ApproximateEntropyTest(),
        BinaryMatrixRankTest(),
        CumulativeSumsTest(),
        DiscreteFourierTransformTest(),
        FrequencyWithinBlockTest(),
        LongestRunOnesInABlockTest(),
        OverlappingTemplateMatchingTest(),
        RandomExcursionTest(),
        RandomExcursionVariantTest(),
        RunsTest(),
        SerialTest(),
        MaurersUniversalTest(),
        NonOverlappingTemplateMatchingTest(),
        LinearComplexityTest(),
    ]

    def run(self, bitstring: Sequence):
        results = {}

        for test in self.tests:
            current_result = test.test(bitstring)

            if (
                test.name == "Monobit Test"
                and current_result.outcome == TestOutcome.FAILED
            ):
                print("Monobit test failed, no need to run other tests.")
                exit(1)
            results[test.name] = (
                current_result.outcome.value,
                current_result.p_value,
                current_result.p_list,
            )
        return results

    def eligible_tests(self, bitstring: Sequence):
        results = {}
        for test in self.tests:
            results[test.name] = test.is_eligible(bitstring)
        return results
