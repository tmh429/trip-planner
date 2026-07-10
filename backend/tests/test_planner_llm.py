"""单独测试 Planner LLM 调用 —— 跳过 Agent 和 MCP"""

import sys
sys.path.insert(0, "..")

from app.services.llm_service import get_llm
from app.agents.trip_planner_agent import PLANNER_AGENT_PROMPT


def test_llm_invoke_simple():
    """最简单的调用：看 LLM 能不能返回内容"""
    llm = get_llm()
    messages = [
        {"role": "system", "content": "你是一个测试助手，请用 JSON 回复。"},
        {"role": "user", "content": '返回 {"status": "ok", "message": "hello"}'}
    ]
    result = llm.invoke(messages, max_tokens=256)
    print(f"简单调用结果 ({len(result)} 字符):\n{result}\n")
    assert len(result) > 0, "LLM 返回了空响应！"


def test_planner_with_minimal_input():
    """用真实的 Planner 提示词 + 最简短的行程数据"""
    llm = get_llm()
    messages = [
        {"role": "system", "content": PLANNER_AGENT_PROMPT},
        {"role": "user", "content": """请生成一个最简单的旅行计划：

**基本信息:**
- 城市: 北京
- 日期: 2026-07-10 至 2026-07-10
- 天数: 1天
- 交通方式: 地铁
- 住宿: 经济型酒店

**景点信息:**
故宫(地址:北京市东城区, 坐标: 116.397, 39.916)

**天气信息:**
7月10日 晴 25°C

**酒店信息:**
如家酒店(地址:北京市, 坐标: 116.4, 39.9)

返回完整的 JSON 格式数据，不要省略任何字段。"""}
    ]
    result = llm.invoke(messages, max_tokens=4096)
    print(f"Planner 调用结果 ({len(result)} 字符):\n{result[:500]}\n")

    assert len(result) > 0, "Planner 返回了空响应！"
    assert "北京" in result, "结果中没有城市名"


if __name__ == "__main__":
    test_llm_invoke_simple()
    test_planner_with_minimal_input()
    print("✅ 全部通过")
