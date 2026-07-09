from hello_agents import HelloAgentsLLM

_llm_instance = None


def get_llm() -> HelloAgentsLLM:
    """
    获取 LLM 实例（单例模式）
    HelloAgentsLLM 会自动从环境变量读取 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL_ID
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = HelloAgentsLLM()
        print(f"✅ LLM服务初始化成功")
        print(f"   提供商: {_llm_instance.provider}")
        print(f"   模型: {_llm_instance.model}")
    return _llm_instance

def reset_llm():
    """重置LLM实例"""
    global _llm_instance
    _llm_instance = None