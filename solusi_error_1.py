#!/usr/bin/env python3
"""
SOLUSI ERROR #1: Insertion Sort
=================================
File ini berisi kunci jawaban untuk error_1_insertion_sort.py

ERROR YANG DITEMUKAN:
  Pada fungsi sort_items(), perbandingan `<` seharusnya `>`
  untuk ascending -> descending.

PERBAIKAN:
  while j >= 0 and item_counts[items[j]] > item_counts[key]:
  (ganti < dengan >)
"""
import csv
from collections import defaultdict


def sort_items(items, item_counts):
    """
    Urutkan item berdasarkan support count secara menurun (descending).
    PERBAIKAN: ganti '<' menjadi '>'
    """
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        # PERBAIKAN: '<' -> '>' (ascending -> descending)
        while j >= 0 and item_counts[items[j]] > item_counts[key]:
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
        # PERBAIKAN: insertion sort sudah benar arahnya
        filtered = sort_items(filtered, item_counts)
        sorted_transactions.append(filtered)
    return sorted_transactions, frequent_items


def run():
    DATA_FILE = "dataset_transaksi.csv"
    MIN_SUPPORT = 2

    transactions = load_transactions(DATA_FILE)
    item_counts = count_items(transactions)

    print("=== SOLUSI ERROR #1: Insertion Sort (DESCENDING) ===")
    print(f"Min Support: {MIN_SUPPORT}\n")

    sorted_tx, freq_items = filter_and_sort(transactions, item_counts, MIN_SUPPORT)

    print("Transaksi setelah sort (DESCENDING - benar):")
    for i, t in enumerate(sorted_tx):
        print(f"  T{i+1}: {t}")

    print("\nUrutan sekarang DESCENDING (support terbesar dulu) - BENAR!")
    print("Bandingkan dengan output error_1 yang ascending (salah).")


if __name__ == "__main__":
    run()
