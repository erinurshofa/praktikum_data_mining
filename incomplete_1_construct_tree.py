#!/usr/bin/env python3
"""
INCOMPLETE #1: Konstruksi FP-Tree
==================================

Program ini memiliki BAGIAN KOSONG (YOUR CODE HERE) pada:
  1. Fungsi build_fp_tree() - konstruksi FP-Tree dari transaksi
  2. Fungsi update_node_link() - update node-link di header table

PETUNJAIN:
- Baca tiap bagian yang bertanda # === YOUR CODE HERE ===
- Lengkapi kode agar program dapat:
  a) Membangun FP-Tree dengan benar
  b) Menghubungkan node-link di header table
- Bandingkan hasil dengan fp_growth_lengkap.py

PETUNJIAN LAIN:
- Gunakan struktur Node class yang sudah diberikan
- header_table[item] = [count, first_node_link]
"""

import csv
from collections import defaultdict


class Node:
    """Node dalam FP-Tree."""

    def __init__(self, item=None, count=0, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None  # node-link ke node berikutnya

    def display(self, indent=0):
        if self.item is None:
            label = "root"
        else:
            label = f"{self.item}:{self.count}"
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


def filter_and_sort(transactions, item_counts, frequent_items):
    sorted_transactions = []
    for transaction in transactions:
        filtered = [item for item in transaction if item in frequent_items]
        filtered.sort(key=lambda x: item_counts[x], reverse=True)
        sorted_transactions.append(filtered)
    return sorted_transactions


def build_header_table(frequent_items, item_counts):
    """Bangun header table dengan format [count, None]."""
    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]
    return header_table


def update_node_link(header_table, item, new_node):
    """
    Update node-link di header table untuk item tertentu.
    Jika belum ada node pertama, set new_node sebagai pertama.
    Jika sudah ada, traverse ke node terakhir lewat link dan append.
    """
    # === YOUR CODE HERE ===
    # Lengkapi fungsi ini
    # Hints:
    # - header_table[item][1] adalah pointer ke node pertama
    # - Traverse menggunakan .next sampai habis, lalu set new_node.next = None
    pass


def build_fp_tree(transactions, header_table, frequent_items):
    """
    Bangun FP-Tree dari daftar transaksi yang sudah disortir.
    Setiap transaksi dimasukkan secara berurutan, menggabungkan jalur yang
    sama.
    """
    root = Node(item=None)

    for transaction in transactions:
        current_node = root
        for item in transaction:
            if item in current_node.children:
                # Item sudah ada di anak, naik ke bawah
                current_node = current_node.children[item]
                current_node.count += 1
            else:
                # === YOUR CODE HERE ===
                # Buat node baru dan masukkan ke children
                # Update node-link via update_node_link()
                # Naik ke node baru
                pass
    return root


def run():
    DATA_FILE = "dataset_transaksi.csv"
    MIN_SUPPORT = 2

    transactions = load_transactions(DATA_FILE)
    item_counts = count_items(transactions)
    print("Perhitungan frekuensi item:")
    for item, count in sorted(item_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {item:12s}: {count}")

    frequent_items = set()
    for item, count in item_counts.items():
        if count >= MIN_SUPPORT:
            frequent_items.add(item)

    sorted_tx = filter_and_sort(transactions, item_counts, frequent_items)
    print(f"\nFrequent items: {frequent_items}")

    header_table = build_header_table(frequent_items, item_counts)

    root = build_fp_tree(sorted_tx, header_table, frequent_items)

    print("\n=== Struktur FP-Tree ===")
    root.display()

    print("\n=== Header Table ===")
    for item, info in sorted(header_table.items(), key=lambda x: x[1][0], reverse=True):
        print(f"  {item:12s}: count={info[0]}, first_link={info[1]}")

    print("\n=== VERIFIKASI ===")
    all_correct = True
    for item, info in header_table.items():
        if info[1] is None:
            print(f"  ERROR: '{item}' tidak memiliki node-link!")
            all_correct = False

    if all_correct:
        print("  Semua node-link terhubung dengan benar!")
    else:
        print("  Beberapa node-link belum terhubung. Lengkapi kode Anda.")

    print("\nBandingkan struktur pohon di atas dengan fp_growth_lengkap.py")


if __name__ == "__main__":
    run()
