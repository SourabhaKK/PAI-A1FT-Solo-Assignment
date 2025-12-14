"""
Recommender Module for Basket Analysis
Provides product recommendations based on graph analysis
Author: Sourabha K Kallapur
"""

from typing import List, Dict, Tuple, Set
from basket_analysis.graph import ProductGraph
from basket_analysis.algorithms import GraphAlgorithms


class ProductRecommender:
    """
    Recommends products based on co-purchase patterns
    """
    
    def __init__(self, graph: ProductGraph):
        """
        Initialize recommender with a product graph
        
        Args:
            graph: ProductGraph with product relationships
        """
        self.graph = graph
        self.algorithms = GraphAlgorithms(graph)
    
    def recommend_for_item(self, item: str, n: int = 5, 
                          exclude_items: Set[str] = None) -> List[Tuple[str, int]]:
        """
        Recommend products to buy with a given item
        
        Args:
            item: Product name
            n: Number of recommendations
            exclude_items: Set of items to exclude from recommendations
            
        Returns:
            List of (product, score) tuples
        """
        if item not in self.graph.get_all_nodes():
            print(f"Item '{item}' not found in graph")
            return []
        
        if exclude_items is None:
            exclude_items = set()
        
        # Get direct neighbors (items bought together with this item)
        neighbors = self.graph.get_neighbors(item)
        
        # Filter out excluded items
        recommendations = [
            (neighbor, weight) 
            for neighbor, weight in neighbors.items() 
            if neighbor not in exclude_items
        ]
        
        # Sort by weight (co-purchase frequency)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n]
    
    def recommend_for_basket(self, basket: List[str], n: int = 5) -> List[Tuple[str, float]]:
        """
        Recommend products based on a basket of items
        
        Args:
            basket: List of items in the basket
            n: Number of recommendations
            
        Returns:
            List of (product, score) tuples
        """
        if not basket:
            return []
        
        # Collect all recommendations from each item in the basket
        all_recommendations = {}
        
        for item in basket:
            if item in self.graph.get_all_nodes():
                # Get recommendations for this item, excluding items already in basket
                item_recs = self.recommend_for_item(item, n=20, exclude_items=set(basket))
                
                # Add to overall recommendations with weighted score
                for rec_item, weight in item_recs:
                    if rec_item not in all_recommendations:
                        all_recommendations[rec_item] = 0
                    all_recommendations[rec_item] += weight
        
        # Convert to list and sort
        recommendations = list(all_recommendations.items())
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n]
    
    def find_product_bundles(self, min_bundle_size: int = 2, 
                            max_bundle_size: int = 3,
                            top_n: int = 10) -> List[Tuple[List[str], float]]:
        """
        Find common product bundles (groups of items frequently bought together)
        
        Args:
            min_bundle_size: Minimum number of items in a bundle
            max_bundle_size: Maximum number of items in a bundle
            top_n: Number of top bundles to return
            
        Returns:
            List of (bundle, score) tuples
        """
        # This is a simplified implementation
        # In a real scenario, you'd use the frequent itemset mining results
        
        bundles = []
        
        # For each node, find its strongest connections
        for node in self.graph.get_all_nodes():
            top_connections = self.graph.get_top_connections(node, n=max_bundle_size-1)
            
            if len(top_connections) >= min_bundle_size - 1:
                # Create a bundle with this node and its top connections
                bundle_items = [node] + [conn[0] for conn in top_connections[:max_bundle_size-1]]
                
                # Calculate bundle score (sum of edge weights)
                score = sum(conn[1] for conn in top_connections[:max_bundle_size-1])
                
                # Sort bundle items for consistency
                bundle_items.sort()
                bundles.append((bundle_items, score))
        
        # Remove duplicates and sort by score
        unique_bundles = {}
        for bundle, score in bundles:
            bundle_key = tuple(bundle)
            if bundle_key not in unique_bundles or unique_bundles[bundle_key] < score:
                unique_bundles[bundle_key] = score
        
        # Convert back to list and sort
        result = [(list(bundle), score) for bundle, score in unique_bundles.items()]
        result.sort(key=lambda x: x[1], reverse=True)
        
        return result[:top_n]
    
    def get_similar_items(self, item: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        Find items similar to the given item based on shared neighbors
        
        Args:
            item: Product name
            n: Number of similar items to return
            
        Returns:
            List of (similar_item, similarity_score) tuples
        """
        if item not in self.graph.get_all_nodes():
            print(f"Item '{item}' not found in graph")
            return []
        
        # Get neighbors of the target item
        target_neighbors = set(self.graph.get_neighbors(item).keys())
        
        if not target_neighbors:
            return []
        
        # Calculate similarity with all other items
        similarities = {}
        
        for other_item in self.graph.get_all_nodes():
            if other_item == item:
                continue
            
            # Get neighbors of the other item
            other_neighbors = set(self.graph.get_neighbors(other_item).keys())
            
            if not other_neighbors:
                continue
            
            # Calculate Jaccard similarity (intersection / union)
            intersection = len(target_neighbors & other_neighbors)
            union = len(target_neighbors | other_neighbors)
            
            if union > 0:
                similarity = intersection / union
                similarities[other_item] = similarity
        
        # Sort by similarity
        similar_items = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        return similar_items[:n]
    
    def get_complementary_items(self, item: str, n: int = 5) -> List[Tuple[str, int]]:
        """
        Get items that complement the given item (frequently bought together)
        This is essentially the same as recommend_for_item but with a different name
        for clarity
        
        Args:
            item: Product name
            n: Number of complementary items
            
        Returns:
            List of (product, co-purchase_count) tuples
        """
        return self.recommend_for_item(item, n)
    
    def print_recommendations(self, item: str, n: int = 5):
        """
        Print recommendations for an item in a readable format
        
        Args:
            item: Product name
            n: Number of recommendations
        """
        recommendations = self.recommend_for_item(item, n)
        
        if not recommendations:
            print(f"\nNo recommendations found for '{item}'")
            return
        
        print(f"\n{'='*60}")
        print(f"RECOMMENDATIONS FOR: {item}")
        print(f"{'='*60}")
        
        for i, (rec_item, score) in enumerate(recommendations, 1):
            print(f"{i}. {rec_item} (co-purchase count: {score})")
        
        print(f"{'='*60}")


# Example usage
if __name__ == "__main__":
    from basket_analysis.graph import ProductGraph
    
    # Create a sample graph
    graph = ProductGraph()
    graph.add_edge("Bread", "Milk", 10)
    graph.add_edge("Bread", "Butter", 7)
    graph.add_edge("Milk", "Eggs", 8)
    graph.add_edge("Bread", "Eggs", 5)
    graph.add_edge("Butter", "Eggs", 3)
    
    # Create recommender
    recommender = ProductRecommender(graph)
    
    # Test recommendations
    # recommender.print_recommendations("Bread", n=3)
    
    # Test basket recommendations
    # basket_recs = recommender.recommend_for_basket(["Bread", "Milk"], n=3)
    # print("\nRecommendations for basket ['Bread', 'Milk']:")
    # for item, score in basket_recs:
    #     print(f"  {item}: {score}")
