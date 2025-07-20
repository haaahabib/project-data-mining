# Prediksi Keterlambatan Penerbangan

Dashboard interaktif ini dibangun untuk memprediksi kemungkinan keterlambatan penerbangan serta memberikan estimasi durasi keterlambatan menggunakan model *Machine Learning*. Proyek ini mencakup analisis data eksplorasi (EDA), rekayasa fitur, pelatihan model, hingga implementasi dalam aplikasi web menggunakan Streamlit.

---

## Daftar Isi

1.  [Pendahuluan](#1-pendahuluan)
2.  [Struktur Proyek](#2-struktur-proyek)
3.  [Instalasi](#3-instalasi)
4.  [Cara Menjalankan Aplikasi](#4-cara-menjalankan-aplikasi)
5.  [Model dan Hasil](#5-model-dan-hasil)
    * [Klasifikasi Keterlambatan](#klasifikasi-keterlambatan)
    * [Regresi Durasi Keterlambatan](#regresi-durasi-keterlambatan)
6.  [Fitur-Fitur Dashboard](#6-fitur-fitur-dashboard)

---

## 1. Pendahuluan

Proyek ini dirancang untuk menjawab dua pertanyaan kunci dalam operasional penerbangan: **apakah sebuah penerbangan akan terlambat?** dan **jika ya, berapa lama estimasi keterlambatannya?** Dengan memanfaatkan data historis seperti maskapai, rute, dan waktu keberangkatan, model ini bertujuan untuk memberikan prediksi yang dapat membantu pengambilan keputusan.

---

## 2. Struktur Proyek

Berikut adalah struktur utama file dan folder dalam proyek ini:

| Nama File/Folder              | Deskripsi                                                                 |
| :---------------------------- | :------------------------------------------------------------------------ |
| **`app.py`** | Skrip utama aplikasi dashboard Streamlit.                                 |
| **`requirements.txt`** | Daftar semua *library* Python yang dibutuhkan proyek.                     |
| **`flight_delays.csv`** | Dataset yang digunakan untuk pelatihan dan analisis.                      |
| **`model_xgb.zip`** | Berkas terkompresi berisi model yang telah dilatih.                       |
| ↳ `xgb_flight_model.pkl`      | Model **XGBoost Classifier** untuk prediksi status keterlambatan.         |
| ↳ `xgb_delay_regressor.pkl`   | Model **XGBoost Regressor** untuk prediksi durasi keterlambatan.          |
| **`notebook/`** | Folder berisi *notebook* untuk pengembangan model.                        |
| ↳ `project_flight_delay.ipynb`| Notebook Jupyter berisi EDA, pra-pemrosesan, dan pelatihan model.         |
| ↳ `project_flight_delay.py`   | Skrip Python berisi fungsi pembantu untuk aplikasi.                       |

**Catatan Penting**: Sebelum menjalankan aplikasi, pastikan Anda telah mengekstrak `model_xgb.zip` sehingga file `.pkl` berada di direktori yang sama dengan `app.py`.

---

## 3. Instalasi

Untuk menyiapkan lingkungan proyek, pastikan Anda memiliki **Python 3.11.0**.

1.  Buka terminal dan navigasi ke direktori utama proyek.
2.  Jalankan perintah berikut untuk menginstal semua *library* yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

---

## 4. Cara Menjalankan Aplikasi

Setelah instalasi selesai dan file model `.pkl` sudah diekstrak, jalankan aplikasi dengan langkah berikut:

1.  Pastikan Anda berada di direktori yang berisi `app.py`.
2.  Jalankan perintah di terminal:
    ```bash
    streamlit run app.py
    ```
    Aplikasi akan otomatis terbuka di *browser* Anda.

---

## 5. Model dan Hasil

Proyek ini menggunakan dua model dari *library* **XGBoost**:

* **XGBoost Classifier**: Mengklasifikasikan penerbangan menjadi `DELAYED` atau `ON-TIME`.
* **XGBoost Regressor**: Memprediksi durasi keterlambatan dalam menit.

Detail lengkap mengenai pelatihan, evaluasi, dan metrik performa kedua model tersedia di `notebook/project_flight_delay.ipynb`.

### Klasifikasi Keterlambatan

Model ini dilatih untuk memprediksi status akhir penerbangan. Metrik evaluasi yang digunakan antara lain:
* **Precision, Recall, F1-Score**: Untuk menilai kemampuan model mengidentifikasi keterlambatan secara akurat.
* **ROC AUC Score**: Mengukur seberapa baik model membedakan antara kelas `ON-TIME` dan `DELAYED`.
* **Confusion Matrix**: Memberikan rincian visual performa prediksi.

### Regresi Durasi Keterlambatan

Model ini bertujuan mengestimasi durasi keterlambatan jika sebuah penerbangan diprediksi `DELAYED`. Metrik evaluasi yang digunakan antara lain:
* **Mean Absolute Error (MAE)**: Rata-rata selisih absolut antara prediksi dan nilai aktual.
* **Root Mean Squared Error (RMSE)**: Ukuran rata-rata kesalahan prediksi yang lebih sensitif terhadap *outlier*.
* **R-squared ($R^2$)**: Proporsi varians pada durasi keterlambatan yang dapat dijelaskan oleh model.

---

## 6. Fitur-Fitur Dashboard

Dashboard interaktif (`app.py`) menyediakan fitur-fitur berikut:

* **Input Data Penerbangan**: Pengguna dapat memasukkan parameter penerbangan seperti maskapai, asal, tujuan, jarak, dan waktu keberangkatan.
* **Prediksi Instan**: Setelah data di-submit, dashboard akan menampilkan:
    * **Status Penerbangan**: `ON-TIME` atau `DELAYED`.
    * **Probabilitas Keterlambatan**: Peluang keterlambatan dalam bentuk persentase.
    * **Estimasi Waktu Keterlambatan**: Estimasi durasi dalam menit jika penerbangan diprediksi terlambat.
* **Fleksibilitas Waktu**: Pengguna dapat memilih waktu keberangkatan manual atau menggunakan waktu saat ini (WIB) secara otomatis.
