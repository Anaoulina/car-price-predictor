import sys
import os

# Add the project root to sys.path to handle local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from cleaner import DataProcessor

def run_test():
    # Define paths relative to this script
    input_file = "../avito_cars_dataset.csv"
    output_file = "cleaned_cars_test.csv"

    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    # Initialize the processor
    processor = DataProcessor(input_file)
    
    # Execute cleaning pipeline
    processor.load_data()
    cleaned_df = processor.process()
    
    # Print results summary
    print("\n[INFO] Preview of cleaned data:")
    print(cleaned_df.head())
    
    # Save the result
    processor.save_cleaned(output_file)
    print(f"\n[SUCCESS] Cleaned data saved to {output_file}")

if __name__ == "__main__":
    run_test()