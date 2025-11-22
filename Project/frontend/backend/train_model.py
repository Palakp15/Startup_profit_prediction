# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import joblib
import os

DATA_PATH = 'startup_data.csv'
MODEL_PATH = 'model.pkl'

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    return df

def train_and_save():
    df = load_data()
    X = df[['R&D Spend','Administration','Marketing Spend','State']]
    y = df['Profit']

    # feature transformer: numeric scale, state one-hot
    numeric_features = ['R&D Spend','Administration','Marketing Spend']
    categorical_features = ['State']

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

    pipeline = Pipeline([
        ('pre', preprocessor),
        ('model', RandomForestRegressor(n_estimators=200, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.12, random_state=42)
    pipeline.fit(X_train, y_train)
    print("Train R^2:", pipeline.score(X_train, y_train))
    print("Test R^2:", pipeline.score(X_test, y_test))

    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == '__main__':
    if not os.path.exists(DATA_PATH):
        print("Dataset not found at", DATA_PATH)
    else:
        train_and_save()
