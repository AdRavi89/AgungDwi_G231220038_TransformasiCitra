Sudah sangat bagus! Saya telah merapikan sedikit format Markdown-nya agar blok kodenya (syntax highlighting) muncul dengan benar di GitHub, memperbaiki struktur navigasi, dan melengkapi kalimat terakhir yang terpotong.

Berikut adalah versi **README.md** yang sudah dikoreksi dan dioptimalkan:

---

```markdown
# 🖼️ Computer Vision Pipeline: Geometric Transformation

Aplikasi web berbasis Python untuk melakukan pengolahan citra digital secara otomatis. Aplikasi ini mengambil 25 gambar dari **Unsplash API**, melakukan pre-processing ke **Grayscale**, dan menerapkan **7 jenis transformasi geometris** secara real-time.

## 🌐 Link Uji Coba
Aplikasi dapat diakses secara langsung melalui:
👉 [https://tugas2projectcv.streamlit.app/](https://tugas2projectcv.streamlit.app/)

---

## 🚀 Alur Kerja Aplikasi (Pipeline)

Aplikasi ini dirancang dengan alur kerja sekuensial (Step-by-Step) untuk memudahkan pengguna memahami proses pengolahan citra:

### 1. Tahap Input (Data Acquisition)
* **Deskripsi:** Pengguna memasukkan kata kunci dan API Key di sidebar.
* **Proses:** Aplikasi memanggil Unsplash API dan mengunduh 25 citra digital dalam format BGR.
* **Tampilan:** Gambar ditampilkan dalam grid 5x5 dengan keterangan nomor urut (Original 1-25).

### 2. Pre-processing (Grayscale Conversion)
* **Deskripsi:** Transformasi ruang warna dari RGB/BGR ke Grayscale.
* **Proses:** Menggunakan OpenCV `cv2.cvtColor` guna mereduksi dimensi data citra untuk efisiensi pemrosesan geometris.
* **Output:** Ditampilkan pada frame tersendiri untuk membedakan hasil pra-pemrosesan dengan data asli.

### 3. Output (Geometric Transformations)
Setiap fungsi menggunakan manipulasi matriks yang ditampilkan secara transparan kepada pengguna:

1. **Translasi:** Menggeser citra pada sumbu X sebesar 50px dan Y sebesar 30px.
2. **Rotasi:** Memutar citra sebesar 45° tepat pada titik pusat (center) citra.
3. **Scaling:** Mengubah dimensi citra menjadi lebih kecil (70% dari ukuran asli).
4. **Shearing:** Memberikan efek miring pada sumbu horizontal dengan faktor shear 0.2.
5. **Refleksi:** Pencerminan gambar secara horizontal (Flip sumbu Y).
6. **Affine:** Transformasi linier yang menjaga hubungan titik-titik sejajar menggunakan 3 titik acuan.
7. **Proyektif:** Mengubah sudut pandang perspektif (efek 3D) menggunakan 4 titik acuan koordinat.

---

## 🛠️ Teknologi yang Digunakan

| Library | Fungsi Utama |
| :--- | :--- |
| **Streamlit** | Framework antarmuka web dan manajemen state aplikasi. |
| **OpenCV (cv2)** | Library inti untuk algoritma pengolahan citra digital. |
| **NumPy** | Perhitungan matriks transformasi dan operasi array. |
| **Requests** | Handling HTTP request ke Unsplash API. |
| **Pillow (PIL)** | Konversi format byte gambar ke array yang didukung OpenCV. |

---

## 📂 Struktur File Proyek

```text
tugas2_project_cv/
├── app.py              # File utama aplikasi Streamlit
├── requirements.txt    # Daftar library (Gunakan opencv-python-headless untuk Cloud)
└── README.md           # Dokumentasi proyek
```

---

## 💻 Implementasi Kode: Transformasi Geometris

Bagian ini berada di **Step 3** di dalam sistem Tabs. Berikut adalah potongan kode spesifik untuk setiap transformasinya:

### 1. Translasi (Pergeseran)
```python
M = np.float32([[1, 0, 50], [0, 1, 30]]) # Matriks translasi
res = [cv2.warpAffine(img, M, (img.shape[1], img.shape[0])) for img in st.session_state.gray_images]
```

### 2. Rotasi (Perputaran)
```python
M = cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1) # Matriks rotasi 45 derajat
res = [cv2.warpAffine(img, M, (cols, rows)) for img in st.session_state.gray_images]
```

### 3. Scaling (Perubahan Ukuran)
```python
# fx dan fy = 0.7 berarti pengecilan ke 70%
res = [cv2.resize(img, None, fx=0.7, fy=0.7) for img in st.session_state.gray_images]
```

### 4. Shearing (Kemiringan)
```python
M = np.float32([[1, 0.2, 0], [0, 1, 0]]) # Matriks kemiringan sumbu X
res = [cv2.warpAffine(img, M, (int(img.shape[1]*1.2), img.shape[0])) for img in st.session_state.gray_images]
```

### 5. Refleksi (Pencerminan)
```python
# flipCode 1 = Horizontal
res = [cv2.flip(img, 1) for img in st.session_state.gray_images]
```

### 6. Transformasi Affine
```python
# Menghitung matriks dari 3 titik asal ke 3 titik tujuan
M = cv2.getAffineTransform(pts1, pts2)
res = [cv2.warpAffine(img, M, (img.shape[1], img.shape[0])) for img in st.session_state.gray_images]
```

### 7. Transformasi Proyektif (Perspektif)
```python
# Menggunakan warpPerspective untuk efek 3D/sudut pandang berbeda
M = cv2.getPerspectiveTransform(pts1, pts2)
res = [cv2.warpPerspective(img, M, (300, 300)) for img in st.session_state.gray_images]
```

> **Catatan:** Semua hasil transformasi di atas dikirim ke fungsi `render_transformation` untuk ditampilkan dalam grid 5x5 lengkap dengan matriks transformasinya sebagai detail teknis bagi pengguna.

---
**Dibuat untuk Tugas Project Computer Vision - 2026**
```