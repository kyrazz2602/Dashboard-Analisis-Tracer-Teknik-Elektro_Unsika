## 📊 Dashboard Analisis Tracer Alumni Teknik Elektro UNSIKA

Selamat datang! Repo ini berisi aplikasi dashboard interaktif berbasis Streamlit untuk menganalisis data tracer study alumni Teknik Elektro UNSIKA. Aplikasi menampilkan pembersihan data, statistik deskriptif, visualisasi, perbandingan, hingga rekomendasi berbasis data. ✨

- **Framework**: `Streamlit`
- **Data**: `Dataset - unsika_tracer_alumni_teknik_elektro.csv` 
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
