import streamlit as st
from datadummy import overview_active_hardware, overview_traffic

st.title("Overview Page")

st.subheader("Active Hardware")
st.text("Table Kondisi hardware yang terpakai atau active saat ini")
st.dataframe(overview_active_hardware, use_container_width=True)

st.subheader("Traffic Overview")
st.text("Grafik ini adalah representasi dari banyaknya absesnsi keseluruhan hardware yang terjadi dalam satuan waktu")
st.line_chart(overview_traffic.set_index("time"))