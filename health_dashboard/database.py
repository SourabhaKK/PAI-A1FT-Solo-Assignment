"""
Database Module for Health Dashboard
Handles SQLite database operations including schema creation and CRUD operations
Author: Sourabha K Kallapur
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Optional, Tuple
import os


class HealthDatabase:
    """
    Manages SQLite database for health data storage
    Implements CRUD operations for countries, vaccination records, and disease outbreaks
    """
    
    def __init__(self, db_path: str = "health_data.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def create_schema(self):
        """
        Create database schema with tables for countries, vaccination records,
        and disease outbreaks
        """
        try:
            # Create Country table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS country (
                    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_name TEXT NOT NULL UNIQUE,
                    region TEXT,
                    population INTEGER
                )
            ''')
            
            # Create Vaccination Record table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vaccination_record (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    vaccine_type TEXT,
                    doses_administered INTEGER,
                    population_vaccinated INTEGER,
                    percentage_vaccinated REAL,
                    FOREIGN KEY (country_id) REFERENCES country(country_id)
                )
            ''')
            
            # Create Disease Outbreak table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS disease_outbreak (
                    outbreak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_id INTEGER NOT NULL,
                    disease_name TEXT NOT NULL,
                    date_reported TEXT NOT NULL,
                    cases_reported INTEGER,
                    deaths_reported INTEGER,
                    recovery_rate REAL,
                    FOREIGN KEY (country_id) REFERENCES country(country_id)
                )
            ''')
            
            # Create indexes for better query performance
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_vaccination_date 
                ON vaccination_record(date)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_outbreak_date 
                ON disease_outbreak(date_reported)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_country_name 
                ON country(country_name)
            ''')
            
            self.conn.commit()
            print("Database schema created successfully")
            
        except sqlite3.Error as e:
            print(f"Error creating schema: {e}")
            raise
    
    # ===== CREATE Operations =====
    
    def add_country(self, country_name: str, region: str = None, 
                   population: int = None) -> int:
        """
        Add a new country to the database
        
        Args:
            country_name: Name of the country
            region: Geographic region
            population: Population count
            
        Returns:
            ID of the inserted country
        """
        try:
            self.cursor.execute('''
                INSERT INTO country (country_name, region, population)
                VALUES (?, ?, ?)
            ''', (country_name, region, population))
            
            self.conn.commit()
            country_id = self.cursor.lastrowid
            print(f"Added country: {country_name} (ID: {country_id})")
            return country_id
            
        except sqlite3.IntegrityError:
            # Country already exists, get its ID
            self.cursor.execute(
                'SELECT country_id FROM country WHERE country_name = ?',
                (country_name,)
            )
            result = self.cursor.fetchone()
            if result:
                return result[0]
            raise
        except sqlite3.Error as e:
            print(f"Error adding country: {e}")
            raise
    
    def add_vaccination_record(self, country_id: int, date: str, 
                              vaccine_type: str = None,
                              doses_administered: int = None,
                              population_vaccinated: int = None,
                              percentage_vaccinated: float = None) -> int:
        """
        Add a vaccination record
        
        Args:
            country_id: ID of the country
            date: Date of the record
            vaccine_type: Type of vaccine
            doses_administered: Number of doses given
            population_vaccinated: Number of people vaccinated
            percentage_vaccinated: Percentage of population vaccinated
            
        Returns:
            ID of the inserted record
        """
        try:
            self.cursor.execute('''
                INSERT INTO vaccination_record 
                (country_id, date, vaccine_type, doses_administered, 
                 population_vaccinated, percentage_vaccinated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (country_id, date, vaccine_type, doses_administered,
                  population_vaccinated, percentage_vaccinated))
            
            self.conn.commit()
            record_id = self.cursor.lastrowid
            print(f"Added vaccination record (ID: {record_id})")
            return record_id
            
        except sqlite3.Error as e:
            print(f"Error adding vaccination record: {e}")
            raise
    
    def add_disease_outbreak(self, country_id: int, disease_name: str,
                            date_reported: str, cases_reported: int = None,
                            deaths_reported: int = None,
                            recovery_rate: float = None) -> int:
        """
        Add a disease outbreak record
        
        Args:
            country_id: ID of the country
            disease_name: Name of the disease
            date_reported: Date the outbreak was reported
            cases_reported: Number of cases
            deaths_reported: Number of deaths
            recovery_rate: Recovery rate (0-100)
            
        Returns:
            ID of the inserted record
        """
        try:
            self.cursor.execute('''
                INSERT INTO disease_outbreak 
                (country_id, disease_name, date_reported, cases_reported,
                 deaths_reported, recovery_rate)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (country_id, disease_name, date_reported, cases_reported,
                  deaths_reported, recovery_rate))
            
            self.conn.commit()
            outbreak_id = self.cursor.lastrowid
            print(f"Added disease outbreak record (ID: {outbreak_id})")
            return outbreak_id
            
        except sqlite3.Error as e:
            print(f"Error adding disease outbreak: {e}")
            raise
    
    # ===== READ Operations =====
    
    def get_all_countries(self) -> pd.DataFrame:
        """Get all countries from the database"""
        query = "SELECT * FROM country"
        return pd.read_sql_query(query, self.conn)
    
    def get_country_by_name(self, country_name: str) -> Optional[Dict]:
        """Get a specific country by name"""
        self.cursor.execute(
            'SELECT * FROM country WHERE country_name = ?',
            (country_name,)
        )
        result = self.cursor.fetchone()
        
        if result:
            return {
                'country_id': result[0],
                'country_name': result[1],
                'region': result[2],
                'population': result[3]
            }
        return None
    
    def get_vaccination_records(self, country_id: int = None) -> pd.DataFrame:
        """
        Get vaccination records, optionally filtered by country
        
        Args:
            country_id: Optional country ID to filter by
        """
        if country_id:
            query = '''
                SELECT vr.*, c.country_name 
                FROM vaccination_record vr
                JOIN country c ON vr.country_id = c.country_id
                WHERE vr.country_id = ?
            '''
            return pd.read_sql_query(query, self.conn, params=(country_id,))
        else:
            query = '''
                SELECT vr.*, c.country_name 
                FROM vaccination_record vr
                JOIN country c ON vr.country_id = c.country_id
            '''
            return pd.read_sql_query(query, self.conn)
    
    def get_disease_outbreaks(self, country_id: int = None) -> pd.DataFrame:
        """
        Get disease outbreak records, optionally filtered by country
        
        Args:
            country_id: Optional country ID to filter by
        """
        if country_id:
            query = '''
                SELECT do.*, c.country_name 
                FROM disease_outbreak do
                JOIN country c ON do.country_id = c.country_id
                WHERE do.country_id = ?
            '''
            return pd.read_sql_query(query, self.conn, params=(country_id,))
        else:
            query = '''
                SELECT do.*, c.country_name 
                FROM disease_outbreak do
                JOIN country c ON do.country_id = c.country_id
            '''
            return pd.read_sql_query(query, self.conn)
    
    # ===== UPDATE Operations =====
    
    def update_country(self, country_id: int, region: str = None,
                      population: int = None):
        """Update country information"""
        try:
            if region:
                self.cursor.execute(
                    'UPDATE country SET region = ? WHERE country_id = ?',
                    (region, country_id)
                )
            if population:
                self.cursor.execute(
                    'UPDATE country SET population = ? WHERE country_id = ?',
                    (population, country_id)
                )
            
            self.conn.commit()
            print(f"Updated country ID: {country_id}")
            
        except sqlite3.Error as e:
            print(f"Error updating country: {e}")
            raise
    
    # ===== DELETE Operations =====
    
    def delete_country(self, country_id: int):
        """Delete a country and all related records"""
        try:
            # Delete related vaccination records first
            self.cursor.execute(
                'DELETE FROM vaccination_record WHERE country_id = ?',
                (country_id,)
            )
            
            # Delete related disease outbreak records
            self.cursor.execute(
                'DELETE FROM disease_outbreak WHERE country_id = ?',
                (country_id,)
            )
            
            # Delete the country
            self.cursor.execute(
                'DELETE FROM country WHERE country_id = ?',
                (country_id,)
            )
            
            self.conn.commit()
            print(f"Deleted country ID: {country_id} and all related records")
            
        except sqlite3.Error as e:
            print(f"Error deleting country: {e}")
            raise
    
    def delete_vaccination_record(self, record_id: int):
        """Delete a vaccination record"""
        try:
            self.cursor.execute(
                'DELETE FROM vaccination_record WHERE record_id = ?',
                (record_id,)
            )
            self.conn.commit()
            print(f"Deleted vaccination record ID: {record_id}")
            
        except sqlite3.Error as e:
            print(f"Error deleting vaccination record: {e}")
            raise
    
    def bulk_insert_from_dataframe(self, df: pd.DataFrame, table_name: str):
        """
        Insert multiple records from a DataFrame
        
        Args:
            df: DataFrame containing the data
            table_name: Name of the table to insert into
        """
        try:
            df.to_sql(table_name, self.conn, if_exists='append', index=False)
            print(f"Inserted {len(df)} records into {table_name}")
        except Exception as e:
            print(f"Error in bulk insert: {e}")
            raise


# Example usage
if __name__ == "__main__":
    db = HealthDatabase("test_health.db")
    db.connect()
    db.create_schema()
    
    # Test adding a country
    # country_id = db.add_country("United Kingdom", "Europe", 67000000)
    
    db.close()
