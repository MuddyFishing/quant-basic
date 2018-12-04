import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score



data=datasets.load_iris(False)
print data.target_names
print data.feature_names
print data.data.shape

# Load the diabetes dataset
diabetes = datasets.load_diabetes()
# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-100]
diabetes_X_test = diabetes_X[-100:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-100]
diabetes_y_test = diabetes.target[-100:]


# create the linear model
regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train,diabetes_y_train)

#make prediction
diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
print('intercept_: \n', regr.intercept_)
print('r^2 coefficient of determination: \n', regr.score(diabetes_X_train,diabetes_y_train))
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_test,diabetes_y_test,color='black')
plt.plot(diabetes_X_test,diabetes_y_pred,color='green',linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()
