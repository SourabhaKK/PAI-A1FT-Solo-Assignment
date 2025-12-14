"""
Frequent Itemset Mining Module for Basket Analysis
Implements Apriori algorithm and frequent pair mining
Author: Sourabha K Kallapur
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
from itertools import combinations


class FrequentItemsetMiner:
    """
    Mines frequent itemsets from transaction data using Apriori algorithm
    """
    
    def __init__(self, transactions: List[List[str]], min_support: float = 0.01):
        """
        Initialize the miner
        
        Args:
            transactions: List of transactions (each is a list of items)
            min_support: Minimum support threshold (0-1)
        """
        self.transactions = transactions
        self.min_support = min_support
        self.num_transactions = len(transactions)
        
        # Calculate minimum support count
        self.min_support_count = int(self.min_support * self.num_transactions)
        if self.min_support_count < 1:
            self.min_support_count = 1
    
    def find_frequent_1_itemsets(self) -> Dict[frozenset, int]:
        """
        Find all frequent 1-itemsets (individual items)
        
        Returns:
            Dictionary of {frozenset({item}): count}
        """
        # Count occurrences of each item
        item_counts = defaultdict(int)
        
        for transaction in self.transactions:
            for item in transaction:
                item_counts[frozenset([item])] += 1
        
        # Filter by minimum support
        frequent_items = {
            itemset: count 
            for itemset, count in item_counts.items() 
            if count >= self.min_support_count
        }
        
        print(f"Found {len(frequent_items)} frequent 1-itemsets")
        return frequent_items
    
    def find_frequent_pairs(self) -> List[Tuple[Tuple[str, str], int]]:
        """
        Find all frequent item pairs (2-itemsets)
        
        Returns:
            List of ((item1, item2), count) tuples sorted by count
        """
        # Count occurrences of each pair
        pair_counts = defaultdict(int)
        
        for transaction in self.transactions:
            # Generate all pairs from this transaction
            if len(transaction) >= 2:
                for item1, item2 in combinations(sorted(transaction), 2):
                    pair_counts[(item1, item2)] += 1
        
        # Filter by minimum support and sort
        frequent_pairs = [
            (pair, count) 
            for pair, count in pair_counts.items() 
            if count >= self.min_support_count
        ]
        
        # Sort by count (descending)
        frequent_pairs.sort(key=lambda x: x[1], reverse=True)
        
        print(f"Found {len(frequent_pairs)} frequent pairs")
        return frequent_pairs
    
    def find_frequent_k_itemsets(self, k: int) -> Dict[frozenset, int]:
        """
        Find all frequent k-itemsets
        
        Args:
            k: Size of itemsets to find
            
        Returns:
            Dictionary of {frozenset(items): count}
        """
        if k < 1:
            return {}
        
        # Count occurrences of each k-itemset
        itemset_counts = defaultdict(int)
        
        for transaction in self.transactions:
            if len(transaction) >= k:
                # Generate all k-combinations from this transaction
                for itemset in combinations(sorted(transaction), k):
                    itemset_counts[frozenset(itemset)] += 1
        
        # Filter by minimum support
        frequent_itemsets = {
            itemset: count 
            for itemset, count in itemset_counts.items() 
            if count >= self.min_support_count
        }
        
        print(f"Found {len(frequent_itemsets)} frequent {k}-itemsets")
        return frequent_itemsets
    
    def apriori(self, max_k: int = 3) -> Dict[int, Dict[frozenset, int]]:
        """
        Run Apriori algorithm to find all frequent itemsets up to size max_k
        
        Args:
            max_k: Maximum itemset size to find
            
        Returns:
            Dictionary of {k: {itemset: count}} for each k
        """
        print(f"\nRunning Apriori algorithm (min_support={self.min_support})...")
        print(f"Minimum support count: {self.min_support_count} transactions")
        
        all_frequent_itemsets = {}
        
        for k in range(1, max_k + 1):
            frequent_k = self.find_frequent_k_itemsets(k)
            
            if not frequent_k:
                print(f"No frequent {k}-itemsets found. Stopping.")
                break
            
            all_frequent_itemsets[k] = frequent_k
        
        return all_frequent_itemsets
    
    def get_top_n_pairs(self, n: int = 10) -> List[Tuple[Tuple[str, str], int]]:
        """
        Get the top N most frequent item pairs
        
        Args:
            n: Number of pairs to return
            
        Returns:
            List of ((item1, item2), count) tuples
        """
        frequent_pairs = self.find_frequent_pairs()
        return frequent_pairs[:n]
    
    def get_association_rules(self, min_confidence: float = 0.5) -> List[Dict]:
        """
        Generate association rules from frequent pairs
        Rule: {item1} -> {item2} with confidence and support
        
        Args:
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of rule dictionaries
        """
        frequent_pairs = self.find_frequent_pairs()
        frequent_1_items = self.find_frequent_1_itemsets()
        
        rules = []
        
        for (item1, item2), pair_count in frequent_pairs:
            # Calculate support and confidence for both directions
            
            # Rule: item1 -> item2
            item1_count = frequent_1_items.get(frozenset([item1]), 0)
            if item1_count > 0:
                confidence_1_to_2 = pair_count / item1_count
                if confidence_1_to_2 >= min_confidence:
                    rules.append({
                        'antecedent': item1,
                        'consequent': item2,
                        'support': pair_count / self.num_transactions,
                        'confidence': confidence_1_to_2,
                        'lift': (pair_count / self.num_transactions) / 
                               ((item1_count / self.num_transactions) * 
                                (frequent_1_items.get(frozenset([item2]), 0) / self.num_transactions))
                    })
            
            # Rule: item2 -> item1
            item2_count = frequent_1_items.get(frozenset([item2]), 0)
            if item2_count > 0:
                confidence_2_to_1 = pair_count / item2_count
                if confidence_2_to_1 >= min_confidence:
                    rules.append({
                        'antecedent': item2,
                        'consequent': item1,
                        'support': pair_count / self.num_transactions,
                        'confidence': confidence_2_to_1,
                        'lift': (pair_count / self.num_transactions) / 
                               ((item2_count / self.num_transactions) * 
                                (item1_count / self.num_transactions))
                    })
        
        # Sort by confidence
        rules.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"Generated {len(rules)} association rules")
        return rules
    
    def print_top_pairs(self, n: int = 10):
        """Print the top N frequent pairs"""
        top_pairs = self.get_top_n_pairs(n)
        
        print(f"\n{'='*60}")
        print(f"TOP {n} FREQUENT ITEM PAIRS")
        print(f"{'='*60}")
        
        for i, ((item1, item2), count) in enumerate(top_pairs, 1):
            support = count / self.num_transactions
            print(f"{i}. {item1} + {item2}")
            print(f"   Count: {count} | Support: {support:.2%}")
        
        print(f"{'='*60}")


# Example usage
if __name__ == "__main__":
    # Sample transactions
    sample_transactions = [
        ['Bread', 'Milk', 'Eggs'],
        ['Bread', 'Butter'],
        ['Milk', 'Eggs', 'Cheese'],
        ['Bread', 'Milk', 'Butter'],
        ['Bread', 'Eggs'],
        ['Milk', 'Butter'],
        ['Bread', 'Milk', 'Eggs', 'Butter']
    ]
    
    # Create miner
    miner = FrequentItemsetMiner(sample_transactions, min_support=0.3)
    
    # Find frequent pairs
    # miner.print_top_pairs(5)
    
    # Run Apriori
    # all_itemsets = miner.apriori(max_k=3)
    
    # Get association rules
    # rules = miner.get_association_rules(min_confidence=0.5)
    # for rule in rules[:5]:
    #     print(f"{rule['antecedent']} -> {rule['consequent']}: "
    #           f"confidence={rule['confidence']:.2%}, support={rule['support']:.2%}")
