from sqlalchemy import create_engine
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

database = create_engine("mysql+pymysql://root:Arshia4030#Z@127.0.0.1:3306/superstore")

order_detail = pd.read_sql("SELECT * FROM order_detail;", database)
order = pd.read_sql("SELECT * FROM `order`;", database)
shipping = pd.read_sql("SELECT * FROM shipping;", database)
customer = pd.read_sql("SELECT * FROM customer;", database)
product = pd.read_sql("SELECT * FROM product;", database)

df = (order_detail
      .merge(order, on="Order ID", how="left")
      .merge(shipping, on="Order ID", how="left")
      .merge(customer, on="Customer ID", how="left")
      .merge(product, on="Product ID", how="left"))

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Day"] = df["Order Date"].dt.day
df["Weekday"] = df["Order Date"].dt.dayofweek
df["Quarter"] = df["Order Date"].dt.quarter
df["Sales_x_Quantity"] = df["Sales"] * df["Quantity"]

q_1, q_99 = df["Profit"].quantile([0.01, 0.99])
df = df[df["Profit"].between(q_1, q_99)]

numeric = ["Sales", "Quantity", "Discount", "Shipping Cost", "Sales_x_Quantity"]
non_numeric = ["Ship Mode", "Region", "State", "Market", "Segment", "Category", "Sub-Category"]

df = pd.get_dummies(df, columns=non_numeric, drop_first=True)

feature = ["Sales", "Quantity", "Discount", "Shipping Cost", "Sales_x_Quantity", "Year", "Month", 
           "Day", "Weekday", "Quarter"] + [col for col in df.columns if "_" in col]
X = df[feature]
y = df["Profit"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

random_forest = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
random_forest.fit(X_train, y_train)

y_pred = random_forest.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"R2 Score: {r2:.4f}")
print(f"MSE: {mse:.2f}")

prediction_actual = pd.DataFrame({
    "Order ID": df.loc[X_test.index, "Order ID"] if "Order ID" in df.columns else X_test.index,
    "Actual Profit": y_test,
    "Predicted Profit": y_pred
})
prediction_actual.to_csv(r"D:\Bootcamp\پروژه پایانی\prediction_actual.csv", index=False)

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": random_forest.feature_importances_
}).sort_values("Importance", ascending=False)
feature_importance.to_csv(r"D:\Bootcamp\پروژه پایانی\feature_importance.csv", index=False)

R2_MSE = pd.DataFrame({"Metric": ["R2", "MSE"], "Value": [r2, mse]})
R2_MSE.to_csv(r"D:\Bootcamp\پروژه پایانی\R2_MSE.csv", index=False)

avg_profit = df.groupby("Year")["Profit"].mean().reset_index().rename(columns={"Profit": "Average_Profit"})
avg_profit.to_csv(r"D:\Bootcamp\پروژه پایانی\yearly_profit.csv", index=False)
