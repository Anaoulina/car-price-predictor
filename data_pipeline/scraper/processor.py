import pandas as pd


def load_data(path):
    """Load dataset from CSV"""
    df = pd.read_csv(path)
    print("Data loaded successfully")
    return df


def clean_data(df):
    """Basic cleaning"""
    df = df.dropna()
    return df


def preprocess(df):
    """Prepare features and target"""
    df = clean_data(df)

    # Convert categorical → numeric
    df['brand'] = df['brand'].astype('category').cat.codes
    df['fuel'] = df['fuel'].astype('category').cat.codes

    X = df.drop("price", axis=1)
    y = df["price"]

    return X, y