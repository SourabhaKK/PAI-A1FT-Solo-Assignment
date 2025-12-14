"""
Graph Data Structure for Basket Analysis
Represents items and their co-purchase relationships
Author: Sourabha K Kallapur
"""

from typing import Dict, List, Set, Optional
from collections import defaultdict


class ProductGraph:
    """
    Graph data structure to represent product relationships
    Nodes = products, Edges = co-purchase relationships with weights
    """
    
    def __init__(self):
        """Initialize an empty graph"""
        # Using adjacency list representation
        # Format: {node: {neighbor: weight, ...}, ...}
        self.graph = defaultdict(dict)
        self.nodes = set()  # Keep track of all nodes
    
    def add_node(self, item: str):
        """
        Add a product node to the graph
        
        Args:
            item: Product name
        """
        if item not in self.nodes:
            self.nodes.add(item)
            # Initialize empty dict for this node if not exists
            if item not in self.graph:
                self.graph[item] = {}
    
    def add_edge(self, item1: str, item2: str, weight: int = 1):
        """
        Add an edge between two items (co-purchase relationship)
        
        Args:
            item1: First product
            item2: Second product
            weight: Weight of the edge (frequency of co-purchase)
        """
        # Make sure both nodes exist
        self.add_node(item1)
        self.add_node(item2)
        
        # Add edge in both directions (undirected graph)
        # If edge already exists, increase the weight
        if item2 in self.graph[item1]:
            self.graph[item1][item2] += weight
        else:
            self.graph[item1][item2] = weight
        
        # Since it's undirected, add the reverse edge too
        if item1 in self.graph[item2]:
            self.graph[item2][item1] += weight
        else:
            self.graph[item2][item1] = weight
    
    def get_neighbors(self, item: str) -> Dict[str, int]:
        """
        Get all neighbors of a node with their edge weights
        
        Args:
            item: Product name
            
        Returns:
            Dictionary of {neighbor: weight}
        """
        if item in self.graph:
            return self.graph[item]
        return {}
    
    def get_edge_weight(self, item1: str, item2: str) -> int:
        """
        Get the weight of an edge between two items
        
        Args:
            item1: First product
            item2: Second product
            
        Returns:
            Weight of the edge, or 0 if no edge exists
        """
        if item1 in self.graph and item2 in self.graph[item1]:
            return self.graph[item1][item2]
        return 0
    
    def get_all_nodes(self) -> Set[str]:
        """Get all nodes in the graph"""
        return self.nodes
    
    def get_node_count(self) -> int:
        """Get the number of nodes in the graph"""
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """Get the number of edges in the graph"""
        # Count edges (divide by 2 since graph is undirected)
        edge_count = 0
        for node in self.graph:
            edge_count += len(self.graph[node])
        return edge_count // 2
    
    def get_degree(self, item: str) -> int:
        """
        Get the degree of a node (number of neighbors)
        
        Args:
            item: Product name
            
        Returns:
            Number of neighbors
        """
        if item in self.graph:
            return len(self.graph[item])
        return 0
    
    def get_top_connections(self, item: str, n: int = 5) -> List[tuple]:
        """
        Get the top N most frequently co-purchased items with the given item
        
        Args:
            item: Product name
            n: Number of top connections to return
            
        Returns:
            List of tuples (neighbor, weight) sorted by weight
        """
        if item not in self.graph:
            return []
        
        # Get neighbors and sort by weight
        neighbors = self.graph[item]
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_neighbors[:n]
    
    def has_edge(self, item1: str, item2: str) -> bool:
        """
        Check if an edge exists between two items
        
        Args:
            item1: First product
            item2: Second product
            
        Returns:
            True if edge exists, False otherwise
        """
        return item1 in self.graph and item2 in self.graph[item1]
    
    def remove_node(self, item: str):
        """
        Remove a node and all its edges from the graph
        
        Args:
            item: Product name to remove
        """
        if item not in self.nodes:
            return
        
        # Remove all edges to this node from other nodes
        for neighbor in list(self.graph[item].keys()):
            if neighbor in self.graph and item in self.graph[neighbor]:
                del self.graph[neighbor][item]
        
        # Remove the node itself
        del self.graph[item]
        self.nodes.remove(item)
    
    def get_graph_info(self) -> Dict:
        """
        Get summary information about the graph
        
        Returns:
            Dictionary with graph statistics
        """
        if not self.nodes:
            return {
                'num_nodes': 0,
                'num_edges': 0,
                'avg_degree': 0,
                'max_degree': 0,
                'min_degree': 0
            }
        
        degrees = [self.get_degree(node) for node in self.nodes]
        
        return {
            'num_nodes': len(self.nodes),
            'num_edges': self.get_edge_count(),
            'avg_degree': sum(degrees) / len(degrees) if degrees else 0,
            'max_degree': max(degrees) if degrees else 0,
            'min_degree': min(degrees) if degrees else 0,
            'density': (2 * self.get_edge_count()) / (len(self.nodes) * (len(self.nodes) - 1)) 
                      if len(self.nodes) > 1 else 0
        }
    
    def print_graph(self):
        """Print the graph structure (for debugging)"""
        print("\n=== Product Graph ===")
        print(f"Nodes: {len(self.nodes)}")
        print(f"Edges: {self.get_edge_count()}")
        print("\nConnections:")
        for node in sorted(self.nodes):
            neighbors = self.graph[node]
            if neighbors:
                print(f"\n{node}:")
                for neighbor, weight in sorted(neighbors.items(), key=lambda x: x[1], reverse=True):
                    print(f"  -> {neighbor} (weight: {weight})")
    
    def __str__(self) -> str:
        """String representation of the graph"""
        info = self.get_graph_info()
        return (f"ProductGraph(nodes={info['num_nodes']}, "
                f"edges={info['num_edges']}, "
                f"avg_degree={info['avg_degree']:.2f})")


# Example usage
if __name__ == "__main__":
    # Create a sample graph
    graph = ProductGraph()
    
    # Add some products and their relationships
    graph.add_edge("Bread", "Milk", 5)
    graph.add_edge("Bread", "Butter", 3)
    graph.add_edge("Milk", "Eggs", 4)
    graph.add_edge("Bread", "Eggs", 2)
    
    # Print graph info
    print(graph)
    print("\nGraph Info:")
    print(graph.get_graph_info())
    
    # Get top connections for Bread
    print("\nTop connections for 'Bread':")
    print(graph.get_top_connections("Bread"))
    
    # Print full graph
    graph.print_graph()
