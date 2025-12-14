"""
Visualizations Module for Health Dashboard
Creates charts and graphs using matplotlib
Author: Sourabha K Kallapur
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional, List
import os


class HealthVisualizer:
    """
    Create visualizations for health data
    """
    
    def __init__(self, data: pd.DataFrame, output_dir: str = "outputs"):
        """
        Initialize visualizer
        
        Args:
            data: DataFrame to visualize
            output_dir: Directory to save charts
        """
        self.data = data
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style for better-looking plots
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_line_chart(self, x_column: str, y_column: str,
                       title: str = None, save_as: str = None):
        """
        Create a line chart showing trends over time
        
        Args:
            x_column: Column for x-axis (usually date)
            y_column: Column for y-axis (values)
            title: Chart title
            save_as: Filename to save chart (optional)
        """
        plt.figure(figsize=(10, 6))
        
        plt.plot(self.data[x_column], self.data[y_column], 
                marker='o', linewidth=2, markersize=6)
        
        plt.xlabel(x_column.replace('_', ' ').title(), fontsize=12)
        plt.ylabel(y_column.replace('_', ' ').title(), fontsize=12)
        
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title(f'{y_column.replace("_", " ").title()} Over Time', 
                     fontsize=14, fontweight='bold')
        
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_as:
            filepath = os.path.join(self.output_dir, save_as)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {filepath}")
        
        plt.show()
    
    def plot_bar_chart(self, x_column: str, y_column: str,
                      title: str = None, save_as: str = None,
                      top_n: int = None):
        """
        Create a bar chart for comparisons
        
        Args:
            x_column: Column for x-axis (categories)
            y_column: Column for y-axis (values)
            title: Chart title
            save_as: Filename to save chart
            top_n: Show only top N items
        """
        # Prepare data
        plot_data = self.data.copy()
        
        if top_n:
            plot_data = plot_data.nlargest(top_n, y_column)
        
        plt.figure(figsize=(10, 6))
        
        bars = plt.bar(plot_data[x_column], plot_data[y_column], 
                      color='steelblue', edgecolor='black', linewidth=0.7)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=9)
        
        plt.xlabel(x_column.replace('_', ' ').title(), fontsize=12)
        plt.ylabel(y_column.replace('_', ' ').title(), fontsize=12)
        
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title(f'{y_column.replace("_", " ").title()} by {x_column.replace("_", " ").title()}',
                     fontsize=14, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_as:
            filepath = os.path.join(self.output_dir, save_as)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {filepath}")
        
        plt.show()
    
    def plot_pie_chart(self, values_column: str, labels_column: str,
                      title: str = None, save_as: str = None,
                      top_n: int = 10):
        """
        Create a pie chart for distribution analysis
        
        Args:
            values_column: Column with values
            labels_column: Column with labels
            title: Chart title
            save_as: Filename to save chart
            top_n: Show only top N items (others grouped as 'Other')
        """
        # Prepare data
        plot_data = self.data.copy()
        plot_data = plot_data.nlargest(top_n, values_column)
        
        plt.figure(figsize=(10, 8))
        
        # Create pie chart
        plt.pie(plot_data[values_column], labels=plot_data[labels_column],
               autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
        
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title(f'Distribution of {values_column.replace("_", " ").title()}',
                     fontsize=14, fontweight='bold')
        
        plt.axis('equal')  # Equal aspect ratio ensures circular pie
        
        if save_as:
            filepath = os.path.join(self.output_dir, save_as)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {filepath}")
        
        plt.show()
    
    def plot_multi_line_chart(self, x_column: str, y_columns: List[str],
                             title: str = None, save_as: str = None):
        """
        Create a line chart with multiple lines
        
        Args:
            x_column: Column for x-axis
            y_columns: List of columns for y-axis
            title: Chart title
            save_as: Filename to save chart
        """
        plt.figure(figsize=(12, 6))
        
        for y_col in y_columns:
            plt.plot(self.data[x_column], self.data[y_col],
                    marker='o', linewidth=2, label=y_col.replace('_', ' ').title())
        
        plt.xlabel(x_column.replace('_', ' ').title(), fontsize=12)
        plt.ylabel('Values', fontsize=12)
        
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title('Comparison Over Time', fontsize=14, fontweight='bold')
        
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_as:
            filepath = os.path.join(self.output_dir, save_as)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {filepath}")
        
        plt.show()
    
    def plot_histogram(self, column: str, bins: int = 20,
                      title: str = None, save_as: str = None):
        """
        Create a histogram for distribution analysis
        
        Args:
            column: Column to plot
            bins: Number of bins
            title: Chart title
            save_as: Filename to save chart
        """
        plt.figure(figsize=(10, 6))
        
        plt.hist(self.data[column], bins=bins, color='skyblue',
                edgecolor='black', linewidth=1.2)
        
        plt.xlabel(column.replace('_', ' ').title(), fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        
        if title:
            plt.title(title, fontsize=14, fontweight='bold')
        else:
            plt.title(f'Distribution of {column.replace("_", " ").title()}',
                     fontsize=14, fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        if save_as:
            filepath = os.path.join(self.output_dir, save_as)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {filepath}")
        
        plt.show()
    
    def create_dashboard(self, date_col: str, value_cols: List[str],
                        group_col: str = None, save_as: str = None):
        """
        Create a comprehensive dashboard with multiple charts
        
        Args:
            date_col: Date column for time series
            value_cols: List of value columns to visualize
            group_col: Column to group by for bar chart
            save_as: Filename to save dashboard
        """
        # Create a figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Health Data Dashboard', fontsize=16, fontweight='bold')
        
        # Plot 1: Line chart for first value column
        axes[0, 0].plot(self.data[date_col], self.data[value_cols[0]],
                       marker='o', linewidth=2, color='steelblue')
        axes[0, 0].set_title(f'{value_cols[0].replace("_", " ").title()} Over Time')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel(value_cols[0].replace('_', ' ').title())
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Bar chart if group column provided
        if group_col and len(value_cols) > 0:
            grouped = self.data.groupby(group_col)[value_cols[0]].sum().sort_values(ascending=False).head(10)
            axes[0, 1].bar(range(len(grouped)), grouped.values, color='coral')
            axes[0, 1].set_xticks(range(len(grouped)))
            axes[0, 1].set_xticklabels(grouped.index, rotation=45, ha='right')
            axes[0, 1].set_title(f'Top {group_col.replace("_", " ").title()}')
            axes[0, 1].set_ylabel(value_cols[0].replace('_', ' ').title())
        
        # Plot 3: Histogram for first value column
        if len(value_cols) > 0:
            axes[1, 0].hist(self.data[value_cols[0]].dropna(), bins=20,
                           color='lightgreen', edgecolor='black')
            axes[1, 0].set_title(f'Distribution of {value_cols[0].replace("_", " ").title()}')
            axes[1, 0].set_xlabel(value_cols[0].replace('_', ' ').title())
            axes[1, 0].set_ylabel('Frequency')
        
        # Plot 4: Multi-line if multiple value columns
        if len(value_cols) > 1:
            for val_col in value_cols[:3]:  # Max 3 lines
                axes[1, 1].plot(self.data[date_col], self.data[val_col],
                               marker='o', linewidth=2, label=val_col.replace('_', ' ').title())
            axes[1, 1].set_title('Multiple Metrics Comparison')
            axes[1, 1].set_xlabel('Date')
            axes[1, 1].set_ylabel('Values')
            axes[1, 1].legend(loc='best', fontsize=8)
            axes[1, 1].grid(True, alpha=0.3)
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_as:
            filepath = os.path.join(self.output_dir, save_as)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Dashboard saved to: {filepath}")
        
        plt.show()


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10),
        'cases': [100, 120, 150, 140, 180, 200, 190, 210, 230, 220],
        'deaths': [10, 12, 15, 14, 18, 20, 19, 21, 23, 22],
        'country': ['UK'] * 5 + ['USA'] * 5
    })
    
    viz = HealthVisualizer(sample_data)
    
    # Test line chart
    # viz.plot_line_chart('date', 'cases', title='COVID Cases Over Time')
