#!/usr/bin/env python3
"""
ERROR #3: Conditional Pattern Base
====================================

Program ini mengandung ERROR pada pencarian conditional pattern base.
Error tersebut menyebabkan pola tidak ditemukan dengan benar.

GETO: Program berjalan tapi menampilkan hasil SALAH (itemset hilang/duplikat/jumlah salah).

PETUNJIAN:
- Jalankan program: python3 error_3_conditional_pattern.py
- Perhatikan hasil frequent itemsets yang salah
- Temukan dan perbaiki error pada find_conditional_patterns()
- Bandingkan hasil dengan fp_growth_lengkap.py

KODE YANG ERROR:
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
                # Update node-link
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    link_node = header_table[item][1]
                    while link_node.next is not None:
                        link_node = link_node.next
                    link_node.next = new_node
                current = new_node
    return root, header_table


def find_conditional_patterns(node):
    """
    Cari conditional pattern base untuk sebuah item.
    *** ADA ERROR DI SINI ***
    """
    patterns = []
    # ERROR: hanya mengambil satu node pertama, seharusnya traverse semua node
    # lewat node-link (node.next)
    # ERROR: while condition salah - harus cek `node is not None`
    # tapi kode ini tidak pernah traverse ke node.next
    if node is not None:
        path = []
        current = node.parent
        while current is not None and current.item is not None:
            path.append(current.item)
            current = current.parent
        if path:
            path.reverse()
            # ERROR: count-nya salah - harusnya node.count, tapi pakai 1
            patterns.append((path, 1))  # HARUS: node.count

        # ERROR: lupa traverse ke node.next!
        # Harusnya ada: node = node.next; while ...

    return patterns


def mine_fp_tree(header_table, item_counts, min_support, prefix, results):
    """Rekursi untuk ekstraksi frequent itemsets."""
    for item in sorted(header_table.keys(), key=lambda x: item_counts[x], reverse=True):
        count = item_counts[item]
        new_prefix = list(prefix) + [item]
        key = tuple(sorted(new_prefix))
        results[key] = count

        node = header_table[item][1]
        cond_patterns = find_conditional_patterns(node)

        if cond_patterns:
            # Bangun conditional tree (simplified - langsung count)
            cond_counts = defaultdict(int)
            for pat, c in cond_patterns:
                cond_counts[item] += c  # simplified
                for p in pat:
                    cond_counts[p] += c

            frequent_cond = {k: v for k, v in cond_counts.items() if v >= min_support and k != item}

            if frequent_cond:
                # Rekursi
                sub_header = {k: [v, None] for k, v in frequent_cond.items()}
                mine_fp_tree(sub_header, cond_counts, min_support, new_prefix, results)


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

    print("=== ERROR #3: Conditional Pattern Base ===")
    print(f"Min Support: {MIN_SUPPORT}\n")

    results = {}
    for item in sorted(frequent_items, key=lambda x: item_counts[x]):
        count = item_counts[item]
        results[(item,)] = count

        node = header_table[item][1]
        cond_patterns = find_conditional_patterns(node)
        print(f"Conditional patterns untuk '{item}':")
        print(f"  Ditemukan: {cond_patterns}  (SEHARUSNYA ada {len(cond_patterns)} patterns)")
        if len(cond_patterns) == 1:
            print(f"  ERROR: hanya 1 pattern tapi seharusnya lebih! Lupa traverse node.next")
        print()

    mine_fp_tree(header_table, item_counts, MIN_SUPPORT, [], results)

    print("Frequent Itemsets yang ditemukan (SALAH):")
    print(f"  Total: {len(results)}")
    for k, v in sorted(results.items(), key=lambda x: (len(x[0]), x[0])):
        print(f"  {', '.join(k):30s} : count={v}")

    print("\nSilakan perbaiki find_conditional_patterns()!")
    print("Hint: (1) traverse semua node via node-link, (2) gunakan node.count yang benar")


if __name__ == "__main__":
    run()
