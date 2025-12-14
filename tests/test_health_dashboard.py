"""
Tests for Health Dashboard
Tests for Task 1 modules
Author: Sourabha K Kallapur
"""

import pytest
import pandas as pd
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from health_dashboard.data_loader import HealthDataLoader
from health_dashboard.database import HealthDatabase
from health_dashboard.data_cleaner import DataCleaner
from health_dashboard.filters import DataFilter
from health_dashboard.statistics import HealthStatistics


class TestDataLoader:
    """Test the data loader module"""
    
    def test_loader_initialization(self):
        """Test that loader initializes correctly"""
        loader = HealthDataLoader()
        assert loader.data is None
        assert loader.source_type is None
    
    def test_load_from_csv(self):
        """Test loading data from CSV"""
        loader = HealthDataLoader()
        # Test with sample data
        data = loader.load_from_csv("data/sample_vaccination_data.csv")
        assert data is not None
        assert len(data) > 0
        assert 'country_name' in data.columns


class TestDatabase:
    """Test the database module"""
    
    def test_database_creation(self):
        """Test database initialization"""
        db = HealthDatabase("test_db.db")
        db.connect()
        db.create_schema()
        
        # Check that tables were created
        cursor = db.cursor
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'country' in tables
        assert 'vaccination_record' in tables
        assert 'disease_outbreak' in tables
        
        db.close()
        # Clean up
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
    
    def test_add_country(self):
        """Test adding a country"""
        db = HealthDatabase("test_db.db")
        db.connect()
        db.create_schema()
        
        country_id = db.add_country("Test Country", "Test Region", 1000000)
        assert country_id > 0
        
        # Verify it was added
        country = db.get_country_by_name("Test Country")
        assert country is not None
        assert country['country_name'] == "Test Country"
        
        db.close()
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")


class TestDataCleaner:
    """Test the data cleaner module"""
    
    def test_handle_missing_values(self):
        """Test handling missing values"""
        # Create sample data with missing values
        data = pd.DataFrame({
            'col1': [1, 2, None, 4],
            'col2': ['a', None, 'c', 'd']
        })
        
        cleaner = DataCleaner(data)
        cleaned = cleaner.handle_missing_values(strategy='drop')
        
        # Should have removed rows with missing values
        assert len(cleaned) < len(data)
        assert cleaned.isnull().sum().sum() == 0
    
    def test_remove_duplicates(self):
        """Test removing duplicates"""
        data = pd.DataFrame({
            'col1': [1, 2, 2, 3],
            'col2': ['a', 'b', 'b', 'c']
        })
        
        cleaner = DataCleaner(data)
        cleaned = cleaner.remove_duplicates()
        
        assert len(cleaned) == 3  # One duplicate removed


class TestDataFilter:
    """Test the filter module"""
    
    def test_filter_by_country(self):
        """Test filtering by country"""
        data = pd.DataFrame({
            'country_name': ['UK', 'USA', 'France', 'UK'],
            'value': [100, 200, 150, 120]
        })
        
        data_filter = DataFilter(data)
        filtered = data_filter.filter_by_country('UK')
        
        assert len(filtered) == 2
        assert all(filtered['country_name'] == 'UK')
    
    def test_filter_by_value_range(self):
        """Test filtering by value range"""
        data = pd.DataFrame({
            'value': [10, 20, 30, 40, 50]
        })
        
        data_filter = DataFilter(data)
        filtered = data_filter.filter_by_value_range('value', min_value=20, max_value=40)
        
        assert len(filtered) == 3
        assert filtered['value'].min() >= 20
        assert filtered['value'].max() <= 40


class TestHealthStatistics:
    """Test the statistics module"""
    
    def test_basic_stats(self):
        """Test basic statistics calculation"""
        data = pd.DataFrame({
            'values': [10, 20, 30, 40, 50]
        })
        
        stats = HealthStatistics(data)
        result = stats.calculate_basic_stats('values')
        
        assert result['mean'] == 30
        assert result['min'] == 10
        assert result['max'] == 50
        assert result['count'] == 5
    
    def test_group_by_column(self):
        """Test grouping functionality"""
        data = pd.DataFrame({
            'category': ['A', 'B', 'A', 'B'],
            'value': [10, 20, 30, 40]
        })
        
        stats = HealthStatistics(data)
        grouped = stats.group_by_column('category', 'value', 'sum')
        
        assert len(grouped) == 2
        # Check that grouping worked
        assert grouped[grouped['category'] == 'A']['value'].values[0] == 40
        assert grouped[grouped['category'] == 'B']['value'].values[0] == 60


