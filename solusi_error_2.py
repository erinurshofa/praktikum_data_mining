#!/usr/bin/env python3
"""
SOLUSI ERROR #2: Header Table
==============================
File ini berisi kunci jawaban untuk error_2_header_table.py

ERROR YANG DITEMUKAN:
  1. build_header_table() pakai key=item.upper() — tidak konsisten
  2. update_node_link() pakai key=item.upper() — mismatch dengan pemanggil

PERBAIKAN:
  1. Hapus .upper() — gunakan key=item secara langsung
  2. Konsistensi key di seluruh header table
"""
import csv
from collections import defaultdict


class Node:
    def __init__(self, item=None, count=0):
        self.item = item
        self.count = count
        self.children = {}
        self.next = None
        self.parent = None


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


def build_header_table(frequent_items, item_counts):
    """
    PERBAIKAN: hapus .upper() — gunakan item langsung sebagai key
    """
    header_table = {}
    for item in frequent_items:
        # PERBAIKAN: item.upper() -> item
        header_table[item] = [item_counts[item], None]
    return header_table


def update_node_link(header_table, item, new_node):
    """
    PERBAIKAN: hapus .upper() — gunakan item langsung sebagai key
    """
    # PERBAIKAN: item.upper() -> item
    key = item
    if key not in header_table:
        return

    if header_table[key][1] is None:
        header_table[key][1] = new_node
    else:
        link_node = header_table[key][1]
        while link_node.next is not None:
            link_node = link_node.next
        link_node.next = new_node


def build_fp_tree(transactions, header_table, item_counts):
    root = Node(item=None)

    for transaction in transactions:
        current = root
        for item in transaction:
            if item in current.children:
                current = current.children[item]
                current.count += 1
            else:
                new_node = Node(item=item, count=1)
                new_node.parent = current
                current.children[item] = new_node
                update_node_link(header_table, item, new_node)
                current = new_node
    return root


def find_prefix_path(node):
    paths = []
    while node is not None:
        path = []
        current = node.parent
        while current is not None and current.item is not None:
            path.append(current.item)
            current = current.parent
        if path:
            path.reverse()
            paths.append((path, node.count))
        node = node.next
    return paths


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

    print("=== SOLUSI ERROR #2: Header Table (kunci konsisten) ===")

    header_table = build_header_table(frequent_items, item_counts)
    root = build_fp_tree(sorted_tx, header_table, item_counts)

    print("\nHeader Table (KEYS KONSISTEN - lowercase):")
    for k, v in header_table.items():
        node_ref = v[1]
        node_info = f"{node_ref.item}:{node_ref.count}" if node_ref else "None"
        print(f"  {k:12s}: count={v[0]}, first_node=({node_info})")

    print("\nPrefix path per item:")
    for item, info in header_table.items():
        node = info[1]
        if node:
            paths = find_prefix_path(node)
            print(f"  {item:12s}: {len(paths)} prefix paths")
        else:
            print(f"  {item:12s}: node_link = None")

    print("\nPerbaikan: semua key di header table konsisten (tidak .upper())")


if __name__ == "__main__":
    run()
