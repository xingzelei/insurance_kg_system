from .retriever import GraphRetriever
import os

try:
    from zhipuai import ZhipuAI
except ImportError:
    ZhipuAI = None

class ZhipuLLM:
    def __init__(self, api_key):
        if not ZhipuAI:
            raise ImportError("Please install zhipuai: pip install zhipuai")
        self.client = ZhipuAI(api_key=api_key)
        
    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling ZhipuAI: {str(e)}"

class MockLLM:
    def generate(self, prompt):
        # Determine intent for mock response
        if "高血压" in prompt and "保险" in prompt:
            return "根据图谱信息，【泰康全能保】覆盖恶性肿瘤和心肌梗死，特别说明指出高血压患者需核保。因此，70岁高血压患者购买需经过核保流程。而【银发无忧防癌险】特别说明三高人群可投保，可能更适合。"
        elif "泰康之家" in prompt:
            return "泰康之家·燕园位于北京，提供独立生活、协助生活等服务，价格在10000-30000/月。"
        else:
            return "这是基于GraphRAG生成的回答示例。根据图谱数据，我们找到了相关实体和关系..."

class RAGPipeline:
    def __init__(self, data_processed_path, api_key=None):
        kg_path = os.path.join(data_processed_path, "kg.pkl")
        self.retriever = GraphRetriever(kg_path)
        
        if api_key:
            print("Initializing ZhipuAI LLM...")
            self.llm = ZhipuLLM(api_key)
        else:
            print("Warning: No API Key provided, using Mock LLM.")
            self.llm = MockLLM()

    def answer_question(self, question):
        # 1. Retrieve
        context = self.retriever.get_context(question, hops=1)
        
        # 2. Construct Prompt
        prompt = f"""
        你是一个智能保险医养助手。请根据以下知识图谱上下文回答用户问题。
        
        上下文信息：
        {context}
        
        用户问题：{question}
        
        回答要求：准确，基于事实，引用上下文。
        """
        
        # 3. Generate
        answer = self.llm.generate(prompt)
        
        return {
            "question": question,
            "context": context,
            "answer": answer
        }