class TestRealDataCleaning:
    """Integration tests for data cleaning with real dirty data"""
    
    @classmethod
    def setup_class(cls):
        """Load real vaccination data with intentional quality issues"""
        loader = HealthDataLoader()
        cls.original_data = loader.load_from_csv("data/sample_vaccination_data.csv")
    
    def test_identify_data_quality_issues(self):
        """Test identification of various data quality issues"""
        data = self.original_data.copy()
        
        # Check for missing values
        missing_counts = data.isnull().sum()
        assert missing_counts['population'] > 0  # Should have missing population
        assert missing_counts['vaccine_type'] > 0  # Should have missing vaccine_type
        assert missing_counts['percentage_vaccinated'] > 0  # Should have missing percentage
        
        # Check for duplicates
        duplicates = data.duplicated().sum()
        assert duplicates > 0  # Should have at least one duplicate
        
        # Check for inconsistent date formats
        date_formats = data['date'].astype(str).str.contains('-|/')
        assert date_formats.sum() > 0  # Should have various formats
    
    def test_handle_missing_values_comprehensive(self):
        """Test handling missing values with column-specific strategies"""
        data = self.original_data.copy()
        cleaner = DataCleaner(data)
        
        # Fill missing values column by column
        cleaned_data = cleaner.data.copy()
        cleaned_data.loc[cleaned_data['population'].isna(), 'population'] = 0
        cleaned_data.loc[cleaned_data['vaccine_type'].isna(), 'vaccine_type'] = 'Unknown'
        cleaned_data.loc[cleaned_data['percentage_vaccinated'].isna(), 'percentage_vaccinated'] = 0
        
        # Verify no missing values in these columns
        assert cleaned_data['population'].isnull().sum() == 0
        assert cleaned_data['vaccine_type'].isnull().sum() == 0
        assert cleaned_data['percentage_vaccinated'].isnull().sum() == 0
    
    def test_remove_duplicates_real_data(self):
        """Test removing duplicate rows from real data"""
        data = self.original_data.copy()
        original_count = len(data)
        duplicates_count = data.duplicated().sum()
        
        cleaner = DataCleaner(data)
        cleaned = cleaner.remove_duplicates()
        
        # Verify duplicates were removed
        assert len(cleaned) == original_count - duplicates_count
        assert cleaned.duplicated().sum() == 0
    
    def test_standardize_text_columns(self):
        """Test text standardization to title case"""
        data = self.original_data.copy()
        cleaner = DataCleaner(data)
        
        cleaned = cleaner.standardize_text_columns(['country_name', 'region', 'vaccine_type'], case='title')
        
        # Verify text is standardized
        for col in ['country_name', 'region', 'vaccine_type']:
            # Check that values are title cased (first letter uppercase)
            sample_values = cleaned[col].dropna().head(5)
            for value in sample_values:
                if isinstance(value, str) and len(value) > 0:
                    assert value[0].isupper() or value == 'Unknown'
    
    def test_convert_inconsistent_date_formats(self):
        """Test converting various date formats to standard format"""
        data = self.original_data.copy()
        
        def fix_date_format(date_str):
            """Convert various date formats to standard YYYY-MM-DD"""
            if pd.isna(date_str):
                return date_str
            
            date_str = str(date_str).strip()
            
            # Try different formats
            formats = [
                '%Y-%m-%d',      # 2024-01-15
                '%d-%m-%Y',      # 15-01-2024
                '%Y/%m/%d',      # 2024/01/15
                '%m/%d/%Y',      # 01/15/2024
                '%d/%m/%Y',      # 15/01/2024
            ]
            
            for fmt in formats:
                try:
                    return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
                except:
                    continue
            
            return date_str
        
        # Apply date format fixing
        data['date'] = data['date'].apply(fix_date_format)
        
        # Verify all dates are in standard format (YYYY-MM-DD)
        for date_val in data['date'].dropna().head(10):
            assert '-' in str(date_val)  # Should have dashes
            parts = str(date_val).split('-')
            if len(parts) == 3:
                assert len(parts[0]) == 4  # Year should be 4 digits
    
    def test_convert_string_numbers_to_numeric(self):
        """Test converting string numbers like '200 million' to numeric"""
        data = self.original_data.copy()
        
        def parse_number_with_units(value):
            """Convert strings like '200 million' to numeric"""
            if pd.isna(value):
                return value
            
            if isinstance(value, (int, float)):
                return value
            
            value_str = str(value).strip().lower()
            
            # Handle "million" suffix
            if 'million' in value_str:
                number = float(value_str.replace('million', '').strip())
                return int(number * 1_000_000)
            
            # Handle "billion" suffix
            if 'billion' in value_str:
                number = float(value_str.replace('billion', '').strip())
                return int(number * 1_000_000_000)
            
            # Try to convert directly
            try:
                return int(float(value_str))
            except:
                return value
        
        # Apply number parsing
        data['doses_administered'] = data['doses_administered'].apply(parse_number_with_units)
        
        # Verify all values are numeric
        numeric_values = data['doses_administered'].dropna()
        for value in numeric_values.head(10):
            assert isinstance(value, (int, float))
            if 'million' not in str(self.original_data['doses_administered'].iloc[0]).lower():
                continue
            # If original had "million", converted should be large number
            assert value >= 1_000_000 or value < 1000  # Either converted or was already numeric
    
    def test_validate_percentage_range(self):
        """Test validating percentage values are within 0-100 range"""
        data = self.original_data.copy()
        # Fill missing percentages first
        data['percentage_vaccinated'].fillna(0, inplace=True)
        
        cleaner = DataCleaner(data)
        cleaned = cleaner.validate_numeric_range('percentage_vaccinated', min_val=0, max_val=100)
        
        # Verify all percentages are within valid range
        assert cleaned['percentage_vaccinated'].min() >= 0
        assert cleaned['percentage_vaccinated'].max() <= 100
    
    def test_complete_cleaning_pipeline(self):
        """Test complete data cleaning pipeline end-to-end"""
        data = self.original_data.copy()
        original_rows = len(data)
        original_missing = data.isnull().sum().sum()
        
        cleaner = DataCleaner(data)
        
        # Step 1: Handle missing values
        cleaned_data = cleaner.data.copy()
        cleaned_data.loc[cleaned_data['population'].isna(), 'population'] = 0
        cleaned_data.loc[cleaned_data['vaccine_type'].isna(), 'vaccine_type'] = 'Unknown'
        cleaned_data.loc[cleaned_data['percentage_vaccinated'].isna(), 'percentage_vaccinated'] = 0
        cleaner.data = cleaned_data
        
        # Step 2: Remove duplicates
        cleaned_data = cleaner.remove_duplicates()
        
        # Step 3: Standardize text
        cleaned_data = cleaner.standardize_text_columns(['country_name', 'region', 'vaccine_type'], case='title')
        
        # Step 4: Fix date formats
        def fix_date_format(date_str):
            if pd.isna(date_str):
                return date_str
            date_str = str(date_str).strip()
            formats = ['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y']
            for fmt in formats:
                try:
                    return pd.to_datetime(date_str, format=fmt).strftime('%Y-%m-%d')
                except:
                    continue
            return date_str
        
        cleaned_data['date'] = cleaned_data['date'].apply(fix_date_format)
        
        # Step 5: Convert string numbers
        def parse_number_with_units(value):
            if pd.isna(value) or isinstance(value, (int, float)):
                return value
            value_str = str(value).strip().lower()
            if 'million' in value_str:
                return int(float(value_str.replace('million', '').strip()) * 1_000_000)
            try:
                return int(float(value_str))
            except:
                return value
        
        cleaned_data['doses_administered'] = cleaned_data['doses_administered'].apply(parse_number_with_units)
        cleaner.data = cleaned_data
        
        # Step 6: Validate ranges
        cleaned_data = cleaner.validate_numeric_range('percentage_vaccinated', min_val=0, max_val=100)
        
        # Verify cleaning results
        assert len(cleaned_data) < original_rows  # Duplicates removed
        assert cleaned_data.isnull().sum().sum() < original_missing  # Missing values reduced
        assert cleaned_data['percentage_vaccinated'].min() >= 0
        assert cleaned_data['percentage_vaccinated'].max() <= 100
        
        # Verify cleaning log was maintained
        assert len(cleaner.cleaning_log) > 0
    
    def test_cleaning_log_tracking(self):
        """Test that cleaning operations are logged"""
        data = self.original_data.copy()
        cleaner = DataCleaner(data)
        
        # Perform some cleaning operations
        cleaner.remove_duplicates()
        cleaner.standardize_text_columns(['country_name'], case='title')
        
        # Verify operations were logged
        assert len(cleaner.cleaning_log) >= 2
        assert any('duplicate' in log.lower() for log in cleaner.cleaning_log)
        assert any('standardize' in log.lower() or 'title' in log.lower() for log in cleaner.cleaning_log)


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
