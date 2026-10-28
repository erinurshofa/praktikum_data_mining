# Praktikum Data Mining: Algoritma FP-Growth
## Petunjuk Lengkap

---

## 1. Gambaran Umum

Algoritma **FP-Growth (Frequent Pattern Growth)** adalah algoritma yang dikembangkan
oleh Han et al. (2001) untuk menemukan pola frekuen (frequent itemsets) tanpa harus
melakukan pemindaian database berulang kali seperti algoritma Apriori.

**Keuntungan utama FP-Growth:**
- Tidak perlu generasi kandidat (candidate generation)
- Hanya dua pemindaian database (2 database scans)
- Lebih efisien karena tidak menghasilkan kandidat yang tidak mungkin
- Strukturnya terpusat pada pohon FP-Tree yang kompresi data transaksi

---

## 2. Konsep Kunci

### 2.1 FP-Tree (Frequent Pattern Tree)

Pohon yang berisi informasi tentang pola frekuen. Setiap node mewakili satu item
dan memiliki:
- **Item name** (nama item)
- **Count** (jumlah dukungan / support count)
- **Node-link** (referensi ke node berikutnya dengan item yang sama)

### 2.2 Header Table

Tabel di puncak FP-Tree yang berisi:
- Nama item
- Support count (jumlah kemunculan)
- Node-link (pointer ke node pertama di pohon)

### 2.3 Konsep Conditionally

FP-Growth menggunakan pendekatan rekursif:
1. Bangun FP-Tree dari database transaksi
2. Untuk setiap item (dari yang paling tidak frequent), bangun **conditional pattern base**
3. Rekursi pada conditional pattern base untuk menemukan pola frekuen

---

## 3. Langkah-Langkah Algoritma FP-Growth

### Langkah 1: Pindai Database (Scan 1)

Hitung dukungan (support count) dari setiap item individu.

### Langkah 2: Filter Item Freq

Buang item dengan support count < min_support (pruning).

### Langkah 3: Urutkan Item

Urutkan item berdasarkan support count secara menurun (descending).

### Langkah 4: Bangun FP-Tree (Scan 2)

- Untuk setiap transaksi, urutkan itemnya sesuai urutan pada Langkah 3
- Masukkan ke dalam pohon, menggabungkan (merge) jalur yang sama

### Langkah 5: Bangun Header Table

- Header table berisi pointer ke node pertama untuk setiap item

### Langkah 6: Ekstrak Pola Frekuen

- Untuk setiap item (dari bawah ke atas dalam header table):
  - Bangun **conditional pattern base**
  - Bangun **conditional FP-Tree**
  - Rekursi hingga tidak ada lagi pola frekuen

---

## 4. Struktur Direktori

```
praktikum_fp_tree/
├── PETUNJUK.md                          # File ini
├── dataset_transaksi.csv                  # Dataset dalam format CSV (delimiter ;)
├── dataset_transaksi.txt                  # Dataset alternatif format spasi
├── fp_growth_lengkap.py                   # Program FP-Growth lengkap & berfungsi
├── error_1_insertion_sort.py              # Program dengan ERROR: algoritma insertion sort salah
├── error_2_header_table.py                # Program dengan ERROR: header table tidak terhubung dengan benar
├── error_3_conditional_pattern.py         # Program dengan ERROR: logika conditional pattern base salah
├── incomplete_1_construct_tree.py         # Program dengan BAGIAN KOSONG: konstruksi FP-Tree
├── incomplete_2_mining.py                 # Program dengan BAGIAN KOSONG: fase mining
├── incomplete_3_header_table.py           # Program dengan BAGIAN KOSONG: pembuatan header table
├── solusi_error_1.py                      # Kunci jawaban error 1
├── solusi_error_2.py                      # Kunci jawaban error 2
├── solusi_error_3.py                      # Kunci jawaban error 3
├── solusi_incomplete_1.py                 # Kunci jawaban incomplete 1
├── solusi_incomplete_2.py                 # Kunci jawaban incomplete 2
├── solusi_incomplete_3.py                 # Kunci jawaban incomplete 3
└── README.md                              # Ringkasan singkat
```

