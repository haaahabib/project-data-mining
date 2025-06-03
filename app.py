import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pytz
from datetime import datetime
import plotly.express as px

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Flight Delay", layout="wide")

# Load model dan data
@st.cache_resource
def load_models():
    clf = joblib.load('xgb_flight_model.pkl')
    reg = joblib.load('xgb_delay_regressor.pkl')
    return clf, reg

@st.cache_data
def load_sample_data():
    try:
        return pd.read_csv("flight_delays.csv")
    except:
        return None

clf, reg = load_models()
sample_df = load_sample_data()

num_feat = ['FlightNumber', 'Distance', 'DepHour', 'WeekOfYear']
cat_feat = ['Airline', 'Origin', 'Destination', 'DelayReason', 'DayPeriod']

def extract_time_features(df):
    df['DepHour'] = df['ScheduledDeparture'].dt.hour
    df['DayOfWeek'] = df['ScheduledDeparture'].dt.dayofweek
    df['WeekOfYear'] = df['ScheduledDeparture'].dt.isocalendar().week
    df['DayPeriod'] = pd.cut(df['DepHour'], bins=[0,6,12,18,24],
                             labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False)
    return df

def run_inference(input_data):
    df = pd.DataFrame([input_data])
    df['ScheduledDeparture'] = pd.to_datetime(df['ScheduledDeparture'])
    df = extract_time_features(df)
    X = df[num_feat + cat_feat]
    delay_prob = clf.predict_proba(X)[0][1]
    is_delayed = clf.predict(X)[0]
    delay_time = reg.predict(X)[0]
    return {
        'is_delayed': is_delayed,
        'delay_prob': delay_prob,
        'delay_time': delay_time
    }

st.title(" ✈︎ Prediksi Keterlambatan Penerbangan (Flight Delay Prediction)")

# nama dan NIM
st.markdown("""
**Nama & NIM**  
- 202110370311259 - Muhammad Habibulloh  
- 202010370311463 - Yupi Bagus Suhartono
""")

st.markdown("""
### Tujuan Pembangunan Model
1. **Memprediksi kemungkinan keterlambatan** berdasarkan data penerbangan (maskapai, bandara, dan waktu keberangkatan).
2. **Mengestimasi durasi keterlambatan** jika diprediksi terjadi delay.
3. **Meningkatkan efisiensi operasional** penerbangan dengan informasi berbasis prediksi.
4. **Analisis visual interaktif** untuk mengeksplorasi pola keterlambatan penerbangan.
""")

with st.sidebar:
    halaman = st.radio("📂 Navigasi Halaman", ["📊 Data Ringkasan", "📈 Analisis Visual", "✈︎ Prediksi Keterlambatan"])

# Halaman Dashboard
if halaman == "📊 Data Ringkasan":
    st.subheader("📊 Ringkasan Dataset Keterlambatan Penerbangan")
    if sample_df is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Jumlah Data", f"{len(sample_df):,} baris")
        with col2:
            st.metric("Rata-rata Delay", f"{sample_df['DelayMinutes'].mean():.1f} menit")
        with col3:
            st.metric("% Keterlambatan > 5m", f"{(sample_df['DelayMinutes'] > 5).mean()*100:.1f}%")
        st.dataframe(sample_df.head(10).style.hide(axis='index'))
    else:
        st.warning("Data tidak tersedia.")

