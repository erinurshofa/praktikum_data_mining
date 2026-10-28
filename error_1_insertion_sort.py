#!/usr/bin/env python3
"""
ERROR #1: Insertion Sort / Sort Transaksi
============================================

Program ini mengandung ERROR pada fungsi pengurutan item dalam transaksi.
Error tersebut menyebabkan urutan item tidak sesuai dengan support count,
sehingga FP-Tree yang terbentuk tidak optimal.

GETO: Program akan crash / ValueError ketika dijalankan.

PETUNJIAN:
- Jalankan program: python3 error_1_insertion_sort.py
- Baca pesan error
- Temukan dan perbaiki error pada fungsi sort_items()
- Bandingkan hasil dengan fp_growth_lengkap.py

KODE YANG ERROR:
"""
import csv
from collections import defaultdict


def sort_items(items, item_counts):
    """
    Urutkan item berdasarkan support count secara menurun (descending).
    *** ADA ERROR DI SINI ***
    """
    # ERROR: menggunakan insertion sort tetapi perbandingannya salah arah
    # seharusnya descending (terbesar dulu), tapi kode ini ascending (terkecil dulu)
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        # ERROR: perbandingan '<' seharusnya '>'
        while j >= 0 and item_counts[items[j]] < item_counts[key]:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key
    return items


def load_transactions(filepath):
    transactions = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items = row["Barang"].split(";")
            items = [item.strip() for item in items if item.strip()]
            transactions.append(items)
    return transactions


def count_items(transactions):
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1
    return dict(item_counts)


def filter_and_sort(transactions, item_counts, min_support):
    frequent_items = set()
    for item, count in item_counts.items():
        if count >= min_support:
            frequent_items.add(item)

    sorted_transactions = []
    for transaction in transactions:
        filtered = [item for item in transaction if item in frequent_items]
        # ERROR akan menyebabkan FP-Tree salah / hasil salah
        filtered = sort_items(filtered, item_counts)
        sorted_transactions.append(filtered)
    return sorted_transactions, frequent_items


def build_fp_tree(transactions, frequent_items, item_counts):
    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]

    root = {"children": {}, "item": None, "count": 0}

    for transaction in transactions:
        current = root
        for item in transaction:
            if item in current["children"]:
                current = current["children"][item]
                current["count"] += 1
            else:
                current["children"][item] = {"children": {}, "item": item, "count": 1}
                if header_table[item][1] is None:
                    pass  # simplified
                current = current["children"][item]
    return root, header_table


def run():
    DATA_FILE = "dataset_transaksi.csv"
    MIN_SUPPORT = 2

    transactions = load_transactions(DATA_FILE)
    item_counts = count_items(transactions)

    print("=== ERROR #1: Insertion Sort ===")
    print(f"Min Support: {MIN_SUPPORT}\n")

    sorted_tx, freq_items = filter_and_sort(transactions, item_counts, MIN_SUPPORT)

    print("Transaksi setelah sort (URUTAN SALAH - ascending):")
    for i, t in enumerate(sorted_tx):
        print(f"  T{i+1}: {t}")

    print("\nIni menyebabkan FP-Tree tidak optimal!")
    print("Urutan seharusnya DESCENDING (terbesar/support terbesar dulu).")
    print("\nSilakan perbaiki fungsi sort_items().")

    root, header = build_fp_tree(sorted_tx, freq_items, item_counts)
    print(f"\nFP-Tree (terbangun dengan urutan salah):")
    print(f"  Root children: {list(root['children'].keys())}")


if __name__ == "__main__":
    run()
