"""测试数据模型 —— 零外部依赖，纯 Pydantic 校验"""

import pytest
import sys
sys.path.insert(0, "..")

from app.models.schemas import (
    Location,
    Attraction,
    Meal,
    Hotel,
    DayPlan,
    WeatherInfo,
    Budget,
    TripPlan,
    TripRequest,
    TripPlanResponse,
)


class TestLocation:
    def test_create_valid(self):
        loc = Location(longitude=116.4, latitude=39.9)
        assert loc.longitude == 116.4
        assert loc.latitude == 39.9

    def test_accepts_negative_values(self):
        loc = Location(longitude=-73.9, latitude=-33.4)
        assert loc.longitude == -73.9


class TestWeatherInfo:
    def test_strips_degree_symbol(self):
        w = WeatherInfo(
            date="2026-07-10",
            day_weather="晴",
            night_weather="多云",
            day_temp="25℃",
            night_temp="15°C",
            wind_direction="南风",
            wind_power="1-3级"
        )
        assert w.day_temp == 25
        assert w.night_temp == 15

    def test_plain_number_passes_through(self):
        w = WeatherInfo(
            date="2026-07-10", day_weather="晴", night_weather="阴",
            day_temp=30, night_temp=20,
            wind_direction="北风", wind_power="3级"
        )
        assert w.day_temp == 30
        assert w.night_temp == 20


class TestMeal:
    def test_address_and_location_optional(self):
        m = Meal(type="breakfast", name="早餐", description="描述")
        assert m.address == ""
        assert m.location is None

    def test_create_valid_with_default_cost(self):
        m = Meal(
            type="lunch", name="午餐", address="北京市",
            location=Location(longitude=116.4, latitude=39.9),
            description="推荐"
        )
        assert m.estimated_cost == 0  # 默认值


class TestAttraction:
    def test_minimal_attraction(self):
        a = Attraction(
            name="故宫",
            address="北京市东城区",
            location=Location(longitude=116.4, latitude=39.9),
            visit_duration=120,
            description="著名景点",
            category="历史文化"
        )
        assert a.name == "故宫"
        assert a.ticket_price == 0  # 默认值


class TestTripRequest:
    def test_valid_minimal(self):
        r = TripRequest(
            city="北京",
            start_date="2026-07-10",
            end_date="2026-07-12",
            travel_days=3,
            preferences=["历史文化"],
            transportation="地铁",
            accommodation="经济型酒店"
        )
        assert r.city == "北京"
        assert r.travel_days == 3

    def test_free_text_optional(self):
        r = TripRequest(
            city="上海", start_date="2026-07-10", end_date="2026-07-11",
            travel_days=2, preferences=[], transportation="步行", accommodation="民宿"
        )
        assert r.free_text_input == ""

    def test_missing_required_field(self):
        with pytest.raises(Exception):
            TripRequest(city="北京")  # 缺很多必填字段


class TestTripPlanResponse:
    def test_success_response(self):
        resp = TripPlanResponse(success=True, message="ok")
        assert resp.success is True
        assert resp.data is None

    def test_with_data(self):
        plan = TripPlan(
            city="北京", start_date="2026-07-10", end_date="2026-07-10",
            days=[], weather_info=[], overall_suggestions="玩得开心",
            budget=Budget(total_attractions=0, total_hotels=0, total_meals=0,
                          total_transportation=0, total=0)
        )
        resp = TripPlanResponse(success=True, message="ok", data=plan)
        assert resp.data.city == "北京"
