# Bloom Filter in Python

An easy-to-follow, **standard-library-only** implementation of a Bloom filter, using an **IP address blacklist** as a practical cybersecurity example. Suitable for learning about hashing, probabilistic data structures, memory efficiency, and prefiltering expensive database lookups.

## What is a Bloom filter?

A Bloom filter is a space-efficient, probabilistic data structure that tests whether an element may belong to a set. It uses a bit array and multiple hash positions.

- **Definitely not present:** At least one of the item's hash positions contains a `0`. The item was not inserted.
- **Possibly present:** All hash positions contain `1`. The item may have been inserted, or the result may be a **false positive**.
- **No false negatives:** An item that has been added will be reported as possibly present, as long as the same filter and hashing logic are used and its bits are not cleared.

A regular Bloom filter does not support safe deletion of individual items. A *counting Bloom filter* is one alternative when deletion is required.

## The cybersecurity example

Imagine a firewall checking incoming IP addresses against a large blacklist stored in a database.

```text
Incoming IP address
         |
         v
     Bloom filter
       /     \
  No match   Possible match
     |             |
 Definitely     Check the real
 not listed      blacklist
                   /    \
                Found  Absent
                  |      |
                Block  Allow (false positive)
```

**Important:** A Bloom filter must not be the sole basis for a security block decision. All positive matches must be checked against the authoritative blacklist.

## Requirements

- Python 3.9 or newer
- No third-party dependencies

## Run the example

```bash
python bloom_filter.py
```

Example output:

```text
IP blacklist lookup using a Bloom filter:

192.168.1.10: BLOCKED (confirmed in blacklist)
192.168.1.99: NOT LISTED (no database lookup)
10.0.0.5: BLOCKED (confirmed in blacklist)
8.8.8.8: NOT LISTED (no database lookup)
172.16.0.100: BLOCKED (confirmed in blacklist)

Bloom filter configuration:
Bit array: 95,851 bits
Hash functions: 7
Bit-array storage: 11,982 bytes
```

The configuration is sized for **10,000 items** and a target false-positive probability of **1% at that capacity**. The example inserts only four addresses, so its actual false-positive probability is much lower.

## How it works

1. **Initialize:** Create a bit array with all bits set to zero.
2. **Insert:** SHA-256 produces two 128-bit integers. *Double hashing* derives `k` positions and sets the corresponding bits to `1`.
3. **Check:** Calculate the same positions for a candidate item. Any `0` means **definitely absent**; all `1`s means **possibly present**.
4. **Confirm:** If the Bloom filter returns a positive result, consult the real blacklist.

### Filter sizing

For `n` expected elements and target false-positive probability `p`, the standard formulas are:

```text
m = ceil(-n * ln(p) / (ln(2)^2))
k = round((m / n) * ln(2))
```

Here, `m` is the number of bits and `k` is the number of hash positions per element.

Approximate bit-array storage for **10,000 elements**:

| Target false-positive rate | Storage | Hash functions |
| --- | ---: | ---: |
| 10% | 5.9 KiB | 3 |
| 5% | 7.6 KiB | 4 |
| 1% | 11.7 KiB | 7 |
| 0.1% | 17.6 KiB | 10 |
| 0.01% | 23.4 KiB | 13 |

The reported memory is **only the bit array**, excluding Python object overhead and the separate authoritative blacklist. Insertion beyond the planned capacity increases the false-positive probability.

## Measure false positives

The included experiment inserts disjoint `known-N` strings and queries `unknown-N` strings, then prints the observed false-positive percentage:

```bash
python experiment.py
python experiment.py --items 100000 --queries 50000 --fp-rate 0.001
```

The observed percentage varies with the number of queries and the inserted values. The configured rate is a probability target, **not** a guarantee for each experiment.

## Run the tests

```bash
python -m unittest discover -v
```

Tests cover the empty filter, no false negatives for inserted items, duplicates, Unicode, sizing, invalid parameters, and invalid item types.

## Student exercises

1. Read 100,000 IP addresses from a CSV file and insert them into a Bloom filter.
2. Generate another 100,000 IP addresses not present in the source and measure false positives.
3. Compare observed false-positive rates with target rates of 10%, 1%, and 0.1%.
4. Compare lookup time and memory use with a Python `set` and a SQLite database.
5. Investigate how exceeding the planned insertion capacity affects false positives.

> A Bloom filter is especially useful when the authoritative data is large, disk-backed, or remote. For an in-memory blacklist, a Python `set` already provides fast average-case membership checks.

## Files

| File | Description |
| --- | --- |
| `bloom_filter.py` | Bloom filter implementation and IP blacklist demonstration |
| `experiment.py` | Adjustable false-positive-rate experiment |
| `test_bloom_filter.py` | Standard-library `unittest` tests |
| `LICENSE` | Apache License, Version 2.0 |

## License

Apache License 2.0. See [LICENSE](LICENSE).