# Halaman Visualisasi
elif halaman == "📈 Analisis Visual":
    st.subheader("📈 Visualisasi Interaktif Dataset")
    if sample_df is not None:
        opsi = st.selectbox("Pilih Jenis Visualisasi", [
            "Distribusi Delay", "Delay vs Distance", "Delay vs Departure Hour",
            "Delay Berdasarkan Alasan"
        ])

        if opsi == "Distribusi Delay":
            st.markdown("Visualisasi distribusi jumlah keterlambatan penerbangan dalam satuan menit.")
            fig = px.histogram(sample_df, x="DelayMinutes", nbins=50, log_y=True)
            fig.add_vline(x=5, line_dash="dash", line_color="green", annotation_text="> 5 menit")
            st.plotly_chart(fig, use_container_width=True)

        elif opsi == "Delay vs Distance":
            st.markdown("Distribusi delay berdasarkan jarak penerbangan.")
            fig = px.histogram(sample_df, x="Distance", y="DelayMinutes", nbins=40, histfunc='avg',
                               labels={'y': 'Rata-rata Delay (menit)'})
            st.plotly_chart(fig, use_container_width=True)

        elif opsi == "Delay vs Departure Hour":
            st.markdown("Rata-rata delay berdasarkan jam keberangkatan.")
            df_tmp = sample_df.copy()
            df_tmp['DepHour'] = pd.to_datetime(df_tmp['ScheduledDeparture']).dt.hour
            avg_delay = df_tmp.groupby('DepHour')['DelayMinutes'].mean().reset_index()
            fig = px.line(avg_delay, x='DepHour', y='DelayMinutes', markers=True,
                          labels={'DelayMinutes': 'Rata-rata Delay (menit)'},
                          title='Tren Rata-rata Delay per Jam Keberangkatan')
            st.plotly_chart(fig, use_container_width=True)

        elif opsi == "Delay Berdasarkan Alasan":
            st.markdown("Rata-rata keterlambatan berdasarkan kategori alasan keterlambatan.")
            avg_reason = sample_df.groupby('DelayReason')['DelayMinutes'].mean().reset_index()
            fig = px.bar(avg_reason, x='DelayReason', y='DelayMinutes', color='DelayReason',
                         labels={'DelayMinutes': 'Rata-rata Delay (menit)'},
                         title='Rata-rata Delay per Alasan')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data visualisasi tidak tersedia.")

# Halaman Prediksi Keterlambatan
elif halaman == "✈︎ Prediksi Keterlambatan":
    st.subheader("✈︎ Prediksi Keterlambatan Penerbangan")
    with st.form(key="prediksi_form"):
        col1, col2 = st.columns(2)
        with col1:
            airline = st.selectbox("Maskapai", ['Garuda Indonesia', 'Lion Air', 'Citilink'])
            origin = st.selectbox("Bandara Asal", ['CGK', 'SUB', 'DPS'])
            destination = st.selectbox("Bandara Tujuan", ['DPS', 'CGK', 'SUB'])
            reason = st.selectbox("Alasan Delay", ['No Delay', 'Weather', 'Maintenance', 'ATC'])
        with col2:
            flight_num = st.number_input("Nomor Penerbangan", min_value=100, max_value=9999, value=1234)
            distance = st.slider("Jarak (mil)", 100.0, 3000.0, 800.0)
            use_now = st.checkbox("Gunakan waktu sekarang (WIB)", value=True)
            wib = pytz.timezone("Asia/Jakarta")
            now_wib = datetime.now(wib)
            dep_time = now_wib if use_now else st.datetime_input("Waktu Keberangkatan", now_wib)

        submitted = st.form_submit_button("🔍 Prediksi Sekarang")

    if submitted:
        input_data = {
            'Airline': airline,
            'Origin': origin,
            'Destination': destination,
            'DelayReason': reason,
            'FlightNumber': flight_num,
            'Distance': distance,
            'ScheduledDeparture': dep_time
        }
        result = run_inference(input_data)
        status = "🟥 DELAYED" if result['is_delayed'] else "🟩 ON-TIME"
        st.success("✅ Prediksi Berhasil!")
        st.markdown(f"""
        ### ✈︎ Hasil Prediksi
        - **Status**: {status}
        - **Probabilitas Delay**: {result['delay_prob']:.2%}
        - **Estimasi Keterlambatan**: {result['delay_time']:.1f} menit
        """)
