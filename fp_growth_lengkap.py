#!/usr/bin/env python3
"""
FP-Growth Lengkap - Program Referensi
Algoritma Frequent Pattern Growth untuk menemukan pola frekuen.

File ini berisi implementasi lengkap dan BERFUNGSI dari algoritma FP-Growth.
Gunakan sebagai referensi untuk membandingkan dengan versi error/incomplete.

Cara pakai:
    python3 fp_growth_lengkap.py
"""

import csv
from collections import defaultdict, OrderedDict


class FPNode:
    """Node dalam FP-Tree."""

    def __init__(self, item=None, parent=None):
        self.item = item
        self.count = 0
        self.parent = parent
        self.children = {}      # child_name -> FPNode
        self.next = None        # node-link ke node berikutnya dengan item yang sama

    def increment(self):
        """Tambahkan count."""
        self.count += 1

    def display(self, indent=0):
        """Tampilkan struktur pohon (untuk debugging)."""
        if self.item is None:
            label = "root"
        else:
            label = f"{self.item}:{self.count}"
        print("  " * indent + label)
        for child in self.children.values():
            child.display(indent + 1)


def load_transactions_csv(filepath):
    """
    Baca transaksi dari file CSV.
    Format: TID,Barang  (Barang dipisahkan titik koma)
    """
    transactions = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items = row["Barang"].split(";")
            # Hapus whitespace dan item kosong
            items = [item.strip() for item in items if item.strip()]
            transactions.append(items)
    return transactions


def load_transactions_txt(filepath):
    """
    Baca transaksi dari file TXT.
    Format: setiap baris adalah satu transaksi, item dipisahkan spasi.
    """
    transactions = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            items = line.strip().split()
            if items:
                transactions.append(items)
    return transactions


def count_items(transactions):
    """Scan 1: Hitung frekuensi tiap item."""
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1
    return dict(item_counts)


def filter_items(transactions, item_counts, min_support):
    """Filter item yang support-nya < min_support, dan urutkan desc by count."""
    # Buat set item yang memenuhi min_support
    frequent_items = set()
    for item, count in item_counts.items():
        if count >= min_support:
            frequent_items.add(item)

    # Urutkan item dalam setiap transaksi: descending by support count
    sorted_transactions = []
    for transaction in transactions:
        filtered = [item for item in transaction if item in frequent_items]
        # Urutkan descending berdasarkan support count
        filtered.sort(key=lambda x: item_counts[x], reverse=True)
        # Jika ada, tambahkan ke list (jangan lewatkan transaksi kosong)
        sorted_transactions.append(filtered)
    return sorted_transactions, frequent_items


def build_fp_tree(transactions, frequent_items, item_counts):
    """
    Bangun FP-Tree dari transaksi yang sudah di-filter dan diurutkan.

    Returns:
        root: root node dari FP-Tree
        header_table: dict item -> [count, node_link]
    """
    # Buat header table
    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]  # [count, first_node_link]

    # Buat root node
    root = FPNode(item=None, parent=None)

    # Masukkan setiap transaksi ke dalam pohon
    for transaction in transactions:
        if not transaction:
            continue
        # Insert transaction ke pohon
        current_node = root
        for item in transaction:
            # Jika item sudah ada di children, traverse ke bawah
            if item in current_node.children:
                current_node = current_node.children[item]
                current_node.increment()
            else:
                # Buat node baru
                new_node = FPNode(item=item, parent=current_node)
                new_node.count = 1
                current_node.children[item] = new_node

                # Update node-link di header table
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    # Traverse ke node terakhir lewat node-link
                    link_node = header_table[item][1]
                    while link_node.next is not None:
                        link_node = link_node.next
                    link_node.next = new_node

                current_node = new_node
    return root, header_table


def find_prefix_path(node):
    """
    Cari conditional pattern base untuk sebuah node.
    Kembalikan list of (pattern, count).
    """
    paths = []
    # Traverse ke atas dari node ke root untuk dapatkan prefix path
    def _get_prefix_path(n):
        path = []
        current = n.parent
        while current is not None and current.item is not None:
            path.append(current.item)
            current = current.parent
        path.reverse()
        return path

    # Kumpulkan semua prefix path dari semua node yang terhubung lewat node-link
    while node is not None:
        prefix_path = _get_prefix_path(node)
        if prefix_path:
            paths.append((prefix_path, node.count))
        node = node.next

    return paths


def build_conditional_tree(cond_patterns, min_support):
    """
    Bangun conditional FP-Tree dari conditional pattern base.
    """
    if len(cond_patterns) == 0:
        return None, {}

    # Hitung frekuensi tiap item di conditional pattern base
    item_counts = defaultdict(int)
    for pattern, count in cond_patterns:
        for item in pattern:
            item_counts[item] += count

    # Filter item yang memenuhi min_support
    frequent_items = set()
    for item, count in item_counts.items():
        if count >= min_support:
            frequent_items.add(item)

    if len(frequent_items) == 0:
        return None, {}

    # Bangun header table untuk conditional tree
    header_table = {}
    for item in frequent_items:
        header_table[item] = [item_counts[item], None]

    # Bangun pohon
    root = FPNode(item=None, parent=None)

    for pattern, count in cond_patterns:
        # Filter dan urutkan item
        filtered = [item for item in pattern if item in frequent_items]
        filtered.sort(key=lambda x: item_counts[x], reverse=True)

        if not filtered:
            continue

        current_node = root
        for item in filtered:
            if item in current_node.children:
                current_node = current_node.children[item]
                current_node.count += count  # penting: tambahkan count, bukan increment
            else:
                new_node = FPNode(item=item, parent=current_node)
                new_node.count = count
                current_node.children[item] = new_node

                # Update node-link
                if header_table[item][1] is None:
                    header_table[item][1] = new_node
                else:
                    link_node = header_table[item][1]
                    while link_node.next is not None:
                        link_node = link_node.next
                    link_node.next = new_node

                current_node = new_node

    return root, header_table


