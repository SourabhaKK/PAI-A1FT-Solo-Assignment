"""
CLI Module for Basket Analysis
Interactive command-line interface for market basket analysis
Author: Sourabha K Kallapur
"""

import os
from basket_analysis.transaction_loader import TransactionLoader
from basket_analysis.graph import ProductGraph
from basket_analysis.algorithms import GraphAlgorithms
from basket_analysis.mining import FrequentItemsetMiner
from basket_analysis.recommender import ProductRecommender


class BasketAnalysisCLI:
    """
    Command-line interface for Supermarket Basket Analysis
    """
    
    def __init__(self):
        """Initialize the CLI"""
        self.loader = TransactionLoader()
        self.graph = None
        self.algorithms = None
        self.miner = None
        self.recommender = None
        
        print("\n" + "=" * 60)
        print("SUPERMARKET BASKET ANALYSIS SYSTEM")
        print("=" * 60)
        print("Analyze customer purchasing patterns using graph algorithms")
        print("=" * 60 + "\n")
    
    def show_main_menu(self):
        """Display the main menu"""
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("-" * 60)
        print("1. Load Transaction Data")
        print("2. View Graph Information")
        print("3. Graph Traversal (BFS/DFS)")
        print("4. Find Frequent Itemsets")
        print("5. Get Product Recommendations")
        print("6. Analyze Product Bundles")
        print("7. View Transaction Statistics")
        print("8. Exit")
        print("-" * 60)
    
    def load_data_menu(self):
        """Menu for loading transaction data"""
        print("\n--- Load Transaction Data ---")
        file_path = input("Enter path to transaction CSV file: ").strip()
        
        try:
            # Load transactions
            transactions = self.loader.load_from_csv(file_path)
            
            if not transactions:
                print("\n✗ No transactions loaded")
                return
            
            # Build graph
            print("\nBuilding product graph...")
            self.graph = self.loader.build_graph_from_transactions()
            
            # Initialize other components
            self.algorithms = GraphAlgorithms(self.graph)
            self.miner = FrequentItemsetMiner(transactions, min_support=0.01)
            self.recommender = ProductRecommender(self.graph)
            
            print("\n✓ Data loaded and graph built successfully!")
            
            # Show statistics
            self.loader.print_transaction_stats()
            
        except Exception as e:
            print(f"\n✗ Error loading data: {e}")
    
    def view_graph_info(self):
        """Display graph information"""
        if self.graph is None:
            print("\n✗ No data loaded. Please load transaction data first.")
            return
        
        print("\n--- Graph Information ---")
        info = self.graph.get_graph_info()
        
        print(f"Total Products (Nodes): {info['num_nodes']}")
        print(f"Co-purchase Relationships (Edges): {info['num_edges']}")
        print(f"Average Connections per Product: {info['avg_degree']:.2f}")
        print(f"Most Connected Product: {info['max_degree']} connections")
        print(f"Graph Density: {info['density']:.4f}")
        
        # Show some sample products
        print("\nSample Products:")
        for i, product in enumerate(list(self.graph.get_all_nodes())[:10], 1):
            degree = self.graph.get_degree(product)
            print(f"  {i}. {product} ({degree} connections)")
    
    def traversal_menu(self):
        """Menu for graph traversal"""
        if self.graph is None:
            print("\n✗ No data loaded. Please load transaction data first.")
            return
        
        print("\n--- Graph Traversal ---")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        print("3. Find path between two products")
        print("4. Find items within distance")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            start_item = input("Enter starting product: ").strip()
            max_depth = input("Enter max depth (or press Enter for unlimited): ").strip()
            max_depth = int(max_depth) if max_depth else None
            
            result = self.algorithms.bfs(start_item, max_depth)
            print(f"\nBFS Traversal from '{start_item}':")
            print(" -> ".join(result))
        
        elif choice == '2':
            start_item = input("Enter starting product: ").strip()
            max_depth = input("Enter max depth (or press Enter for unlimited): ").strip()
            max_depth = int(max_depth) if max_depth else None
            
            result = self.algorithms.dfs(start_item, max_depth)
            print(f"\nDFS Traversal from '{start_item}':")
            print(" -> ".join(result))
        
        elif choice == '3':
            start_item = input("Enter start product: ").strip()
            end_item = input("Enter end product: ").strip()
            
            path = self.algorithms.find_path(start_item, end_item)
            if path:
                print(f"\nPath from '{start_item}' to '{end_item}':")
                print(" -> ".join(path))
            else:
                print(f"\nNo path found between '{start_item}' and '{end_item}'")
        
        elif choice == '4':
            start_item = input("Enter starting product: ").strip()
            distance = int(input("Enter maximum distance: ").strip())
            
            items = self.algorithms.get_items_within_distance(start_item, distance)
            print(f"\nItems within distance {distance} from '{start_item}':")
            for item in sorted(items):
                print(f"  - {item}")
    
    def frequent_itemsets_menu(self):
        """Menu for frequent itemset mining"""
        if self.miner is None:
            print("\n✗ No data loaded. Please load transaction data first.")
            return
        
        print("\n--- Frequent Itemset Mining ---")
        print("1. Find frequent item pairs")
        print("2. Run Apriori algorithm")
        print("3. Generate association rules")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            n = int(input("How many top pairs to show? (default: 10): ").strip() or "10")
            self.miner.print_top_pairs(n)
        
        elif choice == '2':
            max_k = int(input("Maximum itemset size (default: 3): ").strip() or "3")
            
            print(f"\nRunning Apriori algorithm...")
            all_itemsets = self.miner.apriori(max_k)
            
            print("\n--- Apriori Results ---")
            for k, itemsets in all_itemsets.items():
                print(f"\n{k}-itemsets ({len(itemsets)} found):")
                # Show top 10 for each k
                sorted_itemsets = sorted(itemsets.items(), key=lambda x: x[1], reverse=True)
                for itemset, count in sorted_itemsets[:10]:
                    items_str = ", ".join(sorted(itemset))
                    support = count / self.miner.num_transactions
                    print(f"  {{{items_str}}}: count={count}, support={support:.2%}")
        
        elif choice == '3':
            min_conf = float(input("Minimum confidence (0-1, default: 0.5): ").strip() or "0.5")
            
            rules = self.miner.get_association_rules(min_conf)
            
            print(f"\n--- Association Rules (Top 20) ---")
            for i, rule in enumerate(rules[:20], 1):
                print(f"\n{i}. {rule['antecedent']} → {rule['consequent']}")
                print(f"   Support: {rule['support']:.2%}")
                print(f"   Confidence: {rule['confidence']:.2%}")
                print(f"   Lift: {rule['lift']:.2f}")
    
    def recommendations_menu(self):
        """Menu for product recommendations"""
        if self.recommender is None:
            print("\n✗ No data loaded. Please load transaction data first.")
            return
        
        print("\n--- Product Recommendations ---")
        print("1. Recommend for a single item")
        print("2. Recommend for a basket of items")
        print("3. Find similar items")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            item = input("Enter product name: ").strip()
            n = int(input("Number of recommendations (default: 5): ").strip() or "5")
            
            self.recommender.print_recommendations(item, n)
        
        elif choice == '2':
            items_str = input("Enter items in basket (comma-separated): ").strip()
            basket = [item.strip() for item in items_str.split(',')]
            n = int(input("Number of recommendations (default: 5): ").strip() or "5")
            
            recommendations = self.recommender.recommend_for_basket(basket, n)
            
            print(f"\n{'='*60}")
            print(f"RECOMMENDATIONS FOR BASKET: {', '.join(basket)}")
            print(f"{'='*60}")
            
            for i, (rec_item, score) in enumerate(recommendations, 1):
                print(f"{i}. {rec_item} (score: {score:.1f})")
            
            print(f"{'='*60}")
        
        elif choice == '3':
            item = input("Enter product name: ").strip()
            n = int(input("Number of similar items (default: 5): ").strip() or "5")
            
            similar = self.recommender.get_similar_items(item, n)
            
            print(f"\n{'='*60}")
            print(f"ITEMS SIMILAR TO: {item}")
            print(f"{'='*60}")
            
            for i, (similar_item, similarity) in enumerate(similar, 1):
                print(f"{i}. {similar_item} (similarity: {similarity:.2%})")
            
            print(f"{'='*60}")
    
    def bundles_menu(self):
        """Menu for analyzing product bundles"""
        if self.recommender is None:
            print("\n✗ No data loaded. Please load transaction data first.")
            return
        
        print("\n--- Product Bundle Analysis ---")
        
        min_size = int(input("Minimum bundle size (default: 2): ").strip() or "2")
        max_size = int(input("Maximum bundle size (default: 3): ").strip() or "3")
        top_n = int(input("Number of top bundles (default: 10): ").strip() or "10")
        
        bundles = self.recommender.find_product_bundles(min_size, max_size, top_n)
        
        print(f"\n{'='*60}")
        print(f"TOP {top_n} PRODUCT BUNDLES")
        print(f"{'='*60}")
        
        for i, (bundle, score) in enumerate(bundles, 1):
            print(f"\n{i}. {' + '.join(bundle)}")
            print(f"   Score: {score:.1f}")
        
        print(f"{'='*60}")
    
    def run(self):
        """Main loop for the CLI"""
        while True:
            self.show_main_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.load_data_menu()
            elif choice == '2':
                self.view_graph_info()
            elif choice == '3':
                self.traversal_menu()
            elif choice == '4':
                self.frequent_itemsets_menu()
            elif choice == '5':
                self.recommendations_menu()
            elif choice == '6':
                self.bundles_menu()
            elif choice == '7':
                if self.loader.get_transactions():
                    self.loader.print_transaction_stats()
                else:
                    print("\n✗ No data loaded")
            elif choice == '8':
                print("\n" + "=" * 60)
                print("Thank you for using Basket Analysis System!")
                print("=" * 60)
                break
            else:
                print("\n✗ Invalid choice. Please try again.")


# Main entry point
if __name__ == "__main__":
    cli = BasketAnalysisCLI()
    cli.run()
