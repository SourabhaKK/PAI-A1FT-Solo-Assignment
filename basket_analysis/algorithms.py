"""
Graph Algorithms Module for Basket Analysis
Implements BFS, DFS, and other graph traversal algorithms
Author: Sourabha K Kallapur
"""

from typing import List, Set, Dict, Optional
from collections import deque
from basket_analysis.graph import ProductGraph


class GraphAlgorithms:
    """
    Collection of graph algorithms for analyzing product relationships
    """
    
    def __init__(self, graph: ProductGraph):
        """
        Initialize with a product graph
        
        Args:
            graph: ProductGraph instance
        """
        self.graph = graph
    
    def bfs(self, start_item: str, max_depth: Optional[int] = None) -> List[str]:
        """
        Breadth-First Search traversal starting from a given item
        
        Args:
            start_item: Starting product
            max_depth: Maximum depth to traverse (None for unlimited)
            
        Returns:
            List of items in BFS order
        """
        if start_item not in self.graph.get_all_nodes():
            print(f"Item '{start_item}' not found in graph")
            return []
        
        visited = set()
        queue = deque([(start_item, 0)])  # (item, depth)
        result = []
        
        while queue:
            current_item, depth = queue.popleft()
            
            # Skip if already visited
            if current_item in visited:
                continue
            
            # Skip if max depth exceeded
            if max_depth is not None and depth > max_depth:
                continue
            
            # Mark as visited and add to result
            visited.add(current_item)
            result.append(current_item)
            
            # Add neighbors to queue
            neighbors = self.graph.get_neighbors(current_item)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        
        return result
    
    def dfs(self, start_item: str, max_depth: Optional[int] = None) -> List[str]:
        """
        Depth-First Search traversal starting from a given item
        
        Args:
            start_item: Starting product
            max_depth: Maximum depth to traverse (None for unlimited)
            
        Returns:
            List of items in DFS order
        """
        if start_item not in self.graph.get_all_nodes():
            print(f"Item '{start_item}' not found in graph")
            return []
        
        visited = set()
        result = []
        
        def dfs_recursive(item: str, depth: int):
            """Helper function for recursive DFS"""
            # Skip if already visited
            if item in visited:
                return
            
            # Skip if max depth exceeded
            if max_depth is not None and depth > max_depth:
                return
            
            # Mark as visited and add to result
            visited.add(item)
            result.append(item)
            
            # Visit neighbors
            neighbors = self.graph.get_neighbors(item)
            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs_recursive(neighbor, depth + 1)
        
        # Start the recursive DFS
        dfs_recursive(start_item, 0)
        
        return result
    
    def find_path(self, start_item: str, end_item: str) -> Optional[List[str]]:
        """
        Find a path between two items using BFS
        
        Args:
            start_item: Starting product
            end_item: Target product
            
        Returns:
            List of items forming the path, or None if no path exists
        """
        if start_item not in self.graph.get_all_nodes():
            print(f"Start item '{start_item}' not found")
            return None
        
        if end_item not in self.graph.get_all_nodes():
            print(f"End item '{end_item}' not found")
            return None
        
        # Use BFS to find path
        visited = set()
        queue = deque([(start_item, [start_item])])  # (current_item, path)
        
        while queue:
            current_item, path = queue.popleft()
            
            # Found the target
            if current_item == end_item:
                return path
            
            # Skip if already visited
            if current_item in visited:
                continue
            
            visited.add(current_item)
            
            # Add neighbors to queue
            neighbors = self.graph.get_neighbors(current_item)
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        # No path found
        return None
    
    def find_connected_components(self) -> List[Set[str]]:
        """
        Find all connected components in the graph
        
        Returns:
            List of sets, each set containing items in a connected component
        """
        all_nodes = self.graph.get_all_nodes()
        visited = set()
        components = []
        
        for node in all_nodes:
            if node not in visited:
                # Find all nodes connected to this node using BFS
                component = set(self.bfs(node))
                components.append(component)
                visited.update(component)
        
        return components
    
    def is_connected(self, item1: str, item2: str) -> bool:
        """
        Check if two items are connected (path exists between them)
        
        Args:
            item1: First product
            item2: Second product
            
        Returns:
            True if connected, False otherwise
        """
        path = self.find_path(item1, item2)
        return path is not None
    
    def get_items_within_distance(self, start_item: str, distance: int) -> Set[str]:
        """
        Get all items within a certain distance from the start item
        
        Args:
            start_item: Starting product
            distance: Maximum distance (number of edges)
            
        Returns:
            Set of items within the specified distance
        """
        if start_item not in self.graph.get_all_nodes():
            return set()
        
        visited = set()
        queue = deque([(start_item, 0)])  # (item, current_distance)
        
        while queue:
            current_item, current_dist = queue.popleft()
            
            if current_item in visited:
                continue
            
            if current_dist > distance:
                continue
            
            visited.add(current_item)
            
            # Add neighbors
            neighbors = self.graph.get_neighbors(current_item)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, current_dist + 1))
        
        return visited
    
    def find_strongest_connections(self, item: str, n: int = 5) -> List[tuple]:
        """
        Find the N strongest connections for an item
        (This is a wrapper around the graph's get_top_connections method)
        
        Args:
            item: Product name
            n: Number of top connections
            
        Returns:
            List of (neighbor, weight) tuples
        """
        return self.graph.get_top_connections(item, n)
    
    def get_clustering_coefficient(self, item: str) -> float:
        """
        Calculate the clustering coefficient for a node
        (Measure of how connected a node's neighbors are to each other)
        
        Args:
            item: Product name
            
        Returns:
            Clustering coefficient (0 to 1)
        """
        neighbors = list(self.graph.get_neighbors(item).keys())
        
        if len(neighbors) < 2:
            return 0.0
        
        # Count edges between neighbors
        edges_between_neighbors = 0
        for i, neighbor1 in enumerate(neighbors):
            for neighbor2 in neighbors[i+1:]:
                if self.graph.has_edge(neighbor1, neighbor2):
                    edges_between_neighbors += 1
        
        # Maximum possible edges between neighbors
        max_possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
        
        if max_possible_edges == 0:
            return 0.0
        
        return edges_between_neighbors / max_possible_edges


# Example usage
if __name__ == "__main__":
    from basket_analysis.graph import ProductGraph
    
    # Create a sample graph
    graph = ProductGraph()
    graph.add_edge("Bread", "Milk", 5)
    graph.add_edge("Bread", "Butter", 3)
    graph.add_edge("Milk", "Eggs", 4)
    graph.add_edge("Bread", "Eggs", 2)
    graph.add_edge("Butter", "Eggs", 1)
    
    # Create algorithms instance
    algo = GraphAlgorithms(graph)
    
    # Test BFS
    print("BFS from 'Bread':")
    print(algo.bfs("Bread"))
    
    # Test DFS
    print("\nDFS from 'Bread':")
    print(algo.dfs("Bread"))
    
    # Test path finding
    print("\nPath from 'Bread' to 'Eggs':")
    print(algo.find_path("Bread", "Eggs"))
    
    # Test connected components
    print("\nConnected components:")
    print(algo.find_connected_components())
