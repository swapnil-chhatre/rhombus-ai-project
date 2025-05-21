# Core functionality

import logging
import numpy as np
import pandas as pd
import re

from dateutil.parser import parse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InferenceEngine:
    """
    Class which contains core Python logic of the application
    """

    def __init__(self):
        """Initialize the DataTypeInferenceEngine."""
        # Define mappings from pandas dtypes to user-friendly names
        self.dtype_display_mapping = {
            'object': 'Text',
            'int64': 'Integer',
            'float64': 'Decimal',
            'datetime64[ns]': 'Date/Time',
            'bool': 'Boolean',
            'category': 'Category',
            'timedelta[ns]': 'Time Duration',
            'complex128': 'Complex Number',
        }

    def read_file(self, file_path: str) -> pd.DataFrame:
        """
        Function to read CSV or excel file and covert it into a Pandas Dataframe

        Args:
            file_path: Path to the file to be read

        Returns:
            Dataframe containing file data
        """

        try:
            extension = file_path.split('.')[-1].lower()

            if extension == 'csv':
                try:
                    df = pd.read_csv(file_path, sep=',')
                except pd.errors.ParserError:
                    df = pd.read_csv(file_path, sep=';')
            elif extension in ['xls', 'xlsx']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file extension: {extension}")
            return df
        except Exception as e:
            logger.error(f"Error reading {file_path} : {e}")
            raise

    def check_if_boolean(self, samples: list[str]) -> bool:
        """
        Check if a string value from a list is representing a boolean.

        Args:
            samples: List of strings

        Returns:
            True if the list contains booleans, False otherwise.
        """
        bool_values = {'true', 'false', 't', 'f', 
        'yes', 'no', 'y', 
        'n', '1', '0'}

        valid_count = 0
        total_non_null = 0
        for value in samples:
            if value and isinstance(value, str):
                if value.lower() in bool_values:
                    valid_count += 1
                total_non_null += 1

        return valid_count >= 0.8 * total_non_null

    def check_if_categorical(self, series: pd.Series) -> bool:
        """
        Check if a Pandas Series is categorical.

        Args:
            series: Pandas Series

        Returns:
            True if the series is categorical, False otherwise.
        """
        if series.dtype != 'object':
            return False

        unique_values = series.nunique()
        total_values = len(series)
         
        if unique_values / total_values < 0.05 or unique_values < 20:
            return True
        return False

    def check_if_date(self, samples: list[str]) -> bool:
        """
        Check if a string value from a list is representing a date.

        Args:
            samples: List of strings

        Returns:
            True if the list contains dates, False otherwise.
        """

        date_patterns = [
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YY or MM/DD/YYYY
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YY or MM-DD-YYYY
            r'\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}',  # DD Month YYYY
            r'[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4}'  # Month DD, YYYY
        ]

        valid_count = 0
        total_non_null = 0
        for value in samples:
            if value and isinstance(value, str):
                total_non_null += 1
                if any(re.match(pattern, value) for pattern in date_patterns):
                    valid_count += 1
                else:
                    try:
                        parse(value, fuzzy=False)
                        valid_count += 1
                    except (ValueError, TypeError):
                        pass

        return valid_count >= 0.8 * total_non_null

    def check_if_float(self, samples: list[str]) -> bool:
        """
        Check if a string value from a list is representing a float.

        Args:
            samples: List of strings

        Returns:
            True if the list contains floats, False otherwise.
        """
        value_count = 0
        total_non_null = 0
        for value in samples:
            if value and isinstance(value, str):
                total_non_null += 1
                try:
                    float(value)
                    value_count += 1
                except ValueError:
                    pass

        return value_count >= 0.8 * total_non_null

    def check_if_integer(self, samples: list[str]) -> bool:
        """
        Check if a string value from a list is representing an integer.

        Args:
            samples: List of strings

        Returns:
            True if the list contains integers, False otherwise.
        
        """
        valid_count = 0
        total_non_null = 0
        for value in samples:
            if value and isinstance(value, str):
                total_non_null += 1
                try:
                    int(value)
                    valid_count += 1
                except ValueError:
                    pass

        return valid_count >= 0.8*total_non_null

    def infer_column_types(self, df: pd.DataFrame) -> dict[str, str]:
        """
        Infer the data types for all columns in the DataFrame.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary mapping column names to inferred data types
        """
        inferred_types = {}

        for column in df.columns:
            series = df[column]

            # Accept correctly typed columns
            if series.dtype != 'object':
                inferred_types[column] = str(series.dtype)
                continue

            # Infer all null value columns as 'object'
            if series.isna().all():
                inferred_types[column] = 'object'
                continue

            samples = series.dropna().head(100 if len(series) > 100 else len(series)).tolist()

            # Check for the boolean columns
            if self.check_if_boolean(samples):
                inferred_types[column] = 'bool'
                continue

            # Check for numeric column
            if self.check_if_integer(samples):
                inferred_types[column] = 'int64'
                continue
            elif self.check_if_float(samples):
                inferred_types[column] = 'float64'
                continue

            # Check for date values
            if self.check_if_date(samples):
                inferred_types[column] = 'datetime64[ns]'
                continue

            # Check for categorical values
            if self.check_if_categorical(series):
                inferred_types[column] = 'category'
                continue

        return inferred_types 

    def convert_column_types(self, df: pd.DataFrame, inferred_types: dict[str, str]) -> pd.DataFrame:
        """
        Convert column types to the inferred data type

        Args:
            df: Dataframe to convert
            inferred_types: Disctionary mapping column names to the inferred types

        Return:
            Dataframe with converted data types
        """

        df_copy = df.copy()
        for column, dtype in inferred_types.items():
            if column not in df_copy.columns:
                logger.warning(f"Column {column} not found in DataFrame")
                continue
            
            try:
                if dtype == 'datetime64[ns]':
                    df_copy[column] = pd.to_datetime(df_copy[column], errors='coerce')
                
                elif dtype == 'category':
                    df_copy[column] = df_copy[column].astype('category')
                
                elif dtype == 'bool':
                    # Handle various boolean representations
                    bool_map = {'true': True, 'false': False, 'yes': True, 'no': False, 
                                't': True, 'f': False, 'y': True, 'n': False, '1': True, '0': False}
                    df_copy[column] = df_copy[column].apply(
                        lambda x: bool_map.get(str(x).strip().lower(), None) 
                        if pd.notnull(x) 
                        else None
                    )
                
                else:
                    df_copy[column] = df_copy[column].astype(dtype)
                
                logger.info(f"Successfully converted column {column} to {dtype}")
            
            except Exception as e:
                logger.error(f"Error converting column {column} to {dtype}: {str(e)}")
                # Keep the original column unchanged
        
        return df_copy

    def get_dataframe_info(self, df: pd.DataFrame) -> dict:
        """
        Get detailed information about a DataFrame.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary containing DataFrame information
        """
        
        # Get memory usage before optimization
        original_memory = df.memory_usage(deep=True).sum()
        
        # Infer column types
        inferred_types = self.infer_column_types(df)
        
        # Get column information
        columns_info = []
        for column in df.columns:
            non_null_count = df[column].count()
            null_count = df[column].isna().sum()
            unique_count = df[column].nunique()
            
            # Get sample values (excluding nulls)
            sample_values = df[column].dropna().head(5).tolist()
            
            # Get current and inferred types with user-friendly names
            current_type = str(df[column].dtype)
            inferred_type = inferred_types[column]
            
            # Map to display names
            current_display_type = self.dtype_display_mapping.get(current_type, current_type)
            inferred_display_type = self.dtype_display_mapping.get(inferred_type, inferred_type)
            
            columns_info.append({
                'name': column,
                'current_type': current_type,
                'current_display_type': current_display_type,
                'inferred_type': inferred_type,
                'inferred_display_type': inferred_display_type,
                'non_null_count': int(non_null_count),
                'null_count': int(null_count),
                'unique_count': int(unique_count),
                'sample_values': sample_values
            })
        
        # Get dataframe shape
        rows, cols = df.shape
        
        return {
            'total_rows': rows,
            'total_columns': cols,
            'memory_usage_bytes': int(original_memory),
            'columns': columns_info
        }

    def process_file(self, file_path:str, convert_to_inferred_type:bool = False) -> tuple[pd.DataFrame, dict]:
        """
        Process a data file to infer datatypes of the columns
        Attempt to convert them to the appropriate inferred type

        Args:
            file_path: Path to the data file
            
        Returns:
            Tuple containing the processed DataFrame and information dictionary
        """

        df = self.read_file(file_path)
        info_dict = self.get_dataframe_info(df)

        if convert_to_inferred_type:
            inferred_types = {col['name']: col['inferred_type'] for col in info_dict['columns']}
            df = self.convert_column_types(df, inferred_types)
            # Update info after conversion
            info_dict = self.get_dataframe_info(df)
        
        return df, info_dict
