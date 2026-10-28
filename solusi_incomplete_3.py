#!/usr/bin/env python3
"""
SOLUSI INCOMPLETE #3: Header Table
====================================
File ini berisi kunci jawaban lengkapan untuk incomplete_3_header_table.py

ERROR YANG DITEMUKAN:
  verify_header_links() hanya menghitung node unik, bukan semua node yang
  terhubung lewat node-link chain.

PERBAIKAN:
  Traverse seluruh pohon BFS untuk menghitung jumlah node per item,
  lalu bandingkan dengan count di header table.
"""
import csv
from collections import defaultdict, deque


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
    LENGKAP: Bangun header table dengan format [count, None].
    """
    # === LENGKAP YOUR CODE HERE ===
    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]
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

                # LENGKAP: Update node-link di header table
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    link_node = header_table[item][1]
                    while link_node.next is not None:
                        link_node = link_node.next
                    link_node.next = new_node

                current = new_node
    return root


def verify_header_links(root, header_table):
    """
    LENGKAP: Verifikasi bahwa header table mengarah ke semua node
    dengan item tersebut di pohon.

    Traversal BFS pohon, akumulat count per item (jumlah total count).
    Bandingkan dengan count di header table.

    Catatan: header_table[item][0] = total support count (jumlah semua
    node dengan item ini). Kita harus akumulasi count, bukan hitung node.
    """
    verification = {}
    item_total_counts = defaultdict(int)

    # BFS traversal pohon — akumulasi count per item
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.item is not None:
            item_total_counts[node.item] += node.count
        for child in node.children.values():
            queue.append(child)

    # Bandingkan dengan header table count
    for item in header_table:
        verification[item] = item_total_counts.get(item, 0)

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

    print("Header table (sebelum FP-Tree):")
    for item, info in header_table.items():
        print(f"  {item:12s}: count={info[0]}, link={info[1]}")

    print("\n=== Membangun FP-Tree ===")
    root = build_fp_tree(sorted_tx, header_table, item_counts)

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
