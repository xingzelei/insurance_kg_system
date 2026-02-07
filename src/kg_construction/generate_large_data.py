import random
import json
import os

# 配置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# Fix: Path should be ../../data/raw relative to src/kg_construction
raw_data_path = os.path.join(current_dir, "../../data/raw")
os.makedirs(raw_data_path, exist_ok=True)

# === 基础词库 ===
departments = ["心血管内科", "神经内科", "内分泌科", "呼吸内科", "消化内科", "肿瘤科", "骨科", "老年病科"]
disease_cores = ["高血压", "糖尿病", "冠心病", "脑卒中", "肺癌", "胃炎", "关节炎", "白内障", "阿尔茨海默病", "帕金森", "支气管哮喘", "慢性阻塞性肺疾病", "骨质疏松", "心力衰竭", "肾功能不全"]
disease_prefixes = ["原发性", "继发性", "急性", "慢性", "老年", "小儿", "复发性", "早期", "晚期"]
drug_cores = ["阿司匹林", "二甲双胍", "硝苯地平", "头孢拉定", "阿莫西林", "布洛芬", "胰岛素", "美托洛尔", "辛伐他汀", "奥美拉唑", "氨氯地平", "多奈哌齐", "甘露醇", "洛伐他汀", "异烟肼", "利福平", "乙胺丁醇", "吡嗪酰胺", "阿奇霉素", "罗红霉素", "克拉霉素", "左氧氟沙星", "莫西沙星", "青霉素", "头孢克肟"]
drug_suffixes = ["片", "胶囊", "注射液", "缓释片", "口服液", "颗粒", "分散片", "软胶囊", "滴丸", "栓剂"]
dosages = ["10mg", "20mg", "50mg", "100mg", "0.5g", "0.25g", "5ml", "10ml"]

insurance_adjectives = ["全能", "乐享", "安康", "长寿", "无忧", "尊享", "惠民", "百万", "终身", "特定", "至尊", "卓越", "守护", "关爱", "安心"]
insurance_types = ["医疗险", "重疾险", "护理险", "意外险", "防癌险"]

services = ["独立生活", "协助生活", "专业护理", "记忆照护", "康复训练", "老年大学", "居家上门", "陪诊服务", "临终关怀", "中医理疗"]
locations = ["北京", "上海", "广州", "深圳", "成都", "武汉", "杭州", "苏州", "南京", "天津"]
nursing_names = ["泰康之家·燕园", "泰康之家·申园", "泰康之家·粤园", "泰康之家·蜀园", "泰康之家·楚园", "泰康之家·吴园", "泰康之家·苏园", "幸福人家", "夕阳红公寓", "松鹤楼", "颐和山庄"]

# === 生成逻辑 ===

def generate_diseases(count=250):
    diseases = []
    generated_names = set()
    
    # 保证核心疾病都在
    for d in disease_cores:
        name = d
        if name not in generated_names:
            dept = random.choice(departments) # 简化逻辑：随机分配科室
            diseases.append({
                "疾病名称": name,
                "相关科室": dept,
                "常用药物": [],
                "饮食建议": "清淡饮食，遵医嘱。",
                "护理建议": "定期复查，注意休息。"
            })
            generated_names.add(name)

    while len(diseases) < count:
        core = random.choice(disease_cores)
        prefix = random.choice(disease_prefixes)
        name = f"{prefix}{core}"
        
        if name in generated_names:
            name = f"{name}({random.randint(1,3)}型)"
        
        if name not in generated_names:
            dept = random.choice(departments)
            diseases.append({
                "疾病名称": name,
                "相关科室": dept,
                "常用药物": [],
                "饮食建议": "低盐低脂，避免劳累。",
                "护理建议": "监测生命体征。"
            })
            generated_names.add(name)
            
    return diseases

