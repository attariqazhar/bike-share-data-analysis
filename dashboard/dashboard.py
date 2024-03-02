import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import datetime


# Fungsi untuk mengembalikan dataframe baru
def df_month(df):
    return df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

def df_mean_hourly(df):
    return df.groupby('hr')['cnt'].mean().reset_index()

def df_weather(df):
    return df.groupby('weathersit')['cnt'].sum().reset_index().sort_values('cnt', ascending=False, ignore_index=True)

# Membaca file CSV
df = pd.read_csv('cleaned_bike_sharing.csv')

# Fitur Filtering
min_date = df["dteday"].min()
max_date = df["dteday"].max()

# Melakukan string formatting dan mengubah min date max date menjadi tipe date time
min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d').date()
max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d').date()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://r2.easyimg.io/gwsp322ia/brown_vintage_sport_bike_logo_1_-removebg-preview.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Select time range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['dteday'] >= str(start_date)) & (df['dteday'] <= str(end_date))]

# Header
st.header('🚴 Bike Sharing Data Dashboard 🚴')

sum_cnt = main_df['cnt'].sum()
formatted_sum_cnt = "{:,.0f}".format(sum_cnt).replace(',', '.')
st.metric('Total Rental Bikes ({start_date} to {end_date})'.format(start_date=start_date, end_date=end_date), formatted_sum_cnt)

# Rata-rata Jumlah Peminjaman Sepeda Setiap Harinya
st.subheader('Average Bike Rental by Day (Rounded)')

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    try:
        st.metric('Monday', int(round(main_df[main_df['weekday'] == 'Monday']['cnt'].mean(), 0)))
    except ValueError:
        st.metric('Monday', 0)

with col2:
    try:
        st.metric('Tuesday', int(round(main_df[main_df['weekday'] == 'Tuesday']['cnt'].mean(), 0)))
    except ValueError:
        st.metric('Tuesday', 0)

with col3:
    try:
        st.metric('Wednesday', int(round(main_df[main_df['weekday'] == 'Wednesday']['cnt'].mean(), 0)))
    except ValueError:
        st.metric('Wednesday', 0)

with col4:
    st.metric('Thursday', int(round(main_df[main_df['weekday'] == 'Thursday']['cnt'].mean(), 0)))

with col5:
    st.metric('Friday', int(round(main_df[main_df['weekday'] == 'Friday']['cnt'].mean(), 0)))

with col6:
    st.metric('Saturday', int(round(main_df[main_df['weekday'] == 'Saturday']['cnt'].mean(), 0)))

with col7:
    try:
        st.metric('Sunday', int(round(main_df[main_df['weekday'] == 'Sunday']['cnt'].mean(), 0)))   
    except ValueError:
        st.metric('Sunday', 0)


# Rata-rata jumlah peminjaman sepeda di hari libur dan hari kerja
col8, col9 = st.columns(2)

with col8:
    st.metric('Working Day', int(round(main_df[main_df['workingday'] == 1]['cnt'].mean(), 0)))

with col9:
    st.metric('Holiday', int(round(main_df[main_df['workingday'] == 0]['cnt'].mean(), 0)))


col10, col11 = st.columns(2)

with col10:
    # Jumlah peminjaman sepeda di setiap bulannya pada tahun 2011-2012
    st.subheader('Sum Bike Rental by Month')

with col11:
    # if min_date and max-date is still in 2011 then the checkbox will only be 2011
    if start_date.year == 2011 and end_date.year == 2011:
        year = '2011'
    elif start_date.year == 2012 and end_date.year == 2012:
        year = '2012'
    else:
        year = st.selectbox('Year', ('2011 & 2012', '2011', '2012'))

fig, ax = plt.subplots(figsize=(16, 8))
plt.style.use("dark_background")

if year == '2011 & 2012':
    sns.lineplot(data=df_month(main_df), x="mnth", y="cnt", hue="yr", errorbar=None, marker="o", palette=['purple','green'])
elif year == '2011':
    df_month = df_month(main_df)
    sns.lineplot(data=df_month[df_month['yr'] == 2011], x="mnth", y="cnt", hue="yr", errorbar=None, marker="o", palette=['purple'])
elif year == '2012':
    df_month = df_month(main_df)
    sns.lineplot(data=df_month[df_month['yr'] == 2012], x="mnth", y="cnt", hue="yr", errorbar=None, marker="o", palette=['green'])

# Memberi ticks pada sumbu x sesuai urutan bulan
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12])

# Memberi label pada sumbu x dan y
plt.xlabel('Month')
plt.ylabel('Sum Users')


st.pyplot(fig)

col12, col13 = st.columns(2)
with col12:
    # Rata-rata jumlah peminjaman sepeda di setiap jam 
    st.subheader('Average Bike Rental by Hour')
with col13:
    values = st.slider('Select hour range',0, 23, (0,23))
    # Menyimpan value ke dalam dua variabel
    start_hour, end_hour = values

df_mean_hourly = df_mean_hourly(main_df)
fig = plt.figure(figsize=(16, 8))
ax = sns.lineplot(data=df_mean_hourly[(df['hr'] >= start_hour)&(df['hr'] <= end_hour)], x="hr", y="cnt", color='blue', errorbar=None, marker="o",)

# Memberi label pada sumbu x dan y
plt.xlabel("Hour")
plt.ylabel("Average Users")

plt.xticks([i for i in range(start_hour, end_hour+1)])

plt.grid()
st.pyplot(fig)

# Jumlah peminjaman sepeda di setiap cuaca
st.subheader('Sum Bike Rentals by Weather')
fig = plt.figure(figsize=(20, 10))
sns.barplot(data=df_weather(main_df), y="weathersit", x="cnt", errorbar=None, color="cyan")

# Menyimpan informasi detail mengenai jumlah peminjam di samping bar
for index, row in df_weather(main_df).iterrows():
  plt.text(row['cnt'], index, str(row['cnt']), ha='left', va='center')

# Memberi label pada sumbu x dan y
plt.xlabel('Sum Users')
plt.ylabel('Weather')

st.pyplot(fig)



# Clustering musim dengan membuat scatter plot antara jumlah peminjaman dengan suhu
st.subheader('Distribution of Bike Rental in Each Season')

options = st.multiselect(
'Select season(s)',
['Spring', 'Summer', 'Fall', 'Winter'],
['Spring', 'Summer', 'Fall', 'Winter'])

palette = []
for option in options:
    if option == 'Spring':
        palette.append('red')
    elif option == 'Summer':
        palette.append('green')
    elif option == 'Fall':
        palette.append('blue')
    elif option == 'Winter':
        palette.append('purple')

# Membuat figur
fig = plt.figure(figsize=(16, 8))

# Membuat scatter plot antara jumlah peminjaman sepeda dengan suhu dengan clustering musim
sns.scatterplot(data=main_df[main_df['season'].isin(options)], x='cnt', y='temp', hue="season", alpha=0.5, palette=palette)

plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
plt.title("Clustering Musim Berdsarkan Jumlah Peminjam dan Suhu")

st.pyplot(fig)
