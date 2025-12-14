"""
Filters Module for Health Dashboard
Provides filtering capabilities for health data
Author: Sourabha K Kallapur
"""

import pandas as pd
from datetime import datetime
from typing import List, Optional, Union


class DataFilter:
    """
    Provides various filtering operations on health data
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame
        
        Args:
            data: DataFrame to filter
        """
        self.original_data = data
        self.filtered_data = data.copy()
    
    def filter_by_country(self, countries: Union[str, List[str]]) -> pd.DataFrame:
        """
        Filter data by country name(s)
        
        Args:
            countries: Single country name or list of country names
            
        Returns:
            Filtered DataFrame
        """
        # Convert single country to list for uniform handling
        if isinstance(countries, str):
            countries = [countries]
        
        # Check if we have a country column
        country_col = None
        for col in self.filtered_data.columns:
            if 'country' in col.lower():
                country_col = col
                break
        
        if country_col is None:
            print("Warning: No country column found in data")
            return self.filtered_data
        
        # Filter the data
        self.filtered_data = self.filtered_data[
            self.filtered_data[country_col].isin(countries)
        ]
        
        print(f"Filtered to {len(self.filtered_data)} records for countries: {', '.join(countries)}")
        return self.filtered_data
    
    def filter_by_date_range(self, start_date: str, end_date: str,
                            date_column: str = None) -> pd.DataFrame:
        """
        Filter data by date range
        
        Args:
            start_date: Start date (format: 'YYYY-MM-DD')
            end_date: End date (format: 'YYYY-MM-DD')
            date_column: Name of the date column (auto-detected if not provided)
            
        Returns:
            Filtered DataFrame
        """
        # Find date column if not specified
        if date_column is None:
            for col in self.filtered_data.columns:
                if 'date' in col.lower():
                    date_column = col
                    break
        
        if date_column is None:
            print("Warning: No date column found in data")
            return self.filtered_data
        
        # Convert dates to datetime if they aren't already
        if self.filtered_data[date_column].dtype != 'datetime64[ns]':
            self.filtered_data[date_column] = pd.to_datetime(
                self.filtered_data[date_column]
            )
        
        # Convert input dates to datetime
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        # Filter the data
        self.filtered_data = self.filtered_data[
            (self.filtered_data[date_column] >= start) &
            (self.filtered_data[date_column] <= end)
        ]
        
        print(f"Filtered to {len(self.filtered_data)} records between {start_date} and {end_date}")
        return self.filtered_data
    
    def filter_by_value_range(self, column: str, min_value: float = None,
                             max_value: float = None) -> pd.DataFrame:
        """
        Filter data by numeric value range
        
        Args:
            column: Column name to filter
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
            
        Returns:
            Filtered DataFrame
        """
        if column not in self.filtered_data.columns:
            print(f"Warning: Column '{column}' not found")
            return self.filtered_data
        
        if min_value is not None:
            self.filtered_data = self.filtered_data[
                self.filtered_data[column] >= min_value
            ]
        
        if max_value is not None:
            self.filtered_data = self.filtered_data[
                self.filtered_data[column] <= max_value
            ]
        
        print(f"Filtered to {len(self.filtered_data)} records with {column} in range")
        return self.filtered_data
    
    def filter_by_region(self, regions: Union[str, List[str]]) -> pd.DataFrame:
        """
        Filter data by region(s)
        
        Args:
            regions: Single region name or list of region names
            
        Returns:
            Filtered DataFrame
        """
        # Convert single region to list
        if isinstance(regions, str):
            regions = [regions]
        
        # Find region column
        region_col = None
        for col in self.filtered_data.columns:
            if 'region' in col.lower():
                region_col = col
                break
        
        if region_col is None:
            print("Warning: No region column found in data")
            return self.filtered_data
        
        # Filter the data
        self.filtered_data = self.filtered_data[
            self.filtered_data[region_col].isin(regions)
        ]
        
        print(f"Filtered to {len(self.filtered_data)} records for regions: {', '.join(regions)}")
        return self.filtered_data
    
    def filter_by_disease(self, diseases: Union[str, List[str]]) -> pd.DataFrame:
        """
        Filter data by disease name(s)
        
        Args:
            diseases: Single disease name or list of disease names
            
        Returns:
            Filtered DataFrame
        """
        # Convert single disease to list
        if isinstance(diseases, str):
            diseases = [diseases]
        
        # Find disease column
        disease_col = None
        for col in self.filtered_data.columns:
            if 'disease' in col.lower():
                disease_col = col
                break
        
        if disease_col is None:
            print("Warning: No disease column found in data")
            return self.filtered_data
        
        # Filter the data
        self.filtered_data = self.filtered_data[
            self.filtered_data[disease_col].isin(diseases)
        ]
        
        print(f"Filtered to {len(self.filtered_data)} records for diseases: {', '.join(diseases)}")
        return self.filtered_data
    
    def filter_by_custom_condition(self, condition: str) -> pd.DataFrame:
        """
        Filter data using a custom pandas query condition
        
        Args:
            condition: Query string (e.g., "cases_reported > 1000")
            
        Returns:
            Filtered DataFrame
        """
        try:
            self.filtered_data = self.filtered_data.query(condition)
            print(f"Applied custom filter: {condition}")
            print(f"Result: {len(self.filtered_data)} records")
        except Exception as e:
            print(f"Error applying custom filter: {e}")
        
        return self.filtered_data
    
    def get_filtered_data(self) -> pd.DataFrame:
        """Return the filtered DataFrame"""
        return self.filtered_data
    
    def reset_filters(self) -> pd.DataFrame:
        """Reset to original unfiltered data"""
        self.filtered_data = self.original_data.copy()
        print("Filters reset to original data")
        return self.filtered_data
    
    def get_filter_summary(self) -> dict:
        """Get summary of current filter state"""
        return {
            'original_records': len(self.original_data),
            'filtered_records': len(self.filtered_data),
            'records_removed': len(self.original_data) - len(self.filtered_data),
            'percentage_remaining': (len(self.filtered_data) / len(self.original_data) * 100)
                                   if len(self.original_data) > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'country_name': ['UK', 'USA', 'France', 'UK', 'USA'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'cases': [100, 200, 150, 120, 250],
        'region': ['Europe', 'Americas', 'Europe', 'Europe', 'Americas']
    })
    
    print("Original data:")
    print(sample_data)
    
    # Create filter and apply multiple filters
    data_filter = DataFilter(sample_data)
    
    # Filter by country
    data_filter.filter_by_country(['UK', 'USA'])
    
    # Filter by date range
    data_filter.filter_by_date_range('2024-01-01', '2024-01-03')
    
    print("\nFiltered data:")
    print(data_filter.get_filtered_data())
    
    print("\nFilter summary:")
    print(data_filter.get_filter_summary())
