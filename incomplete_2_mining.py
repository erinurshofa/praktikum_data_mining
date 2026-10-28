#!/usr/bin/env python3
"""
INCOMPLETE #2: Fase Mining (Ekstraksi Pola Frekuen)
=====================================================

Program ini memiliki BAGIAN KOSONG (YOUR CODE HERE) pada:
  1. Fungsi find_prefix_path() - mencari conditional pattern base
  2. Fungsi extract_frequent_itemsets() - rekursi untuk mining

PETUNJIN:
- Baca tiap bagian yang bertanda # === YOUR CODE HERE ===
- Lengkapi kode agar program dapat mengekstrak semua frequent itemsets
- Bandingkan hasil dengan fp_growth_lengkap.py

PETUNJIAN LAIN:
- Conditional pattern base = semua prefix path dari node yang sama
- Gunakan rekursi untuk conditional FP-Tree
"""

import csv
from collections import defaultdict


class Node:
    def __init__(self, item=None, count=0, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None

    def display(self, indent=0):
        label = "root" if self.item is None else f"{self.item}:{self.count}"
        print("  " * indent + label)
        for child in self.children.values():
            child.display(indent + 1)


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


def build_fp_tree(transactions, frequent_items, item_counts):
    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]

    root = Node(item=None)

    for transaction in transactions:
        current = root
        for item in transaction:
            if item in current.children:
                current = current.children[item]
                current.count += 1
            else:
                new_node = Node(item=item, count=1, parent=current)
                current.children[item] = new_node
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    link_node = header_table[item][1]
                    while link_node.next is not None:
                        link_node = link_node.next
                    link_node.next = new_node
                current = new_node
    return root, header_table


def find_prefix_path(node):
    """
    Cari semua conditional pattern base (prefix path) dari sebuah node.
    Traverse ke atas sampai root, kumpulkan item.
    Lakukan untuk SEMUA node yang terhubung lewat node-link.

    Returns: list of (prefix_path, count)
    """
    # === YOUR CODE HERE ===
    # Lengkapi: traverse node-link chain (node -> node.next -> ...)
    # Untuk tiap node, crawl ke atas ke root, kumpulkan path
    # Kembalikan list of tuples (path_reversed, node.count)
    return []  # ganti dengan implementasi Anda


def build_conditional_tree(cond_patterns, min_support):
    """
    Bangun conditional FP-Tree dari conditional pattern base.
    """
    if not cond_patterns:
        return None, {}

    # Hitung frekuensi item di conditional pattern base
    item_counts = defaultdict(int)
    for path, count in cond_patterns:
        for item in path:
            item_counts[item] += count

    frequent_items = {item for item, c in item_counts.items() if c >= min_support}

    if not frequent_items:
        return None, {}

    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]

    root = Node(item=None)

    for path, count in cond_patterns:
        filtered = [item for item in path if item in frequent_items]
        filtered.sort(key=lambda x: item_counts[x], reverse=True)
        if not filtered:
            continue
        current = root
        for item in filtered:
            if item in current.children:
                current = current.children[item]
                current.count += count
            else:
                new_node = Node(item=item, count=count, parent=current)
                current.children[item] = new_node
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    link_node = header_table[item][1]
                    while link_node.next is not None:
                        link_node = link_node.next
                    link_node.next = new_node
                current = new_node

    return root, header_table


def extract_frequent_itemsets(header_table, item_counts, min_support, prefix, results, transactions_count):
    """
    Ekstraksi frequent itemsets secara rekursif.
    """
    # Urutkan item ascending (dari tidak frequent ke frequent) untuk header table
    items_order = sorted(header_table.keys(), key=lambda x: item_counts.get(x, header_table[x][0]))

    for item in items_order:
        # === YOUR CODE HERE (bagian 1) ===
        # Dapatkan support count untuk item ini
        # Tambahkan frequent itemset individual ke results

        # === YOUR CODE HERE (bagian 2) ===
        # Dapatkan node-link dari header_table[item]
        # Panggil find_prefix_path() untuk dapatkan conditional pattern base
        # Jika ada conditional patterns, bangun conditional tree
        # Rekursi dengan prefix yang diperluas

        pass  # ganti dengan implementasi Anda


def run():
    DATA_FILE = "dataset_transaksi.csv"
    MIN_SUPPORT = 2

    transactions = load_transactions(DATA_FILE)
    item_counts = count_items(transactions)
    frequent_items = {item for item, c in item_counts.items() if c >= MIN_SUPPORT}

    sorted_tx = []
    for t in transactions:
        filtered = [item for item in t if item in frequent_items]
        filtered.sort(key=lambda x: item_counts[x], reverse=True)
        sorted_tx.append(filtered)

    root, header_table = build_fp_tree(sorted_tx, frequent_items, item_counts)

    print("=== Struktur FP-Tree ===")
    root.display()

    print("\n=== Header Table ===")
    for item, info in sorted(header_table.items(), key=lambda x: x[1][0], reverse=True):
        print(f"  {item:12s}: count={info[0]}, first_link={info[1]}")

    print("\n=== Testing find_prefix_path ===")
    for item, info in header_table.items():
        node = info[1]
        paths = find_prefix_path(node)
        print(f"  {item}: {len(paths)} prefix paths -> {paths}")

    # Tambahkan frequent itemset individual
    results = {}
    for item, count in item_counts.items():
        if count >= MIN_SUPPORT:
            results[(item,)] = count

    print("\n=== Mining Frequent Itemsets ===")
    extract_frequent_itemsets(header_table, item_counts, MIN_SUPPORT, [], results, len(transactions))

    print(f"\nTotal frequent itemsets: {len(results)}")
    for k, v in sorted(results.items(), key=lambda x: (len(x[0]), x[0])):
        print(f"  {', '.join(k):30s} : count={v}")

    print(f"\nExpected: 42 itemsets (bandingkan dengan fp_growth_lengkap.py)")
    if len(results) < 42:
        print("  -> Lengkapi YOUR CODE HERE di atas!")


if __name__ == "__main__":
    run()
