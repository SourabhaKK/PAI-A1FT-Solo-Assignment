"""
CLI Module for Health Dashboard
Interactive command-line interface for the health data dashboard
Author: Sourabha K Kallapur
"""

import os
import sys
from datetime import datetime

# Import our custom modules
from health_dashboard.data_loader import HealthDataLoader
from health_dashboard.database import HealthDatabase
from health_dashboard.data_cleaner import DataCleaner
from health_dashboard.filters import DataFilter
from health_dashboard.statistics import HealthStatistics
from health_dashboard.visualizations import HealthVisualizer
from health_dashboard.export import DataExporter
from health_dashboard.logger import ActivityLogger


class HealthDashboardCLI:
    """
    Command-line interface for the Health Data Dashboard
    """
    
    def __init__(self):
        """Initialize the CLI"""
        self.loader = HealthDataLoader()
        self.db = HealthDatabase("health_data.db")
        self.logger = ActivityLogger()
        self.exporter = DataExporter()
        
        self.current_data = None
        self.filtered_data = None
        
        print("\n" + "=" * 60)
        print("HEALTH DATA INSIGHTS DASHBOARD")
        print("=" * 60)
        print("Welcome! This tool helps you analyze public health data.")
        print("=" * 60 + "\n")
        
        self.logger.log_user_action("CLI Started")
    
    def show_main_menu(self):
        """Display the main menu"""
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("-" * 60)
        print("1. Load Data")
        print("2. View Data")
        print("3. Filter Data")
        print("4. Calculate Statistics")
        print("5. Create Visualizations")
        print("6. Export Data")
        print("7. Database Operations")
        print("8. Exit")
        print("-" * 60)
    
    def load_data_menu(self):
        """Menu for loading data"""
        print("\n--- Load Data ---")
        print("1. Load from CSV file")
        print("2. Load from JSON file")
        print("3. Load from API")
        print("4. Load from Database")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            file_path = input("Enter CSV file path: ").strip()
            try:
                self.current_data = self.loader.load_from_csv(file_path)
                self.logger.log_data_load("CSV", len(self.current_data), file_path)
                print("\n✓ Data loaded successfully!")
                print(f"Loaded {len(self.current_data)} records")
            except Exception as e:
                print(f"\n✗ Error loading CSV: {e}")
                self.logger.log_error("Failed to load CSV", e)
        
        elif choice == '2':
            file_path = input("Enter JSON file path: ").strip()
            try:
                self.current_data = self.loader.load_from_json(file_path)
                self.logger.log_data_load("JSON", len(self.current_data), file_path)
                print("\n✓ Data loaded successfully!")
            except Exception as e:
                print(f"\n✗ Error loading JSON: {e}")
                self.logger.log_error("Failed to load JSON", e)
        
        elif choice == '3':
            api_url = input("Enter API URL: ").strip()
            try:
                self.current_data = self.loader.load_from_api(api_url)
                self.logger.log_data_load("API", len(self.current_data), api_url)
                print("\n✓ Data loaded successfully!")
            except Exception as e:
                print(f"\n✗ Error loading from API: {e}")
                self.logger.log_error("Failed to load from API", e)
        
        elif choice == '4':
            self.load_from_database()
    
    def load_from_database(self):
        """Load data from database"""
        print("\n--- Load from Database ---")
        print("1. Load all countries")
        print("2. Load vaccination records")
        print("3. Load disease outbreaks")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        try:
            self.db.connect()
            
            if choice == '1':
                self.current_data = self.db.get_all_countries()
                print(f"\n✓ Loaded {len(self.current_data)} countries")
            elif choice == '2':
                self.current_data = self.db.get_vaccination_records()
                print(f"\n✓ Loaded {len(self.current_data)} vaccination records")
            elif choice == '3':
                self.current_data = self.db.get_disease_outbreaks()
                print(f"\n✓ Loaded {len(self.current_data)} disease outbreak records")
            
            self.logger.log_database_operation("SELECT", "various", len(self.current_data))
            
        except Exception as e:
            print(f"\n✗ Error loading from database: {e}")
            self.logger.log_error("Database load failed", e)
        finally:
            self.db.close()
    
    def view_data_menu(self):
        """Menu for viewing data"""
        if self.current_data is None:
            print("\n✗ No data loaded. Please load data first.")
            return
        
        print("\n--- View Data ---")
        print(f"Total records: {len(self.current_data)}")
        print(f"Columns: {', '.join(self.current_data.columns)}")
        
        num_rows = input("\nHow many rows to display? (default: 10): ").strip()
        num_rows = int(num_rows) if num_rows else 10
        
        print("\n" + "=" * 60)
        print(self.current_data.head(num_rows).to_string())
        print("=" * 60)
        
        self.logger.log_user_action("Viewed data", f"{num_rows} rows")
    
    def filter_data_menu(self):
        """Menu for filtering data"""
        if self.current_data is None:
            print("\n✗ No data loaded. Please load data first.")
            return
        
        print("\n--- Filter Data ---")
        print("1. Filter by country")
        print("2. Filter by date range")
        print("3. Filter by value range")
        print("4. Reset filters")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        # Use filtered_data if it exists, otherwise use current_data
        data_to_filter = self.filtered_data if self.filtered_data is not None else self.current_data
        data_filter = DataFilter(data_to_filter)
        
        records_before = len(data_to_filter)
        
        if choice == '1':
            countries = input("Enter country name(s) (comma-separated): ").strip()
            country_list = [c.strip() for c in countries.split(',')]
            self.filtered_data = data_filter.filter_by_country(country_list)
            self.logger.log_filter_applied("country", countries, records_before, len(self.filtered_data))
        
        elif choice == '2':
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            self.filtered_data = data_filter.filter_by_date_range(start_date, end_date)
            self.logger.log_filter_applied("date_range", f"{start_date} to {end_date}", 
                                          records_before, len(self.filtered_data))
        
        elif choice == '3':
            column = input("Enter column name: ").strip()
            min_val = input("Enter minimum value (or press Enter to skip): ").strip()
            max_val = input("Enter maximum value (or press Enter to skip): ").strip()
            
            min_val = float(min_val) if min_val else None
            max_val = float(max_val) if max_val else None
            
            self.filtered_data = data_filter.filter_by_value_range(column, min_val, max_val)
            self.logger.log_filter_applied("value_range", column, records_before, len(self.filtered_data))
        
        elif choice == '4':
            self.filtered_data = None
            print("\n✓ Filters reset")
            self.logger.log_user_action("Reset filters")
    
    def statistics_menu(self):
        """Menu for calculating statistics"""
        if self.current_data is None:
            print("\n✗ No data loaded. Please load data first.")
            return
        
        # Use filtered data if available
        data_to_analyze = self.filtered_data if self.filtered_data is not None else self.current_data
        stats = HealthStatistics(data_to_analyze)
        
        print("\n--- Calculate Statistics ---")
        print("1. Basic statistics (mean, median, min, max)")
        print("2. Group by column")
        print("3. Trend over time")
        print("4. Top N records")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            column = input("Enter column name for statistics: ").strip()
            result = stats.calculate_basic_stats(column)
            print("\n--- Statistics ---")
            for key, value in result.items():
                print(f"{key}: {value}")
            self.logger.log_statistics_calculation("basic_stats", column, str(result))
        
        elif choice == '2':
            group_col = input("Enter column to group by: ").strip()
            value_col = input("Enter column to aggregate: ").strip()
            agg_type = input("Aggregation type (sum/mean/count): ").strip()
            
            result = stats.group_by_column(group_col, value_col, agg_type)
            print("\n--- Grouped Results ---")
            print(result.to_string())
            self.logger.log_user_action("Grouped statistics", f"{group_col} by {value_col}")
        
        elif choice == '3':
            date_col = input("Enter date column name: ").strip()
            value_col = input("Enter value column name: ").strip()
            freq = input("Frequency (D=daily, W=weekly, M=monthly): ").strip()
            
            result = stats.get_trend_over_time(date_col, value_col, freq)
            print("\n--- Trend Analysis ---")
            print(result.to_string())
            self.logger.log_user_action("Trend analysis", f"{value_col} over time")
        
        elif choice == '4':
            column = input("Enter column to sort by: ").strip()
            n = int(input("How many top records? ").strip())
            
            result = stats.get_top_n(column, n)
            print(f"\n--- Top {n} Records ---")
            print(result.to_string())
            self.logger.log_user_action("Top N query", f"Top {n} by {column}")
    
    def visualization_menu(self):
        """Menu for creating visualizations"""
        if self.current_data is None:
            print("\n✗ No data loaded. Please load data first.")
            return
        
        data_to_visualize = self.filtered_data if self.filtered_data is not None else self.current_data
        viz = HealthVisualizer(data_to_visualize)
        
        print("\n--- Create Visualizations ---")
        print("1. Line chart (trends over time)")
        print("2. Bar chart (comparisons)")
        print("3. Pie chart (distribution)")
        print("4. Create dashboard")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            x_col = input("Enter X-axis column (usually date): ").strip()
            y_col = input("Enter Y-axis column (values): ").strip()
            save = input("Save chart? (y/n): ").strip().lower()
            
            save_as = None
            if save == 'y':
                save_as = input("Enter filename: ").strip()
            
            viz.plot_line_chart(x_col, y_col, save_as=save_as)
            self.logger.log_visualization("line_chart", save_as)
        
        elif choice == '2':
            x_col = input("Enter X-axis column (categories): ").strip()
            y_col = input("Enter Y-axis column (values): ").strip()
            save = input("Save chart? (y/n): ").strip().lower()
            
            save_as = None
            if save == 'y':
                save_as = input("Enter filename: ").strip()
            
            viz.plot_bar_chart(x_col, y_col, save_as=save_as)
            self.logger.log_visualization("bar_chart", save_as)
        
        elif choice == '3':
            value_col = input("Enter values column: ").strip()
            label_col = input("Enter labels column: ").strip()
            save = input("Save chart? (y/n): ").strip().lower()
            
            save_as = None
            if save == 'y':
                save_as = input("Enter filename: ").strip()
            
            viz.plot_pie_chart(value_col, label_col, save_as=save_as)
            self.logger.log_visualization("pie_chart", save_as)
    
    def export_menu(self):
        """Menu for exporting data"""
        if self.current_data is None:
            print("\n✗ No data loaded. Please load data first.")
            return
        
        data_to_export = self.filtered_data if self.filtered_data is not None else self.current_data
        
        print("\n--- Export Data ---")
        print("1. Export to CSV")
        print("2. Export to JSON")
        print("3. Export summary report")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            filename = input("Enter filename (or press Enter for auto-generated): ").strip()
            filename = filename if filename else None
            
            filepath = self.exporter.export_to_csv(data_to_export, filename)
            self.logger.log_export("CSV", filepath, len(data_to_export))
        
        elif choice == '2':
            filename = input("Enter filename (or press Enter for auto-generated): ").strip()
            filename = filename if filename else None
            
            filepath = self.exporter.export_to_json(data_to_export, filename)
            self.logger.log_export("JSON", filepath, len(data_to_export))
        
        elif choice == '3':
            # Calculate some basic stats for the report
            stats = HealthStatistics(data_to_export)
            stats_dict = {}
            
            # Get stats for numeric columns
            numeric_cols = data_to_export.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
                col_stats = stats.calculate_basic_stats(col)
                stats_dict[f"{col}_mean"] = col_stats.get('mean', 'N/A')
            
            filepath = self.exporter.export_summary_report(data_to_export, stats_dict)
            self.logger.log_export("Summary Report", filepath, len(data_to_export))
    
    def database_menu(self):
        """Menu for database operations"""
        print("\n--- Database Operations ---")
        print("1. Create/Initialize database schema")
        print("2. Add country")
        print("3. Add vaccination record")
        print("4. View all countries")
        print("5. Import current data to database")
        print("6. Back to main menu")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        try:
            self.db.connect()
            
            if choice == '1':
                self.db.create_schema()
                print("\n✓ Database schema created successfully")
                self.logger.log_database_operation("CREATE SCHEMA", "all", None)
            
            elif choice == '2':
                name = input("Enter country name: ").strip()
                region = input("Enter region: ").strip()
                pop = input("Enter population: ").strip()
                
                country_id = self.db.add_country(name, region, int(pop) if pop else None)
                print(f"\n✓ Country added with ID: {country_id}")
                self.logger.log_database_operation("INSERT", "country", 1)
            
            elif choice == '3':
                country_id = int(input("Enter country ID: ").strip())
                date = input("Enter date (YYYY-MM-DD): ").strip()
                vaccine = input("Enter vaccine type: ").strip()
                doses = int(input("Enter doses administered: ").strip())
                
                record_id = self.db.add_vaccination_record(country_id, date, vaccine, doses)
                print(f"\n✓ Vaccination record added with ID: {record_id}")
                self.logger.log_database_operation("INSERT", "vaccination_record", 1)
            
            elif choice == '4':
                countries = self.db.get_all_countries()
                print("\n--- All Countries ---")
                print(countries.to_string())
            
            elif choice == '5':
                if self.current_data is not None:
                    # This is a simplified import - in reality you'd need to map columns properly
                    print("\n⚠ Note: This requires proper column mapping")
                    print("Current data columns:", list(self.current_data.columns))
                else:
                    print("\n✗ No data loaded to import")
        
        except Exception as e:
            print(f"\n✗ Database error: {e}")
            self.logger.log_error("Database operation failed", e)
        finally:
            self.db.close()
    
    def run(self):
        """Main loop for the CLI"""
        while True:
            self.show_main_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.load_data_menu()
            elif choice == '2':
                self.view_data_menu()
            elif choice == '3':
                self.filter_data_menu()
            elif choice == '4':
                self.statistics_menu()
            elif choice == '5':
                self.visualization_menu()
            elif choice == '6':
                self.export_menu()
            elif choice == '7':
                self.database_menu()
            elif choice == '8':
                print("\n" + "=" * 60)
                print("Thank you for using Health Data Insights Dashboard!")
                print("=" * 60)
                self.logger.log_session_end()
                break
            else:
                print("\n✗ Invalid choice. Please try again.")


# Main entry point
if __name__ == "__main__":
    cli = HealthDashboardCLI()
    cli.run()
