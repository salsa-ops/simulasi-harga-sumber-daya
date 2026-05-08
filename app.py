import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================

data = pd.read_csv("data_emas.csv")

# =========================
# BAGIAN 1 & 2: SIDEBAR & KONFIGURASI
# =========================

# Pindahkan slider ke Sidebar (saran Point 2)
st.sidebar.header("⚙️ Pengaturan Parameter")
tingkat_bunga = st.sidebar.slider("Pilih Tingkat Bunga (%)", 0, 20, 5)
pajak_karbon = st.sidebar.slider("Pajak Karbon Masa Depan (%)", 0, 50, 10)

# ==========================================
# BAB I & II: PENDAHULUAN & LANDASAN TEORI
# ==========================================
st.title("🏆 Analisis Intertemporal Sumber Daya Emas")
st.write("Project Ekonomi SDA dan Lingkungan")

st.info("""
**Landasan Filosofis (George Santayana - The Sense of Beauty):**
Emas bukan sekadar komoditas fisik, tetapi cerminan nilai yang muncul dari preferensi manusia terhadap keindahan dan keamanan aset (*Safe Haven*). 
Nilai ini memengaruhi cara kita mengevaluasi risiko masa depan dan memutuskan kapan waktu terbaik untuk melakukan ekstraksi.
""")

# =========================
# BAGIAN 3: METRICS (Saran Point 1)
# =========================
# Kita letakkan Metrics di bawah teori agar menjadi jembatan ke data
st.subheader("Kondisi Pasar Saat Ini")
col1, col2, col3 = st.columns(3)

with col1:
    # Mengambil data terakhir dari file CSV kamu
    st.metric("Harga Emas Saat Ini", f"${data['Harga_Emas'].iloc[-1]}", "Stable")

with col2:
    st.metric("Total Cadangan", "801,473 Kg", "-0.4%")

with col3:
    st.metric("Status Kelangkaan", "High Alert", "Critical", delta_color="inverse")

st.markdown("---")

# =========================
# TAMPILKAN DATA
# =========================

st.subheader("Data Historis")

st.dataframe(data)

# =========================
# GRAFIK HARGA EMAS
# =========================

st.subheader("Perkembangan Harga Emas")

fig, ax = plt.subplots()

ax.plot(data["Tahun"], data["Harga_Emas"], marker='o')

ax.set_xlabel("Tahun")
ax.set_ylabel("Harga Emas")

st.pyplot(fig)

# =========================
# GRAFIK STOCK EMAS
# =========================

st.subheader("Perubahan Stock Emas")

fig2, ax2 = plt.subplots()

ax2.plot(data["Tahun"], data["Stock_Emas"], marker='o')

ax2.set_xlabel("Tahun")
ax2.set_ylabel("Stock Emas")

st.pyplot(fig2)
# ==========================================
# BAB II & IV: SIMULASI HOTELLING RULE (DASAR)
# ==========================================
st.divider()
st.subheader("Simulasi Hotelling Rule (Model Dasar)")

# Gunakan key unik agar tidak bentrok dengan slider di bawah

harga_awal = data["Harga_Emas"][0]
data["Hotelling_Price_Dasar"] = [
    harga_awal * ((1 + tingkat_bunga/100) ** i) 
    for i in range(len(data))
]

st.write("Perbandingan Harga Aktual vs Proyeksi Teoretis")
st.dataframe(data[["Tahun", "Harga_Emas", "Hotelling_Price_Dasar"]])

fig_dasar, ax_dasar = plt.subplots()
ax_dasar.plot(data["Tahun"], data["Harga_Emas"], marker='o', label="Harga Aktual")
ax_dasar.plot(data["Tahun"], data["Hotelling_Price_Dasar"], ls='--', label="Teori Hotelling", color="red")
ax_dasar.set_title("Uji Teori Hotelling Murni")
ax_dasar.legend()
st.pyplot(fig_dasar)

st.write("""
**Interpretasi Awal:** Jika harga aktual menyimpang dari garis merah, maka asumsi pasar persaingan sempurna dalam teori Hotelling tidak terpenuhi. 
Penyimpangan ini akan dibahas lebih mendalam pada bagian Mekanisme Pasar di bawah.
""")

# =========================
# GREEN PARADOX
# =========================

st.subheader("Simulasi Green Paradox")

data["Ekstraksi"] = (
    data["Stock_Emas"].shift(1) - data["Stock_Emas"]
)

data["Ekstraksi"] = data["Ekstraksi"].fillna(0)

data["Race_to_Extract"] = (
    data["Ekstraksi"] * (1 + pajak_karbon+ tingkat_bunga/100)
)

st.write("Simulasi Percepatan Ekstraksi")

st.dataframe(
    data[["Tahun", "Ekstraksi", "Race_to_Extract"]]
)

fig4, ax4 = plt.subplots()

ax4.plot(
    data["Tahun"],
    data["Ekstraksi"],
    marker='o',
    label="Ekstraksi Normal"
)

ax4.plot(
    data["Tahun"],
    data["Race_to_Extract"],
    marker='o',
    label="Race to Extract"
)

ax4.legend()

st.pyplot(fig4)

