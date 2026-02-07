import streamlit as st
import os
import sys

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "../../")
sys.path.append(src_path)

from src.rag_engine.rag_pipeline import RAGPipeline

st.set_page_config(page_title="保险+医养 知识图谱问答系统", layout="wide")

st.sidebar.header("⚙️ 系统设置")

model_option = st.sidebar.radio(
    "选择大模型类型",
    ["ZhipuAI API", "Mock 模拟模式"],
    index=0  # 默认选择 API
)

api_key = None

if model_option == "ZhipuAI API":
    api_key = st.sidebar.text_input("🔑 ZhipuAI API Key", type="password", placeholder="请输入您的 API Key")
    if api_key:
        st.sidebar.success("✅ 已配置 API Key")
    else:
        st.sidebar.warning("⚠️ 请输入 API Key 以使用大模型")
else:
    st.sidebar.info("💡 当前运行在 **模拟模式 (Mock)**，仅返回预设答案。")

@st.cache_resource
def load_pipeline(key):
    # Path relative to where we run streamlit
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_path, "data/processed")
    return RAGPipeline(data_path, api_key=key)

try:
    pipeline = load_pipeline(api_key)
except FileNotFoundError:
    st.error("Knowledge Graph not found. Please run 'src/kg_construction/graph_builder.py' first.")
    st.stop()

st.title("🏥 保险+医养 跨域知识图谱问答系统")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("💡 示例问题")
    example = st.radio("选择一个问题:", 
             ["高血压能买什么保险？", 
              "泰康之家·燕园在哪里？", 
              "泰康全能保覆盖什么疾病？"])

with col2:
    st.subheader("💬 对话交互")
    user_input = st.text_input("请输入您的问题:", value=example)
    
    if st.button("提问"):
        if user_input:
            # 1. Retrieval Phase
            with st.status("🔍 正在检索知识图谱...", expanded=True) as status:
                st.write("正在搜索相关实体...")
                # Split the pipeline call to show progress
                context = pipeline.retriever.get_context(user_input, hops=1)
                st.write("检索完成，找到相关知识上下文。")
                status.update(label="✅ 图谱检索完成", state="complete", expanded=False)

            # 2. Generation Phase
            with st.spinner("🤖 模型正在思考 (本地运行速度取决于硬件配置)..."):
                # Construct prompt manually (replicating logic from pipeline to decouple UI)
                prompt = f"""
                你是一个智能保险医养助手。请根据以下知识图谱上下文回答用户问题。
                
                上下文信息：
                {context}
                
                用户问题：{user_input}
                
                回答要求：准确，基于事实，引用上下文。
                """
                
                answer = pipeline.llm.generate(prompt)
                
                st.success("回答生成成功")
                st.markdown(f"### 🤖 回答\n{answer}")
                
                with st.expander("查看知识图谱证据 (Context)"):
                    st.text(context)
