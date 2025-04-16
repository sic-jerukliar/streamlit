import streamlit as st
from datadummy import mahasiswa_data
from utils import generatePdfAndSendEmail

st.title("Students Monitoring and Actions")

st.subheader("Table Presentase Kehadiran Siswa")
st.dataframe(mahasiswa_data, use_container_width=True)

# Inisialisasi session_state
if 'show_filtered' not in st.session_state:
    st.session_state.show_filtered = False

treshold_str = st.text_input("Presentasi Minimal Siswa", placeholder="Masukkan batas maksimal persentase kehadiran (misal: 0.7)")
cari = st.button("Cari")

if cari:
    try:
        treshold = float(treshold_str)
        # Simpan hasil filter ke dalam session_state
        st.session_state.data_treshold = mahasiswa_data[mahasiswa_data['Persentase Kehadiran'] < treshold]
        st.session_state.show_filtered = True
    except ValueError:
        st.error("Masukkan angka desimal yang valid, contoh: 0.7")
        st.session_state.show_filtered = False

# Tampilkan hasil filter kalau tersedia
if st.session_state.show_filtered:
    data_treshold = st.session_state.data_treshold
    st.subheader("📉 Siswa dengan Kehadiran di bawah ambang")
    st.dataframe(data_treshold, use_container_width=True)

    if not data_treshold.empty:
        if st.button("Buat Surat dan Kirim"):
            generatePdfAndSendEmail(data_treshold)
            st.success("✅ Semua surat berhasil dibuat dan dikirim!")