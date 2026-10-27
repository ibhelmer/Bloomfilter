"""Unit tests for the educational Bloom filter implementation."""

import unittest

from bloom_filter import BloomFilter


class BloomFilterTests(unittest.TestCase):
    def test_empty_filter_reports_absent(self):
        bloom = BloomFilter(100)
        self.assertNotIn("192.168.1.10", bloom)

    def test_added_items_have_no_false_negatives(self):
        bloom = BloomFilter(1_000, 0.01)
        addresses = [f"10.0.{i // 256}.{i % 256}" for i in range(1_000)]
        for address in addresses:
            bloom.add(address)
        for address in addresses:
            self.assertIn(address, bloom)

    def test_duplicate_insertions_and_unicode(self):
        bloom = BloomFilter(100)
        bloom.add("Malmø")
        bloom.add("Malmø")
        self.assertIn("Malmø", bloom)

    def test_array_size_matches_reported_bits(self):
        bloom = BloomFilter(10_000, 0.01)
        self.assertEqual(bloom.bit_count, 95_851)
        self.assertEqual(bloom.hash_count, 7)
        self.assertEqual(bloom.memory_bytes, 11_982)

    def test_bad_expected_items(self):
        for value in (0, -1, 1.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                BloomFilter(value)

    def test_bad_false_positive_rates(self):
        for value in (0, 1, -0.01, 1.1, float("nan")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                BloomFilter(100, value)

    def test_non_string_item(self):
        bloom = BloomFilter(100)
        with self.assertRaises(TypeError):
            bloom.add(42)
        with self.assertRaises(TypeError):
            _ = 42 in bloom


if __name__ == "__main__":
    unittest.main()
