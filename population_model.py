import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

def format_population(value):
    if value >= 1e6:
        return f"{value / 1e6:.1f}M"
    return f"{int(value):,}"

def get_country_list():
    df = pd.read_csv(r"C:\Users\Asus\Downloads\archive\world_population.csv")
    countries = sorted(df['Country/Territory'].dropna().unique())
    return countries

def forecast_population_arima(country, years_ahead=10):
    df = pd.read_csv(r"C:\Users\Asus\Downloads\archive\world_population.csv")
    df = df[df['Country/Territory'] == country]

    if df.empty:
        return None, None, f"Không tìm thấy dữ liệu cho '{country}'"

    year_cols = [col for col in df.columns if col.endswith('Population')]

    data = {}
    for col in year_cols:
        try:
            year = int(col.split()[0])
            population = df.iloc[0][col]
            if pd.isna(population):
                continue
            data[year] = population
        except:
            continue

    years = sorted(data.keys())
    population_values = [data[y] for y in years]
    population = np.array(population_values)

    if len(population) < 5:
        return None, None, "Dữ liệu dân số không đủ để dự báo."

    model = ARIMA(population, order=(2, 1, 2))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=years_ahead)
    future_years = np.arange(years[-1] + 1, years[-1] + 1 + years_ahead)

    # Vẽ biểu đồ
    plt.figure(figsize=(10, 5))
    plt.plot(years, population, label='Dân số thực tế', marker='o')
    plt.plot(future_years, forecast, label='Dự báo ARIMA', linestyle='--', marker='.', color='red')  # <-- đã sửa đường kẻ

    plt.xlabel('Năm')
    plt.ylabel('Dân số')
    plt.title(f'Dự báo dân số cho {country} (ARIMA)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    combined_data = [(y, int(data[y]), None) for y in years] + [(int(y), None, int(f)) for y, f in
                                                                zip(future_years, forecast)]

    return img_base64, combined_data, None
