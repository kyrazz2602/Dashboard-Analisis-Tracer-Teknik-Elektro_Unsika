## 📊 Dashboard Analisis Tracer Alumni Teknik Elektro UNSIKA

Selamat datang! Repo ini berisi aplikasi dashboard interaktif berbasis Streamlit untuk menganalisis data tracer study alumni Teknik Elektro UNSIKA. Aplikasi menampilkan pembersihan data, statistik deskriptif, visualisasi, perbandingan, hingga rekomendasi berbasis data. ✨

- **Framework**: `Streamlit`
- **Data**: `Dataset - unsika_tracer_alumni_teknik_elektro.csv` (tidak di-commit; di-ignore oleh git)
- **Script utama**: `analisis_tracer_alumni_teknik_elektro_unsika.py`

---

### 🚀 Fitur Utama
- **Laporan Kualitas Data**: deteksi duplikat, missing value, dan normalisasi outlier.
- **Statistik Ringkas**: metrik kunci seperti median IPK, TTFJ, dan gaji awal.
- **Visualisasi**: distribusi status, tren gaji per angkatan, histogram TTFJ, rasio kesesuaian per sektor, gaji per level jabatan.
- **Analisis Perbandingan**: magang vs non-magang, dan gaji per level.
- **Ringkasan Eksekutif & Rekomendasi**: insight cepat untuk pengambil keputusan.

---

### 🗂️ Struktur Proyek
- `analisis_tracer_alumni_teknik_elektro_unsika.py` — aplikasi Streamlit utama
- `Dataset - unsika_tracer_alumni_teknik_elektro.csv` — dataset tracer alumni (hanya lokal)
- `requirements.txt` — dependensi Python
- `README.md` — dokumentasi proyek

---

### 📦 Instalasi & Menjalankan (Windows / PowerShell)
1. Pastikan Python 3.9+ terpasang. Cek versi:
```powershell
python --version
```
2. (Opsional) Buat dan aktifkan virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
3. Instal dependensi:
```powershell
pip install -r requirements.txt
```
4. Jalankan aplikasi Streamlit:
```powershell
streamlit run analisis_tracer_alumni_teknik_elektro_unsika.py
```
5. Aplikasi akan terbuka di browser (alamat biasanya `http://localhost:8501`). 🌐

---

### 🧰 Konfigurasi
- Lokasi dataset diatur melalui konstanta `DATASET_PATH` di dalam `analisis_tracer_alumni_teknik_elektro_unsika.py`.
- Pastikan file dataset `Dataset - unsika_tracer_alumni_teknik_elektro.csv` berada di folder yang sama dengan script.
- File CSV sudah dimasukkan ke `.gitignore`, sehingga tidak akan ter-push ke GitHub.

---

### 🔒 Privasi Data & .gitignore
- File dataset CSV berisi data sensitif dan telah ditambahkan ke `.gitignore` agar tidak diunggah ke repository publik.
- Untuk menjalankan aplikasi, letakkan file `Dataset - unsika_tracer_alumni_teknik_elektro.csv` di root folder proyek (sejajar dengan `analisis_tracer_alumni_teknik_elektro_unsika.py`).
- Jika file terlanjur ter-track, jalankan perintah berikut agar dihapus dari indeks git (tetap ada di disk):
```powershell
git rm --cached "Dataset - unsika_tracer_alumni_teknik_elektro.csv"
git add .gitignore
git commit -m "Ignore dataset CSV dari repository"
```

---

### 🧪 Validasi & Pembersihan Data (Ringkas)
Aplikasi melakukan:
- Penghapusan duplikat baris.
- Menghapus baris dengan missing value pada kolom kunci (`ttfj_bulan`, `gaji_awal_idr`).
- Menjaga nilai wajar dengan winsorization (persentil 5–95) pada `gaji_awal_idr` untuk responden bekerja/wirausaha.

---

### 📣 Lisensi
Gunakan untuk keperluan akademik/pembelajaran. Cantumkan atribusi bila disebarluaskan. 🙌

---

### 🙏 Kredit
Program Studi Teknik Elektro UNSIKA dan kontributor yang berpartisipasi dalam pengembangan dashboard ini. 💙

---

### ⬆️ Publikasi ke GitHub (Windows / PowerShell)
Ikuti langkah berikut untuk mem-publish proyek ini ke GitHub.

1) Buat repo kosong di GitHub
- Masuk ke GitHub dan buat repository baru (tanpa README/License agar tidak konflik).

2) Inisialisasi git di folder proyek
```powershell
cd "C:\Users\LENOVO\Downloads\Dashboard Analisis Tracer Alumni Teknik Elektro Unsika"
git init
```

3) Atur identitas git (sekali saja di mesin ini)
```powershell
git config --global user.name "Nama Anda"
git config --global user.email "email@anda.com"
```

4) Tambahkan remote ke repo GitHub Anda
Ganti URL di bawah dengan URL repo Anda (HTTPS disarankan):
```powershell
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
```

5) Tambahkan semua file dan commit
```powershell
git add .
git commit -m "Inisialisasi proyek: dashboard tracer alumni"
```

6) Ganti nama branch (opsional, jika repo GitHub default `main`)
```powershell
git branch -M main
```

7) Push ke GitHub
```powershell
git push -u origin main
```

