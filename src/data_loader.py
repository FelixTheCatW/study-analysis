import pandas as pd

def load_dataset(url):
    data = pd.read_csv(url)
    return data