st.write("""
Semakin tinggi ekspektasi pajak karbon di masa depan,
produsen memiliki insentif mempercepat ekstraksi saat ini.

Fenomena ini dikenal sebagai Green Paradox,
di mana kebijakan lingkungan justru dapat
mempercepat eksploitasi sumber daya.
""")
# ==========================================
# BAB III & IV: TAKSONOMI CADANGAN (MCKELVEY BOX)
# ==========================================
st.divider()
st.header("Simulasi Spektrum Cadangan")

# Slider Teknologi (Wajib ada menurut rubrik)
tek_index = st.slider("Kemajuan Teknologi Ekstraksi (%)", 0, 100, 20)

total_sumber_daya = 1000000
# Reserve berubah berdasarkan Harga DAN Teknologi
data["Resource"] = total_sumber_daya
data["Reserve"] = (data["Harga_Emas"] / data["Harga_Emas"].max()) * (total_sumber_daya * 0.7) * (1 + (tek_index - tingkat_bunga - pajak_karbon)/100)
data["Reserve"] = data["Reserve"].clip(upper=total_sumber_daya) 

fig_res, ax_res = plt.subplots()
ax_res.plot(data["Tahun"], data["Resource"], label="Total Resource (Tetap)", linestyle="--", color="gray")
ax_res.plot(data["Tahun"], data["Reserve"], marker='o', label="Economic Reserve (Dinamis)", color="gold")
ax_res.set_title("Pergeseran Resource menjadi Reserve")
ax_res.legend()
st.pyplot(fig_res)

st.write(f"**Analisis Spektrum:** Dengan kemajuan teknologi {tek_index}%, cadangan yang layak secara ekonomi meningkat karena efisiensi teknik menekan biaya ekstraksi.")

# ==========================================
# EVALUASI HOTELLING & MEKANISME PASAR (DYNAMIC VERSION)
# ==========================================
st.divider()
st.header("Mekanisme Struktur Pasar & Evaluasi Hotelling")

r_eval = st.slider("Tingkat Bunga Diskonto (%)", 1, 15, 5, key="slider_hotelling_final")

# ==========================================
# BAB IV: MEKANISME PASAR & EVALUASI HOTELLING
# ==========================================
st.divider()
st.header("⚖️ Mekanisme Struktur Pasar & Evaluasi Hotelling")

# Slider diletakkan di sini agar dekat dengan grafiknya
r_eval = tingkat_bunga  # Mengambil nilai dari slider yang sudah ada di sidebar

market_type = st.radio(
    "Pilih Perspektif Struktur Pasar (Grafik akan Berubah Secara Matematis):",
    ["Persaingan Sempurna", "Oligopoli", "Monopoli Lokal"],
    key="market_final",
    horizontal=True
)

harga_awal = data["Harga_Emas"].iloc[0]

# LOGIKA PERUBAHAN MATEMATIS (Disatukan agar tidak dobel hitung)
if market_type == "Persaingan Sempurna":
    r_adj = r_eval / 100
    label_plot = "Prediksi Hotelling (Efisien)"
    color_plot = "green"
    analisis_teks = "**Analisis:** Jalur harga mendekati kondisi efisiensi alokasi intertemporal sesuai teori dasar."
    st.info(analisis_teks)
    
elif market_type == "Oligopoli":
    r_adj = (r_eval * 0.6) / 100
    label_plot = "Prediksi Oligopoli (Harga Tertahan)"
    color_plot = "orange"
    analisis_teks = "**Analisis Kritis:** Grafik menunjukkan bahwa pertumbuhan harga riil lebih lambat karena adanya kontrol volume oleh produsen besar."
    st.warning(analisis_teks)

else: # Monopoli Lokal
    r_adj = (r_eval * 1.5) / 100
    label_plot = "Prediksi Monopoli (Race to Extract)"
    color_plot = "darkred"
    analisis_teks = "**Analisis Kritis:** Kurva yang lebih curam menunjukkan ekspektasi pengurasan cepat (Race to Extract). Produsen mengabaikan nilai masa depan demi profit jangka pendek."
    st.error(analisis_teks)

# Perhitungan Data
data["Hotelling_Price"] = [harga_awal * ((1 + r_adj) ** i) for i in range(len(data))]

# PEMBUATAN GRAFIK TUNGGAL YANG DINAMIS
fig_final, ax_final = plt.subplots(figsize=(10, 5))
ax_final.plot(data["Tahun"], data["Harga_Emas"], marker='o', label="Harga Aktual", color="blue", linewidth=2)
ax_final.plot(data["Tahun"], data["Hotelling_Price"], ls='--', label=label_plot, color=color_plot, linewidth=2)

ax_final.set_title(f"Evaluasi Jalur Harga Intertemporal: {market_type}")
ax_final.set_xlabel("Tahun")
ax_final.set_ylabel("Harga (USD)")
ax_final.legend()

# Menampilkan grafik dengan ukuran proporsional
st.pyplot(fig_final)

# ==========================================
# BAB V: KESIMPULAN & REKOMENDASI
# ==========================================
st.divider()
st.header("📌 Kesimpulan & Rekomendasi Kebijakan")
st.success("""
1. **Kesimpulan:** Alokasi intertemporal emas sangat bergantung pada struktur pasar dan kebijakan lingkungan.
2. **Rekomendasi:** Diperlukan regulasi yang stabil untuk memitigasi dampak Green Paradox agar ekstraksi tetap berkelanjutan.
""")
