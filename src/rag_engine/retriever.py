import networkx as nx
import pickle
import os

class GraphRetriever:
    def __init__(self, kg_path):
        print(f"Loading Graph from {kg_path}")
        with open(kg_path, "rb") as f:
            self.G = pickle.load(f)

    def search_entities(self, query):
        """Simple keyword matching for entities."""
        # Limit the number of matched seeds to 3 to prevent explosion
        matches = []
        for node in self.G.nodes():
            if query in node or node in query:
                matches.append(node)
        return matches[:3]

    def get_context(self, query, hops=1):
        """Retrieves subgraphs for entities found in query."""
        entities = self.search_entities(query)
        if not entities:
            return "No relevant entities found in Knowledge Graph."
        
        context_str = ""
        visited_nodes = set()
        
        for start_node in entities:
            context_str += f"\n--- Context for '{start_node}' ---\n"
            # Get ego graph (subgraph)
            # radius=1 means 1 hop. Use undirected to get incoming edges (like Insurance -> Disease)
            # Optimization: Pre-compute undirected graph only once if needed, or use G.to_undirected(as_view=True)
            # to avoid copying data. Since we query frequently, let's keep it simple but efficient.
            subgraph = nx.ego_graph(self.G.to_undirected(as_view=True), start_node, radius=hops)
            
            # Use original directed edges for display where possible, or just list relations found
            # But the subgraph edges might have lost direction or attributes if we rely on G_undir
            # Better: Get nodes from undirected ego graph, then induce subgraph from original G
            subgraph_nodes = list(subgraph.nodes())
            subgraph = self.G.subgraph(subgraph_nodes)
            
            for u, v, data in subgraph.edges(data=True):
                if u not in visited_nodes:
                    node_data = self.G.nodes[u]
                    # Print node properties
                    props = ", ".join([f"{k}: {v}" for k,v in node_data.items() if k!='type'])
                    if props:
                        context_str += f"Entity: {u} ({props})\n"
                    visited_nodes.add(u)
                    
                if v not in visited_nodes:
                    node_data = self.G.nodes[v]
                    props = ", ".join([f"{k}: {v}" for k,v in node_data.items() if k!='type'])
                    if props:
                        context_str += f"Entity: {v} ({props})\n"
                    visited_nodes.add(v)
                
                rel_type = data.get('relation', 'RELATED')
                context_str += f"({u}) --[{rel_type}]--> ({v})\n"
                
        return context_str

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    kg_path = os.path.join(current_dir, "../../data/processed/kg.pkl")
    retriever = GraphRetriever(kg_path)
    print(retriever.get_context("高血压"))
