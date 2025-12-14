"""
Tests for Basket Analysis
Tests for Task 2 modules
Author: Sourabha K Kallapur
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from basket_analysis.graph import ProductGraph
from basket_analysis.algorithms import GraphAlgorithms
from basket_analysis.transaction_loader import TransactionLoader
from basket_analysis.mining import FrequentItemsetMiner
from basket_analysis.recommender import ProductRecommender


class TestProductGraph:
    """Test the graph data structure"""
    
    def test_graph_initialization(self):
        """Test that graph initializes correctly"""
        graph = ProductGraph()
        assert graph.get_node_count() == 0
        assert graph.get_edge_count() == 0
    
    def test_add_node(self):
        """Test adding nodes"""
        graph = ProductGraph()
        graph.add_node("Bread")
        graph.add_node("Milk")
        
        assert graph.get_node_count() == 2
        assert "Bread" in graph.get_all_nodes()
        assert "Milk" in graph.get_all_nodes()
    
    def test_add_edge(self):
        """Test adding edges"""
        graph = ProductGraph()
        graph.add_edge("Bread", "Milk", weight=5)
        
        assert graph.get_node_count() == 2
        assert graph.get_edge_count() == 1
        assert graph.get_edge_weight("Bread", "Milk") == 5
        assert graph.get_edge_weight("Milk", "Bread") == 5  # Undirected
    
    def test_get_neighbors(self):
        """Test getting neighbors"""
        graph = ProductGraph()
        graph.add_edge("Bread", "Milk", 5)
        graph.add_edge("Bread", "Butter", 3)
        
        neighbors = graph.get_neighbors("Bread")
        assert len(neighbors) == 2
        assert "Milk" in neighbors
        assert "Butter" in neighbors
    
    def test_top_connections(self):
        """Test getting top connections"""
        graph = ProductGraph()
        graph.add_edge("Bread", "Milk", 10)
        graph.add_edge("Bread", "Butter", 5)
        graph.add_edge("Bread", "Eggs", 8)
        
        top = graph.get_top_connections("Bread", n=2)
        assert len(top) == 2
        assert top[0][0] == "Milk"  # Highest weight
        assert top[0][1] == 10


class TestGraphAlgorithms:
    """Test graph algorithms"""
    
    def setup_method(self):
        """Set up a sample graph for testing"""
        self.graph = ProductGraph()
        self.graph.add_edge("Bread", "Milk", 5)
        self.graph.add_edge("Bread", "Butter", 3)
        self.graph.add_edge("Milk", "Eggs", 4)
        self.graph.add_edge("Bread", "Eggs", 2)
        self.algo = GraphAlgorithms(self.graph)
    
    def test_bfs(self):
        """Test BFS traversal"""
        result = self.algo.bfs("Bread")
        
        assert len(result) > 0
        assert result[0] == "Bread"  # Start node should be first
        assert "Milk" in result
        assert "Butter" in result
    
    def test_dfs(self):
        """Test DFS traversal"""
        result = self.algo.dfs("Bread")
        
        assert len(result) > 0
        assert result[0] == "Bread"  # Start node should be first
        assert "Milk" in result
        assert "Butter" in result
    
    def test_find_path(self):
        """Test path finding"""
        path = self.algo.find_path("Bread", "Eggs")
        
        assert path is not None
        assert path[0] == "Bread"
        assert path[-1] == "Eggs"
    
    def test_is_connected(self):
        """Test connectivity check"""
        assert self.algo.is_connected("Bread", "Eggs") == True
        
        # Add disconnected node
        self.graph.add_node("Isolated")
        assert self.algo.is_connected("Bread", "Isolated") == False


class TestTransactionLoader:
    """Test transaction loader"""
    
    def test_loader_initialization(self):
        """Test loader initialization"""
        loader = TransactionLoader()
        assert len(loader.transactions) == 0
    
    def test_load_from_csv(self):
        """Test loading transactions from real supermarket CSV"""
        import pandas as pd
        
        # Load real supermarket dataset
        df = pd.read_csv("data/Supermarket_dataset_PAI.csv")
        transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).tolist()
        
        assert len(transactions) > 0
        assert len(transactions) == 14963  # Expected transaction count
        assert isinstance(transactions[0], list)
    
    def test_build_graph(self):
        """Test building graph from real transactions"""
        import pandas as pd
        
        loader = TransactionLoader()
        # Load real dataset
        df = pd.read_csv("data/Supermarket_dataset_PAI.csv")
        loader.transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).tolist()
        
        graph = loader.build_graph_from_transactions()
        
        assert graph.get_node_count() == 167  # Expected unique products
        assert graph.get_edge_count() == 6292  # Expected co-purchase relationships



class TestFrequentItemsetMiner:
    """Test frequent itemset mining"""
    
    def setup_method(self):
        """Set up sample transactions"""
        self.transactions = [
            ['Bread', 'Milk', 'Eggs'],
            ['Bread', 'Butter'],
            ['Milk', 'Eggs'],
            ['Bread', 'Milk', 'Butter'],
            ['Bread', 'Eggs']
        ]
        self.miner = FrequentItemsetMiner(self.transactions, min_support=0.4)
    
    def test_find_frequent_1_itemsets(self):
        """Test finding frequent individual items"""
        frequent = self.miner.find_frequent_1_itemsets()
        
        assert len(frequent) > 0
        # Bread appears in 4/5 transactions
        assert frozenset(['Bread']) in frequent
    
    def test_find_frequent_pairs(self):
        """Test finding frequent pairs"""
        pairs = self.miner.find_frequent_pairs()
        
        assert len(pairs) > 0
        # Check that pairs are tuples
        assert isinstance(pairs[0][0], tuple)
        assert isinstance(pairs[0][1], int)


class TestProductRecommender:
    """Test product recommender"""
    
    def setup_method(self):
        """Set up a sample graph"""
        self.graph = ProductGraph()
        self.graph.add_edge("Bread", "Milk", 10)
        self.graph.add_edge("Bread", "Butter", 7)
        self.graph.add_edge("Milk", "Eggs", 8)
        self.recommender = ProductRecommender(self.graph)
    
    def test_recommend_for_item(self):
        """Test item recommendations"""
        recs = self.recommender.recommend_for_item("Bread", n=2)
        
        assert len(recs) > 0
        assert len(recs) <= 2
        # Milk should be top recommendation (highest weight)
        assert recs[0][0] == "Milk"
    
    def test_recommend_for_basket(self):
        """Test basket recommendations"""
        recs = self.recommender.recommend_for_basket(["Bread"], n=2)
        
        assert len(recs) > 0
        assert len(recs) <= 2


class TestRealSupermarketDataset:
    """Integration tests using real supermarket dataset"""
    
    @classmethod
    def setup_class(cls):
        """Load real dataset once for all tests in this class"""
        import pandas as pd
        
        # Load the real supermarket dataset
        df = pd.read_csv("data/Supermarket_dataset_PAI.csv")
        
        # Group by Member_number and Date to form transactions
        cls.transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list).tolist()
        
        # Build graph from transactions
        cls.loader = TransactionLoader()
        cls.loader.transactions = cls.transactions
        cls.graph = cls.loader.build_graph_from_transactions()
        
        # Initialize components
        cls.algorithms = GraphAlgorithms(cls.graph)
        cls.miner = FrequentItemsetMiner(cls.transactions, min_support=0.01)
        cls.recommender = ProductRecommender(cls.graph)
    
    def test_dataset_loading(self):
        """Test that dataset loads correctly"""
        assert len(self.transactions) > 0
        assert len(self.transactions) == 14963  # Expected transaction count
        
        # Check sample transaction structure
        assert all(isinstance(t, list) for t in self.transactions[:10])
    
    def test_graph_construction(self):
        """Test graph is built correctly from real data"""
        info = self.graph.get_graph_info()
        
        # Verify expected graph statistics
        assert info['num_nodes'] == 167  # Expected unique products
        assert info['num_edges'] == 6292  # Expected co-purchase relationships
        assert info['avg_degree'] > 70  # Highly connected graph
        assert 0.4 < info['density'] < 0.5  # Expected density range
    
    def test_bfs_on_real_data(self):
        """Test BFS traversal on real dataset"""
        # Get a sample product
        sample_product = list(self.graph.get_all_nodes())[0]
        
        # Run BFS
        bfs_result = self.algorithms.bfs(sample_product, max_depth=2)
        
        assert len(bfs_result) > 0
        assert bfs_result[0] == sample_product
        assert len(bfs_result) <= self.graph.get_node_count()
    
    def test_dfs_on_real_data(self):
        """Test DFS traversal on real dataset"""
        # Get a sample product
        sample_product = list(self.graph.get_all_nodes())[0]
        
        # Run DFS
        dfs_result = self.algorithms.dfs(sample_product, max_depth=2)
        
        assert len(dfs_result) > 0
        assert dfs_result[0] == sample_product
    
    def test_frequent_pairs_real_data(self):
        """Test frequent itemset mining on real data"""
        top_pairs = self.miner.get_top_n_pairs(10)
        
        # Should find at least some frequent pairs
        assert len(top_pairs) > 0
        assert len(top_pairs) <= 10
        
        # Verify top pair structure
        (item1, item2), count = top_pairs[0]
        assert isinstance(item1, str)
        assert isinstance(item2, str)
        assert isinstance(count, int)
        assert count > 0
        
        # Verify pairs are sorted by count (descending)
        if len(top_pairs) > 1:
            assert top_pairs[0][1] >= top_pairs[1][1]
    
    def test_recommendations_real_data(self):
        """Test recommendation system on real data"""
        # Find most common item
        item_counts = {}
        for trans in self.transactions:
            for item in trans:
                item_counts[item] = item_counts.get(item, 0) + 1
        
        most_common_item = max(item_counts.items(), key=lambda x: x[1])[0]
        
        # Get recommendations
        recs = self.recommender.recommend_for_item(most_common_item, n=5)
        
        assert len(recs) > 0
        assert len(recs) <= 5
        
        # Verify recommendation structure
        for item, score in recs:
            assert isinstance(item, str)
            assert isinstance(score, (int, float))
            assert score > 0
    
    def test_basket_recommendations_real_data(self):
        """Test basket-based recommendations on real data"""
        # Use a sample basket
        sample_basket = ["whole milk", "other vegetables"]
        
        # Get recommendations
        recs = self.recommender.recommend_for_basket(sample_basket, n=5)
        
        assert len(recs) >= 0  # May be empty if items not in graph
        
        # If recommendations exist, verify structure
        for item, score in recs:
            assert isinstance(item, str)
            assert item not in sample_basket  # Should exclude basket items
            assert isinstance(score, (int, float))
    
    def test_graph_statistics_real_data(self):
        """Test graph statistics calculations"""
        # Get top connections for a well-connected product
        nodes = list(self.graph.get_all_nodes())
        if len(nodes) > 0:
            sample_node = nodes[0]
            top_connections = self.graph.get_top_connections(sample_node, n=5)
            
            assert len(top_connections) > 0
            
            # Verify connections are sorted by weight
            if len(top_connections) > 1:
                assert top_connections[0][1] >= top_connections[1][1]
    
    def test_transaction_statistics(self):
        """Test transaction statistics calculation"""
        stats = self.loader.get_transaction_stats()
        
        assert stats['total_transactions'] == len(self.transactions)
        assert stats['unique_items'] == 167
        assert stats['avg_transaction_size'] > 0
        assert stats['min_transaction_size'] > 0
        assert stats['max_transaction_size'] >= stats['min_transaction_size']
        assert len(stats['most_common_items']) > 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
