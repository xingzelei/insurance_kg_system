import networkx as nx
import os
import pickle
try:
    from .data_loader import DataLoader
    from .ontology import EntityType, RelationType
except ImportError:
    from data_loader import DataLoader
    from ontology import EntityType, RelationType

class GraphBuilder:
    def __init__(self, data_path, output_path):
        self.loader = DataLoader(data_path)
        self.output_path = output_path
        self.G = nx.MultiDiGraph()

    def build_graph(self):
        print("Starting Graph Construction...")
        # 1. Process Insurance
        ins_data = self.loader.load_insurance_data()
        for item in ins_data:
            p_name = item.get("产品名称")
            if not p_name: continue
            
            # Create Node
            self.G.add_node(p_name, type=EntityType.INSURANCE_PRODUCT.value, 
                            age_limit=item.get("适用年龄"), 
                            special_note=item.get("特别说明"))
            
            # Relations
            covered_diseases = item.get("且覆盖疾病", "").replace("，", ",").split(",")
            for d in covered_diseases:
                d = d.strip()
                if d:
                    self.G.add_node(d, type=EntityType.DISEASE.value) # Ensure node exists
                    self.G.add_edge(p_name, d, relation=RelationType.COVERS_DISEASE.value)
        
        # 2. Process Medical
        med_data = self.loader.load_medical_data()
        for item in med_data:
            d_name = item.get("疾病名称")
            if not d_name: continue
            
            # Update or Create Node
            if self.G.has_node(d_name):
                self.G.nodes[d_name].update({"diet": item.get("饮食建议"), "care": item.get("护理建议")})
            else:
                self.G.add_node(d_name, type=EntityType.DISEASE.value,
                                diet=item.get("饮食建议"), care=item.get("护理建议"))
                                
            # Department
            dept = item.get("相关科室")
            if dept:
                self.G.add_node(dept, type=EntityType.DEPARTMENT.value)
                self.G.add_edge(d_name, dept, relation=RelationType.BELONGS_TO.value)
                
            # Drugs
            drugs = item.get("常用药物", "").replace("，", ",").split(",")
            for drug in drugs:
                drug = drug.strip()
                if drug:
                    self.G.add_node(drug, type=EntityType.DRUG.value)
                    # Relations: Drug TREATS Disease
                    self.G.add_edge(drug, d_name, relation=RelationType.TREATS.value)

        # 3. Process Nursing
        nurs_data = self.loader.load_nursing_data()
        for item in nurs_data:
            n_name = item["name"]
            self.G.add_node(n_name, type=EntityType.NURSING_HOME.value, price=item["price_range"])
            
            loc = item["location"]
            self.G.add_node(loc, type=EntityType.LOCATION.value)
            self.G.add_edge(n_name, loc, relation=RelationType.LOCATED_IN.value)
            
            for svc in item["services"]:
                self.G.add_node(svc, type=EntityType.SERVICE.value)
                self.G.add_edge(n_name, svc, relation=RelationType.PROVIDES_SERVICE.value)

        print(f"Graph built with {self.G.number_of_nodes()} nodes and {self.G.number_of_edges()} edges.")
        self.save_graph()

    def save_graph(self):
        # Save as pickle for easy python loading
        with open(os.path.join(self.output_path, "kg.pkl"), "wb") as f:
            pickle.dump(self.G, f)
        print(f"Graph saved to {os.path.join(self.output_path, 'kg.pkl')}")

    def export_cypher(self):
        # Generate Cypher statements (Mock)
        cypher_file = os.path.join(self.output_path, "import.cypher")
        with open(cypher_file, "w", encoding="utf-8") as f:
            for node, data in self.G.nodes(data=True):
                labels = data.get("type", "Thing")
                props = ", ".join([f"{k}: '{v}'" for k,v in data.items() if k != "type" and v])
                f.write(f"MERGE (n:`{labels}` {{name: '{node}', {props}}});\n")
            
            for u, v, data in self.G.edges(data=True):
                rel = data.get("relation", "RELATED_TO")
                f.write(f"MATCH (a {{name: '{u}'}}), (b {{name: '{v}'}}) MERGE (a)-[:{rel}]->(b);\n")
        print(f"Cypher exported to {cypher_file}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Fix: Correct relative path
    raw_path = os.path.join(current_dir, "../../data/raw")
    proc_path = os.path.join(current_dir, "../../data/processed")
    builder = GraphBuilder(raw_path, proc_path)
    builder.build_graph()
    builder.export_cypher()
