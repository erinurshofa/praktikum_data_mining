#!/usr/bin/env python3
"""
ERROR #2: Header Table
========================

Program ini mengandung ERROR pada pembuatan header table dan node-link.
Error tersebut menyebabkan node-link tidak terhubung dengan benar,
sehingga pencarian conditional pattern base gagal.

GETO: Program akan crash / AttributeError / TypeError.

PETUNJIAN:
- Jalankan program: python3 error_2_header_table.py
- Baca pesan error atau output yang salah
- Temukan dan perbaiki error pada build_header_table() dan/atau
  update_node_link()
- Bandingkan hasil dengan fp_growth_lengkap.py

KODE YANG ERROR:
"""
import csv
from collections import defaultdict


class Node:
    def __init__(self, item=None, count=0):
        self.item = item
        self.count = count
        self.children = {}
        self.next = None  # node-link


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
    *** ADA ERROR DI SINI ***
    """
    header_table = {}
    for item in frequent_items:
        # ERROR: hanya menyimpan [count, None], tapi seharusnya
        # menyimpan referensi ke node pertama.
        # Masalahnya: key-nya salah (string vs reference)
        # ERROR: pakai item.upper() — menyebabkan key tidak konsisten
        header_table[item.upper()] = [item_counts[item], None]
    return header_table


def update_node_link(header_table, item, node):
    """
    Update node-link di header table.
    *** ADA ERROR DI SINI ***
    """
    # ERROR: tidak cek apakah item ada di header_table
    # ERROR: key-nya pakai item.upper() tapi pemanggil pakai item semula
    key = item.upper()  # ini menyebabkan mismatch
    if key not in header_table:
        return  # ERROR: seharusnya tidak terjadi karena key harus konsisten

    if header_table[key][1] is None:
        header_table[key][1] = node
    else:
        link_node = header_table[key][1]
        while link_node.next is not None:
            link_node = link_node.next
        link_node.next = node


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
                current.children[item] = new_node
                # ERROR: panggil update_node_link dengan key yang tidak konsisten
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

    print("=== ERROR #2: Header Table ===")
    print(f"Min Support: {MIN_SUPPORT}\n")

    header_table = build_header_table(frequent_items, item_counts)

    print("Header Table (KEYS SALAH - uppercase!):")
    for k, v in header_table.items():
        print(f"  {k:12s}: count={v[0]}, link={v[1]}")

    root = build_fp_tree(sorted_tx, header_table, item_counts)

    print("\n--- Mencari prefix path (akan gagal) ---")
    try:
        for item, info in header_table.items():
            node = info[1]
            if node is None:
                print(f"  {item}: node_link = None (ERROR! seharusnya ada isi)")
            else:
                paths = find_prefix_path(node)
                print(f"  {item}: {len(paths)} prefix paths")
    except Exception as e:
        print(f"ERROR saat mencari prefix path: {type(e).__name__}: {e}")

    print("\nSilakan perbaiki build_header_table() dan update_node_link().")
    print("Hint: konsistensi key di header table sangat penting!")


if __name__ == "__main__":
    run()
