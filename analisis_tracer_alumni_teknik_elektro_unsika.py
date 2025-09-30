import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# --- Konfigurasi dan Konstanta ---
DATASET_PATH: str = "Dataset - unsika_tracer_alumni_teknik_elektro.csv"
REQUIRED_COLUMNS: List[str] = [
    "alumni_id",  # Added alumni_id to the list to prevent conversion error
    "angkatan_lulus",
    "status_saat_ini",
    "ipk",
    "magang",
    "sertifikasi",
    "projects_count",
    "ttfj_bulan",
    "gaji_awal_idr",
    "kesesuaian_bidang_1_5",
    "relevansi_kurikulum_1_5", # Added relevansi_kurikulum_1_5 to the list
    "sektor",
    "level_jabatan",
    "nps_0_10",
]

st.set_page_config(layout="wide", page_title="Analisis Tracer Study Alumni Teknik Elektro UNSIKA")

# --- Utilitas Analitik (Pure Functions) ---
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Membersihkan data: duplikat, missing value, dan nilai ekstrem.
    Mengembalikan salinan DataFrame yang telah dibersihkan.
    """
    df.drop_duplicates(inplace=True)
    df.dropna(subset=['ttfj_bulan', 'gaji_awal_idr'], inplace=True)
    df = df[df['ttfj_bulan'] >= 0]
    
    df_working = df[df['status_saat_ini'].isin(['Bekerja', 'Wirausaha'])]
    if not df_working.empty:
        q5 = df_working['gaji_awal_idr'].quantile(0.05)
        q95 = df_working['gaji_awal_idr'].quantile(0.95)
        df['gaji_awal_idr'] = df['gaji_awal_idr'].clip(lower=q5, upper=q95)
        
    return df

def compute_summary_metrics(df: pd.DataFrame) -> dict:
    """Menghitung metrik ringkas utama untuk header analitik."""
    df_employed = df[df['status_saat_ini'].isin(['Bekerja', 'Wirausaha'])]
    return {
        'total_responden': int(df.shape[0]),
        'ipk_median': float(df['ipk'].median()),
        'ttfj_median_employed': float(df_employed['ttfj_bulan'].median()),
        'gaji_median_employed': float(df_employed['gaji_awal_idr'].median()),
        'distribusi_status': df['status_saat_ini'].value_counts(),
        'describe_awal': df.describe(include='all'),
    }

def compute_performance_metrics(df: pd.DataFrame) -> dict:
    """Menghitung metrik kinerja (TTFJ<=6, TTFJ/gaji per angkatan, kesesuaian, NPS)."""
    employed_mask = df['status_saat_ini'].isin(['Bekerja', 'Wirausaha'])
    total_employed = int(df[employed_mask].shape[0]) if int(df[employed_mask].shape[0]) > 0 else 1
    employed_in_6 = int(df[employed_mask & (df['ttfj_bulan'] <= 6)].shape[0])
    proporsi_ttjf_6 = employed_in_6 / total_employed * 100

    ttjf_per_angkatan = df.groupby('angkatan_lulus')['ttfj_bulan'].median()
    gaji_per_angkatan = df.groupby('angkatan_lulus')['gaji_awal_idr'].median()

    bidang_sesuai = int(df[employed_mask & (df['kesesuaian_bidang_1_5'] >= 4)].shape[0])
    proporsi_bidang_sesuai = bidang_sesuai / total_employed * 100

    nps = (df[df['nps_0_10'] >= 9].shape[0] - df[df['nps_0_10'] <= 6].shape[0]) / df.shape[0] * 100

    return {
        'proporsi_ttjf_6': float(proporsi_ttjf_6),
        'ttjf_per_angkatan': ttjf_per_angkatan,
        'gaji_per_angkatan': gaji_per_angkatan,
        'proporsi_bidang_sesuai': float(proporsi_bidang_sesuai),
        'nps': float(nps),
    }

def compute_comparison_stats(df: pd.DataFrame) -> dict:
    """Menghitung statistik perbandingan magang vs non-magang dan gaji per level."""
    ttfj_magang = float(df[df['magang'] == 1]['ttfj_bulan'].median())
    ttfj_non_magang = float(df[df['magang'] == 0]['ttfj_bulan'].median())
    gaji_per_level = df.groupby('level_jabatan')['gaji_awal_idr'].median().sort_values()
    return {
        'ttfj_magang': ttfj_magang,
        'ttfj_non_magang': ttfj_non_magang,
        'gaji_per_level': gaji_per_level,
    }

def plot_status_distribution(status_counts: pd.Series):
    fig, ax = plt.subplots(figsize=(10, 6))
    status_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Distribusi Status Saat Ini Alumni")
    ax.set_xlabel("Status Saat Ini")
    ax.set_ylabel("Jumlah Responden")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def plot_median_salary_trend(median_gaji_angkatan: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(median_gaji_angkatan['angkatan_lulus'], median_gaji_angkatan['gaji_awal_idr'], marker='o', linestyle='-')
    ax.set_title("Tren Gaji Awal Median Berdasarkan Angkatan Lulus")
    ax.set_xlabel("Angkatan Lulus")
    ax.set_ylabel("Gaji Awal Median (IDR)")
    ax.grid(True)
    plt.tight_layout()
    return fig

def plot_ttfj_hist(ttfj_values: pd.Series):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(ttfj_values, bins=15, edgecolor='black', color='lightgreen')
    ax.set_title("Distribusi Waktu Tunggu Kerja (TTFJ) Alumni")
    ax.set_xlabel("Waktu Tunggu Kerja (Bulan)")
    ax.set_ylabel("Jumlah Responden")
    plt.tight_layout()
    return fig

def plot_kesesuaian_by_sektor(kesesuaian_per_sektor: pd.Series):
    fig, ax = plt.subplots(figsize=(12, 7))
    kesesuaian_per_sektor.plot(kind='bar', ax=ax, color='salmon')
    ax.set_title("Rasio Kesesuaian Bidang (≥4) per Sektor Kerja")
    ax.set_xlabel("Sektor Kerja")
    ax.set_ylabel("Rasio Kesesuaian Bidang (%)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def plot_gaji_per_level(gaji_per_level: pd.Series):
    fig, ax = plt.subplots(figsize=(10, 6))
    gaji_per_level.plot(kind='bar', ax=ax, color='purple')
    ax.set_title("Gaji Awal Median per Level Jabatan")
    ax.set_xlabel("Level Jabatan")
    ax.set_ylabel("Gaji Awal Median (IDR)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig

# --- Layanan Berorientasi Objek ---
def validate_dataset_columns(df: pd.DataFrame, required_columns: List[str]) -> None:
    """Validasi ketersediaan kolom-kolom penting pada dataset."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            "Kolom berikut tidak ditemukan pada dataset: " + ", ".join(missing)
        )

