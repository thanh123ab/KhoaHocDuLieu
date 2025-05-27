from flask import Flask, render_template, request
from population_model import forecast_population_arima
import pandas as pd

app = Flask(__name__)

df = pd.read_csv(r"C:\Users\Asus\Downloads\archive\world_population.csv")
country_list = sorted(df['Country/Territory'].unique().tolist())

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_data = None
    table_data = None
    error = None
    country = ''
    years = 10

    if request.method == 'POST':
        country = request.form['country'].strip()
        years = request.form.get('years', 10)
        try:
            years = int(years)
        except:
            years = 10

        if country == "":
            error = "Vui lòng chọn quốc gia hợp lệ."
        else:
            plot_data, table_data, error = forecast_population_arima(country, years)

    return render_template('index.html',
                           plot_data=plot_data,
                           table_data=table_data,
                           error=error,
                           country_list=country_list,
                           selected_country=country,
                           selected_years=years)

if __name__ == '__main__':
    app.run(debug=True)
