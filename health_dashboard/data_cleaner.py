"""
Data Cleaner Module for Health Dashboard
Handles data cleaning, validation, and type conversions
Author: Sourabha K Kallapur
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional


class DataCleaner:
    """
    Cleans and validates health data
    Handles missing values, type conversions, and data normalization
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame
        
        Args:
            data: DataFrame to clean
        """
        self.data = data.copy()  # Work on a copy to preserve original
        self.cleaning_log = []  # Keep track of cleaning operations
    
    def handle_missing_values(self, strategy: str = 'drop', 
                             fill_value=None) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Args:
            strategy: How to handle missing values ('drop', 'fill', 'forward_fill')
            fill_value: Value to use when strategy is 'fill'
            
        Returns:
            Cleaned DataFrame
        """
        missing_count = self.data.isnull().sum().sum()
        
        if missing_count == 0:
            print("No missing values found")
            return self.data
        
        print(f"Found {missing_count} missing values")
        
        if strategy == 'drop':
            # Drop rows with any missing values
            before_count = len(self.data)
            self.data = self.data.dropna()
            after_count = len(self.data)
            removed = before_count - after_count
            self.cleaning_log.append(f"Dropped {removed} rows with missing values")
            print(f"Dropped {removed} rows with missing values")
            
        elif strategy == 'fill':
            # Fill missing values with a specific value
            if fill_value is not None:
                self.data = self.data.fillna(fill_value)
                self.cleaning_log.append(f"Filled missing values with {fill_value}")
                print(f"Filled missing values with {fill_value}")
            else:
                # Fill numeric columns with mean, others with 'Unknown'
                for col in self.data.columns:
                    if self.data[col].dtype in ['float64', 'int64']:
                        mean_val = self.data[col].mean()
                        self.data[col].fillna(mean_val, inplace=True)
                    else:
                        self.data[col].fillna('Unknown', inplace=True)
                self.cleaning_log.append("Filled missing values with column-specific defaults")
                print("Filled missing values with defaults")
                
        elif strategy == 'forward_fill':
            # Forward fill - use previous value
            self.data = self.data.fillna(method='ffill')
            self.cleaning_log.append("Applied forward fill for missing values")
            print("Applied forward fill")
        
        return self.data
    
    def convert_date_columns(self, date_columns: List[str], 
                            date_format: str = None) -> pd.DataFrame:
        """
        Convert string columns to datetime format
        
        Args:
            date_columns: List of column names containing dates
            date_format: Optional date format string (e.g., '%Y-%m-%d')
            
        Returns:
            DataFrame with converted date columns
        """
        for col in date_columns:
            if col not in self.data.columns:
                print(f"Warning: Column '{col}' not found")
                continue
            
            try:
                if date_format:
                    self.data[col] = pd.to_datetime(self.data[col], format=date_format)
                else:
                    # Let pandas infer the format
                    self.data[col] = pd.to_datetime(self.data[col])
                
                self.cleaning_log.append(f"Converted '{col}' to datetime")
                print(f"Converted '{col}' to datetime")
                
            except Exception as e:
                print(f"Error converting '{col}' to datetime: {e}")
        
        return self.data
    
    def convert_numeric_columns(self, numeric_columns: List[str]) -> pd.DataFrame:
        """
        Convert columns to numeric type
        
        Args:
            numeric_columns: List of column names to convert to numeric
            
        Returns:
            DataFrame with converted numeric columns
        """
        for col in numeric_columns:
            if col not in self.data.columns:
                print(f"Warning: Column '{col}' not found")
                continue
            
            try:
                # Convert to numeric, coercing errors to NaN
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                self.cleaning_log.append(f"Converted '{col}' to numeric")
                print(f"Converted '{col}' to numeric")
                
            except Exception as e:
                print(f"Error converting '{col}' to numeric: {e}")
        
        return self.data
    
    def remove_duplicates(self, subset: List[str] = None) -> pd.DataFrame:
        """
        Remove duplicate rows
        
        Args:
            subset: Optional list of columns to consider for duplicates
            
        Returns:
            DataFrame with duplicates removed
        """
        before_count = len(self.data)
        
        if subset:
            self.data = self.data.drop_duplicates(subset=subset)
        else:
            self.data = self.data.drop_duplicates()
        
        after_count = len(self.data)
        removed = before_count - after_count
        
        if removed > 0:
            self.cleaning_log.append(f"Removed {removed} duplicate rows")
            print(f"Removed {removed} duplicate rows")
        else:
            print("No duplicates found")
        
        return self.data
    
    def standardize_text_columns(self, text_columns: List[str],
                                case: str = 'title') -> pd.DataFrame:
        """
        Standardize text in specified columns
        
        Args:
            text_columns: List of column names containing text
            case: How to standardize ('lower', 'upper', 'title')
            
        Returns:
            DataFrame with standardized text
        """
        for col in text_columns:
            if col not in self.data.columns:
                print(f"Warning: Column '{col}' not found")
                continue
            
            try:
                if case == 'lower':
                    self.data[col] = self.data[col].str.lower()
                elif case == 'upper':
                    self.data[col] = self.data[col].str.upper()
                elif case == 'title':
                    self.data[col] = self.data[col].str.title()
                
                # Also strip whitespace
                self.data[col] = self.data[col].str.strip()
                
                self.cleaning_log.append(f"Standardized text in '{col}' to {case} case")
                print(f"Standardized '{col}' to {case} case")
                
            except Exception as e:
                print(f"Error standardizing '{col}': {e}")
        
        return self.data
    
    def validate_numeric_range(self, column: str, min_val: float = None,
                              max_val: float = None) -> pd.DataFrame:
        """
        Validate that numeric values are within a specified range
        
        Args:
            column: Column name to validate
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value
            
        Returns:
            DataFrame with invalid values removed or flagged
        """
        if column not in self.data.columns:
            print(f"Warning: Column '{column}' not found")
            return self.data
        
        before_count = len(self.data)
        
        if min_val is not None:
            self.data = self.data[self.data[column] >= min_val]
        
        if max_val is not None:
            self.data = self.data[self.data[column] <= max_val]
        
        after_count = len(self.data)
        removed = before_count - after_count
        
        if removed > 0:
            self.cleaning_log.append(
                f"Removed {removed} rows with out-of-range values in '{column}'"
            )
            print(f"Removed {removed} rows with invalid range in '{column}'")
        
        return self.data
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Return the cleaned DataFrame"""
        return self.data
    
    def get_cleaning_summary(self) -> List[str]:
        """Return a summary of all cleaning operations performed"""
        return self.cleaning_log
    
    def print_cleaning_summary(self):
        """Print a summary of cleaning operations"""
        print("\n=== Data Cleaning Summary ===")
        if not self.cleaning_log:
            print("No cleaning operations performed")
        else:
            for i, operation in enumerate(self.cleaning_log, 1):
                print(f"{i}. {operation}")
        print("=" * 30)


# Helper function for quick cleaning
def quick_clean_health_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform standard cleaning operations on health data
    
    Args:
        df: DataFrame to clean
        
    Returns:
        Cleaned DataFrame
    """
    cleaner = DataCleaner(df)
    
    # Remove duplicates
    cleaner.remove_duplicates()
    
    # Handle missing values (fill with defaults)
    cleaner.handle_missing_values(strategy='fill')
    
    # Try to identify and convert date columns
    date_like_columns = [col for col in df.columns 
                        if 'date' in col.lower() or 'time' in col.lower()]
    if date_like_columns:
        cleaner.convert_date_columns(date_like_columns)
    
    cleaner.print_cleaning_summary()
    
    return cleaner.get_cleaned_data()


# Example usage
if __name__ == "__main__":
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'country': ['UK', 'usa', 'FRANCE', 'UK'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-01'],
        'cases': [100, 200, None, 100],
        'deaths': [10, 20, 5, 10]
    })
    
    print("Original data:")
    print(sample_data)
    
    cleaner = DataCleaner(sample_data)
    cleaner.standardize_text_columns(['country'], case='title')
    cleaner.remove_duplicates()
    cleaner.handle_missing_values(strategy='fill', fill_value=0)
    cleaner.convert_date_columns(['date'])
    
    print("\nCleaned data:")
    print(cleaner.get_cleaned_data())
    cleaner.print_cleaning_summary()