---

## 5. Cara Menjalankan Program

### 5.1 Program Lengkap (Referensi)

```bash
cd praktikum_fp_tree
python3 fp_growth_lengkap.py
```

Program ini akan:
1. Membaca dataset dari `dataset_transaksi.csv`
2. Membangun FP-Tree
3. Mengekstrak semua frequent itemsets
4. Menampilkan hasil di layar

### 5.2 Program Error (Latihan Perbaiki)

```bash
python3 error_1_insertion_sort.py   # Error: insertion sort
python3 error_2_header_table.py     # Error: header table
python3 error_3_conditional_pattern.py  # Error: conditional pattern
```

Setiap program akan crash dan menampilkan pesan error.
**Tugas Anda:** Temukan dan perbaiki error tersebut agar program berjalan
dan menampilkan hasil yang sama dengan `fp_growth_lengkap.py`.

### 5.3 Program Incomplete (Latihan Melengkapi)

```bash
python3 incomplete_1_construct_tree.py    # Bagian kosong: konstruksi pohon
python3 incomplete_2_mining.py            # Bagian kosong: fase mining
python3 incomplete_3_header_table.py      # Bagian kosong: header table
```

Setiap program memiliki bagian yang diganti dengan `# === YOUR CODE HERE ===`.
**Tugas Anda:** Lengkapi kode tersebut agar program berjalan dengan benar.

---

## 6. Dataset

### Format CSV (dataset_transaksi.csv)

Setiap baris merepresentasikan satu transaksi.
Kolom `TID` adalah ID transaksi, kolom `Barang` berisi item yang dibeli
dipisahkan dengan titik koma (`;`).

```
TID,Barang
T1,Rice;Apple;Pen;Bag
T2,Rice;Apple;Pen
...
```

### Format TXT (dataset_transaksi.txt)

Format alternatif, item dipisahkan dengan spasi. Setiap baris adalah satu transaksi.

```
Rice Apple Pen Bag
Rice Apple Pen
...
```

---

## 7. Teori Singkat (untuk Referensi)

### 7.1 FP-Tree Representation

Contoh transaksi:
```
T1: Rice, Apple, Pen, Bag     (sorted by support: Rice, Apple, Pen, Bag)
T2: Rice, Apple, Pen
T3: Rice, Apple, Bag, Blanket
```

FP-Tree yang terbentuk (dengan min_support = 2):

```
         root
       /   |   \
     Rice  ...   ...
       |
     Apple
    /  |
   Pen  Bag
   /    / \
  Bag  Blanket
```

### 7.2 Conditional Pattern Base

Untuk item "Bag", conditional pattern base adalah:
```
Rice Apple Pen : 1
Rice Apple     : 1
Rice Pen        : 1
Rice            : 1
```

Dari conditional pattern base ini, kita bangun conditional FP-Tree dan
lanjutkan untuk menemukan pola frekuen yang mengandung "Bag".

### 7.3 Rekursi

Proses ini berlanjut secara rekursif untuk setiap item hingga tidak ada
lagi item yang memenuhi min_support.

---

## 8. Kuis / Tugas

Setelah menyelesaikan semua latihan, jawab pertanyaan berikut:

1. Apa perbedaan utama antara Apriori dan FP-Growth?
2. Apa keuntungan memakai FP-Tree dibanding pemindaian database berulang?
3. Urutkan langkah-langkah FP-Growth dari yang paling penting.
4. Pada dataset ini, berapa frequent itemsets dengan min_support = 2?

---

## 9. Referensi

- Han, J., Pei, J., & Kamber, M. (2012). *Data Mining: Concepts and Techniques* (3rd ed.). Morgan Kaufmann.
- Han, J., Pei, J., & Yang, Y. (2001). "Mining Frequent Pattern without Candidate Generation." *Proceedings of the 2001 ACM SIGMOD International Conference on Management of Data (SIGMOD)*, 41-52.

---

*Copyright: Program Studi Teknik Informatika, Universitas Sriwijaya*
*Modul Praktikum Data Mining - 2026*
