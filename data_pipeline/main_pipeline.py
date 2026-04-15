from scraper.processor import load_data, preprocess

# Path to dataset
path = "data/cars.csv"

# Load data
df = load_data(path)

# Preprocess
X, y = preprocess(df)

print("\nFeatures:")
print(X)

print("\nTarget:")
print(y)