#!/usr/bin/env python3
"""
SOLUSI INCOMPLETE #2: Fase Mining
===================================
File ini berisi kunci jawaban lengkapan untuk incomplete_2_mining.py
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
    LENGKAP: Cari semua conditional pattern base (prefix path).
    Traverse ke atas sampai root, kumpulkan item.
    Lakukan untuk SEMUA node yang terhubung lewat node-link.
    """
    # LENGKAP: traverse node-link chain
    patterns = []
    while node is not None:
        path = []
        current = node.parent
        while current is not None and current.item is not None:
            path.append(current.item)
            current = current.parent
        if path:
            path.reverse()
            patterns.append((path, node.count))
        node = node.next
    return patterns


def build_conditional_tree(cond_patterns, min_support):
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


def extract_frequent_itemsets(header_table, item_counts, min_support, prefix, results, transactions_count):
    """
    LENGKAP: Ekstraksi frequent itemsets secara rekursif.
    """
    # Urutkan item ascending
    items_order = sorted(header_table.keys(), key=lambda x: item_counts.get(x, header_table[x][0]))

    for item in items_order:
        # LENGKAP (bagian 1): Dapatkan support count dan tambahkan itemset
        count = item_counts[item]
        new_prefix = list(prefix) + [item]
        key = tuple(sorted(new_prefix))
        results[key] = count

        # LENGKAP (bagian 2): Dapatkan conditional pattern base, bangun conditional tree, rekursi
        node = header_table[item][1]
        if node is None:
            continue
        cond_patterns = find_prefix_path(node)
        if cond_patterns:
            cond_tree, cond_header = build_conditional_tree(cond_patterns, min_support)
            if cond_tree is not None:
                # Hitung item_counts untuk conditional tree
                cond_item_counts = defaultdict(int)
                for pat, c in cond_patterns:
                    for p in pat:
                        cond_item_counts[p] += c
                extract_frequent_itemsets(cond_header, cond_item_counts, min_support, new_prefix, results, transactions_count)


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

    results = {}
    for item, count in item_counts.items():
        if count >= MIN_SUPPORT:
            results[(item,)] = count

    print("\n=== Mining Frequent Itemsets ===")
    extract_frequent_itemsets(header_table, item_counts, MIN_SUPPORT, [], results, len(transactions))

    print(f"\nTotal frequent itemsets: {len(results)}")
    for k, v in sorted(results.items(), key=lambda x: (len(x[0]), x[0])):
        print(f"  {', '.join(k):30s} : count={v}")

    print(f"\nExpected: 42 itemsets (sesuai fp_growth_lengkap.py)")


if __name__ == "__main__":
    run()
