"""
Export Module for Health Dashboard
Handles exporting data to various formats
Author: Sourabha K Kallapur
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Optional


class DataExporter:
    """
    Export health data to different formats
    """
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize exporter
        
        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
    
    def export_to_csv(self, data: pd.DataFrame, filename: str = None) -> str:
        """
        Export data to CSV file
        
        Args:
            data: DataFrame to export
            filename: Name of the output file (auto-generated if not provided)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_data_export_{timestamp}.csv"
        
        # Make sure filename ends with .csv
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            data.to_csv(filepath, index=False)
            print(f"Data exported to CSV: {filepath}")
            print(f"Exported {len(data)} records with {len(data.columns)} columns")
            return filepath
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            raise
    
    def export_to_json(self, data: pd.DataFrame, filename: str = None,
                      orient: str = 'records') -> str:
        """
        Export data to JSON file
        
        Args:
            data: DataFrame to export
            filename: Name of the output file
            orient: JSON orientation ('records', 'index', 'columns')
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_data_export_{timestamp}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            data.to_json(filepath, orient=orient, indent=2)
            print(f"Data exported to JSON: {filepath}")
            print(f"Exported {len(data)} records")
            return filepath
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            raise
    
    def export_summary_report(self, data: pd.DataFrame, stats_dict: dict,
                             filename: str = None) -> str:
        """
        Export a formatted summary report as text file
        
        Args:
            data: DataFrame being summarized
            stats_dict: Dictionary with statistics
            filename: Name of the output file
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_report_{timestamp}.txt"
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("HEALTH DATA SUMMARY REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Records: {len(data)}\n")
                f.write(f"Total Columns: {len(data.columns)}\n")
                f.write("\n")
                
                f.write("COLUMNS:\n")
                f.write("-" * 60 + "\n")
                for col in data.columns:
                    f.write(f"  - {col}\n")
                f.write("\n")
                
                f.write("STATISTICS:\n")
                f.write("-" * 60 + "\n")
                for key, value in stats_dict.items():
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
                
                f.write("DATA PREVIEW (First 10 rows):\n")
                f.write("-" * 60 + "\n")
                f.write(data.head(10).to_string())
                f.write("\n\n")
                
                f.write("=" * 60 + "\n")
                f.write("END OF REPORT\n")
                f.write("=" * 60 + "\n")
            
            print(f"Summary report exported: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error exporting summary report: {e}")
            raise
    
    def export_filtered_data(self, data: pd.DataFrame, filter_description: str,
                            format: str = 'csv', filename: str = None) -> str:
        """
        Export filtered data with description
        
        Args:
            data: Filtered DataFrame
            filter_description: Description of filters applied
            format: Export format ('csv' or 'json')
            filename: Name of the output file
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"filtered_data_{timestamp}"
        
        # Add metadata as a comment or separate file
        metadata = {
            'filter_description': filter_description,
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'record_count': len(data)
        }
        
        # Save metadata
        metadata_file = os.path.join(self.output_dir, f"{filename}_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Export data
        if format == 'csv':
            return self.export_to_csv(data, filename)
        elif format == 'json':
            return self.export_to_json(data, filename)
        else:
            print(f"Unknown format: {format}. Using CSV.")
            return self.export_to_csv(data, filename)


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'country': ['UK', 'USA', 'France'],
        'cases': [100, 200, 150],
        'deaths': [10, 20, 15]
    })
    
    exporter = DataExporter()
    
    # Test CSV export
    # exporter.export_to_csv(sample_data, "test_export.csv")
    
    # Test summary report
    # stats = {'mean_cases': 150, 'total_deaths': 45}
    # exporter.export_summary_report(sample_data, stats)
