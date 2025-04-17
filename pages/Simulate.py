import streamlit as st
import validators

st.set_page_config(page_title="Presensi Stream", layout="centered")

st.title("📸 Simulating Prototype")
st.subheader("Simulasi Prototype Presensi dengan Kamera IP")

# Input URL stream
CAMERA_STREAM_URL = st.text_input(
    "🔗 Masukkan URL stream (contoh: http://123.928.98.123.21)",
    placeholder="http://your.camera.ip.address/stream"
)

# State untuk kontrol START/STOP stream
if "streaming" not in st.session_state:
    st.session_state.streaming = False

col1, col2 = st.columns(2)

if not st.session_state.streaming:
    if st.button("🚀 START STREAM"):
        if validators.url(CAMERA_STREAM_URL):
            st.session_state.streaming = True
        else:
            st.error("❌ URL tidak valid. Pastikan formatnya benar (harus diawali http:// atau https://)")

if st.session_state.streaming:
    if st.button("🛑 STOP STREAM"):
        st.session_state.streaming = False

st.markdown("---")

# Tampilkan stream hanya jika streaming aktif
if st.session_state.streaming:
    st.success("✅ Streaming aktif. Menampilkan stream dari kamera...")
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center;'>
            <img src="{CAMERA_STREAM_URL}" width="640" height="480" style="border: 2px solid #4CAF50; border-radius: 10px;" />
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("💡 Masukkan URL kamera dan klik START STREAM untuk memulai.")
