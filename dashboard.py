import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

## Membuat fungsi bantuan
def create_pm25_df(df):
    pm25_df = df.resample(rule='D',on='date').agg({
        "station": "nunique",
        "PM2.5": "mean"
    })
    return pm25_df
def create_co_df(df):
    co_df = df.resample(rule='D',on='date').agg({
        "station": "nunique",
        "CO": "mean"
    })
    return co_df
def create_pm10_df(df):
    pm10_df = df.resample(rule='D',on='date').agg({
        "station": "nunique",
        "PM10": "mean"
    })
    return pm10_df
def create_so2_df(df):
    so2_df = df.resample(rule='D',on='date').agg({
        "station": "nunique",
        "SO2": "mean"
    })
    return so2_df
def create_no2_df(df):
    no2_df = df.resample(rule='D',on='date').agg({
        "station": "nunique",
        "NO2": "mean"
    })
    return no2_df
def create_o3_df(df):
    o3_df = df.resample(rule='D',on='date').agg({
        "station": "nunique",
        "O3": "mean"
    })
    return o3_df
def plot_parameter(data, parameter):
    sorted_data = data.sort_values(by=parameter, ascending=False)
    top_5 = sorted_data.head()
    
    num_stations = min(5, len(top_5))
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(range(num_stations), top_5[parameter][:num_stations], color='skyblue')
    ax.set_title(f'Top 5 Stasiun dengan Nilai Tertinggi untuk Parameter {parameter}')
    ax.set_xlabel('Stasiun')
    ax.set_ylabel(parameter)
    ax.set_xticks(range(num_stations))
    ax.set_xticklabels(top_5['station'][:num_stations], rotation=45, ha='right')

    for index, value in enumerate(top_5[parameter][:num_stations]):
        ax.text(index, value, round(value, 2), ha='center', va='bottom')

    st.pyplot(fig)



## Load data
all_df = pd.read_csv("airquality_daily_data.csv")
all_df["date"] = pd.to_datetime(all_df["date"])
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)

# Filter
min_date = all_df["date"].min()
max_date = all_df["date"].max()

## Komponen dashboard sidebar
with st.sidebar:
    # Menambahkan logo 
    st.image("https://github.com/SFikri-Project/Submission/raw/main/Screenshot%202024-03-03%20211042-modified.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

parameter = st.sidebar.selectbox(
    'Pilih Parameter Kualitas Udara:',
    ('PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3')
)


main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

## Menghitung nilai dengan fungsi yang udah dibuat
pm25_df = create_pm25_df(main_df)
co_df = create_co_df(main_df)
pm10_df = create_pm10_df(main_df)
no2_df = create_no2_df(main_df)
so2_df = create_so2_df(main_df)
o3_df = create_o3_df(main_df)

## Komponen visual dashboard

st.header('Air Quality Dashboard:fog:')

st.subheader('Indeks Kualitas Udara')
 
col1, col2, col3, col4, col5, col6 = st.columns(6)
 
# Format angka untuk metric
format_metric = lambda x: "{:.1f}".format(x)  # Format angka dengan 2 desimal

# Membuat metric
with col1:
    indeks_pm = pm25_df['PM2.5'].mean()
    st.metric("PM2.5", value=format_metric(indeks_pm))
with col2:
    indeks_co = co_df['CO'].mean()
    st.metric("CO", value=format_metric(indeks_co))
with col3:
    indeks_pm10 = pm10_df['PM10'].mean()  # Perbaikan disini
    st.metric("PM10", value=format_metric(indeks_pm10))
with col4:
    indeks_no2 = no2_df['NO2'].mean()
    st.metric("NO2", value=format_metric(indeks_no2))
with col5:
    indeks_so2 = so2_df['SO2'].mean()
    st.metric("SO2", value=format_metric(indeks_so2))
with col6:
    indeks_o3 = o3_df['O3'].mean()
    st.metric("O3", value=format_metric(indeks_o3))

# Plot Tren Harian 
fig, ax = plt.subplots(figsize=(16, 8))
if parameter == 'PM2.5':
    plt.plot(pm25_df.index, pm25_df["PM2.5"], marker='o', linewidth=2, color="#90CAF9")
    plt.title(f'Tren Harian Indeks Kualitas Udara {parameter}')
elif parameter == 'CO':
    plt.plot(co_df.index, co_df["CO"], marker='o', linewidth=2, color="#FF7043")
    plt.title(f'Tren Harian Indeks Kualitas Udara {parameter}')
elif parameter == 'PM10':
    plt.plot(pm10_df.index, pm10_df["PM10"], marker='o', linewidth=2, color="#81C784")
    plt.title(f'Tren Harian Indeks Kualitas Udara {parameter}')
elif parameter == 'NO2':
    plt.plot(no2_df.index, no2_df["NO2"], marker='o', linewidth=2, color="#4DB6AC")
    plt.title(f'Tren Harian Indeks Kualitas Udara {parameter}')
elif parameter == 'SO2':
    plt.plot(so2_df.index, so2_df["SO2"], marker='o', linewidth=2, color="#FFCA28")
    plt.title(f'Tren Harian Indeks Kualitas Udara {parameter}')
elif parameter == 'O3':
    plt.plot(o3_df.index, o3_df["O3"], marker='o', linewidth=2, color="#9575CD")
    plt.title(f'Tren Harian Indeks Kualitas Udara {parameter}')

plt.xlabel('Tanggal')
plt.ylabel('Rata-rata Harian')
plt.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot Top 5 Lokasi
st.subheader("5 Lokasi Stasiun dengan Nilai Parameter Kualitas Udara Tertinggi")
plot_parameter(main_df, parameter)


# Plot Histogram Distribusi
air_quality_variables = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
weather_variables = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
st.subheader("Distribution Of Air Quality Parameters and Weather Variabels")
selected_parameter = st.radio("Select Parameter", ("Air Quality", "Weather"))
plt.figure(figsize=(12, 8))

if selected_parameter == "Air Quality":
    st.subheader("Histogram of Air Quality Parameters")
    for i, variable in enumerate(air_quality_variables, 1):
        plt.subplot(2, 3, i)
        sns.histplot(all_df[variable], kde=True, color='skyblue')
        plt.title(f'Distribution of {variable}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.subheader("Histogram of Weather Variables")
    for i, variable in enumerate(weather_variables, 1):
        plt.subplot(2, 3, i)
        sns.histplot(all_df[variable], kde=True, color='lightgreen')
        plt.title(f'Distribution of {variable}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
    plt.tight_layout()
    st.pyplot(plt)
st.caption('Copyright (c) Saeful Fikri 2024')
