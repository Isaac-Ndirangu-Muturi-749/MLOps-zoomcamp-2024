import pytest
import pandas as pd
from batch import read_data, main

def test_read_data():
    # Example test for read_data function
    data = {
        'tpep_dropoff_datetime': pd.to_datetime(['2023-03-01 00:15:00']),
        'tpep_pickup_datetime': pd.to_datetime(['2023-03-01 00:00:00']),
        'PULocationID': [1],
        'DOLocationID': [2],
    }
    df = pd.DataFrame(data)
    df.to_parquet('test.parquet', engine='pyarrow')

    categorical = ['PULocationID', 'DOLocationID']
    df_result = read_data('test.parquet', categorical)

    assert df_result is not None
    assert 'duration' in df_result.columns

def test_main(monkeypatch):
    # Example test for main function
    def mock_read_data(filename, categorical):
        data = {
            'tpep_dropoff_datetime': pd.to_datetime(['2023-03-01 00:15:00']),
            'tpep_pickup_datetime': pd.to_datetime(['2023-03-01 00:00:00']),
            'PULocationID': ['1'],
            'DOLocationID': ['2'],
            'duration': [15]
        }
        return pd.DataFrame(data)

    monkeypatch.setattr('batch.read_data', mock_read_data)

    main(2023, 3)
    # Check if the output file is created and has the expected content

if __name__ == "__main__":
    pytest.main()
