#!/usr/bin/env python3
"""
INCOMPLETE #3: Header Table
==============================

Program ini memiliki BAGIAN KOSONG (YOUR CODE HERE) pada:
  1. Fungsi build_header_table() - inisialisasi header table
  2. Fungsi verify_header_links() - verifikasi node-link

PETUNJIAN:
- Baca tiap bagian yang bertanda # === YOUR CODE HERE ===
- Lengkapi kode agar header table terhubung dengan benar ke node di pohon
- Header table format: {item: [count, node_link]}

PETUNJIAN LAIN:
- Setelah membangun FP-Tree, setiap item di header table harus memiliki
  node_link yang merujuk ke node pertama di pohon
- Jalankan verifikasi di akhir
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
    Bangun header table.
    Format: {item: [count, None]}  (None = belum ada node-link)

    Setelah pohon dibangun, node-link harus diisi dengan referensi
    ke node pertama untuk item tersebut di pohon.
    """
    # === YOUR CODE HERE ===
    # Inisialisasi header_table dengan format [count, None]
    # untuk setiap item di frequent_items
    header_table = {}
    # Lengkapi di sini
    return header_table


def build_fp_tree(transactions, header_table, item_counts):
    """Bangun FP-Tree dan update header table node-link."""
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

                # Update node-link di header table
                # === YOUR CODE HERE ===
                # Jika header_table[item][1] is None, set ke new_node
                # Jika sudah ada, traverse lewat .next sampai node terakhir, lalu append

                current = new_node
    return root


def verify_header_links(root, header_table):
    """
    Verifikasi bahwa setiap item di header table memiliki node-link yang
    mengarah ke semua node dengan item tersebut di pohon.

    Returns: dict {item: jumlah_node_yang_ditemukan}
    """
    # === YOUR CODE HERE ===
    # Traverse pohon secara BFS/DFS, untuk setiap node, cek apakah
    # item-nya ada di header table
    # Hitung berapa node dengan item tersebut
    # Bandingkan dengan count di header table

    verification = {}
    return verification


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

    print("=== Membangun Header Table ===")
    header_table = build_header_table(frequent_items, item_counts)

    # Tampilkan header table sebelum pohon dibangun
    print("Header table (sebelum FP-Tree):")
    for item, info in header_table.items():
        print(f"  {item:12s}: count={info[0]}, link={info[1]}")

    print("\n=== Membangun FP-Tree ===")
    root = build_fp_tree(sorted_tx, header_table, item_counts)

    # Display tree
    def display(node, indent=0):
        label = "root" if node.item is None else f"{node.item}:{node.count}"
        print("  " * indent + label)
        for child in node.children.values():
            display(child, indent + 1)
    display(root)

    print("\n=== Header Table (setelah FP-Tree) ===")
    for item, info in sorted(header_table.items(), key=lambda x: x[1][0], reverse=True):
        node_ref = info[1]
        node_info = f"{node_ref.item}:{node_ref.count}" if node_ref else "None"
        print(f"  {item:12s}: count={info[0]}, first_node=({node_info})")

    print("\n=== Verifikasi Node-Link ===")
    verification = verify_header_links(root, header_table)

    for item, node_count in verification.items():
        expected = item_counts[item]
        status = "OK" if node_count == expected else "ERROR"
        print(f"  {item:12s}: ditemukan {node_count} node (expected {expected}) -> {status}")

    all_ok = all(node_count == item_counts[item] for item, node_count in verification.items())
    if all_ok:
        print("\n  Semua node-link terhubung dengan benar!")
    else:
        print("\n  Beberapa node-link belum benar. Lengkapi YOUR CODE HERE!")


if __name__ == "__main__":
    run()
