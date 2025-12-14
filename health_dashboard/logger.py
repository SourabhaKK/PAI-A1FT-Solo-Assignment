"""
Logger Module for Health Dashboard
Handles activity logging and error tracking
Author: Sourabha K Kallapur
"""

import logging
import os
from datetime import datetime
from typing import Optional


class ActivityLogger:
    """
    Logs user activities and system events
    """
    
    def __init__(self, log_dir: str = "logs", log_file: str = None):
        """
        Initialize logger
        
        Args:
            log_dir: Directory to store log files
            log_file: Name of log file (auto-generated if not provided)
        """
        self.log_dir = log_dir
        
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Generate log filename if not provided
        if log_file is None:
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = f"health_dashboard_{date_str}.log"
        
        self.log_file = os.path.join(log_dir, log_file)
        
        # Set up logging configuration
        self.logger = logging.getLogger('HealthDashboard')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler for important messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log initialization
        self.logger.info("=" * 60)
        self.logger.info("Health Dashboard Logger Initialized")
        self.logger.info(f"Log file: {self.log_file}")
        self.logger.info("=" * 60)
    
    def log_data_load(self, source_type: str, record_count: int, source_path: str = None):
        """
        Log data loading activity
        
        Args:
            source_type: Type of source (CSV, JSON, API)
            record_count: Number of records loaded
            source_path: Path or URL of the source
        """
        message = f"Data loaded from {source_type}"
        if source_path:
            message += f" ({source_path})"
        message += f" - {record_count} records"
        
        self.logger.info(message)
    
    def log_filter_applied(self, filter_type: str, filter_value: str, 
                          records_before: int, records_after: int):
        """
        Log filter application
        
        Args:
            filter_type: Type of filter (country, date, etc.)
            filter_value: Value used for filtering
            records_before: Record count before filter
            records_after: Record count after filter
        """
        message = (f"Filter applied - Type: {filter_type}, "
                  f"Value: {filter_value}, "
                  f"Records: {records_before} -> {records_after}")
        
        self.logger.info(message)
    
    def log_database_operation(self, operation: str, table: str, 
                              record_count: int = None):
        """
        Log database operations
        
        Args:
            operation: Type of operation (INSERT, UPDATE, DELETE, SELECT)
            table: Table name
            record_count: Number of records affected
        """
        message = f"Database {operation} on table '{table}'"
        if record_count:
            message += f" - {record_count} records"
        
        self.logger.info(message)
    
    def log_export(self, export_format: str, filename: str, record_count: int):
        """
        Log data export
        
        Args:
            export_format: Format of export (CSV, JSON, etc.)
            filename: Name of exported file
            record_count: Number of records exported
        """
        message = (f"Data exported to {export_format} - "
                  f"File: {filename}, Records: {record_count}")
        
        self.logger.info(message)
    
    def log_visualization(self, chart_type: str, filename: str = None):
        """
        Log visualization creation
        
        Args:
            chart_type: Type of chart (line, bar, pie, etc.)
            filename: Filename if saved
        """
        message = f"Visualization created - Type: {chart_type}"
        if filename:
            message += f", Saved as: {filename}"
        
        self.logger.info(message)
    
    def log_user_action(self, action: str, details: str = None):
        """
        Log general user action
        
        Args:
            action: Description of the action
            details: Additional details
        """
        message = f"User action: {action}"
        if details:
            message += f" - {details}"
        
        self.logger.info(message)
    
    def log_error(self, error_message: str, exception: Exception = None):
        """
        Log an error
        
        Args:
            error_message: Description of the error
            exception: Exception object if available
        """
        if exception:
            self.logger.error(f"{error_message} - Exception: {str(exception)}")
        else:
            self.logger.error(error_message)
    
    def log_warning(self, warning_message: str):
        """
        Log a warning
        
        Args:
            warning_message: Warning message
        """
        self.logger.warning(warning_message)
    
    def log_statistics_calculation(self, stat_type: str, column: str, result: str):
        """
        Log statistics calculation
        
        Args:
            stat_type: Type of statistic (mean, median, etc.)
            column: Column being analyzed
            result: Result of calculation
        """
        message = f"Statistics calculated - {stat_type} of '{column}': {result}"
        self.logger.info(message)
    
    def log_session_end(self):
        """Log end of session"""
        self.logger.info("=" * 60)
        self.logger.info("Session ended")
        self.logger.info("=" * 60)
    
    def get_log_file_path(self) -> str:
        """Return path to the log file"""
        return self.log_file


# Example usage
if __name__ == "__main__":
    logger = ActivityLogger()
    
    # Test logging
    logger.log_data_load("CSV", 1000, "data/sample.csv")
    logger.log_filter_applied("country", "UK", 1000, 500)
    logger.log_export("CSV", "export.csv", 500)
    logger.log_session_end()
