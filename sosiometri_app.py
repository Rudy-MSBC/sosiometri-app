
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

st.title("📊 Aplikasi Sosiometri dan Sosiogram untuk Anak Usia Dini")

st.subheader("1. Masukkan Daftar Nama Anak")
names_input = st.text_area("Tulis nama anak, pisahkan dengan koma", "Alya, Bima, Citra, Dodi, Elsa, Fajar, Gita")
names = [name.strip() for name in names_input.split(',') if name.strip()]

st.subheader("2. Masukkan Pilihan Teman (Sosiometri)")
sosiometri_data = {}
for name in names:
    pilihan = st.multiselect(f"{name} memilih teman yang paling disukai (maks 3)", [n for n in names if n != name], max_selections=3)
    sosiometri_data[name] = pilihan

if st.button("🔍 Proses dan Tampilkan Sosiogram"):
    popularitas = {name: 0 for name in names}
    for pilihan in sosiometri_data.values():
        for teman in pilihan:
            popularitas[teman] += 1

    df_popularitas = pd.DataFrame(list(popularitas.items()), columns=["Nama", "Dipilih Oleh (Skor Popularitas)"])
    st.subheader("📈 Hasil Skoring Popularitas")
    st.dataframe(df_popularitas.sort_values(by="Dipilih Oleh (Skor Popularitas)", ascending=False))

    G = nx.DiGraph()
    G.add_nodes_from(names)
    for anak, pilihans in sosiometri_data.items():
        for teman in pilihans:
            G.add_edge(anak, teman)

    st.subheader("🧠 Sosiogram Visual (Graf Relasi Sosial)")
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, arrows=True, ax=ax)
    st.pyplot(fig)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("⬇️ Unduh Gambar Sosiogram", data=buf.getvalue(), file_name="sosiogram.png", mime="image/png")
    st.download_button("⬇️ Unduh Data Popularitas", data=df_popularitas.to_csv(index=False), file_name="skor_sosiometri.csv", mime="text/csv")
