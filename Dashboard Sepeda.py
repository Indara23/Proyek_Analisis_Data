import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
day_df = pd.read_csv("data_day.csv")
hour_df = pd.read_csv("data_hour.csv")

st.title("Dashboard Penyewaan Sepeda")

# Filtering dataset berdasarkan data perjam atau perhari dan sesuai jenis penggunanya
st.subheader("Tampilkan Data")
dataset_option = st.selectbox("Pilih dataset yang ingin ditampilkan:", ["Data Harian", "Data Per Jam"])
user_type_option = st.selectbox("Pilih jenis pengguna:", ["casual", "registered"])

if dataset_option == "Data Harian":
    df = day_df.copy()
else:
    df = hour_df.copy()

df["cnt"] = df[user_type_option]

if st.checkbox("Tampilkan Data"):
    st.write(df.head())

# Korelasi Data
st.subheader("Korelasi antara Jumlah Penyewaan Sepeda dan Variabel Lainnya")
corr_columns = ["cnt", "temp", "atemp", "hum", "windspeed"]
correlation_matrix = df[corr_columns].corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Grafik Penyewaan Sepeda berdasarkan Cuaca
weather_mapping = {1: "Cerah / Berawan", 2: "Berkabut", 3: "Hujan Ringan / Salju", 4: "Hujan Lebat / Badai"}
df["weather_label"] = df["weathersit"].map(weather_mapping)

st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_avg = df.groupby("weather_label")["cnt"].mean().reset_index().sort_values(by="cnt", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weather_label", y="cnt", data=weather_avg, color="#72BCD4", ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
st.pyplot(fig)

# Grafik Penyewaan Sepeda berdasarkan Musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df["season_label"] = df["season"].map(season_mapping)

st.subheader("Penyewaan Sepeda Berdasarkan Musim")
season_avg = df.groupby("season_label")["cnt"].mean().reset_index().sort_values(by="cnt", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season_label", y="cnt", data=season_avg, color="#72BCD4", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
st.pyplot(fig)

# Grafik Penyewaan Sepeda per Jam (jika dipilih "Data Per Jam")
if dataset_option == "Data Per Jam":
    st.subheader("Penyewaan Sepeda per Jam")
    hourly = df.groupby("hr")["cnt"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(hourly["hr"], hourly["cnt"], marker='o', color="#72BCD4")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Grafik Distribusi Penyewaan Sepeda pada Hari Kerja dan Libur
st.subheader("Distribusi Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x="workingday", y="cnt", data=df, palette=["#72BCD4"], ax=ax)
ax.set_xticklabels(["Hari Libur", "Hari Kerja"])
st.pyplot(fig)

# Grafik Rata-rata Penyewaan Perhari
st.subheader("Rata-rata Penyewaan Sepeda per Hari")
avg_rent_per_day = df.groupby("weekday")["cnt"].mean().reset_index()
day_mapping = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}

avg_rent_per_day["weekday"] = avg_rent_per_day["weekday"].replace(day_mapping)
avg_rent_per_day = avg_rent_per_day.sort_values(by="cnt", ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weekday", y="cnt", data=avg_rent_per_day, color="#72BCD4", ax=ax)
st.pyplot(fig)
