import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import pickle

# Read the data
data = pd.read_csv('price_data.csv')

# Define features and target variables
X = data[['temperature', 'precipitation', 'time_of_day']]
y = data['percentage']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define and train the Gradient Boosting Regressor model for Prediction
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

model.fit(X_train, y_train)

# Predict result on test data
y_pred = model.predict(X_test)

# Compute mean squared error of the result
mse = mean_squared_error(y_test, y_pred)

print(f'Mean Squared Error: {mse}')

# save the trained model
filename = 'price_model.sav'
pickle.dump(model, open(filename, 'wb'))
 
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

# Evaluate score of the model based on test data result
result = loaded_model.score(X_test, y_test)
print(result)