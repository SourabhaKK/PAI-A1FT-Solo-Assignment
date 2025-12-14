"""
Data Loader Module for Health Dashboard
This module handles loading data from various sources: CSV files, JSON files, and APIs
Author: Sourabha K Kallapur
"""

import pandas as pd
import json
import requests
from typing import Dict, List, Optional
import os


class HealthDataLoader:
    """
    A class to load health data from different sources.
    Supports CSV, JSON files, and API endpoints.
    """
    
    def __init__(self):
        """Initialize the data loader"""
        self.data = None
        self.source_type = None
    
    def load_from_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load data from a CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            DataFrame containing the loaded data
        """
        try:
            # Check if file exists first
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            # Read the CSV file using pandas
            self.data = pd.read_csv(file_path)
            self.source_type = "CSV"
            
            print(f"Successfully loaded {len(self.data)} records from CSV")
            return self.data
            
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            raise
    
    def load_from_json(self, file_path: str) -> pd.DataFrame:
        """
        Load data from a JSON file
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            DataFrame containing the loaded data
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"JSON file not found: {file_path}")
            
            # Open and read the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Convert JSON to DataFrame
            # Handle both list of records and nested structures
            if isinstance(json_data, list):
                self.data = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # If it's a dict, try to find the data array
                # Common patterns: {"data": [...]} or {"records": [...]}
                if 'data' in json_data:
                    self.data = pd.DataFrame(json_data['data'])
                elif 'records' in json_data:
                    self.data = pd.DataFrame(json_data['records'])
                else:
                    # Just convert the dict directly
                    self.data = pd.DataFrame([json_data])
            
            self.source_type = "JSON"
            print(f"Successfully loaded {len(self.data)} records from JSON")
            return self.data
            
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            raise
    
    def load_from_api(self, api_url: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        Load data from a public API endpoint
        
        Args:
            api_url: URL of the API endpoint
            params: Optional dictionary of query parameters
            
        Returns:
            DataFrame containing the loaded data
        """
        try:
            # Make GET request to the API
            print(f"Fetching data from API: {api_url}")
            response = requests.get(api_url, params=params, timeout=30)
            
            # Check if request was successful
            if response.status_code != 200:
                raise Exception(f"API request failed with status code: {response.status_code}")
            
            # Parse JSON response
            json_data = response.json()
            
            # Convert to DataFrame
            # Similar logic to load_from_json
            if isinstance(json_data, list):
                self.data = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # Try common data field names
                if 'data' in json_data:
                    self.data = pd.DataFrame(json_data['data'])
                elif 'records' in json_data:
                    self.data = pd.DataFrame(json_data['records'])
                elif 'results' in json_data:
                    self.data = pd.DataFrame(json_data['results'])
                else:
                    self.data = pd.DataFrame([json_data])
            
            self.source_type = "API"
            print(f"Successfully loaded {len(self.data)} records from API")
            return self.data
            
        except requests.exceptions.Timeout:
            print("Error: API request timed out")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            raise
        except Exception as e:
            print(f"Error loading data from API: {e}")
            raise
    
    def get_data_info(self) -> Dict:
        """
        Get information about the loaded data
        
        Returns:
            Dictionary with data information
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        info = {
            "source_type": self.source_type,
            "num_records": len(self.data),
            "num_columns": len(self.data.columns),
            "columns": list(self.data.columns),
            "memory_usage": f"{self.data.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        
        return info
    
    def preview_data(self, num_rows: int = 5) -> pd.DataFrame:
        """
        Preview the first few rows of loaded data
        
        Args:
            num_rows: Number of rows to display (default: 5)
            
        Returns:
            DataFrame with first n rows
        """
        if self.data is None:
            print("No data loaded yet")
            return None
        
        return self.data.head(num_rows)


# Example usage (for testing purposes)
if __name__ == "__main__":
    loader = HealthDataLoader()
    
    # Example: Load from CSV
    # data = loader.load_from_csv("data/sample_vaccination_data.csv")
    # print(loader.get_data_info())
    # print(loader.preview_data())
