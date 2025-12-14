"""
Transaction Loader Module for Basket Analysis
Loads transaction data and builds the product graph
Author: Sourabha K Kallapur
"""

import pandas as pd
import csv
from typing import List, Dict
from basket_analysis.graph import ProductGraph


class TransactionLoader:
    """
    Loads transaction data and builds a product co-purchase graph
    """
    
    def __init__(self):
        """Initialize the transaction loader"""
        self.transactions = []
        self.graph = ProductGraph()
    
    def load_from_csv(self, file_path: str, delimiter: str = ',') -> List[List[str]]:
        """
        Load transactions from a CSV file
        Each row represents a transaction (basket of items)
        
        Args:
            file_path: Path to the CSV file
            delimiter: Delimiter used in the CSV (default: comma)
            
        Returns:
            List of transactions (each transaction is a list of items)
        """
        self.transactions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                
                # Skip header if it exists
                first_row = next(reader, None)
                if first_row:
                    # Check if first row looks like a header
                    if first_row[0].lower() in ['transaction', 'items', 'basket', 'transaction_id']:
                        # It's a header, skip it
                        pass
                    else:
                        # It's data, add it
                        # Remove empty strings and strip whitespace
                        items = [item.strip() for item in first_row if item.strip()]
                        if items:
                            self.transactions.append(items)
                
                # Read the rest of the transactions
                for row in reader:
                    # Remove empty strings and strip whitespace
                    items = [item.strip() for item in row if item.strip()]
                    if items:  # Only add non-empty transactions
                        self.transactions.append(items)
            
            print(f"Loaded {len(self.transactions)} transactions from {file_path}")
            return self.transactions
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return []
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    def build_graph_from_transactions(self) -> ProductGraph:
        """
        Build a product graph from loaded transactions
        Creates edges between items that appear together in transactions
        
        Returns:
            ProductGraph with items and co-purchase relationships
        """
        if not self.transactions:
            print("No transactions loaded. Please load transactions first.")
            return self.graph
        
        print(f"Building graph from {len(self.transactions)} transactions...")
        
        # Process each transaction
        for transaction in self.transactions:
            # For each pair of items in the transaction, add/update an edge
            for i in range(len(transaction)):
                for j in range(i + 1, len(transaction)):
                    item1 = transaction[i]
                    item2 = transaction[j]
                    
                    # Add edge (or increment weight if it already exists)
                    self.graph.add_edge(item1, item2, weight=1)
        
        print(f"Graph built successfully!")
        print(f"Nodes (unique items): {self.graph.get_node_count()}")
        print(f"Edges (co-purchase relationships): {self.graph.get_edge_count()}")
        
        return self.graph
    
    def get_transaction_stats(self) -> Dict:
        """
        Get statistics about the loaded transactions
        
        Returns:
            Dictionary with transaction statistics
        """
        if not self.transactions:
            return {"error": "No transactions loaded"}
        
        # Calculate statistics
        transaction_sizes = [len(t) for t in self.transactions]
        all_items = set()
        for transaction in self.transactions:
            all_items.update(transaction)
        
        # Find most common items
        item_counts = {}
        for transaction in self.transactions:
            for item in transaction:
                item_counts[item] = item_counts.get(item, 0) + 1
        
        # Sort items by frequency
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        
        stats = {
            'total_transactions': len(self.transactions),
            'unique_items': len(all_items),
            'avg_transaction_size': sum(transaction_sizes) / len(transaction_sizes),
            'min_transaction_size': min(transaction_sizes),
            'max_transaction_size': max(transaction_sizes),
            'most_common_items': sorted_items[:10]  # Top 10 items
        }
        
        return stats
    
    def print_transaction_stats(self):
        """Print transaction statistics in a readable format"""
        stats = self.get_transaction_stats()
        
        if "error" in stats:
            print(stats["error"])
            return
        
        print("\n" + "=" * 60)
        print("TRANSACTION STATISTICS")
        print("=" * 60)
        print(f"Total Transactions: {stats['total_transactions']}")
        print(f"Unique Items: {stats['unique_items']}")
        print(f"Average Transaction Size: {stats['avg_transaction_size']:.2f} items")
        print(f"Min Transaction Size: {stats['min_transaction_size']} items")
        print(f"Max Transaction Size: {stats['max_transaction_size']} items")
        
        print("\nMost Common Items:")
        for item, count in stats['most_common_items']:
            percentage = (count / stats['total_transactions']) * 100
            print(f"  {item}: {count} ({percentage:.1f}%)")
        print("=" * 60)
    
    def get_transactions(self) -> List[List[str]]:
        """Return the loaded transactions"""
        return self.transactions
    
    def get_graph(self) -> ProductGraph:
        """Return the built graph"""
        return self.graph
    
    def filter_transactions_by_item(self, item: str) -> List[List[str]]:
        """
        Get all transactions containing a specific item
        
        Args:
            item: Item to filter by
            
        Returns:
            List of transactions containing the item
        """
        filtered = [t for t in self.transactions if item in t]
        print(f"Found {len(filtered)} transactions containing '{item}'")
        return filtered


# Example usage
if __name__ == "__main__":
    loader = TransactionLoader()
    
    # Example: Load from CSV
    # transactions = loader.load_from_csv("data/sample_transactions.csv")
    
    # Build graph
    # graph = loader.build_graph_from_transactions()
    
    # Print stats
    # loader.print_transaction_stats()
    
    # Print graph info
    # print("\nGraph Info:")
    # print(graph.get_graph_info())
