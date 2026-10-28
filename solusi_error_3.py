#!/usr/bin/env python3
"""
SOLUSI ERROR #3: Conditional Pattern Base
===========================================
File ini berisi kunci jawaban untuk error_3_conditional_pattern.py

ERROR YANG DITEMUKAN:
  1. find_conditional_patterns() hanya ambil satu node, lupa traverse node.next
  2. count-nya pakai 1, seharusnya node.count

PERBAIKAN:
  1. Tambahkan while loop untuk traverse semua node lewat node.next
  2. Gunakan node.count bukan hardcode 1
  3. mine_tree() harus membangun conditional FP-Tree secara rekursif penuh
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
    PERBAIKAN: traverse semua node lewat node-link, gunakan node.count yang benar
    """
    patterns = []
    # PERBAIKAN: traverse seluruh node via node.next (bukan hanya satu node)
    while node is not None:
        path = []
        current = node.parent
        while current is not None and current.item is not None:
            path.append(current.item)
            current = current.parent
        if path:
            path.reverse()
            # PERBAIKAN: pakai node.count, bukan hardcode 1
            patterns.append((path, node.count))
        node = node.next  # PERBAIKAN: lanjutkan ke node berikutnya
    return patterns


def build_conditional_tree(cond_patterns, min_support):
    """Bangun conditional FP-Tree dari conditional pattern base."""
    if not cond_patterns:
        return None, {}

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


def mine_tree(header_table, item_counts, min_support, prefix, results):
    """Rekursi: ekstraksi frequent itemsets dari conditional tree."""
    # Urutkan ascending (item tidak frequent -> frequent)
    items_order = sorted(header_table.keys(),
                         key=lambda x: item_counts.get(x, header_table[x][0]))

    for item in items_order:
        # Frequent itemset individual + kombinasi dengan prefix
        count = item_counts[item]
        new_prefix = list(prefix) + [item]
        key = tuple(sorted(new_prefix))
        results[key] = count

        # Dapatkan conditional pattern base
        node = header_table[item][1]
        if node is None:
            continue
        cond_patterns = find_conditional_patterns(node)

        if cond_patterns:
            cond_tree, cond_header = build_conditional_tree(cond_patterns, min_support)
            if cond_tree is not None:
                cond_item_counts = defaultdict(int)
                for pat, c in cond_patterns:
                    for p in pat:
                        cond_item_counts[p] += c
                mine_tree(cond_header, cond_item_counts, min_support,
                          new_prefix, results)


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

    print("=== SOLUSI ERROR #3: Conditional Pattern Base ===")
    print(f"Min Support: {MIN_SUPPORT}\n")

    print("Conditional patterns per item:")
    for item, info in header_table.items():
        node = info[1]
        paths = find_conditional_patterns(node)
        print(f"  {item:12s}: {len(paths)} prefix paths -> {paths}")

    results = {}
    mine_tree(header_table, item_counts, MIN_SUPPORT, [], results)

    print(f"\nTotal frequent itemsets: {len(results)}")
    for k, v in sorted(results.items(), key=lambda x: (len(x[0]), x[0])):
        print(f"  {', '.join(k):30s} : count={v}")

    print("\nPerbaikan: traverse node.next + gunakan node.count yang benar")
    print("           + bangun conditional tree secara rekursif penuh")


if __name__ == "__main__":
    run()
