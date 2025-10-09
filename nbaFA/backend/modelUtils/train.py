from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd

dat = pd.read_csv("/Users/ankul/Documents/myPlayers.csv")
dat = dat.map(lambda x: x.strip() if isinstance(x, str) else x)
dat = dat[dat["avg"] != 0]
dat = dat[dat["NxtGm"] != 0]

X = dat.drop(columns=["NxtGm"], errors="ignore").drop(columns=["Name"], errors="ignore")
Y = dat["NxtGm"]

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42,
    shuffle=True
)

model = GradientBoostingRegressor(n_estimators=300, random_state=67)
model.fit(X_train, Y_train)

score = model.score(X_test, Y_test)
preds = model.predict(X_test)
print("Test R^2 score:", score)
print("MAE:", mean_absolute_error(Y_test, preds))
print("MSE:", mean_squared_error(Y_test, preds))