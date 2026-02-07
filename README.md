# 面向“保险+医养”生态的跨域知识图谱构建与问答系统

本项目实现了基于知识图谱检索增强 (GraphRAG) 的问答系统原型。

## 项目结构
- `data/raw`: 原始数据（保险条款、医疗指南、养老机构信息）。
- `data/processed`: 处理后的图谱文件 (kg.pkl) 和 Cypher 导入脚本。
- `src/kg_construction`: 图谱构建模块 (ETL, Graph Builder)。
- `src/rag_engine`: 检索与问答逻辑 (Retriever, Mock LLM)。
- `src/ui`: Streamlit 前端界面。

## 快速开始

1. **环境安装**
   ```bash
   pip install -r requirements.txt
   ```

2. **构建知识图谱**
   从原始数据抽取并构建图谱：
   ```bash
   cd src/kg_construction
   # 注意：需要确保在该目录下运行，或者调整脚本中的路径
   # 建议在根目录下运行模块:
   python -m src.kg_construction.graph_builder
   ```
   这将生成 `data/processed/kg.pkl` (用于本地 Python 演示) 和 `data/processed/import.cypher` (用于导入 Neo4j)。

3. **启动问答系统**
   ```bash
   streamlit run src/ui/app.py
   ```

## 功能说明
- **图谱检索**: 能够根据实体（如“高血压”）检索相关的保险产品、药物、科室等。
- **问答**: 结合检索到的上下文，通过 LLM 生成回答。
- **Mock 模式**: 当前 LLM 为 Mock 实现，仅对特定关键词返回预设答案。可修改 `src/rag_engine/rag_pipeline.py` 对接真实 API。
