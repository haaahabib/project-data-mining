# Prediksi Keterlambatan Penerbangan

Dashboard ini dibangun untuk memprediksi kemungkinan keterlambatan penerbangan dan estimasi durasi keterlambatan menggunakan model Machine Learning. Proyek ini meliputi tahap analisis data (EDA), rekayasa fitur (feature engineering), pelatihan model klasifikasi dan regresi, serta pembangunan aplikasi web interaktif menggunakan Streamlit.

## Daftar Isi

1.  [Pendahuluan](#1-pendahuluan)
2.  [Struktur Proyek](#2-struktur-proyek)
3.  [Instalasi](#3-instalasi)
4.  [Cara Menjalankan Aplikasi](#4-cara-menjalankan-aplikasi)
5.  [Model dan Hasil](#5-model-dan-hasil)
    * [Klasifikasi Keterlambatan](#klasifikasi-keterlambatan)
    * [Regresi Durasi Keterlambatan](#regresi-durasi-keterlambatan)
6.  [Fitur-Fitur Dashboard](#6-fitur-fitur-dashboard)

## 1. Pendahuluan

Proyek ini bertujuan untuk membantu memprediksi apakah suatu penerbangan akan mengalami keterlambatan atau tidak, serta berapa lama durasi keterlambatan yang mungkin terjadi. Prediksi ini didasarkan pada berbagai fitur penerbangan seperti maskapai, asal, tujuan, nomor penerbangan, jarak, dan waktu keberangkatan yang dijadwalkan.

## 2. Struktur Proyek

Berikut adalah struktur utama file dan folder dalam proyek ini:

- `app.py`: Aplikasi Streamlit untuk dashboard.
- `requirements.txt`: Daftar semua pustaka/library Python yang diperlukan untuk menjalankan proyek.
- `flight_delays.csv`: Dataset yang digunakan untuk pelatihan model dan visualisasi di dashboard.
- `model_xgb.zip`: Berkas zip yang berisi model Machine Learning yang telah dilatih. Setelah diekstrak, akan terdapat:
  - `xgb_flight_model.pkl`: Model XGBoost Classifier untuk prediksi klasifikasi keterlambatan.
  - `xgb_delay_regressor.pkl`: Model XGBoost Regressor untuk prediksi durasi keterlambatan.
- Folder `notebook/`: Berisi skrip dan notebook terkait pengembangan model.
  - `project_flight_delay.ipynb`: Notebook Jupyter yang berisi langkah-langkah EDA, pra-pemrosesan data, pelatihan model klasifikasi dan regresi, serta evaluasi model.
  - `project_flight_delay.py`: Skrip Python yang berisi fungsi-fungsi pembantu atau fungsi prediksi yang digunakan oleh `app.py`.

**Catatan**: Sebelum menjalankan aplikasi, pastikan Anda telah mengekstrak isi dari `model_xgb.zip` (yaitu `xgb_flight_model.pkl` dan `xgb_delay_regressor.pkl`) ke direktori yang dapat diakses oleh `app.py`. Biasanya, ini berarti menempatkannya di direktori yang sama dengan `app.py`.

## 3. Instalasi

Untuk menjalankan proyek ini, Anda perlu menginstal semua dependensi Python yang terdaftar dalam `requirements.txt`. Pastikan Anda memiliki Python 3.11.0 terinstal di sistem Anda.

1.  Buka terminal atau command prompt.
2.  Navigasi ke direktori akar proyek ini.
3.  Jalankan perintah berikut untuk menginstal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

## 4. Cara Menjalankan Aplikasi

Setelah semua dependensi terinstal dan model `.pkl` telah diekstrak dari `model_xgb.zip` ke lokasi yang benar, Anda dapat menjalankan aplikasi dashboard Streamlit:

1.  Buka terminal atau command prompt.
2.  Navigasi ke direktori `app.py` berada.
3.  Jalankan perintah berikut:

    ```bash
    python -m streamlit run app.py
    ```

Setelah perintah dijalankan, aplikasi akan secara otomatis terbuka di browser web default Anda pada alamat lokal.

## 5. Model dan Hasil

Proyek ini menggunakan dua model Machine Learning utama untuk prediksi keterlambatan penerbangan:

* **XGBoost Classifier**: Digunakan untuk mengklasifikasikan apakah suatu penerbangan akan mengalami keterlambatan (`DELAYED`) atau tidak (`ON-TIME`).
* **XGBoost Regressor**: Digunakan untuk memprediksi durasi keterlambatan dalam satuan menit, khusus untuk penerbangan yang diprediksi akan terlambat.

Detail pelatihan, evaluasi, dan metrik kinerja untuk kedua model ini didokumentasikan sepenuhnya dalam `notebook/project_flight_delay.ipynb`.

### Klasifikasi Keterlambatan

Model klasifikasi (XGBoost Classifier) dilatih untuk memprediksi probabilitas dan status akhir (DELAYED/ON-TIME) suatu penerbangan.

**Metrik Evaluasi Utama:**

* **Precision, Recall, F1-Score**: Metrik ini sangat penting untuk menilai kinerja model, terutama pada kelas minoritas ('DELAYED'), menunjukkan kemampuan model untuk mengidentifikasi keterlambatan secara akurat dan meminimalkan kesalahan identifikasi.
* **ROC AUC Score**: Mengukur kemampuan diskriminasi model dalam membedakan antara penerbangan on-time dan terlambat.
* **Confusion Matrix**: Memberikan gambaran rinci tentang True Positives, True Negatives, False Positives, dan False Negatives dari prediksi model.

### Regresi Durasi Keterlambatan

Model regresi (XGBoost Regressor) bertujuan untuk memperkirakan berapa lama keterlambatan yang akan terjadi jika penerbangan diprediksi terlambat.

**Metrik Evaluasi Utama:**

* **Mean Absolute Error (MAE)**: Menunjukkan rata-rata dari selisih absolut antara nilai durasi keterlambatan yang diprediksi dan nilai sebenarnya. Semakin rendah MAE, semakin akurat prediksi model.
* **Root Mean Squared Error (RMSE)**: Mengukur ukuran rata-rata kesalahan prediksi model. RMSE lebih sensitif terhadap outlier dibandingkan MAE.
* **R-squared (R2 Score)**: Menunjukkan proporsi varians dalam variabel target (durasi keterlambatan) yang dapat dijelaskan oleh model. Nilai R2 yang lebih tinggi menunjukkan kecocokan model yang lebih baik.

## 6. Fitur-Fitur Dashboard

Dashboard Streamlit (`app.py`) menyediakan antarmuka yang intuitif bagi pengguna untuk berinteraksi dengan model prediksi:

* **Input Data Penerbangan**: Pengguna dapat dengan mudah memasukkan berbagai parameter penerbangan seperti maskapai, bandara asal dan tujuan, alasan potensial keterlambatan (misalnya, Cuaca, Perawatan), nomor penerbangan, jarak penerbangan, dan waktu keberangkatan yang dijadwalkan.
* **Prediksi Instan**: Setelah data input diserahkan, dashboard akan secara instan menampilkan hasil prediksi. Ini termasuk:
    * **Status Penerbangan**: Menunjukkan apakah penerbangan diprediksi `ON-TIME` atau `DELAYED`.
    * **Probabilitas Keterlambatan**: Menampilkan probabilitas numerik (dalam persentase) bahwa penerbangan akan terlambat.
    * **Estimasi Waktu Keterlambatan**: Jika penerbangan diprediksi terlambat, estimasi durasi keterlambatan dalam menit akan ditampilkan.
* **Fleksibilitas Waktu**: Opsi untuk menggunakan waktu saat ini (WIB) sebagai waktu keberangkatan yang dijadwalkan, atau memilih waktu keberangkatan secara manual.
