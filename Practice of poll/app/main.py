from model import train_model
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    model = train_model()

    # тест прогнозу
    prediction = model.predict([[50, 27]])
    print("Прогноз використання хімії:", prediction)

   # 3. Побудова графіка з прогнозом
data = pd.read_csv("../data/dataset.csv")

# точки (реальні дані)
plt.scatter(data['pool_volume'], data['chemical_usage'])

# створюємо значення для лінії
volumes = data['pool_volume']
temps = [27] * len(volumes)  # фіксована температура

predictions = model.predict(list(zip(volumes, temps)))

# лінія прогнозу
plt.plot(volumes, predictions)

plt.xlabel("Обʼєм басейну")
plt.ylabel("Використання хімії")
plt.title("Прогноз використання хімії")

plt.show()