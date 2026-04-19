import pandas as pd
import re

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        # Read with utf-8-sig to handle Windows/Excel encoding issues
        self.df = pd.read_csv(self.file_path, encoding='utf-8-sig')
        print(f"📊 Loaded {len(self.df)} rows.")

    def clean_price(self, price):
        if pd.isna(price) or 'N/A' in str(price): return None
        nums = re.findall(r'\d+', str(price).replace(' ', ''))
        return int(nums[0]) if nums else None

    def clean_km(self, km):
        if pd.isna(km) or 'N/A' in str(km): return None
        nums = re.findall(r'\d+', str(km).replace(' ', ''))
        return int(nums[0]) if nums else None

    def process(self):
        # 1. Normalize Column Names (Fixes AnnÃ©e, KilomÃ©trage, etc.)
        # We rename columns by position to avoid encoding matching errors
        column_mapping = {
            self.df.columns[2]: 'Price',
            self.df.columns[3]: 'Year',
            self.df.columns[4]: 'Mileage',
            self.df.columns[5]: 'Fuel',
            self.df.columns[6]: 'Gearbox',
            self.df.columns[7]: 'Brand'
        }
        self.df.rename(columns=column_mapping, inplace=True)

        # 2. Clean numerical columns using the new names
        self.df['Price'] = self.df['Price'].apply(self.clean_price)
        self.df['Mileage'] = self.df['Mileage'].apply(self.clean_km)
        
        # 3. Handle missing Brands using the Title (Titre)
        self.df['Brand'] = self.df.apply(
            lambda x: str(x['Titre']).split()[0] if pd.isna(x['Brand']) or x['Brand'] == 'N/A' else x['Brand'], 
            axis=1
        )

        # 4. Final Filtration
        self.df.dropna(subset=['Price'], inplace=True)
        self.df = self.df[self.df['Price'] > 1000] # Remove 0 DH or fake prices

        print("✅ Data cleaning & Column normalization finished.")
        return self.df

    def save_cleaned(self, output_path):
        # Always use utf-8-sig for Excel compatibility
        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"💾 Cleaned data saved to: {output_path}")