"""An educational Bloom filter implemented using Python's standard library.

Copyright 2026 Ib Helmer Nielsen
Licensed under the Apache License, Version 2.0 (see LICENSE).
"""

import hashlib
import math
from collections.abc import Iterator


class BloomFilter:
    """Space-efficient probabilistic membership test for strings.

    False means the item was definitely not added. True means the item
    *might* have been added; always confirm positive security decisions
    against an authoritative data source.
    """

    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        if isinstance(expected_items, bool) or not isinstance(expected_items, int) or expected_items <= 0:
            raise ValueError("expected_items must be a positive integer")
        if not isinstance(false_positive_rate, (float, int)) or not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be between 0 and 1")

        # m = -n * ln(p) / (ln(2) ** 2)
        self.bit_count = math.ceil(
            -expected_items * math.log(false_positive_rate) / math.log(2) ** 2
        )
        # k = (m/n) * ln(2)
        self.hash_count = max(1, round(self.bit_count / expected_items * math.log(2)))
        self._bits = bytearray((self.bit_count + 7) // 8)

    @property
    def memory_bytes(self) -> int:
        """Return the storage size of the bit array (excluding Python overhead)."""
        return len(self._bits)

    def _hash_positions(self, item: str) -> Iterator[int]:
        if not isinstance(item, str):
            raise TypeError("Bloom filter items must be strings")

        # Double hashing derives k positions from a single SHA-256 digest.
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big") or 1
        for index in range(self.hash_count):
            yield (h1 + index * h2) % self.bit_count

    def add(self, item: str) -> None:
        """Add an item to the filter."""
        for position in self._hash_positions(item):
            self._bits[position // 8] |= 1 << (position % 8)

    def __contains__(self, item: str) -> bool:
        """Check whether an item *might* be in the filter."""
        return all(
            self._bits[position // 8] & (1 << (position % 8))
            for position in self._hash_positions(item)
        )


def main() -> None:
    """Show how to prefilter an IP blacklist without blocking false positives."""
    bloom = BloomFilter(expected_items=10_000, false_positive_rate=0.01)

    # This set represents the authoritative blacklist (e.g. a database).
    blacklist = {"192.168.1.10", "192.168.1.20", "10.0.0.5", "172.16.0.100"}
    for ip_address in blacklist:
        bloom.add(ip_address)

    test_addresses = [
        "192.168.1.10",
        "192.168.1.99",
        "10.0.0.5",
        "8.8.8.8",
        "172.16.0.100",
    ]

    print("IP blacklist lookup using a Bloom filter:\n")
    for ip_address in test_addresses:
        if ip_address not in bloom:
            print(f"{ip_address}: NOT LISTED (no database lookup)")
        elif ip_address in blacklist:
            print(f"{ip_address}: BLOCKED (confirmed in blacklist)")
        else:
            print(f"{ip_address}: FALSE POSITIVE (do not block)")

    print("\nBloom filter configuration:")
    print(f"Bit array: {bloom.bit_count:,} bits")
    print(f"Hash functions: {bloom.hash_count}")
    print(f"Bit-array storage: {bloom.memory_bytes:,} bytes")


if __name__ == "__main__":
    main()
