import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_model():
    data = pd.read_csv("../data/dataset.csv")

    X = data[['pool_volume', 'temperature']]
    y = data['chemical_usage']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Модель 1
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_score = lr.score(X_test, y_test)

    # Модель 2
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    rf_score = rf.score(X_test, y_test)

    print("Linear Regression:", lr_score)
    print("Random Forest:", rf_score)

    # обираємо кращу
    if rf_score > lr_score:
        print("Обрана модель: Random Forest")
        return rf
    else:
        print("Обрана модель: Linear Regression")
        return lr