"""
Statistics Module for Health Dashboard
Provides statistical analysis and summary calculations
Author: Sourabha K Kallapur
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class HealthStatistics:
    """
    Calculate various statistics on health data
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame
        
        Args:
            data: DataFrame to analyze
        """
        self.data = data
    
    def calculate_basic_stats(self, column: str) -> Dict:
        """
        Calculate basic statistics for a numeric column
        
        Args:
            column: Name of the column to analyze
            
        Returns:
            Dictionary with mean, median, min, max, std
        """
        if column not in self.data.columns:
            return {"error": f"Column '{column}' not found"}
        
        # Make sure it's numeric
        if self.data[column].dtype not in ['int64', 'float64']:
            return {"error": f"Column '{column}' is not numeric"}
        
        stats = {
            'mean': self.data[column].mean(),
            'median': self.data[column].median(),
            'min': self.data[column].min(),
            'max': self.data[column].max(),
            'std': self.data[column].std(),
            'count': self.data[column].count(),
            'sum': self.data[column].sum()
        }
        
        return stats
    
    def get_trend_over_time(self, date_column: str, value_column: str,
                           freq: str = 'D') -> pd.DataFrame:
        """
        Calculate trends over time
        
        Args:
            date_column: Name of the date column
            value_column: Name of the value column to track
            freq: Frequency for grouping ('D'=daily, 'W'=weekly, 'M'=monthly)
            
        Returns:
            DataFrame with time-based aggregation
        """
        # Make sure date column is datetime
        if self.data[date_column].dtype != 'datetime64[ns]':
            self.data[date_column] = pd.to_datetime(self.data[date_column])
        
        # Set date as index temporarily
        temp_df = self.data.set_index(date_column)
        
        # Resample based on frequency and calculate sum
        trend = temp_df[value_column].resample(freq).sum().reset_index()
        
        return trend
    
    def group_by_column(self, group_column: str, value_column: str,
                       aggregation: str = 'sum') -> pd.DataFrame:
        """
        Group data by a column and aggregate values
        
        Args:
            group_column: Column to group by (e.g., 'country')
            value_column: Column to aggregate
            aggregation: Type of aggregation ('sum', 'mean', 'count', 'max', 'min')
            
        Returns:
            DataFrame with grouped results
        """
        if aggregation == 'sum':
            result = self.data.groupby(group_column)[value_column].sum().reset_index()
        elif aggregation == 'mean':
            result = self.data.groupby(group_column)[value_column].mean().reset_index()
        elif aggregation == 'count':
            result = self.data.groupby(group_column)[value_column].count().reset_index()
        elif aggregation == 'max':
            result = self.data.groupby(group_column)[value_column].max().reset_index()
        elif aggregation == 'min':
            result = self.data.groupby(group_column)[value_column].min().reset_index()
        else:
            result = self.data.groupby(group_column)[value_column].sum().reset_index()
        
        # Sort by value in descending order
        result = result.sort_values(by=value_column, ascending=False)
        
        return result
    
    def calculate_percentage_change(self, date_column: str, value_column: str) -> pd.DataFrame:
        """
        Calculate percentage change over time
        
        Args:
            date_column: Name of the date column
            value_column: Name of the value column
            
        Returns:
            DataFrame with percentage change column added
        """
        # Sort by date first
        sorted_data = self.data.sort_values(by=date_column).copy()
        
        # Calculate percentage change
        sorted_data['pct_change'] = sorted_data[value_column].pct_change() * 100
        
        return sorted_data
    
    def get_top_n(self, column: str, n: int = 10, ascending: bool = False) -> pd.DataFrame:
        """
        Get top N records based on a column value
        
        Args:
            column: Column to sort by
            n: Number of records to return
            ascending: If True, get bottom N instead of top N
            
        Returns:
            DataFrame with top N records
        """
        sorted_data = self.data.sort_values(by=column, ascending=ascending)
        return sorted_data.head(n)
    
    def calculate_correlation(self, col1: str, col2: str) -> float:
        """
        Calculate correlation between two numeric columns
        
        Args:
            col1: First column name
            col2: Second column name
            
        Returns:
            Correlation coefficient
        """
        if col1 not in self.data.columns or col2 not in self.data.columns:
            print("Error: One or both columns not found")
            return None
        
        correlation = self.data[col1].corr(self.data[col2])
        return correlation
    
    def get_summary_by_group(self, group_column: str) -> pd.DataFrame:
        """
        Get comprehensive summary statistics grouped by a column
        
        Args:
            group_column: Column to group by
            
        Returns:
            DataFrame with summary statistics for each group
        """
        # Get numeric columns only
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Group and calculate multiple aggregations
        summary = self.data.groupby(group_column)[numeric_cols].agg([
            'count', 'mean', 'sum', 'min', 'max'
        ])
        
        return summary
    
    def calculate_moving_average(self, column: str, window: int = 7) -> pd.Series:
        """
        Calculate moving average for a column
        
        Args:
            column: Column name
            window: Window size for moving average (default: 7 days)
            
        Returns:
            Series with moving average values
        """
        return self.data[column].rolling(window=window).mean()


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'country': ['UK', 'USA', 'France', 'UK', 'USA'],
        'date': pd.date_range('2024-01-01', periods=5),
        'cases': [100, 200, 150, 120, 250],
        'deaths': [10, 20, 15, 12, 25]
    })
    
    stats = HealthStatistics(sample_data)
    
    # Test basic statistics
    print("Basic stats for cases:")
    print(stats.calculate_basic_stats('cases'))
    
    # Test grouping
    print("\nCases by country:")
    print(stats.group_by_column('country', 'cases', 'sum'))
