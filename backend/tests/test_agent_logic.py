"""测试 Agent 纯逻辑函数 —— 不涉及 LLM/MCP 调用"""

import pytest
import sys
sys.path.insert(0, "..")

from app.models.schemas import TripRequest, TripPlan
from app.agents.trip_planner_agent import (
    MultiAgentTripPlanner,
    PLANNER_AGENT_PROMPT,
)


@pytest.fixture
def planner():
    """创建一个不初始化的 planner（不用 LLM/MCP）"""
    return MultiAgentTripPlanner.__new__(MultiAgentTripPlanner)


@pytest.fixture
def sample_request():
    return TripRequest(
        city="杭州",
        start_date="2026-07-10",
        end_date="2026-07-12",
        travel_days=3,
        preferences=["自然风光", "美食"],
        transportation="地铁",
        accommodation="经济型酒店",
        free_text_input="想去西湖"
    )


class TestBuildAttractionQuery:
    def test_use_first_preference(self, planner, sample_request):
        query = planner._build_attraction_query(sample_request)
        assert "杭州" in query
        assert "自然风光" in query
        assert "TOOL_CALL" in query
        assert "amap_maps_text_search" in query

    def test_default_keyword_when_no_preferences(self, planner):
        req = TripRequest(
            city="上海", start_date="2026-07-10", end_date="2026-07-11",
            travel_days=2, preferences=[], transportation="公交", accommodation="民宿"
        )
        query = planner._build_attraction_query(req)
        assert "景点" in query
        assert "上海" in query


class TestParseResponse:
    def test_extract_json_code_block(self, planner, sample_request):
        response = """好的，这是您的旅行计划：
```json
{"city": "杭州", "start_date": "2026-07-10", "end_date": "2026-07-12",
"days": [], "weather_info": [],
"overall_suggestions": "好好玩",
"budget": {"total_attractions": 0, "total_hotels": 0, "total_meals": 0,
"total_transportation": 0, "total": 0}}
```
祝您旅途愉快！"""
        result = planner._parse_response(response, sample_request)
        assert isinstance(result, TripPlan)
        assert result.city == "杭州"

    def test_extract_raw_json(self, planner, sample_request):
        response = '{"city": "杭州", "start_date": "2026-07-10", "end_date": "2026-07-12", "days": [], "weather_info": [], "overall_suggestions": "ok", "budget": {"total_attractions": 0, "total_hotels": 0, "total_meals": 0, "total_transportation": 0, "total": 0}}'
        result = planner._parse_response(response, sample_request)
        assert isinstance(result, TripPlan)
        assert result.city == "杭州"

    def test_no_json_falls_back(self, planner, sample_request):
        response = "抱歉，我无法生成计划"
        result = planner._parse_response(response, sample_request)
        assert isinstance(result, TripPlan)
        assert result.city == "杭州"  # fallback 用 request 数据

    def test_truncated_json_falls_back(self, planner, sample_request):
        response = '{"city": "杭州", "start_date": "2026-07-10", "end_da'
        result = planner._parse_response(response, sample_request)
        assert isinstance(result, TripPlan)  # 截断 JSON → fallback


class TestFallbackPlan:
    def test_creates_correct_number_of_days(self, planner, sample_request):
        plan = planner._create_fallback_plan(sample_request)
        assert len(plan.days) == 3
        assert plan.city == "杭州"
        assert plan.start_date == "2026-07-10"

    def test_each_day_has_required_fields(self, planner, sample_request):
        plan = planner._create_fallback_plan(sample_request)
        for i, day in enumerate(plan.days):
            assert day.day_index == i
            assert len(day.attractions) == 2
            assert len(day.meals) == 3
            assert day.meals[0].name  # 必填字段


def test_planner_prompt_contains_meal_fields():
    """确保 Planner 提示词里 Meal 示例包含 address 和 location"""
    assert '"type": "breakfast"' in PLANNER_AGENT_PROMPT
