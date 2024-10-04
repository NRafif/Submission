# Import Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


# Import Data
all_df = pd.read_csv("https://raw.githubusercontent.com/NRafif/Submission/c75b82da0cd80c8fc687ceb4c934e971593071dc/Submisson/Dashboard/all_data.csv")
datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

# Fix Data Type
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
# Create Helper Function
def create_day_df():
    day_df = all_df.groupby('dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return day_df

def create_hour_df():
    hour_df = all_df.groupby(['dteday']).agg({
        'cnt': 'sum'
    }).reset_index()
    return hour_df

def create_holiday_df():
    holiday_df = all_df.groupby('holiday').agg({
        'cnt': 'sum',
        'instant': 'count'
    }).reset_index()
    return holiday_df

def create_workingday_df():
    workingday_df = all_df.groupby('workingday').agg({
        'cnt': 'sum',
        'instant': 'count'
    }).reset_index()
    return workingday_df


def bytemp2(df):
    temp2_df = df.groupby('temp2').agg({
        'cnt': 'sum'
    }).reset_index()
    return temp2_df

def byhum2(df):
    hum2_df = df.groupby('hum2').agg({
        'cnt': 'sum'
    }).reset_index()
    return hum2_df

def bywindspeed2(df):
    windspeed2_df = df.groupby('windspeed2').agg({
        'cnt': 'sum'
    }).reset_index()
    return windspeed2_df


def create_rfm_df(df):
    rfm_df = df.groupby('instant').agg({
        'dteday': lambda x: (pd.Timestamp('2012-12-31') - pd.to_datetime(x.max())).days,
        'cnt': 'count',
        'casual': 'sum'
    })
    
    rfm_df.columns = ['Recency', 'Frequency', 'Monetary']
    rfm_df['Recency'] = rfm_df['Recency'].astype(int)

    
    return rfm_df

hour_df = create_hour_df()
day_df = create_day_df()
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
# Sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/NRafif/DicodingProject/67596c3aa6a94b993c3c643da8cdd6c69e7c6f65/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu yang dipilih
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# Header
st.header('Renant Company :sparkles:')

# Membuat visualisasi total user
# Membuat visualisasi total user
st.subheader('Total Pengguna Harian')

col1, col2 = st.columns(2)

with col1:
    total_users = main_df['cnt'].sum()
    st.metric("Total Pengguna", value=total_users)

with col2:
    avg_daily_users = main_df['cnt'].mean()
    st.metric("Rata-rata Pengguna Harian", value=f"{avg_daily_users:.0f}")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Pengguna", fontsize=12)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10, rotation=45)
ax.set_title("Total Pengguna Harian", fontsize=16)

st.pyplot(fig)

# Menambahkan interpretasi
st.write("Grafik ini menunjukkan total pengguna harian layanan bike sharing.")
st.write(f"Total pengguna selama periode ini adalah {total_users:,} dengan rata-rata {avg_daily_users:.0f} pengguna per hari.")

max_users_day = main_df.loc[main_df['cnt'].idxmax(), 'dteday'].strftime('%Y-%m-%d')
min_users_day = main_df.loc[main_df['cnt'].idxmin(), 'dteday'].strftime('%Y-%m-%d')

st.write(f"Jumlah pengguna tertinggi terjadi pada tanggal {max_users_day}, "
         f"sementara jumlah pengguna terendah terjadi pada tanggal {min_users_day}.")

# Membuat Visualisasi Permintaan Harian Berdasarkan Weekday
st.subheader('Daily Bike Sharing Demand')
daily_weekday_df = main_df.groupby('weekday').agg({
    'cnt': 'mean'
}).reset_index()

# Mengurutkan hari dalam seminggu
hari_urutan = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
daily_weekday_df['weekday'] = pd.Categorical(daily_weekday_df['weekday'], categories=hari_urutan, ordered=True)
daily_weekday_df = daily_weekday_df.sort_values('weekday')

# Membuat plot
fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(x='weekday', y='cnt', data=daily_weekday_df, ax=ax)

ax.set_title('Rata-rata Penggunaan Sepeda Harian Berdasarkan Hari dalam Seminggu')
ax.set_xlabel('Hari')
ax.set_ylabel('Rata-rata Jumlah Penggunaan')

# Menambahkan label nilai di atas setiap bar
for i, v in enumerate(daily_weekday_df['cnt']):
    ax.text(i, v, f'{v:.0f}', ha='center', va='bottom')

# Menampilkan plot
st.pyplot(fig)

# Menambahkan interpretasi
st.write("Grafik ini menunjukkan rata-rata penggunaan sepeda harian berdasarkan hari dalam seminggu.")

hari_tertinggi = daily_weekday_df.loc[daily_weekday_df['cnt'].idxmax(), 'weekday']
hari_terendah = daily_weekday_df.loc[daily_weekday_df['cnt'].idxmin(), 'weekday']

st.write(f"Penggunaan sepeda tertinggi terjadi pada hari {hari_tertinggi}, "
         f"sementara penggunaan terendah terjadi pada hari {hari_terendah}.")

if daily_weekday_df.loc[daily_weekday_df['weekday'].isin(['Sat', 'Sun']), 'cnt'].mean() > daily_weekday_df.loc[daily_weekday_df['weekday'].isin(['Mon', 'Tue', 'Wed', 'Thu', 'Fri']), 'cnt'].mean():
    st.write("Rata-rata penggunaan sepeda pada akhir pekan (Sabtu dan Minggu) lebih tinggi dibandingkan hari kerja. "
             "Ini mungkin menunjukkan bahwa banyak orang menggunakan sepeda untuk rekreasi pada akhir pekan.")
else:
    st.write("Rata-rata penggunaan sepeda pada hari kerja lebih tinggi dibandingkan akhir pekan. "
             "Ini mungkin menunjukkan bahwa banyak orang menggunakan sepeda untuk pergi bekerja atau sekolah.")


# Membuat Visualisasi Permintaan Bulanan
st.subheader('Monthly Bike Sharing Demand')
monthly_df = main_df.groupby(main_df['dteday'].dt.to_period('M')).agg({
    'casual': 'sum',
    'registered': 'sum'
}).reset_index()

monthly_df['dteday'] = monthly_df['dteday'].dt.to_timestamp()

# Membuat plot
fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(monthly_df['dteday'], monthly_df['casual'], marker='o', linestyle='-', color='b', label='Casual')
ax.plot(monthly_df['dteday'], monthly_df['registered'], marker='o', linestyle='-', color='r', label='Registered')

ax.set_title('Monthly Bike Sharing Demand: Casual vs Registered')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penggunaan')
ax.legend()

# Merotasi label sumbu x untuk memudahkan pembacaan
plt.xticks(rotation=45)

# Menampilkan plot
st.pyplot(fig)

# Menambahkan interpretasi
st.write("Grafik ini menunjukkan perbandingan antara pengguna casual dan registered setiap bulannya. "
         "Kita dapat melihat tren dan pola penggunaan sepeda untuk kedua jenis pengguna ini sepanjang waktu.")

if monthly_df['registered'].mean() > monthly_df['casual'].mean():
    st.write("Secara umum, jumlah pengguna registered lebih tinggi dibandingkan pengguna casual. "
             "Ini mungkin menunjukkan bahwa layanan bike sharing ini memiliki basis pelanggan tetap yang kuat.")
else:
    st.write("Secara umum, jumlah pengguna casual lebih tinggi dibandingkan pengguna registered. "
             "Ini mungkin menunjukkan bahwa layanan ini populer di kalangan wisatawan atau pengguna sesekali.")

st.write("Perhatikan juga pola musiman yang mungkin muncul, seperti peningkatan penggunaan pada bulan-bulan tertentu.")


# Membuat Visualisasi Perbandingan Workingday dan Holiday
st.subheader('Perbandingan Workingday dan Holiday')

# Menghitung rata-rata jumlah penggunaan sepeda untuk workingday dan holiday
workingday_avg = main_df[main_df['workingday'] == 1]['cnt'].mean()
holiday_avg = main_df[main_df['holiday'] == 1]['cnt'].mean()

# Membuat DataFrame untuk plot
comparison_df = pd.DataFrame({
    'Jenis Hari': ['Hari Kerja', 'Hari Libur'],
    'Rata-rata Penggunaan': [workingday_avg, holiday_avg]
})

# Membuat plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Jenis Hari', y='Rata-rata Penggunaan', data=comparison_df, ax=ax)

ax.set_title('Perbandingan Rata-rata Penggunaan Sepeda: Hari Kerja vs Hari Libur')
ax.set_ylabel('Rata-rata Jumlah Penggunaan')

# Menambahkan label nilai di atas setiap bar
for i, v in enumerate(comparison_df['Rata-rata Penggunaan']):
    ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')

# Menampilkan plot
st.pyplot(fig)

# Menambahkan interpretasi
if workingday_avg > holiday_avg:
    st.write("Rata-rata penggunaan sepeda pada hari kerja lebih tinggi dibandingkan hari libur. "
             "Ini mungkin menunjukkan bahwa banyak orang menggunakan sepeda untuk pergi bekerja atau sekolah.")
else:
    st.write("Rata-rata penggunaan sepeda pada hari libur lebih tinggi dibandingkan hari kerja. "
             "Ini mungkin menunjukkan bahwa banyak orang menggunakan sepeda untuk rekreasi pada hari libur.")


# Membuat Visualisasi Faktor Cuaca
temp2_df = bytemp2(main_df)
hum2_df = byhum2(main_df)
windspeed2_df = bywindspeed2(main_df)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Plot untuk Suhu
sns.barplot(x="cnt", y="temp2", data=temp2_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Penggunaan", fontsize=30)
ax[0].set_title("Pengaruh Suhu", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Plot untuk Kelembaban
sns.barplot(x="cnt", y="hum2", data=hum2_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Penggunaan", fontsize=30)
ax[1].set_title("Pengaruh Kelembaban", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Plot untuk Kecepatan Angin
sns.barplot(x="cnt", y="windspeed2", data=windspeed2_df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Jumlah Penggunaan", fontsize=30)
ax[2].set_title("Pengaruh Kecepatan Angin", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=35)
ax[2].tick_params(axis='x', labelsize=30)

plt.tight_layout()
st.pyplot(fig)

# Menambahkan interpretasi
st.write("Grafik ini menunjukkan pengaruh faktor cuaca terhadap permintaan sepeda. "
         "Kita dapat melihat bahwa suhu, kelembaban, dan kecepatan angin memiliki pengaruh yang signifikan terhadap jumlah penggunaan sepeda.")

st.write("Perhatikan bahwa pada grafik suhu, kategori teratas memiliki jumlah penggunaan yang lebih tinggi. "
         "Hal ini menunjukkan bahwa suhu tertentu cenderung meningkatkan permintaan sepeda.")

st.write("Pada grafik kelembaban, kategori teratas memiliki jumlah penggunaan yang lebih tinggi. "
         "Hal ini menunjukkan bahwa tingkat kelembaban tertentu cenderung meningkatkan permintaan sepeda.")

st.write("Pada grafik kecepatan angin, kategori teratas memiliki jumlah penggunaan yang lebih tinggi. "
         "Hal ini menunjukkan bahwa kecepatan angin tertentu cenderung meningkatkan permintaan sepeda.")

# Membuat Visualisasi RFM
st.pyplot(fig)

st.subheader('Analisis RFM (Recency, Frequency, Monetary)')

# Menghitung RFM
rfm = main_df.groupby('instant').agg({
    'dteday': lambda x: (pd.Timestamp('2012-12-31') - pd.to_datetime(x.max())).days,
    'cnt': 'count',
    'registered': 'sum'
})

rfm.columns = ['recency', 'frequency', 'monetary']
rfm['recency'] = rfm['recency'].astype(int)

# Membuat plot scatter 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(rfm['recency'], rfm['frequency'], rfm['monetary'], 
                     c=rfm['monetary'], cmap='viridis')

ax.set_xlabel('Recency (hari)')
ax.set_ylabel('Frequency (jumlah transaksi)')
ax.set_zlabel('Monetary (jumlah pengguna terdaftar)')

plt.colorbar(scatter, label='Monetary')
ax.set_title('Analisis RFM')

st.pyplot(fig)

# Menampilkan statistik deskriptif RFM
st.write("Statistik Deskriptif RFM:")
st.write(rfm.describe())

# Visualisasi distribusi RFM
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 6))

sns.histplot(rfm['recency'], kde=True, ax=ax1)
ax1.set_title('Distribusi Recency')
ax1.set_xlabel('Recency (hari)')

sns.histplot(rfm['frequency'], kde=True, ax=ax2)
ax2.set_title('Distribusi Frequency')
ax2.set_xlabel('Frequency (jumlah transaksi)')

sns.histplot(rfm['monetary'], kde=True, ax=ax3)
ax3.set_title('Distribusi Monetary')
ax3.set_xlabel('Monetary (jumlah pengguna terdaftar)')

plt.tight_layout()
st.pyplot(fig)











    

    
