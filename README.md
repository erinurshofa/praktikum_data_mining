# Praktikum Data Mining: Algoritma FP-Growth

**Program Studi Teknik Informatika**
**Universitas Sriwijaya**
**Modul Praktikum Data Mining - 2026**

---

## Deskripsi

Modul praktikum ini mengajarkan algoritma **FP-Growth (Frequent Pattern Growth)**
untuk menemukan pola frekuen (frequent itemsets) dari data transaksional.
FP-Growth lebih efisien dibanding Apriori karena tidak melakukan generate
kandidat dan hanya memindai database dua kali.

Baca file **PETUNJUK.md** terlebih dahulu untuk panduan lengkap.

---

## Struktur File

| File                          | Deskripsi                              |
|-------------------------------|----------------------------------------|
| `PETUNJUK.md`                 | Panduan lengkap (baca ini dulu)        |
| `dataset_transaksi.csv`       | Dataset transaksi format CSV           |
| `dataset_transaksi.txt`       | Dataset transaksi format TXT           |
| `fp_growth_lengkap.py`        | Program referensi (complete & working) |
| `error_1_insertion_sort.py`   | Latihan perbaiki: insertion sort       |
| `error_2_header_table.py`     | Latihan perbaiki: header table         |
| `error_3_conditional_pattern.py` | Latihan perbaiki: conditional pattern |
| `incomplete_1_construct_tree.py` | Latihan lengkapi: konstruksi pohon    |
| `incomplete_2_mining.py`      | Latihan lengkapi: fase mining          |
| `incomplete_3_header_table.py`| Latihan lengkapi: header table         |
| `solusi_error_1.py`           | Kunci jawaban error 1                  |
| `solusi_error_2.py`           | Kunci jawaban error 2                  |
| `solusi_error_3.py`           | Kunci jawaban error 3                  |
| `solusi_incomplete_1.py`      | Kunci jawaban incomplete 1             |
| `solusi_incomplete_2.py`      | Kunci jawaban incomplete 2             |
| `solusi_incomplete_3.py`      | Kunci jawaban incomplete 3             |

---

## Cara Menggunakan

### 1. Referensi: Program Lengkap

```bash
python3 fp_growth_lengkap.py
```

Program ini menampilkan langkah demi langkah:
1. Perhitungan frekuensi item (Scan 1)
2. Filtering & sorting transaksi
3. Struktur FP-Tree yang terbentuk
4. Header table
5. Frequent itemsets yang diekstrak (42 itemsets untuk min_support=2)

### 2. Latihan Perbaiki (Error)

Jalankan program error, baca pesan error, lalu perbaiki:

```bash
python3 error_1_insertion_sort.py   # Sort descending salah
python3 error_2_header_table.py     # Header table key tidak konsisten
python3 error_3_conditional_pattern.py  # Conditional pattern base error
```

Setelah memperbaiki, bandingkan hasil dengan solusi:

```bash
python3 solusi_error_1.py
python3 solusi_error_2.py
python3 solusi_error_3.py
```

### 3. Latihan Lengkapi (Incomplete)

Program incomplete memiliki bagian `# === YOUR CODE HERE ===` yang harus
diisi oleh mahasiswa:

```bash
python3 incomplete_1_construct_tree.py   # Konstruksi FP-Tree
python3 incomplete_2_mining.py            # Fase mining
python3 incomplete_3_header_table.py      # Header table
```

Setelah melengkapi, bandingkan dengan solusi:

```bash
python3 solusi_incomplete_1.py
python3 solusi_incomplete_2.py
python3 solusi_incomplete_3.py
```

---

## Dataset

Dataset berisi 15 transaksi dengan 9 item unik (Rice, Coffee, Apple, Pen,
Bag, Blanket, Bread, Milk, Sugar). Semua item memenuhi min_support=2.

Dataset ini sengaja dirancang untuk latihan:
- Kelompok Rice/Apple/Pen/Bag muncul 6-8 kali (frequent)
- Kelompok Coffee/Bread/Milk/Sugar muncul 4-7 kali (frequent)
- Memungkinkan testing conditional pattern base yang kompleks

---

## Hasil yang Diharapkan (min_support = 2)

Berdasarkan `fp_growth_lengkap.py`, program harus menemukan **42 frequent
itemsets**:
- 9 item individual
- 18 itemsets berukuran 2
- 12 itemsets berukuran 3
- 3 itemsets berukaran 4 (termasuk Rice-Apple-Pen-Bag)

---

## Troubleshooting

Jika program error, pastikan:
1. Python 3.10+ terpasang (`python3 --version`)
2. File dataset berada di direktori yang sama
3. Jalankan dari dalam direktori `praktikum_fp_tree/`

---

*Copyright: Program Studi Teknik Informatika, Universitas Sriwijaya*
