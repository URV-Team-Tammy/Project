import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

data = pd.read_csv('PL_sum.csv')
data['ds'] = pd.to_datetime(data['ds'], format='%Y-%m-%d %H:%M:%S')
print(data.head())
model = Prophet()
model.fit(data)

future = model.make_future_dataframe(periods=17520, freq='h')
forecast = model.predict(future)

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
forecast.to_csv('data.csv', index=False)


fig = model.plot(forecast)
plt.title("2 year forecast, PL")
plt.xlabel('Date')
plt.ylabel('Value')
plt.yticks(range(200, 901, 100))
years = pd.date_range(start='2017', end='2026', freq='YS')
plt.xticks(years, years.year)
plt.tight_layout()
plt.savefig('PL2.png', dpi=300)
plt.show()