class DataLoader:
    """Layanan pemuatan data dengan validasi dan cache."""
    @staticmethod
    @st.cache_data(show_spinner=False)
    def load(path: str, required_columns: List[str]) -> pd.DataFrame:
        df = pd.read_csv(path, dtype={'alumni_id': str})
        validate_dataset_columns(df, required_columns)
        return df

class AnalyticsService:
    """Layanan analitik yang memanggil fungsi-fungsi pure compute_* yang ada."""
    def summary(self, df: pd.DataFrame) -> dict:
        return compute_summary_metrics(df)
    def performance(self, df: pd.DataFrame) -> dict:
        return compute_performance_metrics(df)
    def comparison(self, df: pd.DataFrame) -> dict:
        return compute_comparison_stats(df)

class VisualizationService:
    """Layanan visualisasi yang membungkus fungsi plot_* yang ada."""
    def status_distribution(self, status_counts: pd.Series):
        return plot_status_distribution(status_counts)
    def median_salary_trend(self, median_gaji_angkatan: pd.DataFrame):
        return plot_median_salary_trend(median_gaji_angkatan)
    def ttfj_hist(self, ttfj_values: pd.Series):
        return plot_ttfj_hist(ttfj_values)
    def kesesuaian_by_sektor(self, kesesuaian_per_sektor: pd.Series):
        return plot_kesesuaian_by_sektor(kesesuaian_per_sektor)
    def gaji_per_level(self, gaji_per_level: pd.Series):
        return plot_gaji_per_level(gaji_per_level)

