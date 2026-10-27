"""Measure the observed false-positive rate of a Bloom filter.

Copyright 2026 Ib Helmer Nielsen
Licensed under the Apache License, Version 2.0 (see LICENSE).
"""

import argparse

from bloom_filter import BloomFilter


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", type=int, default=10_000,
                        help="number of unique items to insert (default: 10000)")
    parser.add_argument("--queries", type=int, default=20_000,
                        help="number of absent items to test (default: 20000)")
    parser.add_argument("--fp-rate", type=float, default=0.01,
                        help="target false-positive probability (default: 0.01)")
    args = parser.parse_args()
    if args.queries <= 0:
        parser.error("--queries must be a positive integer")

    bloom = BloomFilter(args.items, args.fp_rate)
    for index in range(args.items):
        bloom.add(f"known-{index}")

    # The tested strings are disjoint from the inserted strings.
    false_positives = sum(
        f"unknown-{index}" in bloom for index in range(args.queries)
    )
    observed_rate = false_positives / args.queries

    print(f"Inserted unique items: {args.items:,}")
    print(f"Absent queries:        {args.queries:,}")
    print(f"Bit-array size:        {bloom.bit_count:,} bits")
    print(f"Bit-array storage:     {bloom.memory_bytes:,} bytes")
    print(f"Hash functions:        {bloom.hash_count}")
    print(f"Target FP rate:        {args.fp_rate:.2%}")
    print(f"False positives:       {false_positives:,}")
    print(f"Observed FP rate:      {observed_rate:.2%}")
    print("Note: observed results vary with the input and sample size.")


if __name__ == "__main__":
    main()
