import os
from hello_agents import HelloAgentsLLM

_llm_instance = None


def get_llm() -> HelloAgentsLLM:
    """
    获取 LLM 实例（单例模式）
    HelloAgentsLLM 会自动从环境变量读取 LLM_API_KEY、LLM_BASE_URL、LLM_MODEL_ID
    """
    global _llm_instance
    if _llm_instance is None:
        # 从环境变量读取 max_tokens，框架不自动读取，需要显式传入
        max_tokens_str = os.getenv("LLM_MAX_TOKENS")
        max_tokens = int(max_tokens_str) if max_tokens_str else None
        _llm_instance = HelloAgentsLLM(max_tokens=max_tokens)
        print(f"✅ LLM服务初始化成功")
        print(f"   提供商: {_llm_instance.provider}")
        print(f"   模型: {_llm_instance.model}")
        print(f"   max_tokens: {max_tokens}")
    return _llm_instance

def reset_llm():
    """重置LLM实例"""
    global _llm_instance
    _llm_instance = None