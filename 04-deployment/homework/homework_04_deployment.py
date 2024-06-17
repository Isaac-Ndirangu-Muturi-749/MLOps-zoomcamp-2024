import argparse
import pandas as pd
import numpy as np
import pickle

# Load the model and vectorizer
with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = (df.tpep_dropoff_datetime - df.tpep_pickup_datetime).dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def predict_duration(df):
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred

def main(year, month):
    filename = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'
    df = read_data(filename)
    y_pred = predict_duration(df)
    mean_duration = np.mean(y_pred)
    print(f"Mean predicted duration for {year}-{month:02d}: {mean_duration:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict ride durations")
    parser.add_argument('--year', type=int, required=True, help='Year of the dataset')
    parser.add_argument('--month', type=int, required=True, help='Month of the dataset')
    args = parser.parse_args()

    main(args.year, args.month)

# python homework_04_deployment.py --year 2023 --month 4