8) Update berikutnya
```powershell
git add .
git commit -m "Perbarui fitur/README/dll"
git push
```

Tips:
- Pastikan `.gitignore` sudah benar agar file lokal (venv, cache) tidak ikut ter-push.
- Jika diminta login, gunakan GitHub credentials atau Personal Access Token.

## Dashboard Analisis Tracer Alumni Teknik Elektro UNSIKA

Dashboard interaktif berbasis Streamlit untuk menganalisis data tracer study alumni Program Studi Teknik Elektro UNSIKA. Proyek ini memuat, membersihkan, menganalisis, dan memvisualisasikan data, serta menyajikan ringkasan eksekutif dan rekomendasi berbasis data.

### Fitur Utama
- **Pemuatan & Validasi Data**: Membaca CSV dan memverifikasi kolom wajib.
- **Pembersihan Data**: Menghapus duplikat, menangani missing value pada `ttfj_bulan` dan `gaji_awal_idr`, menghapus nilai `ttfj_bulan < 0`, dan winsorization gaji pada persentil 5–95.
- **Statistik Deskriptif**: Ringkasan responden, IPK median, distribusi status, dan deskripsi data.
- **Metrik Kinerja**: Proporsi TTFJ ≤ 6 bulan, median TTFJ & gaji (bagi yang bekerja/wirausaha), kesesuaian bidang, serta NPS.
- **Visualisasi**: Distribusi status, tren median gaji per angkatan, histogram TTFJ, kesesuaian bidang per sektor, gaji per level jabatan.
- **Analisis Perbandingan**: TTFJ alumni magang vs non-magang; gaji per level jabatan.
- **Ringkasan Eksekutif & Rekomendasi**: Kesimpulan utama dan rekomendasi prioritas.

### Struktur Proyek
```
Dashboard Analisis Tracer Alumni Teknik Elektro Unsika/
├─ analisis_tracer_alumni_teknik_elektro_unsika.py
├─ Dataset - unsika_tracer_alumni_teknik_elektro.csv   # hanya lokal, gitignored
├─ requirements.txt
└─ README.md
```

### Dependensi
- Python 3.9+ (direkomendasikan)
- streamlit
- pandas
- numpy
- matplotlib

Instalasi paket (opsi cepat):
```bash
pip install streamlit pandas numpy matplotlib
```

### Menjalankan Aplikasi
Pastikan file dataset berada di root proyek dengan nama persis:
`Dataset - unsika_tracer_alumni_teknik_elektro.csv`

Jalankan skrip berikut dengan Streamlit:
```bash
streamlit run analisis_tracer_alumni_teknik_elektro_unsika.py
```

Secara default, aplikasi akan terbuka di `http://localhost:8501`.

### Cara Pakai (Singkat)
1. Buka aplikasi Streamlit.
2. Bagian 1: Tinjau kualitas data (missing value, duplikat) dan sampel data.
3. Bagian 2: Lihat metrik ringkasan dan kinerja (TTFJ, gaji, kesesuaian, NPS).
4. Bagian 3: Telusuri visualisasi untuk pola utama.
5. Bagian 4: Bandingkan TTFJ magang vs non-magang, serta gaji per level jabatan.
6. Bagian 5: Baca rekomendasi prioritas dan ringkasan eksekutif.

### Kolom Wajib Dataset
Skrip mengharapkan kolom berikut ada di CSV (lihat `REQUIRED_COLUMNS` dalam `analisis_tracer_alumni_teknik_elektro_unsika.py`):
- `alumni_id`
- `angkatan_lulus`
- `status_saat_ini` (contoh: Bekerja, Wirausaha, Studi Lanjut, Belum Bekerja)
- `ipk`
- `magang` (0/1)
- `sertifikasi` (0/1)
- `projects_count`
- `ttfj_bulan` (time-to-first-job, bulan)
- `gaji_awal_idr`
- `kesesuaian_bidang_1_5`
- `relevansi_kurikulum_1_5`
- `sektor`
- `level_jabatan`
- `nps_0_10`

Jika salah satu kolom tidak ada, aplikasi akan menampilkan error validasi.

### Penjelasan Pembersihan Data (Inti)
- Hapus baris duplikat.
- Hapus baris dengan missing pada `ttfj_bulan` atau `gaji_awal_idr`.
- Filter `ttfj_bulan >= 0`.
- Winsorization `gaji_awal_idr` untuk responden bekerja/wirausaha pada persentil 5–95 untuk mengurangi pengaruh outlier ekstrem.

### Troubleshooting (Windows/PowerShell)
- Perintah tidak dikenali: pastikan Python & pip sudah ada di PATH. Coba: `python --version` dan `pip --version`.
- Streamlit tidak terpasang: jalankan `pip install streamlit`.
- Konflik paket: gunakan environment terpisah.
  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install -U pip
  pip install streamlit pandas numpy matplotlib
  ```
- Port 8501 sudah terpakai: jalankan dengan port lain, contoh `streamlit run app.py --server.port 8502`.
- Perubahan kode tidak terlihat: bersihkan cache `streamlit cache clear` lalu jalankan ulang.

### Lisensi
Proyek ini untuk tujuan pembelajaran/akademik. Sesuaikan lisensi sesuai kebutuhan institusi Anda.

### Kredit
Disusun untuk analisis tracer study alumni Teknik Elektro UNSIKA.


