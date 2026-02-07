import json
import re
from typing import List, Dict, Any
import os

class DataLoader:
    def __init__(self, raw_data_path):
        self.raw_data_path = raw_data_path

    def load_insurance_data(self) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.raw_data_path, "insurance_clauses.txt")
        products = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.split('\n\n')
        for block in blocks:
            if not block.strip():
                continue
            item = {}
            lines = block.split('\n')
            for line in lines:
                if ':' in line:
                    key, val = line.split(':', 1)
                    item[key.strip()] = val.strip()
            if item:
                products.append(item)
        return products

    def load_medical_data(self) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.raw_data_path, "medical_guidelines.txt")
        diseases = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        blocks = content.split('\n\n')
        for block in blocks:
            if not block.strip():
                continue
            item = {}
            lines = block.split('\n')
            for line in lines:
                if ':' in line:
                    key, val = line.split(':', 1)
                    item[key.strip()] = val.strip()
            if item:
                diseases.append(item)
        return diseases

    def load_nursing_data(self) -> List[Dict[str, Any]]:
        file_path = os.path.join(self.raw_data_path, "nursing_homes.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

if __name__ == "__main__":
    loader = DataLoader("../../data/raw")
    print("Insurance:", len(loader.load_insurance_data()))
    print("Medical:", len(loader.load_medical_data()))
    print("Nursing:", len(loader.load_nursing_data()))