def extract_frequent_itemsets(header_table, header_table_items, min_support, prefix, total_frequent_itemsets, cond_tree_root=None):
    """
    Ekstraksi frequent itemsets secara rekursif.
    """
    if cond_tree_root is not None:
        # Dari conditional tree
        for item in header_table_items:
            current_count = header_table[item][0]
            new_prefix = list(prefix)
            new_prefix.append(item)
            # Simpan frequent itemset
            itemset_tuple = tuple(sorted(new_prefix))
            total_frequent_itemsets[itemset_tuple] = current_count

            # Cari prefix path
            node = header_table[item][1]
            cond_patterns = find_prefix_path(node)

            if len(cond_patterns) > 0:
                # Bangun conditional tree
                cond_tree, cond_header = build_conditional_tree(cond_patterns, min_support)
                if cond_tree is not None:
                    cond_items = [i for i in sorted(cond_header.keys(),
                                                     key=lambda x: cond_header[x][0],
                                                     reverse=True)
                                  if cond_header[i][0] >= min_support]
                    extract_frequent_itemsets(
                        cond_header, cond_items, min_support, new_prefix,
                        total_frequent_itemsets, cond_tree
                    )
    else:
        # Dari main FP-tree
        for item in header_table_items:
            current_count = header_table[item][0]
            new_prefix = [item]
            itemset_tuple = tuple(sorted(new_prefix))
            total_frequent_itemsets[itemset_tuple] = current_count

            # Cari prefix path
            node = header_table[item][1]
            cond_patterns = find_prefix_path(node)

            if len(cond_patterns) > 0:
                cond_tree, cond_header = build_conditional_tree(cond_patterns, min_support)
                if cond_tree is not None:
                    cond_items = [i for i in sorted(cond_header.keys(),
                                                     key=lambda x: cond_header[x][0],
                                                     reverse=True)
                                  if cond_header[i][0] >= min_support]
                    extract_frequent_itemsets(
                        cond_header, cond_items, min_support, new_prefix,
                        total_frequent_itemsets, cond_tree
                    )


def run_fp_growth(filepath, min_support, delimiter="csv"):
    """
    Jalankan algoritma FP-Growth lengkap.

    Args:
        filepath: path ke file dataset
        min_support: minimum support count (integer)
        delimiter: "csv" atau "txt"
    """
    # 1. Load transaksi
    if delimiter == "csv":
        transactions = load_transactions_csv(filepath)
    else:
        transactions = load_transactions_txt(filepath)

    print("=" * 60)
    print("ALGORITMA FP-GROWTH")
    print("=" * 60)
    print(f"\nDataset: {filepath}")
    print(f"Min Support: {min_support}")
    print(f"Total Transaksi: {len(transactions)}")

    # 2. Scan 1: Hitung frekuensi item
    print("\n[Scan 1] Perhitungan frekuensi item:")
    item_counts = count_items(transactions)
    for item, count in sorted(item_counts.items(), key=lambda x: x[1], reverse=True):
        status = "FREQUENT" if count >= min_support else "tidak frequent"
        print(f"  {item:12s}: {count:3d}  ({status})")

    # 3. Filter & sort
    sorted_transactions, frequent_items = filter_items(transactions, item_counts, min_support)

    print("\n[Filter & Sort] Transaksi setelah filtering & sorting:")
    for i, t in enumerate(sorted_transactions):
        print(f"  T{i+1}: {t}")

    # 4. Bangun FP-Tree
    print("\n[Membangun FP-Tree] ...")
    root, header_table = build_fp_tree(sorted_transactions, frequent_items, item_counts)
    print("\nStruktur FP-Tree:")
    root.display()

    print("\nHeader Table:")
    for item, info in sorted(header_table.items(), key=lambda x: x[1][0], reverse=True):
        print(f"  {item:12s}: count={info[0]:3d}, link=...", )

    # 5. Ekstraksi pola frekuen
    print("\n[Membangun Header Table Order] ...")
    header_items = [item for item in sorted(header_table.keys(),
                                             key=lambda x: header_table[x][0])]

    total_frequent_itemsets = {}
    extract_frequent_itemsets(header_table, header_items, min_support, [], total_frequent_itemsets)

    # Tambahkan frequent itemset individual
    for item, count in item_counts.items():
        if count >= min_support:
            key = (item,)
            if key not in total_frequent_itemsets:
                total_frequent_itemsets[key] = count

    # 6. Tampilkan hasil
    print("\n" + "=" * 60)
    print("HASIL: Frequent Itemsets (min_support = {})".format(min_support))
    print("=" * 60)
    print(f"\nTotal frequent itemsets ditemukan: {len(total_frequent_itemsets)}")
    print()

    # Urutkan berdasarkan panjang itemset, lalu abjad
    sorted_results = sorted(total_frequent_itemsets.items(),
                            key=lambda x: (len(x[0]), x[0]))
    for itemset, count in sorted_results:
        support_percent = count / len(transactions) * 100
        print(f"  {', '.join(itemset):30s} : count={count:3d}  ({support_percent:.1f}%)")

    print("\n" + "=" * 60)
    print("SELESAI")
    print("=" * 60)
    return total_frequent_itemsets


if __name__ == "__main__":
    DATA_FILE = "dataset_transaksi.csv"
    MIN_SUPPORT = 2

    results = run_fp_growth(DATA_FILE, MIN_SUPPORT, delimiter="csv")
