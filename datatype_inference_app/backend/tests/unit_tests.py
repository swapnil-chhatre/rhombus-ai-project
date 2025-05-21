# tests/test_inference.py
import pandas as pd
import os
import sys
import logging

# Add the parent directory to the path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_inference.infer_data_type import InferenceEngine

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_type_inference():
    """Test the type inference engine with a sample dataset."""
    # Create a test CSV file
    test_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'age': ['25', '30', '22', '28', '35'],
        'salary': ['50000.50', '60000.75', '45000.25', '70000.00', '55000.50'],
        'hire_date': ['2020-01-15', '2019-05-20', '2021-03-10', '2018-11-05', '2020-07-22'],
        'department': ['IT', 'HR', 'IT', 'Finance', 'Marketing'],
        'is_manager': ['Yes', 'No', 'No', 'Yes', 'No']
    }
    
    test_df = pd.DataFrame(test_data)
    test_file = 'test_data.csv'
    test_df.to_csv(test_file, index=False)
    
    # Initialize the engine
    engine = InferenceEngine()
    
    try:
        # Test file reading
        df = engine.read_file(test_file)
        print(f"Successfully read file with shape: {df.shape}")
        
        # Test type inference
        inferred_types = engine.infer_column_types(df)
        print("\nInferred types:")
        for col, dtype in inferred_types.items():
            print(f"  {col}: {dtype}")
        
        # Test conversion
        converted_df = engine.convert_column_types(df, inferred_types)
        print("\nConverted DataFrame dtypes:")
        for col, dtype in converted_df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        # Test full processing
        processed_df, info_dict = engine.process_file(test_file, convert_to_inferred_type=True)
        
        print("\nFull processing info:")
        print(f"Total rows: {info_dict['total_rows']}")
        print(f"Total columns: {info_dict['total_columns']}")
        print(f"Memory usage: {info_dict['memory_usage_bytes']} bytes")
        
        print("\nColumn details:")
        for col_info in info_dict['columns']:
            print(f"  {col_info['name']}:")
            print(f"    Current type: {col_info['current_type']}")
            print(f"    Inferred type: {col_info['inferred_type']}")
            print(f"    Sample values: {col_info['sample_values'][:3]}")
        
        print("\nTest completed successfully!")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_type_inference()