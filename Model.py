from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class model:
    def __init__(self):
        #loading values
        df = pd.read_csv("multi_label_op.csv", sep=";")

        #loading X-inputs
        x_features_cols = [df.columns[i] for i in range(9)]
        x_Features = df[x_features_cols]

        #Loading y-inputs
        y_features_cols = [df.columns[i] for i in range(9, len(df.columns))]
        y_Features = df[y_features_cols]

        X_train, x_test, Y_train, y_test = train_test_split(x_Features, y_Features, test_size=0.01)
        self.model = DecisionTreeClassifier(random_state=13)
        self.model.fit(X_train, Y_train)

    def getModel(self):
        return self.model

    def getPredValue(self, x_val):
        x_val = np.array(x_val).reshape(1, len(x_val))
        y_pred = np.reshape(self.model.predict(x_val), x_val.shape[1])
        return y_pred