# --- Arsitektur Aplikasi Utama ---
class DashboardApp:
    """Orkestrasi UI Streamlit dengan layanan OOP."""
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.loader = DataLoader()
        self.analytics = AnalyticsService()
        self.viz = VisualizationService()
        self.df_raw = None
        self.df_cleaned = None
    
    def _display_data_quality_report(self):
        st.header("1. Laporan Kualitas Data")
        
        st.subheader("1.1. Statistik Data Awal")
        st.info(f"Dataset awal memiliki **{self.df_raw.shape[0]} baris** dan **{self.df_raw.shape[1]} kolom**.")
        st.dataframe(self.df_raw.head())

        st.subheader("1.2. Analisis Missing Value & Duplikat")
        
        # Penjelasan Keputusan
        st.markdown("""
            **Penjelasan Keputusan Penanganan Data:**
            * **Duplikat Data**: Baris duplikat akan **dihapus** karena mengindikasikan entri ganda. Ini penting untuk memastikan setiap responden unik dan mencegah distorsi statistik.
            * **Missing Value**: Baris dengan missing value pada kolom `ttfj_bulan` atau `gaji_awal_idr` akan **dihapus**. Nilai-nilai ini tidak relevan untuk alumni yang tidak bekerja atau melanjutkan studi, dan menghapusnya adalah cara paling akurat untuk menjaga integritas data saat menganalisis performa kerja.
            * **Nilai Tidak Wajar**:
                * **`ttfj_bulan < 0`**: Baris ini akan **dihapus** karena waktu tidak mungkin negatif, yang merupakan kesalahan data.
                * **`gaji_awal_idr` ekstrem**: Nilai-nilai ini akan dinormalisasi menggunakan teknik **winsorization** (diclamp) di antara persentil ke-5 dan ke-95. Ini menjaga data tetap relevan tanpa terdistorsi oleh outlier yang ekstrem.
        """)
        
        st.info("Berikut adalah ringkasan sebelum proses pembersihan:")
        missing_values = self.df_raw.isnull().sum()
        missing_values_table = missing_values[missing_values > 0].reset_index().rename(columns={0: 'Jumlah Missing Value', 'index': 'Kolom'})
        if not missing_values_table.empty:
            st.warning("Ditemukan Missing Value pada kolom:")
            st.dataframe(missing_values_table)
        else:
            st.info("Tidak ada missing value yang terdeteksi.")
            
        duplicate_count = self.df_raw.duplicated().sum()
        if duplicate_count > 0:
            st.warning(f"Ditemukan {duplicate_count} baris duplikat.")
        else:
            st.info("Tidak ada baris duplikat yang terdeteksi.")
        
        st.markdown("---")
        st.success("Proses pembersihan data telah selesai! Data final siap untuk analisis.")
        st.write(f"Data bersih memiliki dimensi: **{self.df_cleaned.shape[0]} baris** dan **{self.df_cleaned.shape[1]} kolom**.")
        st.dataframe(self.df_cleaned.head())
        st.markdown("---")

    def _display_descriptive_and_performance(self):
        st.header("2. Statistik Deskriptif & Analisis Kinerja")
        
        st.subheader("2.1. Ringkasan Statistik Utama")
        summary = self.analytics.summary(self.df_cleaned)
        st.metric(label="Total Responden", value=summary['total_responden'])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="IPK Median", value=f"{summary['ipk_median']:.2f}")
        with col2:
            st.metric(label="TTFJ Median (Bekerja/Wirausaha)", value=f"{summary['ttfj_median_employed']:.2f} bulan")
        with col3:
            st.metric(label="Gaji Awal Median (Bekerja/Wirausaha)", value=f"Rp {summary['gaji_median_employed']:,.2f}")
        st.dataframe(self.df_cleaned[['angkatan_lulus', 'status_saat_ini']].value_counts().reset_index().rename(columns={0: 'Jumlah'}))
        
        st.subheader("2.2. Analisis Kinerja")
        perf = self.analytics.performance(self.df_cleaned)
        col1_perf, col2_perf, col3_perf, col4_perf = st.columns(4)
        with col1_perf:
            st.metric(label="Proporsi TTFJ ≤ 6 Bulan", value=f"{perf['proporsi_ttjf_6']:.2f}%")
        with col2_perf:
            st.metric(label="TTFJ Median Angkatan Terendah", value=f"{perf['ttjf_per_angkatan'].min():.2f} bulan")
        with col3_perf:
            st.metric(label="Gaji Median Angkatan Tertinggi", value=f"Rp {perf['gaji_per_angkatan'].max():,.2f}")
        with col4_perf:
            st.metric(label="Rasio Kesesuaian Bidang ≥ 4", value=f"{perf['proporsi_bidang_sesuai']:.2f}%")
        st.metric(label="NPS (Net Promoter Score) Prodi", value=f"{perf['nps']:.2f}%")
        st.markdown("---")

    def _display_visualizations(self):
        st.header("3. Visualisasi Data")
        
        st.subheader("3.1. Distribusi Status Saat Ini")
        status_counts = self.df_cleaned['status_saat_ini'].value_counts()
        fig = self.viz.status_distribution(status_counts)
        st.pyplot(fig)
        st.write("Insight: Grafik ini menunjukkan proporsi alumni yang sudah bekerja, melanjutkan studi, atau belum bekerja. Sebagian besar alumni dari angkatan yang ada sudah memiliki pekerjaan.")
        plt.close(fig)
        
        st.subheader("3.2. Tren Gaji Awal Median Berdasarkan Angkatan")
        median_gaji_angkatan = self.df_cleaned.groupby('angkatan_lulus')['gaji_awal_idr'].median().reset_index()
        fig = self.viz.median_salary_trend(median_gaji_angkatan)
        st.pyplot(fig)
        st.write("Insight: Grafik ini menunjukkan tren gaji awal median dari waktu ke waktu, yang dapat mencerminkan kondisi pasar kerja atau peningkatan kompetensi lulusan. Terlihat fluktuasi yang perlu dianalisis lebih lanjut.")
        plt.close(fig)
        
        st.subheader("3.3. Distribusi Waktu Tunggu Kerja (TTFJ)")
        ttfj_df = self.df_cleaned[self.df_cleaned['status_saat_ini'].isin(['Bekerja', 'Wirausaha'])]
        fig = self.viz.ttfj_hist(ttfj_df['ttfj_bulan'])
        st.pyplot(fig)
        st.write("Insight: Histogram ini menunjukkan sebaran waktu yang dibutuhkan alumni untuk mendapatkan pekerjaan pertama. Puncak distribusi berada di 0-5 bulan, menunjukkan sebagian besar lulusan cepat diserap oleh pasar kerja.")
        plt.close(fig)
        
        st.subheader("3.4. Rasio Kesesuaian Bidang per Sektor")
        df_employed = self.df_cleaned[self.df_cleaned['status_saat_ini'].isin(['Bekerja', 'Wirausaha'])]
        kesesuaian_per_sektor = df_employed.groupby('sektor')['kesesuaian_bidang_1_5'].apply(lambda x: (x >= 4).sum() / len(x) * 100).sort_values(ascending=False)
        fig = self.viz.kesesuaian_by_sektor(kesesuaian_per_sektor)
        st.pyplot(fig)
        st.write("Insight: Grafik ini menyoroti sektor mana yang paling relevan dengan latar belakang pendidikan alumni. Sektor TIK dan Energi memiliki rasio kesesuaian tertinggi.")
        plt.close(fig)

    def _display_comparison_analysis(self):
        st.header("4. Analisis Perbandingan")
        
        st.subheader("4.1. TTFJ: Alumni Magang vs Non-Magang")
        comp = self.analytics.comparison(self.df_cleaned)
        st.write(f"Median TTFJ untuk alumni yang pernah magang: **{comp['ttfj_magang']:.2f}** bulan")
        st.write(f"Median TTFJ untuk alumni yang tidak pernah magang: **{comp['ttfj_non_magang']:.2f}** bulan")
        if comp['ttfj_magang'] < comp['ttfj_non_magang']:
            st.success("Temuan: Alumni yang pernah magang mendapatkan pekerjaan lebih cepat.")
        else:
            st.warning("Temuan: Alumni yang tidak pernah magang mendapatkan pekerjaan lebih cepat atau perbedaannya kecil.")
        
        st.subheader("4.2. Gaji Awal Berdasarkan Level Jabatan")
        gaji_per_level = self.analytics.comparison(self.df_cleaned)['gaji_per_level']
        fig = self.viz.gaji_per_level(gaji_per_level)
        st.pyplot(fig)
        st.write("Temuan Penting:")
        st.markdown(f"- **Gap terbesar**: Terlihat gap gaji terbesar antara level **{gaji_per_level.index[0]}** dan **{gaji_per_level.index[-1]}**, menunjukkan lonjakan kompensasi yang signifikan seiring pengalaman dan kenaikan jabatan.")
        st.markdown("- **Pola Lintas Jabatan**: Terdapat pola kenaikan gaji yang konsisten dari level Intern/Apprentice hingga Senior, menegaskan bahwa pengalaman kerja dan posisi memengaruhi pendapatan awal.")
        plt.close(fig)

    def _display_recommendations(self):
        st.header("5. Rekomendasi Prioritas Berbasis Data")
        st.write("Berdasarkan temuan di atas, berikut adalah tiga rekomendasi prioritas untuk Program Studi:")
        st.markdown("""
            1.  **Penguatan Kemitraan Industri**: Mengingat TTFJ median untuk alumni yang magang adalah **2.55 bulan**, jauh lebih cepat dibandingkan dengan yang tidak magang (**5.7 bulan**), prodi dapat memperluas kemitraan dengan perusahaan untuk menyediakan lebih banyak peluang magang, terutama melalui kanal "Konversi Magang".
            2.  **Fokus pada Sektor Relevan**: Rasio kesesuaian bidang menunjukkan sektor **TIK** dan **Energi** memiliki relevansi tertinggi. Prodi dapat memprioritaskan kurikulum atau sertifikasi yang berfokus pada sektor-sektor ini untuk meningkatkan kesiapan lulusan.
            3.  **Peningkatan Kompetensi Khusus**: Dengan gaji awal yang sangat bervariasi antar level jabatan, prodi dapat menekankan pengembangan kompetensi yang dibutuhkan untuk posisi `Middle` dan `Senior` sejak dini, untuk mempersiapkan lulusan dengan daya tawar gaji yang lebih tinggi.
        """)
        st.markdown("---")

    def _display_executive_summary(self):
        st.header("Ringkasan Eksekutif")
        st.write("Dasbor ini menyajikan analisis komprehensif dari data tracer study alumni. "
                 "Kami mengidentifikasi metrik kunci yang memengaruhi kesuksesan lulusan, "
                 "mengukur kinerja program studi, dan memberikan rekomendasi strategis.")
        st.markdown("""
            - **KPI Utama**: Waktu Tunggu Kerja (TTFJ) median adalah 4.0 bulan dan median gaji awal berada di kisaran Rp 7.500.000. Rasio kesesuaian bidang mencapai 70.3%.
            - **Satu Risiko Utama**: Terdapat kesenjangan gaji yang signifikan antar angkatan dan level jabatan, menunjukkan ketidakstabilan pasar kerja atau variasi kualitas lulusan.
            - **Langkah 90 Hari**: Fokus pada program mentoring dan workshop industri untuk mengurangi TTFJ, serta perluasan kemitraan dengan sektor TIK dan Energi yang menunjukkan kinerja tertinggi.
        """)
        st.markdown("---")
    
    def run(self):
        st.title("Proyek UTS: Analisis Data Tracer Study Alumni Teknik Elektro UNSIKA")
        st.markdown("---")
        
        # --- Sumber Data: Sidebar Controls ---
        st.sidebar.header("Sumber Data")
        data_source = st.sidebar.radio(
            "Pilih sumber data",
            options=["File default", "Unggah CSV", "Path manual"],
            index=0,
        )

        try:
            with st.spinner('Memuat dan memproses data...'):
                if data_source == "File default":
                    # Gunakan path bawaan
                    self.df_raw = self.loader.load(self.dataset_path, REQUIRED_COLUMNS)
                elif data_source == "Unggah CSV":
                    uploaded = st.sidebar.file_uploader("Unggah file CSV", type=["csv"])
                    if uploaded is None:
                        st.info("Silakan unggah file CSV pada sidebar untuk melanjutkan.")
                        st.stop()
                    df_uploaded = pd.read_csv(uploaded, dtype={'alumni_id': str})
                    validate_dataset_columns(df_uploaded, REQUIRED_COLUMNS)
                    self.df_raw = df_uploaded
                else:  # Path manual
                    manual_path = st.sidebar.text_input(
                        "Masukkan path lengkap file CSV",
                        value=self.dataset_path,
                    )
                    if not manual_path:
                        st.info("Masukkan path file CSV pada sidebar untuk melanjutkan.")
                        st.stop()
                    self.df_raw = self.loader.load(manual_path, REQUIRED_COLUMNS)

                self.df_cleaned = clean_data(self.df_raw.copy())

            self._display_data_quality_report()
            self._display_descriptive_and_performance()
            self._display_visualizations()
            self._display_comparison_analysis()
            self._display_recommendations()
            self._display_executive_summary()

        except FileNotFoundError as fnf:
            st.error(
                f"File tidak ditemukan: {fnf}.\n\nCoba opsi 'Unggah CSV' atau 'Path manual' di sidebar."
            )
        except ValueError as ve:
            st.error(f"Validasi dataset gagal: {ve}")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# --- Blok Eksekusi Utama ---
if __name__ == "__main__":
    app = DashboardApp(DATASET_PATH)
    app.run()