def generate_drugs(count=200):
    drugs = []
    generated_names = set()
    while len(drugs) < count:
        core = random.choice(drug_cores)
        suffix = random.choice(drug_suffixes)
        dosage = random.choice(dosages)
        # 增加剂量组合以扩大样本空间
        name = f"{core}{suffix}({dosage})"
        if name not in generated_names:
            drugs.append(name)
            generated_names.add(name)
        
        # 安全退出机制，防止死循环
        if len(generated_names) >= len(drug_cores) * len(drug_suffixes) * len(dosages):
             print("Warning: Max possible drug combinations reached.")
             break
    return list(generated_names)

def generate_insurances(count=60, disease_list=[]):
    products = []
    generated_names = set()
    
    for _ in range(count):
        adj = random.choice(insurance_adjectives)
        itype = random.choice(insurance_types)
        letter = random.choice(["A", "B", "C", "Pro", "Plus", "2026版"])
        name = f"泰康{adj}{itype} {letter}"
        
        if name not in generated_names:
            # 随机覆盖 5-15 种疾病
            covered = random.sample([d["疾病名称"] for d in disease_list], k=random.randint(5, 15))
            
            products.append({
                "产品名称": name,
                "适用年龄": f"{random.randint(0, 60)}-{random.randint(70, 100)}岁",
                "保险责任": f"提供{itype}相关保障，包含住院津贴。",
                "且覆盖疾病": "，".join(covered),
                "特别说明": "具体条款以合同为准。"
            })
            generated_names.add(name)
    return products

def generate_nursing_homes(count=30):
    homes = []
    for i in range(count):
        base_name = random.choice(nursing_names)
        loc = random.choice(locations)
        # 避免重名
        name = f"{base_name} ({loc}分院 {i+1}部)"
        
        my_services = random.sample(services, k=random.randint(3, 8))
        
        homes.append({
            "name": name,
            "location": loc,
            "services": my_services,
            "price_range": f"{random.randint(5000, 20000)}-{random.randint(21000, 50000)}/月"
        })
    return homes

# === 执行生成并写入文件 ===
def main():
    print("Generating synthetic data...")
    
    # 1. Medical Data
    # 增加数量以确保覆盖 500+实体和 1000+关系
    drugs = generate_drugs(300)      # 300 药品实体
    diseases = generate_diseases(300) # 300 疾病实体
    
    # 关联药品到疾病 (关系：Treats)
    # 每个疾病关联 1-3 个药品
    for d in diseases:
        d_drugs = random.sample(drugs, k=random.randint(1, 3))
        d["常用药物"] = "，".join(d_drugs)
        
    print(f"Generated {len(diseases)} diseases and {len(drugs)} drugs.")
    
    # 写入 medical_guidelines.txt
    with open(os.path.join(raw_data_path, "medical_guidelines.txt"), "w", encoding="utf-8") as f:
        for d in diseases:
            f.write(f"疾病名称: {d['疾病名称']}\n")
            f.write(f"相关科室: {d['相关科室']}\n")
            f.write(f"常用药物: {d['常用药物']}\n")
            f.write(f"饮食建议: {d['饮食建议']}\n")
            f.write(f"护理建议: {d['护理建议']}\n")
            f.write("\n") # Block separator

    # 2. Insurance Data
    # 100 保险产品实体
    insurances = generate_insurances(100, diseases)
    print(f"Generated {len(insurances)} insurance products.")
    
    with open(os.path.join(raw_data_path, "insurance_clauses.txt"), "w", encoding="utf-8") as f:
        for p in insurances:
            f.write(f"产品名称: {p['产品名称']}\n")
            f.write(f"适用年龄: {p['适用年龄']}\n")
            f.write(f"保险责任: {p['保险责任']}\n")
            f.write(f"且覆盖疾病: {p['且覆盖疾病']}\n")
            f.write(f"特别说明: {p['特别说明']}\n")
            f.write("\n")

    # 3. Nursing Data
    # 50 养老机构实体
    homes = generate_nursing_homes(50)
    print(f"Generated {len(homes)} nursing homes.")
    
    with open(os.path.join(raw_data_path, "nursing_homes.json"), "w", encoding="utf-8") as f:
        json.dump(homes, f, ensure_ascii=False, indent=4)
        
    print("All data generated successfully!")

if __name__ == "__main__":
    main()
